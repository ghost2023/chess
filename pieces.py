from constants import *
import game


def is_valid(loc):
    x_valid = loc[0] >= 0 and loc[0] < 8
    y_valid = loc[1] >= 0 and loc[1] < 8
    return x_valid and y_valid


def posvalid(pos):
    return pos >= 0 and pos < 8


def is_available(loc):
    for p in game.white_pieces:
        if loc == p.location:
            return False
    for p in game.black_pieces:
        if loc == p.location:
            return False
    return True


class King:
    def __init__(self, color, loc: list) -> None:
        self.color = color
        self.location = loc
        self.img = WHITE_KING if color == "W" else BLACK_KING
        self.available = []
        self.available_kills = []
        self.blocked = []
        self.phantom_moves = []
        self.moved = False

    def move(self, pos):
        self.location = pos
        return True

    def check_moves(self):
        self.available = []
        self.available_kills = []
        self.blocked = []

        enemy = game.white_pieces if self.color == "B" else game.black_pieces
        locs = [[i, j] for i in range(-1, 2) for j in range(-1, 2) if i or j]
        for loc in locs:
            next_loc = [self.location[0] + loc[0], self.location[1] + loc[1]]
            if not is_valid(next_loc):
                continue
            for piece in enemy:
                if isinstance(piece, Pawn):
                    pawn_dxn = -1 if piece.color == "W" else 1
                    pawn_kills = [
                        [piece.location[0] + 1, piece.location[1] + pawn_dxn],
                        [piece.location[0] - 1, piece.location[1] + pawn_dxn],
                    ]
                    if next_loc in pawn_kills:
                        break
                    if piece.location[0] == next_loc[0]:
                        continue
                else:
                    if next_loc in piece.available or next_loc in piece.phantom_moves:
                        break
            else:
                blocker = game.find_piece(next_loc)
                if blocker == None:
                    if not self.moved:
                        if (
                            next_loc == [self.location[0] + 1, self.location[1]]
                            and game.checked != self
                        ):
                            over = game.find_piece(
                                [self.location[0] + 2, self.location[1]]
                            )
                            if not over:
                                rock_loc = [self.location[0] + 3, self.location[1]]
                                rock = game.find_piece(rock_loc)
                                if rock:
                                    if game.isrock(rock):
                                        if not rock.moved:
                                            self.available.append(
                                                [self.location[0] + 2, self.location[1]]
                                            )

                        if (
                            next_loc == [self.location[0] - 1, self.location[1]]
                            and game.checked != self
                        ):
                            over = game.find_piece(
                                [self.location[0] - 2, self.location[1]]
                            )
                            if not over:
                                rock_loc = [self.location[0] - 4, self.location[1]]
                                rock = game.find_piece(rock_loc)
                                if rock:
                                    if game.isrock(rock):
                                        if not rock.moved:
                                            self.available.append(
                                                [self.location[0] - 2, self.location[1]]
                                            )

                    self.available.append(next_loc)
                elif blocker.color != self.color:
                    for piece in enemy:
                        if blocker.location in piece.blocked:
                            break
                    else:
                        self.available_kills.append(next_loc)
                else:
                    self.blocked.append(next_loc)


class Pawn:
    def __init__(self, color, loc: list) -> None:
        self.color = color
        self.location = loc
        self.img = WHITE_PAWN if color == "W" else BLACK_PAWN
        self.moves = 0
        self.available = []
        self.available_kills = []
        self.blocked = []
        self.phantom_moves = []
        self.phantom_kills = []

    def move(self, pos):
        if pos in self.available or pos in self.available_kills:
            self.location = pos
            self.moves = 1
            return True

    def check_moves(self):
        self.available = []
        self.available_kills = []
        self.blocked = []

        dxn = -1 if self.color == "W" else 1
        stop = 3 if self.moves == 0 else 2
        for i in range(1, stop):
            step = dxn * i
            next_loc = [self.location[0], self.location[1] + step]

            if not is_valid(next_loc):
                continue

            if is_available(next_loc):
                self.available.append(next_loc)
            else:
                break

        for i in [-1, 1]:
            diagonal = [self.location[0] + i, self.location[1] + dxn]
            if not is_valid(diagonal):
                continue
            enemy = game.find_piece(diagonal)
            if enemy == None:
                continue
            if enemy.color == self.color:
                self.blocked.append(diagonal)
                continue
            if isinstance(enemy, King):
                game.checked = enemy
            self.available_kills.append(diagonal)


