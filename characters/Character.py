import enum
from collections import namedtuple
import abc

ChessCoordinate = namedtuple('ChessCoordinate', ('x', 'y'))

FIELD_SIZE = 8
IMAGE_DIR = 'characters/images/'

class Groups(enum.Enum):
    BLACK = 1,
    WHITE = 2,
    SPECTATING = 3



class Character(abc.ABC):

    def __init__(self, ownership, coordinate: ChessCoordinate, shape, id) -> None:
        self.ownership = ownership
        self.coordinate = coordinate
        self.shape = shape
        self.id = id
        self.has_been_moved = False
        self.dead = False
    
    def move(self, coordinate: ChessCoordinate, obstacles: list[ChessCoordinate]):
        all_movable = self.get_movable(obstacles)
        if (coordinate in all_movable):
            self.has_been_moved = True
            self.coordinate = coordinate
            return True
        return False
    
    def get_movable(self) -> list[ChessCoordinate]:
        pass
    
    def hit(self, other) -> None:
        del other
    
    def set_dead(self) -> None:
        self.dead = True
        self.coordinate = None
        self.shape = None
        self.has_been_moved = None
