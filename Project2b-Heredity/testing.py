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


# people_lib = {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False}, 
#               'Charlie': {'name': 'Charlie', 'mother': 'Molly', 'father': 'Arthur', 'trait': False}, 
#               'Fred': {'name': 'Fred', 'mother': 'Molly', 'father': 'Arthur', 'trait': True}, 
#               'Ginny': {'name': 'Ginny', 'mother': 'Molly', 'father': 'Arthur', 'trait': None}, 
#               'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': False}, 
#               'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': None}}


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
    names = set(people)
    # names = {'Ron', 'Ginny', 'Arthur', 'Charlie', 'Fred', 'Molly'}
    
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        # print(bool(fails_evidence))
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # print(f"one_gene: {one_gene}, two_genes: {two_genes}")

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
                up = update
    # Ensure probabilities sum to 1
    normalize(probabilities)
    
    # # Print results
    # for person in people:
    #     print(f"{person}:")
    #     for field in probabilities[person]:
    #         print(f"  {field.capitalize()}:")
    #         for value in probabilities[person][field]:
    #             p = probabilities[person][field][value]
    #             print(f"    {value}: {p:.4f}")



    # Run test in terminal
        #  python testing.py data/family1.csv
def joint_probability(people, one_gene, two_genes, have_trait):
    # people: {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False},
    joint_probability = 1

    # iterate Names in dictionary e.g Arthur
    for person in people:
        mother = people[person]["mother"]
        father = people[person]["father"]
        trait_TF = people[person]["trait"] # True or False
        mutation = PROBS["mutation"] # 0.01

        # ❗️❗️ 'one_gene' and 'two_genes' are predefined in the project. 
            # We only need to use these values to calculate the joint_probability.
        if person in one_gene:
            gene_prob = PROBS["gene"][1] # 0.03, from PROBS dic
            gene_num = 1                 # assign a variable to know how many gene e.g Arthur have 
        elif person in two_genes:
            gene_prob = PROBS["gene"][2]
            gene_num = 2
        else:
            gene_prob = PROBS["gene"][0]
            gene_num = 0


        """ ### No parent data ### """
        # Handle the situation where there is no parent information available.
        ### Parent data both are None ###
        if mother == None and father == None:

            if trait_TF == None:
                trait_prob = PROBS["trait"][gene_num][True] + PROBS["trait"][gene_num][False]
                joint_probability = joint_probability * (gene_prob * trait_prob)
            else:
                trait_prob = PROBS["trait"][gene_num][trait_TF]

                # Update `joint_probability`
                joint_probability = joint_probability * (gene_prob * trait_prob)
        
        ### Father or Mother data are None ###
        elif mother == None or father == None:
            if mother == None:
                parent = father # Set a variable `parent` to check how many genes the parents have.
            else:
                parent = mother
            
            # Get parent gene number
            if parent in one_gene:
                parent_gene_num = 1
            elif parent in two_genes:
                parent_gene_num = 2
            else:
                parent_gene_num = 0
                
            # Iterated through 3 possible scenarios of the child's gene quantity (0, 1 or 2)
            # Why iterate through 3 situations? 
                # Because we want the `prob_gene` obtained in each case, and then use this value to update the `joint_probability`.
            for child_genes in range(3): 
                if child_genes == 0:
                    if parent_gene_num == 0:
                        prob_gene = 1 - mutation # child and parent no gene
                    else:
                        prob_gene = mutation # child no gene and parent have gene
                elif child_genes == 1:
                    if parent_gene_num == 0 or parent_gene_num == 2: 
                        prob_gene = mutation # child 1 gene and parent have NO genes or 2 genes
                    else:
                        prob_gene = 1 - mutation # child 1 gene and parent have 1 genes
                else:  # child_genes == 2
                    if parent_gene_num == 2:
                        prob_gene = 1 - mutation # child 2 gene and parent have 2 genes
                    else:
                        prob_gene = mutation # child 2 gene and parent NOT have 2 genes
                

                # Use the child_genes to get(and calculate) `trait_prob` from PROBS dictionary
                if trait_TF == None:
                    trait_prob = PROBS["trait"][child_genes][True] + PROBS["trait"][child_genes][False]
                else:
                    trait_prob = PROBS["trait"][child_genes][trait_TF]
                    
                # Update `joint_probability`
                joint_probability *= prob_gene * trait_prob
                # joint_probability = joint_probability * prob_gene * trait_prob


            """ ### With parent data ### """
            # Handle the situation where there is WITH parent information available.
            ### Iterate all scenarios of (mother have 0,1,2 gene) and (father have 0,1,2 gene)
        else:
           # Get mother gene number
            if mother in one_gene:
                mother_gene_prob = PROBS["gene"][1]
                mother_gene_num = 1
            elif mother in two_genes:
                mother_gene_prob = PROBS["gene"][2]
                mother_gene_num = 2
            else:
                mother_gene_prob = PROBS["gene"][0]
                mother_gene_num = 0

            # Get father gene number
            if father in one_gene:
                father_gene_prob = PROBS["gene"][1]
                father_gene_num = 1
            elif father in two_genes:
                father_gene_prob = PROBS["gene"][2]
                father_gene_num = 2
            else:
                father_gene_prob = PROBS["gene"][0]
                father_gene_num = 0


            # Intialize 0, 1, 2 genes probability 
            zero_gene_prob = 0 # The probability of child have 1 gene
            one_gene_prob = 0
            two_genes_prob = 0
            

            ### Knowing the number of genes in the parents ###
                # we can calculate the probability of the child getting 0, 1, or 2 genes. 
            ###### ❗️ Different scenarios will use different probability formulas. ######
            parent_total_genes = mother_gene_num + father_gene_num

            # One parent has one gene, and the other parent has zero genes.
            if parent_total_genes == 1:
                zero_gene_prob = (1 - mutation) * (1 - mutation)
                one_gene_prob = (1 - mutation) * mutation + mutation * (1 - mutation)
                # two_genes_prob = This is not possible here because only one of the parties has the genes
                
            # Both parents each have one gene.
            if parent_total_genes == 2:
                zero_gene_prob = mutation * (1 - mutation) + mutation * (1 - mutation)
                one_gene_prob = (1 - mutation) * (1 - mutation) + mutation * mutation
                two_genes_prob = (1 - mutation) * mutation + (1 - mutation) * mutation

            # One parent has one gene, while the other parent has two genes.
            if parent_total_genes == 3:
                zero_gene_prob = (1 - mutation) * mutation
                one_gene_prob = 2 * (1 - mutation) * (1 - mutation)
                two_genes_prob = (1 - mutation) * (1 - mutation) + 2 * mutation * (1 - mutation)

            # The probability of both parents having no genes is "one_gene_prob".
            if parent_total_genes == 0:
                zero_gene_prob = (1 - mutation) * (1 - mutation)
                one_gene_prob = (1 - mutation) * mutation + mutation * (1 - mutation)
                # two_genes_prob = It's impossible because neither parent has the gene.

            # The scenario where both parents have 2 genes
            if parent_total_genes == 4:
                zero_gene_prob = mutation * mutation
                one_gene_prob = mutation * (1 - mutation) + (1 - mutation) * mutation
                two_genes_prob = (1 - mutation) * (1 - mutation)

            # The case where the parents' gene combination is (2,0) or (0,2).
            if parent_total_genes == 2 and (mother_gene_num == 2 or father_gene_num == 2):
                zero_gene_prob = mutation * (1 - mutation)
                one_gene_prob = (1 - mutation) * (1 - mutation) + mutation * mutation
                two_genes_prob = (1 - mutation) * mutation


            ########################################################################
            # # Get trait_prob in PROBS dictionary based on different gene numbers
            # # child have 0 gene 
            # trait_prob_zero = PROBS["trait"][0][True] 
            # joint_zero_gene_prob = zero_gene_prob * trait_prob_zero

            # # child have 1 gene 
            # trait_prob_one = PROBS["trait"][1][True] 
            # joint_one_gene_prob = one_gene_prob * trait_prob_one

            # # child have 2 gene 
            # trait_prob_two = PROBS["trait"][2][True] 
            # joint_two_gene_prob = two_genes_prob * trait_prob_two
            ########################################################################


            # Check how many gene child have 
                # Then assign a probability from above part e.g `one_gene_prob`
            if person in one_gene:
                gene_prob = one_gene_prob
            elif person in two_genes:
                gene_prob = two_genes_prob
            else:
                gene_prob = zero_gene_prob


            # Check if child have trait or not
                # then get the probability from PROBS dictionary
            if person in have_trait:
                trait_prob = PROBS["trait"][gene_num][True]
            else:
                trait_prob = PROBS["trait"][gene_num][False]
            
            # Update `joint_probability`
            joint_probability *= gene_prob * trait_prob


        # Check if child have "trait" or not
            # then get the probability from PROBS dictionary
        if person in have_trait:
            trait_prob = PROBS["trait"][gene_num][True]
        else:
            trait_prob = PROBS["trait"][gene_num][False]
        
        # Update `joint_probability`
        # Final `joint_probability`
        joint_probability *= gene_prob * trait_prob


    # print(joint_probability)
    return joint_probability
    



