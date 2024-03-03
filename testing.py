from control import train,hash_board_r
from game import board

X_alpha= 0.1
X_epsilon = 0.15
O_alpha = 0.1
O_epsilon = 0.05
X_gamma = 0.9
O_gamma= 0.9


player1, player2 = train(X_alpha,X_epsilon,O_alpha,O_epsilon,X_gamma,O_gamma)
b = board(3)
player1.epsilon=0
player2.epsilon=0
print(player1.Q)
while True:
    
    bot_action  = player1.policy(hash_board_r(b.current_state()))
    print(bot_action)
    b.place(player1.symbol,bot_action)
    b.draw_board()
    user = input("ENTER ROW COL: ").split(',')
    row,col = int(user[0]),int(user[1])
    b.place('O',(row,col))
    if b.game_over():
        b.reset()