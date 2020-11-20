import copy
import random

class Node:
    def __init__(self, x_coord=None, y_coord=None, probability=None, owner=None):
        self.part_of_ship = False
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.hit = False
        self.prob = probability
        self.owner = owner
    
    def print_info(self):
        print("({0},{1})".format(self.x_coord, self.y_coord))
    
    def print_node(self):
        if self.hit == False:
            print("[-]", end='')
        elif self.hit == True and self.part_of_ship == True:
            print("[O]", end='')
        else:
            print("[X]", end='')
        
        if self.y_coord == 9:
            print("\n")

    def view_info(self):
        if self.part_of_ship == False:
            print("[ ]", end='')
        else:
            print("[{0}]".format(self.owner), end='')
        
        if self.y_coord == 9:
            print("\n")




class AI:
    def __init__(self):
        pass
    
    def set_ai_ships(self, board):
        ships = [5,4,3,3,2]
        for ship in ships:
            random_x = random.randint(0,9)
            random_y = random.randint(0,9)
            # if initial node is not a legal move, randomly select a different node
            while(board[random_x][random_y].part_of_ship):
                random_x = random.randint(0,9)
                random_y = random.randint(0,9)

            direction = random.randint(1,4)
            # check to make sure the randomly selected node is a legal starting node
            # i.e. not isolated
            north = legal_ship_direction(board, ship, 1, [random_x, random_y])
            east = legal_ship_direction(board, ship, 2, [random_x, random_y])
            south = legal_ship_direction(board, ship, 3, [random_x, random_y])
            west = legal_ship_direction(board, ship, 4, [random_x, random_y])


            while(not north and not east and not south and not west):
                random_x = random.randint(0,9)
                random_y = random.randint(0,9)
                while(board[random_x][random_y].part_of_ship):
                    random_x = random.randint(0,9)
                    random_y = random.randint(0,9)
                north = legal_ship_direction(board, ship, 1, [random_x, random_y])
                east = legal_ship_direction(board, ship, 2, [random_x, random_y])
                south = legal_ship_direction(board, ship, 3, [random_x, random_y])
                west = legal_ship_direction(board, ship, 4, [random_x, random_y])
                # if initial node is not a legal move, randomly select a different node    
            while(legal_ship_direction(board, ship, direction, [random_x,random_y]) == False):
                direction = random.randint(1,4)

            set_ship(board, ship, direction, [random_x,random_y], human_player=False)

            


def legal_ship_direction(board, ship_size, direction, coords):
    """
    Function to return true or false according to a ship's initial placement
    and facing direction - returns true if the move is legal, false otherwise
    """
    if direction == 1:
        # North facing check, decrement x coord each step and check if move is legal
        for i in range(0,ship_size):
            try:
                if coords[0]-ship_size < 0:
                    return False
                if(board[coords[0]-i][coords[1]].part_of_ship):
                    return False
            except:
                return False
        return True
    
    if direction == 2:
        # East facing check, increment y coord each step and check if move is legal
        for i in range(0,ship_size):
            try:
                if coords[1]+ship_size > 9:
                    return False
                if(board[coords[0]][coords[1]+i].part_of_ship):
                    return False
            except:
                return False
        return True
    
    if direction == 3:
        # South facing check, increment x coord each step and check if move is legal
        for i in range(0,ship_size):
            try:
                if coords[0]+ship_size > 9:
                    return False
                if(board[coords[0]+i][coords[1]].part_of_ship):
                    return False
            except:
                return False
        return True
    
    if direction == 4:
        # West facing check, decrement y coord each step and check if move is legal
        for i in range(0,ship_size):
            try:
                if coords[1]-ship_size < 0:
                    return False
                if(board[coords[0]][coords[1]-i].part_of_ship):
                    return False
            except:
                return False
        return True

                