def update(probabilities, one_gene, two_genes, have_trait, p):
        # probabilities[person]["gene"] = {2: 0, 1: 0, 0: 0}
        # probabilities[person]["trait"] = {True: 0, False: 0}
        # joint_probability(people, one_gene, two_genes, have_trait)

    for person in probabilities:
        # In this section, the probabilities are initially 0, so we update the value with `+=`.
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

        if person in two_genes:
            probabilities[person]["gene"][2] += p 
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p

    # When it's done, the `probabilities{}` data will be updated
    

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        print(person)
        print(probabilities[person]["gene"])
        print(probabilities[person]["gene"].values())
        print(gene_total)
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= gene_total


    trait_total = sum(probabilities[person]["trait"].values())
    for trait in probabilities[person]["trait"]:
        probabilities[person]["trait"][trait] /= trait_total






############################# version 1 #############################
# def joint_probability(people, one_gene, two_genes, have_trait):
#     """
#     Compute and return a joint probability.

#     The probability returned should be the probability that
#         * everyone in set `one_gene` has one copy of the gene, and
#         * everyone in set `two_genes` has two copies of the gene, and
#         * everyone not in `one_gene` or `two_gene` does not have the gene, and
#         * everyone in set `have_trait` has the trait, and
#         * everyone not in set` have_trait` does not have the trait.
#     """
# # people: {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False},
#     joint_probability = 1

