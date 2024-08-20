import json


class Ship:
    def __init__(
        self,
        ship_length,
        row=None,
        col=None,
        is_horizontal=True,
        is_alive=True,
        sunk_coordinates=set(),
    ):
        super().__init__()
        self.ship_length = ship_length
        self.move(row, col, is_horizontal)
        self.is_alive = is_alive
        self.sunk_coordinates = sunk_coordinates

    def sunk_coordinate(self, row, col):
        self.sunk_coordinates.add((row, col))

        if self.is_sunk():
            self.is_alive = False

    def repair_coordinate(self, row, col):
        # Use remove to throw exception
        if self.is_alive:
            self.sunk_coordinates.discard((row, col))

    def is_sunk(self):
        return len(self.sunk_coordinates) == self.ship_length

    def is_coordinate_part_of_ship(self, row, col):
        return (row, col) in self.coordinates

    def fill_coordinates(self):
        if self.row == None and self.col == None:
            self.coordinates = []
            return

        self.coordinates = [
            (
                self.row + tile * (not self.is_horizontal),
                self.col + tile * self.is_horizontal,
            )
            for tile in range(self.ship_length)
        ]

    def flip(self):
        self.is_horizontal = not self.is_horizontal
        self.fill_coordinates()

    def move(self, row, col, is_horizontal):
        self.row = row
        self.col = col
        self.is_horizontal = is_horizontal
        self.fill_coordinates()

    def __repr__(self):
        return f"<Ship with length {self.ship_length}, is horizontal {self.is_horizontal} at {self.coordinates} with sunk {self.sunk_coordinates}>"

    def serialize(self):
        """Serialize the Ship object to a JSON string."""
        ship_data = {
            "ship_length": self.ship_length,
            "row": self.row,
            "col": self.col,
            "is_horizontal": self.is_horizontal,
            "is_alive": self.is_alive,
            "sunk_coordinates": list(self.sunk_coordinates),
        }
        return json.dumps(ship_data)

    @staticmethod
    def deserialize(ship_json):
        """Deserialize a JSON string into a Ship object."""
        ship_data = json.loads(ship_json)
        ship = Ship(
            ship_length=ship_data["ship_length"],
            row=ship_data["row"],
            col=ship_data["col"],
            is_horizontal=ship_data["is_horizontal"],
            is_alive=ship_data["is_alive"],
            sunk_coordinates=set(
                tuple(coord) for coord in ship_data["sunk_coordinates"]
            ),
        )
        return ship


s = Ship(3, 10, 1, False)
s.fill_coordinates()
print(s.is_coordinate_part_of_ship(1, 1))
print(s.is_coordinate_part_of_ship(1, 11))
s.sunk_coordinate(1, 1)
s.sunk_coordinate(2, 1)
s.sunk_coordinate(3, 1)
print(s)

gg = s.serialize()
ss = Ship.deserialize(gg)
print(ss)
