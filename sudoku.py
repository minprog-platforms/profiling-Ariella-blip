########/
# Ariella Hiele
#
# Minor Programmeren
#
# A program that solves a sudoku, if used in combination with solve.py. 
########/


from __future__ import annotations
from typing import Iterable, Sequence


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        new_row = list(self._grid[y])

        new_row[x] = str(value)

        self._grid[y] = ''.join(new_row)

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        row = self._grid[y]
        new_row = row[:x] + "0" + row[x + 1:]
        self._grid[y] = new_row

    def copy(self) -> "Sudoku":
        """Creates a deepcopy of this Sudoku puzzle."""
        return Sudoku(self._grid)

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        row = self._grid[y]
        return int(row[x])

    def options_at(self, x: int, y: int) -> Sequence[int]:
        """Returns all possible values (options) at x,y."""

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        options = ({1, 2, 3, 4, 5, 6, 7, 8, 9}
                   - set(self.row_values(y))
                   - set(self.column_values(x))
                   - set(self.block_values(block_index)))

        return list(options)

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            for x in range(9):
                if self.value_at(x, y) == 0:
                    return x, y

        return -1, -1

    def row_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th row."""

        return list(map(int, self._grid[i]))

    def column_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            values.append(self.value_at(i, j))

        return values

    def block_values(self, i: int) -> Sequence[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self.value_at(x, y))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        for i in range(9):
            if (set(self.column_values(i))) - {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return False
            if (set(self.row_values(i))) - {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return False
            if (set(self.block_values(i))) - {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return False

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