#     # iterate Names in dictionary e.g Arthur
#     for person in people:
#         mother = people[person]["mother"]
#         father = people[person]["father"]
#         trait_TF = people[person]["trait"] # True or False
#         mutation = PROBS["mutation"] # 0.01

#         # ❗️❗️ 'one_gene' and 'two_genes' are predefined in the project. 
#             # We only need to use these values to calculate the joint_probability.
#         if person in one_gene:
#             gene_prob = PROBS["gene"][1] # 0.03, from PROBS dic
#             gene_num = 1                 # assign a variable to know how many gene e.g Arthur have 
#         elif person in two_genes:
#             gene_prob = PROBS["gene"][2]
#             gene_num = 2
#         else:
#             gene_prob = PROBS["gene"][0]
#             gene_num = 0


#         """ ### No parent data ### """
#         # Handle the situation where there is no parent information available.
#         ### Parent data both are None ###
#         if mother == None and father == None:

#             if trait_TF == None:
#                 trait_prob = PROBS["trait"][gene_num][True] + PROBS["trait"][gene_num][False]
#                 joint_probability = joint_probability * (gene_prob * trait_prob)
#             else:
#                 trait_prob = PROBS["trait"][gene_num][trait_TF]

#                 # Update `joint_probability`
#                 joint_probability = joint_probability * (gene_prob * trait_prob)
        
#         ### Father or Mother data are None ###
#         elif mother == None or father == None:
#             if mother == None:
#                 parent = father # Set a variable `parent` to check how many genes the parents have.
#             else:
#                 parent = mother
            
#             # Get parent gene number
#             if parent in one_gene:
#                 parent_gene_num = 1
#             elif parent in two_genes:
#                 parent_gene_num = 2
#             else:
#                 parent_gene_num = 0
                
