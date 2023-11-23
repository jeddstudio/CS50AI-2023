from minesweeper import MinesweeperAI, Minesweeper


# ai = MinesweeperAI()

# ai.mark_safe((3,3))

# print(ai.safes)

HEIGHT = 8
WIDTH = 8
cell = (3,3)



# neighbours = set()

# for neighbour_x in [-1, 0, 1]:
    
#     for neighbour_y in [-1, 0, 1]:

#         neighbour_row = cell[0] + neighbour_x 

#         neighbour_col = cell[1] + neighbour_y



#         if (0 <= neighbour_row < HEIGHT and
#             0 <= neighbour_col < WIDTH and
#             (neighbour_x, neighbour_y)!= (0, 0)):

#             print("----------------------------------------")
#             print(f"x = {neighbour_x}")
#             print(f"y = {neighbour_x}")
#             print(f"cell[0][1] = {cell}")

#             print(f"cell[0]: {cell[0]} + x: {neighbour_x} = row: {neighbour_row}")
#             print(f"cell[1]: {cell[0]} + y: {neighbour_x} = col: {neighbour_col}")
#             print(f"neighbour_row = {neighbour_row}, neighbour_col = {neighbour_col}")
#             print(f"0 <= {neighbour_row} < HEIGHT")
#             print(f"0 <= {neighbour_col} < WIDTH")
#             print(f"({neighbour_x}, {neighbour_y})!= (0, 0))")
#             print(f"x, y = {neighbour_x, neighbour_y}")
#             print("----------------------------------------")
        
#         elif(neighbour_x, neighbour_y) == (0, 0):
#             print("############ The cell itself ############")
#             print(f"x = {neighbour_x}")
#             print(f"y = {neighbour_x}")
#             print(f"cell[0][1] = {cell}")

#             print(f"cell[0]: {cell[0]} + x: {neighbour_x} = row: {neighbour_row}")
#             print(f"cell[1]: {cell[0]} + y: {neighbour_x} = col: {neighbour_col}")
#             print(f"neighbour_row = {neighbour_row}, neighbour_col = {neighbour_col}")
#             print(f"0 <= {neighbour_row} < HEIGHT")
#             print(f"0 <= {neighbour_col} < WIDTH")
#             print(f"({neighbour_x}, {neighbour_y})!= (0, 0))")
#             print(f"x, y = {neighbour_x, neighbour_y}")
#             print("########################################")





            # [(2,2), (2,3), (2,4)]
            # [(3,2), (3,3), (3,4)]
            # [(4,2), (4,3), (4,4)]












# # Define the sentences as lists of tuples
# knowledge_base = [
#     [(2,2), (2,3), (2,4)],  # Sentence 1
#     [(3,2), (3,3), (3,4)],  # Sentence 2
#     [(4,2), (4,3), (4,4)]   # Sentence 3
# ]

# # Iterating through all pairs of sentences in the knowledge base
# for i in range(len(knowledge_base)):
#     sentence1 = knowledge_base[i]  # Getting the i-th sentence
    
    
#     for j in range(i+1, len(knowledge_base)):
#         sentence2 = knowledge_base[j]  # Getting the j-th sentence
#         print(f"len(knowledge_base) = {len(knowledge_base)}")
#         print(f"sentence1 = {sentence1}")
#         print(f"sentence2 = {sentence2}")
        
#         # Printing out the sentences being compared
#         print(f"Comparing Sentence {i+1} ({sentence1}) with Sentence {j+1} ({sentence2})")
        
#         # Here you could perform additional operations, like finding common cells,
#         # subtracting sentences, etc., depending on your specific algorithm and what
#         # you want to achieve in each comparison.









# class Sentence:
#     def __init__(self, cells, count):
#         self.cells = cells
#         self.count = count

#     def __repr__(self):
#         return f"Cells: {self.cells}, Count: {self.count}"

# # Initial sentences in the knowledge base
# # Modified sentences in the knowledge base
# knowledge_base = [Sentence({(2,2), (2,3)}, 1),                 # Sentence 1
#                   Sentence({(2,2), (2,3), (2,4)}, 2),         # Sentence 2
#                   Sentence({(4,2), (4,3), (4,4)}, 1),         # Sentence 3
#                   ]



# # Iterating through each pair of sentences in the knowledge base
# for i, sentence_1 in enumerate(knowledge_base):
#     for j, sentence_2 in enumerate(knowledge_base[i+1:], start=i+1):
        
        
        
#         new_sentence = None
        
#         print("\n" + "@"*50 + "\n")
#         if sentence_1.cells.issubset(sentence_2.cells):
#             print("if")
#             # print(f"(sentence_1.cells:{sentence_1.cells}).issubset(sentence_2.cells:{sentence_2.cells})")
#             # print(f"Sentence {i+1} is a subset of Sentence {j+1}")
#             new_cells = sentence_2.cells - sentence_1.cells
#             # print(f"new_cells:{new_cells}")
#             new_count = sentence_2.count - sentence_1.count
#             new_sentence = Sentence(new_cells, new_count)
            
#         elif sentence_2.cells.issubset(sentence_1.cells):
#             print("elif")
#             # print(f"(sentence_2.cells:{sentence_2.cells}).issubset(sentence_1.cells:{sentence_1.cells})")
#             # print(f"Sentence {j+1} is a subset of Sentence {i+1}")
#             new_cells = sentence_1.cells - sentence_2.cells
#             # print(f"new_cells:{new_cells}")
#             new_count = sentence_1.count - sentence_2.count
#             new_sentence = Sentence(new_cells, new_count)
            
#         if new_sentence and new_sentence not in knowledge_base:
            
#             print("\n" + "#"*50 + "\n")
#             print(f"new_cells:{new_cells}")
#             print(f"new_count:{new_count}")
#             print(f"Comparing Sentence {i+1} and Sentence {j+1}")
#             print(f"new_sentence: {new_sentence}")
#             print("Adding new sentence to the knowledge base:")
#             print(new_sentence)
#             print("\n" + "#"*50 + "\n")
#             knowledge_base.append(new_sentence)
            
#         # print("\nCurrent knowledge base:")
#         # for k, sentence in enumerate(knowledge_base, start=1):
#         #     print(f"Sentence {k}: {sentence}")
#         # print("\n" + "-"*50 + "\n")







new_sentence = None


print(bool(new_sentence))


#233
        # When finish the cell(3,3) process 
            # Adding a new sentence("(2, 2), (2, 3),...) to the knowledge base(self.knowledge)
                # Turn(neighbours, count) to a Sentence() objects
                # Then add it into `self.knowledge`
                    # So you can access the attributes (cells and count) in the step 4
        # print(f"It is count: {count}")
        ######## self.knowledge.append(Sentence(neighbours, count)) ########
            # When you click the cell, if it is not mine, it will give you a number(that is the "count")
                # It is telling you how many mine around you


        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
            # `.cells` and `.count` is come from `self.knowledge.append(Sentence(neighbours, count))`
        



               