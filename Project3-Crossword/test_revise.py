from generate import CrosswordCreator, Crossword, Variable

# 假设的测试用的结构和单词文件路径
STRUCTURE_FILE = 'data/structure1.txt'
WORDS_FILE = 'data/words1.txt'

# 创建一个 Crossword 实例和 CrosswordCreator 实例
crossword = Crossword(STRUCTURE_FILE, WORDS_FILE)
creator = CrosswordCreator(crossword)

# # 定义测试用的变量和它们的域
# var1 = Variable(0, 0, 'down', 3)
# # var1 = CrosswordCreator.domain
# var2 = Variable(0, 1, 'across', 3)
# # var2 = CrosswordCreator.domain
# creator.domains[var1] = {'cat', 'car', 'bar'}
# creator.domains[var2] = {'bat', 'ball', 'car'}

# # 测试 revise 函数
# def test_revise(x, y):
#     revised = creator.revise(x, y)
#     print(f'Revised: {revised}')
#     print(f'Domain of {x}: {creator.domains[x]}')

# # 運行測試
# print('Before revise:')
# print(f'Domain of var1: {creator.domains[var1]}')
# print(f'Domain of var2: {creator.domains[var2]}\n')

# test_revise(var1, var2)

# print('\nAfter revise:')
# print(f'Domain of var1: {creator.domains[var1]}')
# print(f'Domain of var2: {creator.domains[var2]}')


creator.ac3()







