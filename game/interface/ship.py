"""
Module that handles the Ship logic as an interface entity.
"""

import json


class Ship:
    def __init__(
        self,
        ship_length,
        row=None,
        col=None,
        is_horizontal=True,
        is_alive=True,
        sunk_coordinates=None,
    ):
        """
        Initialize a new Ship instance.

        Args:
            ship_length (int): The length of the ship.
            row (int, optional): The starting row of the ship. Defaults to None.
            col (int, optional): The starting column of the ship. Defaults to None.
            is_horizontal (bool, optional): Orientation of the ship. Defaults to True.
            is_alive (bool, optional): Status of the ship. Defaults to True.
            sunk_coordinates (set, optional): Coordinates of the sunk parts of the ship. Defaults to None.
        """
        self.ship_length = ship_length
        self.coordinates = None

        self.is_horizontal = is_horizontal
        self.is_alive = is_alive

        self.move(row, col, is_horizontal)

        self.sunk_coordinates = (
            sunk_coordinates if sunk_coordinates is not None else set()
        )

    def sunk_coordinate(self, row, col):
        """
        Mark a coordinate as sunk.

        Args:
            row (int): The row of the coordinate to mark as sunk.
            col (int): The column of the coordinate to mark as sunk.
        """
        if (row, col) in self.coordinates:
            self.sunk_coordinates.add((row, col))

        if self.is_sunk():
            self.is_alive = False

    def repair_coordinate(self, row, col):
        """
        Repair a coordinate of the ship.

        Args:
            row (int): The row of the coordinate to repair.
            col (int): The column of the coordinate to repair.
        """
        # Use remove to throw exception
        if self.is_alive:
            self.sunk_coordinates.discard((row, col))

    def is_sunk(self):
        """
        Checks if the ship is sunk.

        Returns:
            bool: True if the ship is sunk, False otherwise.
        """
        return len(self.sunk_coordinates) == self.ship_length

    def is_coordinate_part_of_ship(self, row, col):
        """
        Checks if the given coordinate (row, col) is part of the ship.

        Parameters:
        - row (int): The row coordinate.
        - col (int): The column coordinate.

        Returns:
        - bool: True if the coordinate is part of the ship, False otherwise.
        """
        return (row, col) in self.coordinates

    def fill_coordinates(self):
        """
        Fills the ship's coordinates based on the given row, column, and orientation.
        If the row and column are not specified (None), the coordinates will be set to an empty list.

        Parameters:
        - self: The Ship object.
        """
        if self.row is None and self.col is None:
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
        """
        Flips the ship's orientation.

        This method toggles the ship's orientation between horizontal and vertical.
        After flipping, the ship's coordinates are updated accordingly.
        """
        self.is_horizontal = not self.is_horizontal
        self.fill_coordinates()

    def move(self, row, col, is_horizontal):
        """
        Moves the ship to the specified row and column on the game board.

        Args:
            row (int): The row index where the ship will be moved.
            col (int): The column index where the ship will be moved.
            is_horizontal (bool): Indicates whether the ship will be placed horizontally or vertically.
        """
        self.row = row
        self.col = col
        self.is_horizontal = is_horizontal
        self.fill_coordinates()

    def __repr__(self):
        """
        Return a string representation of the Ship object.

        The string includes the length of the ship, whether it is horizontal or not,
        its coordinates, and the coordinates of any sunk parts of the ship.

        Returns:
            str: A string representation of the Ship object.
        """
        return (
            f"<Ship with length {self.ship_length}, "
            f"is horizontal {self.is_horizontal}, "
            f"at {self.coordinates}, "
            f"with sunk {self.sunk_coordinates}>"
        )

    def serialize(self):
        """
        Serialize the Ship object to a JSON string.

        Returns:
            str: A JSON string representing the serialized Ship object.
        """
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
        """
        Deserialize a ship object from a JSON string representation.

        Args:
            ship_json (str): The JSON string representing the ship object.

        Returns:
            Ship: The deserialized ship object.

        """
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
