from nim import *



# # 創建 NimAI 實例
# ai = NimAI()

# # 創建測試用的狀態和行動
# test_state = [1, 2, 3]
# test_action = (1, 2)

# # 調用 get_q_value 函數
# ai.get_q_value(test_state, test_action)





n=100
game = Nim()
play = NimAI()
train = train(n)

dic = play.train(n)

state = game.piles.copy()
print(state)

state_tuple = tuple(state)


print(state_tuple)

print(train)