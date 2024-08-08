from game.visuals.visual_board import VisualBoard


class Player:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.board = VisualBoard(x, y)
        self.is_turn = False
        self.x = x
        self.y = y

    def take_turn(self):
        self.is_turn = True

    def end_turn(self):
        self.is_turn = False

    def are_all_ships_sunk(self):
        return self.board.are_all_ships_sunk()
