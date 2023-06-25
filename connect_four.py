import numpy as np
import neat

class ConnectFourGame():
    def __init__(self, x=7, y=6) -> None:
        self.board = np.array([[0 for i in range(y)] for j in range(x)])
        self.current_player = 1
    @property
    def width(self):
        return len(self.board)
    
    @property
    def height(self):
        if (len(self.board) == 0):
            return 0
        return len(self.board)

    @property
    def nn_data(self):
        grid_data = self.board.flatten().tolist()
        return grid_data
    
    def place(self, column: int):
        column = column - 1
        if not (-1 <= column and column < self.width):
            return False
        
        if (self.board[column][-1] != 0):
            return False
        
        index = np.where(self.board[column]==0)[0][0]

        self.board[column][index] = self.current_player
        self.switch_player()
        return True
    
    
    def switch_player(self):
        if (self.current_player == 1):
            self.current_player = 2
        else:
            self.current_player = 1
    
    def print_board(self):
        for row in range(self.height-1):
            print("".join([str(self.height - row - 1), ' '] + [str(self.board[x][self.height - row - 2]) + ' ' for x in range(self.width)]))
        
        print("".join(['  '] + [str(x+1) + ' ' for x in range(self.width)]))
        
    def check_win(self, player):
        board = self.board
        # verticalCheck
        for i in range(len(board) - 3):
            for j in range(len(board[0]) - 1):
                if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                    return True

        # horizontalCheck
        for j in range(len(board[0]) - 4):
            for i in range(len(board) - 1):
                if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player:
                    return True

        # ascendingDiagonalCheck
        for i in range(3, len(board[0]) - 1):
            for j in range(0, len(board) - 3):
                if board[i][j] == player and board[i-1][j+1] == player and board[i-2][j+2] == player and board[i-3][j+3] == player:
                    return True

        # descendingDiagonalCheck
        for i in range(0, len(board[0]) - 3):
            for j in range(3, len(board) - 1):
                if board[i][j] == player and board[i-1][j-1] == player and board[i-2][j-2] == player and board[i-3][j-3] == player:
                    return True

        return False

    def check_board_full(self):
        return all([self.board[x, y] != 0 for y in range(self.height - 1) for x in range(self.width - 1)])
    

game = ConnectFourGame()

# while True:
#     game.place(int(input('hi: ')))
#     game.print_board()
#     print(game.check_win(1))
