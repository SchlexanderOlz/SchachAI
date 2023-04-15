from characters import Character, ChessCoordinate, FIELD_SIZE, IMAGE_DIR, Groups

class Queen(Character):
    
    def __init__(self, ownership: Groups, coordinate: ChessCoordinate, shape, id) -> None:
        shape = IMAGE_DIR + 'Queen_{}.png'.format(ownership.name)
        super().__init__(ownership, coordinate, shape, id)
  

    def get_movable(self, obstacles: list[Character]) -> list[ChessCoordinate]:
        #         X     
        #XXXXX  Tower XXXXXX
        #         X  
     
        all_cords = []
        allowed_1 = allowed_2 = allowed_3 = allowed_4 = True

        for i in range(1, FIELD_SIZE):
            # Move right
            if allowed_1 and self.coordinate.x + i <= FIELD_SIZE:
                new_cord = ChessCoordinate(self.coordinate.x + i, self.coordinate.y)
                allowed_1, new_cord = self.__is_allowed__(new_cord, obstacles)
                
                if new_cord:
                    all_cords.append(new_cord)
            # Move left
            if allowed_2 and self.coordinate.x - i >= 1:
                new_cord = ChessCoordinate(self.coordinate.x - i, self.coordinate.y)
                allowed_2, new_cord = self.__is_allowed__(new_cord, obstacles)
                
                if new_cord:
                    all_cords.append(new_cord)
            # Move up
            if allowed_3 and self.coordinate.y + i <= FIELD_SIZE:
                new_cord = ChessCoordinate(self.coordinate.x, self.coordinate.y + i)
                allowed_3, new_cord = self.__is_allowed__(new_cord, obstacles)
                
                if new_cord:
                    all_cords.append(new_cord)
            # Move down
            if allowed_4 and self.coordinate.y - i >= 1:
                new_cord = ChessCoordinate(self.coordinate.x, self.coordinate.y - i)
                allowed_4, new_cord = self.__is_allowed__(new_cord, obstacles)

                if new_cord:
                    all_cords.append(new_cord)

        allowed_1 = allowed_2 = allowed_3 = allowed_4 = True

        for i in range(1, FIELD_SIZE):
            # Move diagonally to top-right
            if allowed_1 and self.coordinate.x + i <= FIELD_SIZE and self.coordinate.y + i <= FIELD_SIZE:
                new_cord = ChessCoordinate(self.coordinate.x + i, self.coordinate.y + i)
                allowed_1, new_cord = self.__is_allowed__(new_cord, obstacles)
                
                if new_cord:
                    all_cords.append(new_cord)
            # Move diagonally to top-left
            if allowed_2 and self.coordinate.x - i >= 1 and self.coordinate.y + i <= FIELD_SIZE:
                new_cord = ChessCoordinate(self.coordinate.x - i, self.coordinate.y + i)
                allowed_2, new_cord = self.__is_allowed__(new_cord, obstacles)
                
                if new_cord:
                    all_cords.append(new_cord)
            # Move diagonally to bottom-right
            if allowed_3 and self.coordinate.x + i <= FIELD_SIZE and self.coordinate.y - i >= 1:
                new_cord = ChessCoordinate(self.coordinate.x + i, self.coordinate.y - i)
                allowed_3, new_cord = self.__is_allowed__(new_cord, obstacles)
                
                if new_cord:
                    all_cords.append(new_cord)
            # Move diagonally to bottom-left
            if allowed_4 and self.coordinate.x - i >= 1 and self.coordinate.y - i >= 1:
                new_cord = ChessCoordinate(self.coordinate.x - i, self.coordinate.y - i)
                allowed_4, new_cord = self.__is_allowed__(new_cord, obstacles)

                if new_cord:
                    all_cords.append(new_cord)


        return [coord for coord in all_cords if 0 <= coord.y <= FIELD_SIZE and 0 <= coord.x <= FIELD_SIZE]


    def __is_allowed__(self, new_cord: ChessCoordinate, obstacles: list[Character]):
        for obstacle in obstacles:
            if obstacle.coordinate == new_cord:
                if obstacle.ownership != self.ownership:
                    return False, new_cord
                return False, None
        return True, new_cord