class Queen:
    def __init__(self, color, loc: list) -> None:
        self.color = color
        self.location = loc
        self.img = WHITE_QUEEN if color == "W" else BLACK_QUEEN
        self.available = []
        self.available_kills = []
        self.phantom_moves = []
        self.phantom_kills = []

    def move(self, pos):
        self.location = pos
        return True

    def check_moves(self):
        self.available = []
        self.available_kills = []
        self.blocked = []
        self.phantom_moves = []
        self.phantom_kills = []

        # find diagonal
        for multiplier in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
            is_blocked = False
            for move in range(1, 8):
                x = move * multiplier[0]
                y = move * multiplier[1]
                next_loc = [self.location[0] + x, self.location[1] + y]
                if not is_valid(next_loc):
                    break

                if is_blocked:
                    blocker = game.find_piece(next_loc)
                    if not blocker:
                        self.phantom_moves.append(next_loc)
                        continue
                    if blocker.color != self.color:
                        self.phantom_kills.append(next_loc)
                    break

                if is_available(next_loc):
                    self.available.append(next_loc)
                    continue

                blocker = game.find_piece(next_loc)
                if blocker != None:
                    if blocker.color != self.color:
                        if isinstance(blocker, King):
                            game.checked = blocker
                            is_blocked = True
                            continue
                        self.available_kills.append(next_loc)
                    else:
                        self.blocked.append(next_loc)
                    break

        # Horizontal
        for multiplier in [-1, 1]:
            is_blocked = False
            for move in range(1, 8):
                x = move * multiplier
                next_loc = [self.location[0] + x, self.location[1]]
                if not is_valid(next_loc):
                    break

                if is_blocked:
                    blocker = game.find_piece(next_loc)
                    if not blocker:
                        self.phantom_moves.append(next_loc)
                        continue
                    if blocker.color != self.color:
                        self.phantom_kills.append(next_loc)
                    break

                if is_available(next_loc):
                    self.available.append(next_loc)
                    continue

                blocker = game.find_piece(next_loc)
                if blocker != None:
                    if blocker.color != self.color:
                        if isinstance(blocker, King):
                            game.checked = blocker
                            is_blocked = True
                            continue
                        self.available_kills.append(next_loc)
                    else:
                        self.blocked.append(next_loc)
                    break

        # Vertical
        for multiplier in [-1, 1]:
            is_blocked = False
            for move in range(1, 8):
                y = move * multiplier
                next_loc = [self.location[0], self.location[1] + y]
                if not is_valid(next_loc):
                    break

                if is_blocked:
                    blocker = game.find_piece(next_loc)
                    if not blocker:
                        self.phantom_moves.append(next_loc)
                        continue
                    if blocker.color != self.color:
                        self.phantom_kills.append(next_loc)
                    break

                if is_available(next_loc):
                    self.available.append(next_loc)
                    continue

                blocker = game.find_piece(next_loc)
                if blocker != None:
                    if blocker.color != self.color:
                        if isinstance(blocker, King):
                            game.checked = blocker
                            is_blocked = True
                            continue
                        self.available_kills.append(next_loc)
                    else:
                        self.blocked.append(next_loc)
                    break


class Bishop:
    def __init__(self, color, loc: list) -> None:
        self.color = color
        self.location = loc
        self.img = WHITE_BISHOP if color == "W" else BLACK_BISHOP
        self.available = []
        self.available_kills = []
        self.phantom_moves = []
        self.phantom_kills = []

    def move(self, pos):
        if pos in self.available or pos in self.available_kills:
            self.location = pos
            return True

    def check_moves(self):
        self.available = []
        self.available_kills = []
        self.blocked = []
        self.phantom_moves = []
        self.phantom_kills = []

        for multiplier in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
            is_blocked = False
            for move in range(1, 8):
                x = move * multiplier[0]
                y = move * multiplier[1]
                next_loc = [self.location[0] + x, self.location[1] + y]
                if not is_valid(next_loc):
                    break

                if is_blocked:
                    blocker = game.find_piece(next_loc)
                    if not blocker:
                        self.phantom_moves.append(next_loc)
                        continue
                    if blocker.color != self.color:
                        self.phantom_kills.append(next_loc)
                    break

                if is_available(next_loc):
                    self.available.append(next_loc)
                    continue

                blocker = game.find_piece(next_loc)
                if blocker != None:
                    if blocker.color != self.color:
                        if isinstance(blocker, King):
                            game.checked = blocker
                            is_blocked = True
                            continue
                        self.available_kills.append(next_loc)
                    else:
                        self.blocked.append(next_loc)
                    break


