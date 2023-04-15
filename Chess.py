from characters import *
import pygame

WINDOWSIZE = (500, 500)
ELEMENT_SIZE = (WINDOWSIZE[0] / FIELD_SIZE, WINDOWSIZE[1] / FIELD_SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 140, 0)

KING_ID = 69
HIT_BOX_SIZE = 60


pygame.init()


class Chess:
    
    def __init__(self, group: Groups):
        self.display = pygame.display.set_mode(WINDOWSIZE)
        pygame.display.set_caption('Chess')
        
        self.group = group
        self.turn = 0
        self.parties = [Groups.WHITE, Groups.BLACK]
        self.is_dead = False
        self.reset()
        self.create_playing_field()
        self.input_loop()
    
    def create_playing_field(self):
        self.display.fill(BLACK)
        
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if ((j + i) % 2 == 0):
                    pygame.draw.rect(self.display, GREEN, pygame.Rect(ELEMENT_SIZE[0] * j, ELEMENT_SIZE[1] * i, ELEMENT_SIZE[0], ELEMENT_SIZE[1]))
                else:
                    pygame.draw.rect(self.display, WHITE, pygame.Rect(ELEMENT_SIZE[0] * j, ELEMENT_SIZE[1] * i, ELEMENT_SIZE[0], ELEMENT_SIZE[1]))
        self.display_chess_pieces(self.black)
        self.display_chess_pieces(self.white)
        pygame.display.flip()
    
    def display_chess_pieces(self, king: King):
        all_subjects = [king] + king.subjects
        for subject in all_subjects:
            coord = self.coord_to_pixels(subject.coordinate)
            self.display.blit(pygame.image.load(subject.shape), coord)
    
    def input_loop(self):
        running = True
        while running and not self.is_dead:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    running = False
                    break

                if pygame.mouse.get_pressed()[0]: # Make this more efficient by maybe saving the hitbox with the subjects
                    if self.group == Groups.BLACK:
                        tmp = self.get_what_clicked(pygame.mouse.get_pos(), self.black)
                    elif self.group == Groups.WHITE:
                        tmp = self.get_what_clicked(pygame.mouse.get_pos(), self.white)

                    if tmp:
                        self.focus = tmp
                        continue

                    if self.focus:
                        try:
                            new_cord = self.pixel_to_coord(pygame.mouse.get_pos())
                            self.play_next_move(self.group, [self.focus, new_cord.x, new_cord.y])
                            self.check_and_collide(self.id_into_character(self.group, self.focus))
                            self.create_playing_field()
                            self.turn += 1
                            self.focus = None
                        except UnallowedCoordinateError:
                            self.focus = None


    def get_what_clicked(self, click_pos: tuple[int, int], king: King) -> int:
        all_subjects = king.subjects + [king]
        for subject in all_subjects:
            coords = self.coord_to_pixels(subject.coordinate)
            hitbox = pygame.Rect(coords[0], coords[1], HIT_BOX_SIZE, HIT_BOX_SIZE)
            if hitbox.collidepoint(click_pos):
                return subject.id

    def id_into_character(self, group: Groups, id: int):
        if group == Groups.BLACK:
            search_for = self.black.subjects + [self.black]
        elif group == Groups.WHITE:
            search_for = self.white.subjects + [self.white]
        
        for subject in search_for:
            if subject.id == id:
                return subject

    def check_and_collide(self, piece: Character) -> Character:
        all_pieces = []
        if piece.ownership == Groups.BLACK:
            all_pieces = self.white.subjects + [self.white]
        elif piece.ownership == Groups.WHITE:
            all_pieces = self.black.subjects + [self.black]

        for subject in all_pieces:
            if subject == piece: continue
            if subject.coordinate == piece.coordinate:
                if subject.ownership == Groups.BLACK: # Handle the specific wins here
                    try:
                        self.black.subjects.remove(subject)
                    except ValueError:
                        self.game_over()
                if subject.ownership == Groups.BLACK:
                    try:
                        self.black.subjects.remove(subject)
                    except ValueError:
                        self.game_over
                return subject

    def game_over(self):
        self.is_dead = True
        print("Game Over!")

    def play_next_move(self, group: Groups, information: list) -> int:
        # The list which is given as a parameter will have the following style
        #               [piece_id, x, y]
        relevant_obstacles = self.black.subjects + [self.black] + self.white.subjects + [self.white]
        subject = self.id_into_character(group, information[0])

        if (subject.move(ChessCoordinate(information[1], information[2]), relevant_obstacles)):
            return 5 # Adjust this reward later
        raise UnallowedCoordinateError('Not possible to move there!')

    def coord_to_pixels(self, coord: ChessCoordinate):
        return ((coord.x - 1) * ELEMENT_SIZE[0], (coord.y - 1) * ELEMENT_SIZE[1])

    def pixel_to_coord(self, pixel: tuple[int, int]) -> ChessCoordinate:
        return (ChessCoordinate(int(pixel[0] / ELEMENT_SIZE[0]) + 1, int(pixel[1] / ELEMENT_SIZE[1]) + 1))

    def reset(self):
        self.focus = None
        self.black = King(Groups.BLACK, ChessCoordinate(int(FIELD_SIZE / 2), 1), [], KING_ID)
        self.white = King(Groups.WHITE, ChessCoordinate(int(FIELD_SIZE / 2), FIELD_SIZE), [], KING_ID)

        self.black.set_standard_subjects()
        self.white.set_standard_subjects()


class UnallowedCoordinateError(Exception):
    pass


if __name__ == "__main__":
    sos = Chess(Groups.WHITE)