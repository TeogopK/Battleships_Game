from game.visuals.visual_board import VisualBoard


class Player:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.board = VisualBoard(x, y)  # Create a visual board for the player
        self.is_turn = False
        self.x = x
        self.y = y

    def take_turn(self):
        self.is_turn = True

    def end_turn(self):
        self.is_turn = False

    def are_all_ships_sunk(self):
        return self.board.are_all_ships_sunk()

    def choose_attack(self, row, col, opponent):
        if opponent.board.is_coordinate_shot_at(row, col):
            print("Coordinate already shot")
            return False

        if opponent.board.register_shot(row, col):
            print(f"Hit at ({row}, {col})!")
        else:
            print(f"Miss at ({row}, {col})!")

        return True