#             # Iterated through 3 possible scenarios of the child's gene quantity (0, 1 or 2)
#             # Why iterate through 3 situations? 
#                 # Because we want the `prob_gene` obtained in each case, and then use this value to update the `joint_probability`.
#             for child_genes in range(3): 
#                 if child_genes == 0:
#                     if parent_gene_num == 0:
#                         prob_gene = 1 - mutation # child and parent no gene
#                     else:
#                         prob_gene = mutation # child no gene and parent have gene
#                 elif child_genes == 1:
#                     if parent_gene_num == 0 or parent_gene_num == 2: 
#                         prob_gene = mutation # child 1 gene and parent have NO genes or 2 genes
#                     else:
#                         prob_gene = 1 - mutation # child 1 gene and parent have 1 genes
#                 else:  # child_genes == 2
#                     if parent_gene_num == 2:
#                         prob_gene = 1 - mutation # child 2 gene and parent have 2 genes
#                     else:
#                         prob_gene = mutation # child 2 gene and parent NOT have 2 genes
                

#                 # Use the child_genes to get(and calculate) `trait_prob` from PROBS dictionary
#                 if trait_TF == None:
#                     trait_prob = PROBS["trait"][child_genes][True] + PROBS["trait"][child_genes][False]
#                 else:
#                     trait_prob = PROBS["trait"][child_genes][trait_TF]
                    
#                 # Update `joint_probability`
#                 joint_probability *= prob_gene * trait_prob
#                 # joint_probability = joint_probability * prob_gene * trait_prob


#             """ ### With parent data ### """
#             # Handle the situation where there is WITH parent information available.
#             ### Iterate all scenarios of (mother have 0,1,2 gene) and (father have 0,1,2 gene)
#         else:
#            # Get mother gene number
#             if mother in one_gene:
#                 mother_gene_prob = PROBS["gene"][1]
#                 mother_gene_num = 1
#             elif mother in two_genes:
#                 mother_gene_prob = PROBS["gene"][2]
#                 mother_gene_num = 2
#             else:
#                 mother_gene_prob = PROBS["gene"][0]
#                 mother_gene_num = 0

#             # Get father gene number
#             if father in one_gene:
#                 father_gene_prob = PROBS["gene"][1]
#                 father_gene_num = 1
#             elif father in two_genes:
#                 father_gene_prob = PROBS["gene"][2]
#                 father_gene_num = 2
#             else:
#                 father_gene_prob = PROBS["gene"][0]
#                 father_gene_num = 0


#             # Intialize 0, 1, 2 genes probability 
#             zero_gene_prob = 0 # The probability of child have 1 gene
#             one_gene_prob = 0
#             two_genes_prob = 0
            

#             ### Knowing the number of genes in the parents ###
#                 # we can calculate the probability of the child getting 0, 1, or 2 genes. 
#             ###### ❗️ Different scenarios will use different probability formulas. ######
#             parent_total_genes = mother_gene_num + father_gene_num

#             # One parent has one gene, and the other parent has zero genes.
#             if parent_total_genes == 1:
#                 zero_gene_prob = (1 - mutation) * (1 - mutation)
#                 one_gene_prob = (1 - mutation) * mutation + mutation * (1 - mutation)
#                 # two_genes_prob = This is not possible here because only one of the parties has the genes
                
#             # Both parents each have one gene.
#             if parent_total_genes == 2:
#                 zero_gene_prob = mutation * (1 - mutation) + mutation * (1 - mutation)
#                 one_gene_prob = (1 - mutation) * (1 - mutation) + mutation * mutation
#                 two_genes_prob = (1 - mutation) * mutation + (1 - mutation) * mutation

#             # One parent has one gene, while the other parent has two genes.
#             if parent_total_genes == 3:
#                 zero_gene_prob = (1 - mutation) * mutation
#                 one_gene_prob = 2 * (1 - mutation) * (1 - mutation)
#                 two_genes_prob = (1 - mutation) * (1 - mutation) + 2 * mutation * (1 - mutation)

#             # The probability of both parents having no genes is "one_gene_prob".
#             if parent_total_genes == 0:
#                 zero_gene_prob = (1 - mutation) * (1 - mutation)
#                 one_gene_prob = (1 - mutation) * mutation + mutation * (1 - mutation)
#                 # two_genes_prob = It's impossible because neither parent has the gene.

