from characters import Character, ChessCoordinate, FIELD_SIZE, IMAGE_DIR, Groups

class Knight(Character):
    
    def __init__(self, ownership: Groups, coordinate: ChessCoordinate, shape, id) -> None:
        shape = IMAGE_DIR + 'Horse_{}.png'.format(ownership.name)
        super().__init__(ownership, coordinate, shape, id)
  

    def get_movable(self, obstacles: list[Character]) -> list[ChessCoordinate]:
        #     X         X
        #        Bishop
        #     X         X  

        all_cords = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:
                    new_y = self.coordinate.y + i
                    new_x = self.coordinate.x + j
                    new_cord = ChessCoordinate(new_x, new_y)
                    for obstacle in obstacles:
                        if obstacle.ownership == self.ownership and obstacle.coordinate == new_cord:
                            continue
                    if new_y >= 0 and new_y <= FIELD_SIZE and new_x >= 0 and new_x <= FIELD_SIZE:
                        all_cords.append(new_cord)

        return all_cords
