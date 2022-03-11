import pygame

CELL_SIZE = 70

CELL_AREA = (CELL_SIZE, CELL_SIZE)

BLACK_PAWN = pygame.transform.scale(pygame.image.load("images/BPawn.png"), CELL_AREA)
BLACK_KING = pygame.transform.scale(pygame.image.load("images/BKing.png"), CELL_AREA)
BLACK_BISHOP = pygame.transform.scale(
    pygame.image.load("images/BBishop.png"), CELL_AREA
)
BLACK_ROCK = pygame.transform.scale(pygame.image.load("images/BRock.png"), CELL_AREA)
BLACK_KNIGHT = pygame.transform.scale(
    pygame.image.load("images/BKnight.png"), CELL_AREA
)
BLACK_QUEEN = pygame.transform.scale(pygame.image.load("images/BQueen.png"), CELL_AREA)
WHITE_PAWN = pygame.transform.scale(pygame.image.load("images/WPawn.png"), CELL_AREA)
WHITE_KING = pygame.transform.scale(pygame.image.load("images/WKing.png"), CELL_AREA)
WHITE_BISHOP = pygame.transform.scale(
    pygame.image.load("images/WBishop.png"), CELL_AREA
)
WHITE_ROCK = pygame.transform.scale(pygame.image.load("images/WRock.png"), CELL_AREA)
WHITE_KNIGHT = pygame.transform.scale(
    pygame.image.load("images/WKnight.png"), CELL_AREA
)
WHITE_QUEEN = pygame.transform.scale(pygame.image.load("images/WQueen.png"), CELL_AREA)
