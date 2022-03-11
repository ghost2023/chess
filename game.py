from pieces import *
from constants import *

white_pieces = []
black_pieces = []

checked = None

def find_piece(loc):
    for white in white_pieces:
        if white.location == loc:
            return white
    for black in black_pieces:
        if black.location == loc:
            return black
    return None


def kill(piece):
    if piece.color == "W":
        white_pieces.remove(piece)
    else:
        black_pieces.remove(piece)


def isrock(piece):
    return isinstance(piece, Rock)


def reset_all():
    for white in white_pieces:
        white.check_moves()
    for black in black_pieces:
        black.check_moves()


class Game:
    def __init__(self) -> None:
        self.selected = None
        # Generate the white pieces
        offset = 6
        for i in range(8):
            white_pieces.append(Pawn("W", [i, offset]))

        for i in range(8):
            if i == 0 or i == 7:
                white_pieces.append(Rock("W", [i, offset + 1]))
            elif i == 1 or i == 6:
                white_pieces.append(Knight("W", [i, offset + 1]))
            elif i == 2 or i == 5:
                white_pieces.append(Bishop("W", [i, offset + 1]))
            elif i == 3:
                white_pieces.append(Queen("W", [i, offset + 1]))
            else:
                white_pieces.append(King("W", [i, offset + 1]))

        # Generate the Black pieces
        for i in range(8):
            black_pieces.append(Pawn("B", [i, 1]))

        for i in range(8):
            if i == 0 or i == 7:
                black_pieces.append(Rock("B", [i, 0]))
            elif i == 1 or i == 6:
                black_pieces.append(Knight("B", [i, 0]))
            elif i == 2 or i == 5:
                black_pieces.append(Bishop("B", [i, 0]))
            elif i == 3:
                black_pieces.append(Queen("B", [i, 0]))
            else:
                black_pieces.append(King("B", [i, 0]))

        # black_pieces.append(King("B", [3, 3]))
        # white_pieces.append(Pawn("W", [3, 6]))

        for white in white_pieces:
            white.check_moves()
        for black in black_pieces:
            black.check_moves()

        self.turn = "W"

    def select(self, piece):
        self.selected = None
        if piece.color == self.turn:
            self.selected = piece

    def next_turn(self):
        if self.turn == "W":
            self.turn = "B"
            return
        self.turn = "W"


if __name__ == "__main__":
    # g = Game()
    # for p in g.black_pieces:
    #     print(p, p.location)
    #
    pass
