from cmath import pi
import pygame, sys, game, time, pieces
from constants import CELL_SIZE

pygame.init()
screen = pygame.display.set_mode((560, 560))


def draw_pieces():
    for white_piece in game.white_pieces:
        if white_piece == game.checked:
            rec = pygame.Rect(
                white_piece.location[0] * CELL_SIZE,
                white_piece.location[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            print("here", rec)
            pygame.draw.rect(screen, (255, 70, 70), rec)

        loc = (white_piece.location[0] * CELL_SIZE, white_piece.location[1] * CELL_SIZE)
        screen.blit(white_piece.img, loc)

    for black_piece in game.black_pieces:
        if black_piece == game.checked:
            rec = pygame.Rect(
                black_piece.location[0] * CELL_SIZE,
                black_piece.location[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            print("here", rec)
            pygame.draw.rect(screen, (255, 70, 70), rec)

        loc = (black_piece.location[0] * CELL_SIZE, black_piece.location[1] * CELL_SIZE)
        screen.blit(black_piece.img, loc)


def show_available(piece):
    for x, y in piece.available:
        pygame.draw.circle(
            screen, (255, 165, 0), (x * CELL_SIZE + 35, y * CELL_SIZE + 35), 15
        )

    for x, y in piece.available_kills:
        pygame.draw.circle(
            screen, (255, 0, 0), (x * CELL_SIZE + 35, y * CELL_SIZE + 35), 15
        )


def load_background():
    img = pygame.image.load("images/board_portion.png")
    img = pygame.transform.scale(img, (140, 140))

    for i in range(4):
        for j in range(4):
            a = (140 * i, 140 * j)
            screen.blit(img, a)


def user_input(pos):
    if g.selected == None:
        piece = game.find_piece(pos)
        if piece == None:
            return
        piece.check_moves()
        g.select(piece)
        return

    if pos in g.selected.available_kills:
        kill = game.find_piece(pos)
        game.kill(kill)

    piece = g.selected.location
    if pos in g.selected.available or pos in g.selected.available_kills:
        if g.selected.move(pos):
            if isinstance(g.selected, pieces.King):
                if pos == [piece[0] + 2, piece[1]]:
                    rock = game.find_piece([piece[0] + 3, piece[1]])
                    print(rock)
                    rock.move([pos[0] - 1, pos[1]])
                if pos == [piece[0] - 2, piece[1]]:
                    rock = game.find_piece([piece[0] - 4, piece[1]])
                    print(rock)
                    rock.move([pos[0] + 1, pos[1]])
            if isinstance(g.selected, pieces.Pawn):
                opposite = 0 if g.selected.color == "W" else 7
                if pos[1] == opposite:
                    inp = input("what do u want? \n")
                    piece = None
                    if inp == "q":
                        piece = pieces.Queen(g.selected.color, g.selected.location)
                    elif inp == "r":
                        piece = pieces.Rock(g.selected.color, g.selected.location)
                    elif inp == "b":
                        piece = pieces.Bishop(g.selected.color, g.selected.location)
                    elif inp == "k":
                        piece = pieces.Knight(g.selected.color, g.selected.location)
                    if g.selected.color == "W":
                        game.white_pieces.remove(g.selected)
                        game.white_pieces.append(piece)
                    else:
                        game.black_pieces.remove(g.selected)
                        game.black_pieces.append(piece)
            g.next_turn()
            game.checked = None
            game.reset_all()

    g.selected = None


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord = [
                    pygame.mouse.get_pos()[0] // CELL_SIZE,
                    pygame.mouse.get_pos()[1] // CELL_SIZE,
                ]
                user_input(coord)
            load_background()
            draw_pieces()

        if g.selected != None:
            show_available(g.selected)
        pygame.display.update()


g = game.Game()
main()