#             # The scenario where both parents have 2 genes
#             if parent_total_genes == 4:
#                 zero_gene_prob = mutation * mutation
#                 one_gene_prob = mutation * (1 - mutation) + (1 - mutation) * mutation
#                 two_genes_prob = (1 - mutation) * (1 - mutation)

#             # The case where the parents' gene combination is (2,0) or (0,2).
#             if parent_total_genes == 2 and (mother_gene_num == 2 or father_gene_num == 2):
#                 zero_gene_prob = mutation * (1 - mutation)
#                 one_gene_prob = (1 - mutation) * (1 - mutation) + mutation * mutation
#                 two_genes_prob = (1 - mutation) * mutation


#             ########################################################################
#             # # Get trait_prob in PROBS dictionary based on different gene numbers
#             # # child have 0 gene 
#             # trait_prob_zero = PROBS["trait"][0][True] 
#             # joint_zero_gene_prob = zero_gene_prob * trait_prob_zero

#             # # child have 1 gene 
#             # trait_prob_one = PROBS["trait"][1][True] 
#             # joint_one_gene_prob = one_gene_prob * trait_prob_one

#             # # child have 2 gene 
#             # trait_prob_two = PROBS["trait"][2][True] 
#             # joint_two_gene_prob = two_genes_prob * trait_prob_two
#             ########################################################################


#             # Check how many gene child have 
#                 # Then assign a probability from above part e.g `one_gene_prob`
#             if person in one_gene:
#                 gene_prob = one_gene_prob
#             elif person in two_genes:
#                 gene_prob = two_genes_prob
#             else:
#                 gene_prob = zero_gene_prob


#             # Check if child have trait or not
#                 # then get the probability from PROBS dictionary
#             if person in have_trait:
#                 trait_prob = PROBS["trait"][gene_num][True]
#             else:
#                 trait_prob = PROBS["trait"][gene_num][False]
            
#             # Update `joint_probability`
#             joint_probability *= gene_prob * trait_prob


#         # # Check if child have "trait" or not
#         #     # then get the probability from PROBS dictionary
#         # if person in have_trait:
#         #     trait_prob = PROBS["trait"][gene_num][True]
#         # else:
#         #     trait_prob = PROBS["trait"][gene_num][False]
        
#         # # Update `joint_probability`
#         # # Final `joint_probability`
#         # joint_probability *= gene_prob * trait_prob


#     # print(joint_probability)
#     return joint_probability












# This Version is work
# def joint_probability(people, one_gene, two_genes, have_trait):
#     """
#     Compute and return a joint probability.
#     """
#     joint_probability = 1

#     for person in people:
#         genes = 0
#         if person in one_gene:
#             genes = 1
#         elif person in two_genes:
#             genes = 2

#         father = people[person]["father"]
#         mother = people[person]["mother"]

#         # Probability of person having genes
#         if mother is None and father is None:
#             # If there is no parent information, use given gene probabilities
#             joint_probability *= PROBS["gene"][genes]
#         else:
#             passing = {mother: 0, father: 0}

#             for parent in passing:
#                 # Check genes of parents
#                 if parent in two_genes:
#                     passing[parent] = 1 - PROBS["mutation"]
#                 elif parent in one_gene:
#                     passing[parent] = 0.5
#                 else:
#                     passing[parent] = PROBS["mutation"]

#             # Calculate probabilities based on parents' genes
#             if genes == 2:
#                 joint_probability *= passing[mother] * passing[father]
#             elif genes == 1:
#                 joint_probability *= passing[mother] * (1 - passing[father]) + \
#                                      (1 - passing[mother]) * passing[father]
#             else:
#                 joint_probability *= (1 - passing[mother]) * (1 - passing[father])

#         # Update the joint probability for traits
#         trait = person in have_trait
#         joint_probability *= PROBS["trait"][genes][trait]

#         # If the trait is known, check against it
#         if people[person]["trait"] is not None and people[person]["trait"] != trait:
#             joint_probability = 0

#     return joint_probability









##################################################################################################################


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

    




if __name__ == "__main__":
    main()
