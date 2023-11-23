import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01, # 1% chance of having 2 copies of the gene
        1: 0.03, # 3% chance of having 1 copy of the gene
        0: 0.96 # 96% chance of having 0 copies of the gene
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65, # 65% chance of exhibiting the trait
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01, # 65% chance of exhibiting the trait,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
    # If parents have gene, but the child have not
    # If parents have not gene, but the child have
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    # people is a whole library
    names = set(people)
    # names = {'Ron', 'Fred', 'Ginny', 'Charlie', 'Molly', 'Arthur'}
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


# # Run test in terminal
#     #  python testing.py data/family1.csv
def joint_probability(people, one_gene, two_genes, have_trait):
# people: {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False}
    joint_probability = 1
    
    # iterate "names" in dictionary e.g Arthur
    # ❗️❗️ 'one_gene' and 'two_genes' are predefined in the project. 
        # ❗️❗️ Don't need to know why person is in this group
        # We only need to use these values to calculate the joint_probability.
            # The purpose is to determine the number of specific genes (0, 1, or 2) that each person has.
                # then based on this to calculate joint_probability
    for person in people:
        genes = 0
        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2
            
        # Set a variable for mother and father
            # It will be a name or None
        mother = people[person]["mother"]
        father = people[person]["father"]
        

        ###### No parent data ######
        # Handle the situation where there is no parent information available.
        ### Parent data both are None ###
        if mother is None and father is None:
            
            # 1st Update `joint_probability` (no parent data)
            joint_probability *= PROBS["gene"][genes]# if [genes]=[1], it will be 0.03, from PROBS dic
            # If we don't have parental information, 
                # we use 0, 1 or 2 copies of the gene to determine the probability. it can get in PROBS["gene"].
        

        ###### With parent data ######
        else:
            # Set a dictionary to store parent data
                # name: probability
            passing = {mother: 0, father: 0}
             
            # Check which group the parents are in(both check mother and father)
            for parent in passing:
                if parent in two_genes:
                    passing[parent] = 1 - PROBS["mutation"] # Understanding_1
                elif parent in one_gene:
                    passing[parent] = 0.5 # Understanding_2
                else:
                    passing[parent] = PROBS["mutation"] # mother and father both have no gene, only take the mutation probability
            

            ### Calculating probability based on parents' genes ###
            # 1st Update `joint_probability` (with parent data)
            
            # calculate probability of inherits 2 genes from person parents
            if genes == 2: 
                joint_probability *= passing[mother] * passing[father]
                # joint_probability = 1 * passing[mother] * passing[father]

            # calculate probability of inherits 1 genes from person parents
            elif genes == 1: 
                joint_probability *= passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father]
                # 2 satuation: 
                    # a.mother pass father doesn't:  `passing[mother] * (1 - passing[father])`
                    # b.father pass mother doesn't: `(1 - passing[mother]) * passing[father]`

            else:
                joint_probability *= (1 - passing[mother]) * (1 - passing[father])
                # mother and father both dosen't pass 


        # Get traits probability
        trait = people[person]["trait"]
        # 2nd Update `joint_probability`
        if trait is not None:
            joint_probability *= PROBS["trait"][genes][trait]
            # Get the probability from PROBS dictionary
                # e.g joint_probability *= PROBS["trait"][2][True] = 0.65
        
        else: # if person "trait" data is None
            trait = person in have_trait # 
            # check the have_trait, if the name in have_trait it will return True, else return False
            joint_probability *= PROBS["trait"][genes][trait] # trait in here will get a bool value 
        
            ### The above is a new way of writing that I have learnt, 
            ### and the actual concept is as follows
                # if person in have_trait:
                #     has_trait = True 
                # else:
                #     has_trait = False 
                # probability_of_trait = PROBS["trait"][genes][has_trait]
                # joint_probability *= probability_of_trait

    return joint_probability





def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # probabilities[person]["gene"] = {2: 0, 1: 0, 0: 0}
    # probabilities[person]["trait"] = {True: 0, False: 0}

    for person in probabilities:
        # In this section, the probabilities are initially 0, so we update the value with `+=`.
        # p will something like 0.008852852828159999
        if person in have_trait:
            probabilities[person]["trait"][True] += p
            # True: 0 += 0.008852852828159999
        else:
            probabilities[person]["trait"][False] += p

        # According one_gene or two_gene to add the p into the dictionary
        if person in two_genes:
            probabilities[person]["gene"][2] += p 
            # 0 += 0.008852852828159999
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p

    # When it's done, the `probabilities{}` data will be updated
        # probabilities[person]["gene"] = {2: 0.008852852828159999, 1: 0, 0: 0}
        # probabilities[person]["trait"] = {True: 0.008852852828159999, False: 0}


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize genes probability
        # `sum()` is sum up all thing in the ()
            # `.values() get the value of 0,1,2 in gene`, then sum them up
                # dict_values([0.00029218473899999994, 0.014499220722, 0.017026184538999997])
        gene_total = sum(probabilities[person]["gene"].values())
        # gene_total: 0.03181758999999999

        for gene_count in probabilities[person]["gene"]:
            # gene_count will be 0, 1, 2 from "gene"         
            probabilities[person]["gene"][gene_count] /= gene_total
            # 0.00029218473899999994 /= 0.03181758999999999
                # It will kepping update `probabilities[person]["gene"][gene_count]`

        # Normalize trait probability
        trait_total = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_total



if __name__ == "__main__":
    main()




# I'm sorry, it's too hard. It's even harder if I’m understand it in English.🙏🏼
################## Understanding ##################

### Understanding_1 ###
# 當一個人有2份特定基因時（例如兩份突變基因），他們會確定傳遞一份特定基因給孩子，
# 但這份基因在傳遞過程中仍然有可能發生突裝。
# 所以，1- PROBS［"mutation"］= 1-0.01 的解釋是：
# - 確定會傳遞一份特定基因給孩子，但是：    
    # - 有0.01的概率，這份基因在傳遞過程中會發生突變（變成非特定基因）。
    # - 有1-0.01=0.99的概率，這份基因在傳過程中保持不變。
# 因此，當父母有2份特定基因時，他們傳遞並保持這份特定基因不變的概率是1-PROBS™mutation"］= 0.99。


### Understanding_2 ###
# -突變概率 PROBS["mutation”] = 0.01
# 假設父親有一份正常基因和一份突變基因。
# 1. 傳遞正常基因的情況：
    # - 父親有0.5的概率傳遞正常基因。
    # - 但是這份正常基因在傳遞過程中有 0.01的概率突變成異常基因
    # - 所以傳遞正常基因保持不變的概率是：0.5 x (1 - 0.01）= 0.5 x 0.99 = 0.495
# 2. 傳遞突變基因的情況：
    # - 父親有 0.5 的概率傳遞突變基因。
    # - 這份突變基因在傳遞過程中也有 0.01 的概率恢復成正常基因
    # - 所以，傳遞突變基因且基因保持不變的概率是： 0.5 x (1 - 0.01) = 0.5 x 0.99 = 0.495
# 3. 結論：
    # - 傳遞並保持正常基因的概率是 0.495
    # - 傳遞但突變成異常基因的概率是 0.5 x 0.01 = 0.005
# 將以上兩種情況相加，傳