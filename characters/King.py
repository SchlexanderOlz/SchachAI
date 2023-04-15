from characters import Character, ChessCoordinate, Farmer, Bishop, FIELD_SIZE, IMAGE_DIR, Groups
from characters.Tower import Tower
from characters.Knight import Knight
from characters.Queen import Queen
from characters.Bishop import Bishop
from characters.Farmer import Farmer

class King(Character):

    def __init__(self, ownership: Groups, coordinate: ChessCoordinate, subjects: list[Character], id) -> None:
        shape = IMAGE_DIR + 'King_{}.png'.format(ownership.name)
        super().__init__(ownership, coordinate, shape, id)
        self.subjects = subjects
        

    def get_movable(self, obstacles: list[Character]) -> list[ChessCoordinate]:
        #   X       X
        #     Farmer
        all_cords = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_cord = ChessCoordinate(self.coordinate.x + i, self.coordinate.y + j)
                if i == 0 and j == 0:
                    continue
                is_allowed = True
                for obstacle in obstacles:
                    if new_cord == obstacle.coordinate:
                        if self.ownership != obstacle.ownership:
                            break
                        is_allowed = False
                        break
                if is_allowed:
                    all_cords.append(new_cord)
        
        return [coord for coord in all_cords if 1 <= coord.y <= FIELD_SIZE and 1 <= coord.x <= FIELD_SIZE]

    def set_standard_subjects(self):
        self.subjects.clear()
        pattern = [Tower, Knight, Bishop]

        farmer_y = 2
        others_y = 1
        if self.ownership == Groups.WHITE:
            farmer_y = FIELD_SIZE - 1
            others_y = FIELD_SIZE
        
        for i in range(1, FIELD_SIZE + 1):
            self.subjects.append(Farmer(self.ownership, ChessCoordinate(i, farmer_y), None, i))
            
        for i in range(int(FIELD_SIZE / 2) - 1):
            subject_class = pattern[i % len(pattern)]
            self.subjects.append(subject_class(self.ownership, ChessCoordinate(i + 1, others_y), None, i + FIELD_SIZE))
        
        pattern.append(Queen)
        pattern.reverse()
        self.coordinate = ChessCoordinate(int(FIELD_SIZE / 2), others_y)
        for i in range(int(FIELD_SIZE / 2), FIELD_SIZE):
            subject_class = pattern[i % len(pattern)]
            self.subjects.append(subject_class(self.ownership, ChessCoordinate(i + 1, others_y), None, i + FIELD_SIZE))