class Knight:
    def __init__(self, color, loc: list) -> None:
        self.color = color
        self.location = loc
        self.img = WHITE_KNIGHT if color == "W" else BLACK_KNIGHT
        self.available = []
        self.available_kills = []
        self.phantom_moves = []
        self.phantom_kills = []

    def move(self, pos):
        if pos in self.available or pos in self.available_kills:
            self.location = pos
            return True

    def check_moves(self):
        self.available = []
        self.available_kills = []
        self.blocked = []

        for loc in [
            [-2, -1],
            [-2, 1],
            [-1, -2],
            [-1, 2],
            [1, -2],
            [1, 2],
            [2, -1],
            [2, 1],
        ]:
            next_loc = [self.location[0] + loc[0], self.location[1] + loc[1]]
            if not is_valid(next_loc):
                continue
            blocker = game.find_piece(next_loc)
            if not blocker:
                self.available.append(next_loc)
            elif blocker.color != self.color:
                if isinstance(blocker, King):
                    game.checked = blocker
                self.available_kills.append(next_loc)
            else:
                self.blocked.append(next_loc)


class Rock:
    def __init__(self, color, loc: list) -> None:
        self.color = color
        self.location = loc
        self.img = WHITE_ROCK if color == "W" else BLACK_ROCK
        self.available = []
        self.available_kills = []
        self.phantom_moves = []
        self.phantom_kills = []
        self.moved = False

    def move(self, pos):
        self.location = pos
        self.moved = True
        return True

    def check_moves(self):
        self.available = []
        self.available_kills = []
        self.blocked = []
        self.phantom_moves = []
        self.phantom_kills = []

        # Horizontal
        for multiplier in [-1, 1]:
            is_blocked = False
            for move in range(1, 8):
                x = move * multiplier
                next_loc = [self.location[0] + x, self.location[1]]
                if not is_valid(next_loc):
                    break

                if is_blocked:
                    blocker = game.find_piece(next_loc)
                    if not blocker:
                        self.phantom_moves.append(next_loc)
                        continue
                    if blocker.color != self.color:
                        self.phantom_kills.append(next_loc)
                    break

                if is_available(next_loc):
                    self.available.append(next_loc)
                    continue

                blocker = game.find_piece(next_loc)
                if blocker != None:
                    if blocker.color != self.color:
                        if isinstance(blocker, King):
                            game.checked = blocker
                            is_blocked = True
                            continue
                        self.available_kills.append(next_loc)
                    else:
                        self.blocked.append(next_loc)
                    break

        # Vertical
        for multiplier in [-1, 1]:
            is_blocked = False
            for move in range(1, 8):
                y = move * multiplier
                next_loc = [self.location[0], self.location[1] + y]
                if not is_valid(next_loc):
                    break

                if is_blocked:
                    blocker = game.find_piece(next_loc)
                    if not blocker:
                        self.phantom_moves.append(next_loc)
                        continue
                    if blocker.color != self.color:
                        self.phantom_kills.append(next_loc)
                    break

                if is_available(next_loc):
                    self.available.append(next_loc)
                    continue

                blocker = game.find_piece(next_loc)
                if blocker != None:
                    if blocker.color != self.color:
                        if isinstance(blocker, King):
                            game.checked = blocker
                            is_blocked = True
                            continue
                        self.available_kills.append(next_loc)
                    else:
                        self.blocked.append(next_loc)
                    break


if __name__ == "__main__":
    r = King("B", [3, 3])
    r.check_moves()
    print(r.available)
