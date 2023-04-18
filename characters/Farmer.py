from characters import Character, ChessCoordinate, FIELD_SIZE, IMAGE_DIR, Groups

class Farmer(Character):
    
    def __init__(self, ownership: Groups, coordinate: ChessCoordinate, shape, id) -> None:
        shape = IMAGE_DIR + 'Farmer_{}.png'.format(ownership.name)
        super().__init__(ownership, coordinate, shape, id)
        

    def get_movable(self, obstacles: list[Character]) -> list[ChessCoordinate]:
        #   X       X
        #     Farmer
        factor = 1
        if self.ownership == Groups.WHITE:
            factor = -1
        
        front = ChessCoordinate(self.coordinate.x, self.coordinate.y + factor)
        sides = [ChessCoordinate(self.coordinate.x + 1, self.coordinate.y + factor), ChessCoordinate(self.coordinate.x - 1, self.coordinate.y + factor)]
        
        front_front = None
        if not self.has_been_moved:
            front_front = ChessCoordinate(self.coordinate.x, self.coordinate.y + factor * 2)

        all_movable = []
        if front_front:
            all_movable = [front_front]
        all_movable += [front]
        side_movable = []
        for obstacle in obstacles:
            if front == obstacle.coordinate:
                all_movable = []
            if obstacle.coordinate in sides:
                if obstacle.ownership != self.ownership:
                    side_movable.append(obstacle.coordinate)
        
        all_movable += side_movable
        
        return [coord for coord in all_movable if 1 <= coord.y <= FIELD_SIZE and 1 <= coord.x <= FIELD_SIZE]
