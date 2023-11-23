lib = {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False}, 
              'Charlie': {'name': 'Charlie', 'mother': 'Molly', 'father': 'Arthur', 'trait': False}, 
              'Fred': {'name': 'Fred', 'mother': 'Molly', 'father': 'Arthur', 'trait': True}, 
              'Ginny': {'name': 'Ginny', 'mother': 'Molly', 'father': 'Arthur', 'trait': None}, 
              'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': False}, 
              'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': None}}


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


# probabilities = {
#     person: {
#         "gene": {
#             2: 0,
#             1: 0,
#             0: 0
#         },
#         "trait": {
#             True: 0,
#             False: 0
#         }
#     }
# }


# for person in people:
#     genes = 0
#     if person in one_gene:
#         genes = 1
#     elif person in two_genes:
#         genes = 2

t1 = PROBS["gene"][1]

print(t1)