def set_ship(board, ship_size, direction, coords, human_player=True):
    """
    Function to set up the ship after all checks have passed
    """
    try:
        if(human_player):
            board[coords[0]][coords[1]].part_of_ship = True
            board[coords[0]][coords[1]].owner = 1
            if direction == 1:
                # North facing - decrement x and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]-i][coords[1]].part_of_ship = True
                    board[coords[0]-i][coords[1]].owner = 1
            
            if direction == 2:
                # East facing - increment y and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]][coords[1]+i].part_of_ship = True
                    board[coords[0]][coords[1]+i].owner = 1
            if direction == 3:
                # South facing - increment x and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]+i][coords[1]].part_of_ship = True
                    board[coords[0]+i][coords[1]].owner = 1
            if direction == 4:
                # West facing - decrement y and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]][coords[1]-i].part_of_ship = True   
                    board[coords[0]][coords[1]-i].owner = 1
            print_setup(board)
        
        else:
            board[coords[0]][coords[1]].part_of_ship = True
            board[coords[0]][coords[1]].owner = 2
            if direction == 1:
                # North facing - decrement x and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]-i][coords[1]].part_of_ship = True
                    board[coords[0]-i][coords[1]].owner = 2
            
            if direction == 2:
                # East facing - increment y and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]][coords[1]+i].part_of_ship = True
                    board[coords[0]][coords[1]+i].owner = 2
            if direction == 3:
                # South facing - increment x and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]+i][coords[1]].part_of_ship = True
                    board[coords[0]+i][coords[1]].owner = 2
            if direction == 4:
                # West facing - decrement y and set node.part_of_ship to True
                for i in range(1,ship_size):
                    board[coords[0]][coords[1]-i].part_of_ship = True   
                    board[coords[0]][coords[1]-i].owner = 2
    except:
        print("Failed to set ship, parameters are: ")
        print("Ship size: {0}".format(ship_size))
        print("Direction: {0}".format(direction))
        print("Coordinates: x:{0} y:{1}".format(coords[0], coords[1]))


def player_setup(board):
    """
    Function to set up ships
    Will take an initial coordinate and a direction, then set up the proper nodes
    in the game board - will also check to make sure the moves are legal
    """
    ships = [5,4,3,3,2]
    for ship in ships:
        counter = 1
        print("Ship number {0}: size {1}, where would you like to place it?:".format(counter, ship))
        x_coord = int(input("Enter the x_coord: "))
        y_coord = int(input("Enter the y_coord: "))
        # Check to make sure the initial node is a legal move
        while(board[x_coord][y_coord].part_of_ship):
            print("That location is already occupied by a ship, select a different starting node")
            print("Ship number {0}: size {1}, where would you like to place it?:".format(counter, ship))
            x_coord = int(input("Enter the x_coord: "))
            y_coord = int(input("Enter the y_coord: "))
            # check to make sure the selected initial node has some available
            # direction for the ship to face
            north = legal_ship_direction(board, ship, 1, [x_coord, y_coord])
            east = legal_ship_direction(board, ship, 2, [x_coord, y_coord])
            south = legal_ship_direction(board, ship, 3, [x_coord, y_coord])
            west = legal_ship_direction(board, ship, 4, [x_coord, y_coord])
            while(not north and not east and not south and not west):
                print("That node has no legal direction for a ship to face, please select a different node:")
                x_coord = int(input("Enter the x_coord: "))
                y_coord = int(input("Enter the y_coord: "))
                north = legal_ship_direction(board, ship, 1, [x_coord, y_coord])
                east = legal_ship_direction(board, ship, 2, [x_coord, y_coord])
                south = legal_ship_direction(board, ship, 3, [x_coord, y_coord])
                west = legal_ship_direction(board, ship, 4, [x_coord, y_coord])



        direction = int(input("What direction is this ship facing?: \n1) North\n2) East\n3) South\n4) West\n"))
        while(legal_ship_direction(board, ship, direction, [x_coord, y_coord]) == False):
            print("The ship can not face that direction, please select a different direction.")
            direction = int(input("What direction is this ship facing?: \n1) North\n2) East\n3) South\n4) West\n"))
        
        set_ship(board, ship, direction, [x_coord, y_coord])
        counter += 1


def print_game(board):
    for row in board:
        for node in row:
            node.print_node()


def print_setup(board):
    for row in board:
        for node in row:
            node.view_info()


def main():
    player_board = []
    ai_board = []
    ai_player = AI()
    for i in range(10):
        row = []
        for j in range(10):
            new_node = Node(x_coord=i, y_coord=j, probability=1)
            row.append(new_node)
        player_board.append(copy.deepcopy(row))
        ai_board.append(copy.deepcopy(row))

    player_setup(player_board)
    ai_player.set_ai_ships(ai_board)

    print("INITIAL PLAYER BOARD")
    print_setup(player_board)

    print("INITIAL AI BOARD")
    print_setup(ai_board)


main()