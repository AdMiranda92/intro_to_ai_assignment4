import copy
import random
import time

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

    def view_prob(self):
        if self.hit == False:
            print(f"[{self.prob:02d}]", end='')
        elif self.hit == True and self.part_of_ship == True:
            print("[HT]", end='')
        else:
            print("[MS]", end='')
        
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

    def best_move(self, board):
        """
        This function returns a tuple containing the x and y coords of the node with the
        highest probability density
        """
        
        
        ships = [5,4,3,3,2]
        for row in board:
            for node in row:
                node.prob = 0
                
    
        for row in board:
            for node in row:
                if node.hit == True and node.part_of_ship == True:
                        x = node.x_coord
                        y = node.y_coord
                        n = False
                        s = False
                        e = False
                        w = False
                        try:
                            if(not board[x-1][y].hit):
                                n = True
                        except:
                            pass

                        try:
                            if(not board[x+1][y].hit):
                                s = True
                        except:
                            pass

                        try:
                            if(not board[x][y+1].hit):
                                e = True
                        except:
                            pass

                        try:
                            if(not board[x][y-1].hit):
                                w = True
                        except:
                            pass
                        
                        if(n):
                            x -= 1
                            while(x >= 0):
                                if board[x][y].hit and board[x][y].part_of_ship:
                                    x -= 1
                                elif board[x][y].hit and not board[x][y].part_of_ship:
                                    break
                                else:
                                    return (board[x][y].x_coord, board[x][y].y_coord)

                        if(s):
                            x = node.x_coord
                            y = node.y_coord
                            x += 1
                            while(x <= 9):
                                if board[x][y].hit and board[x][y].part_of_ship:
                                    x += 1
                                elif board[x][y].hit and not board[x][y].part_of_ship:
                                    break
                                else:
                                    return (board[x][y].x_coord, board[x][y].y_coord)

                        if(e and not (n or s)):
                            x = node.x_coord
                            y = node.y_coord
                            y += 1
                            while(y <= 9):
                                if board[x][y].hit and board[x][y].part_of_ship:
                                    y += 1
                                elif board[x][y].hit and not board[x][y].part_of_ship:
                                    break
                                else:
                                    return (board[x][y].x_coord, board[x][y].y_coord)
                        
                        if(w and not(n or s)):
                            x = node.x_coord
                            y = node.y_coord
                            y -= 1
                            while(y >= 0):
                                if board[x][y].hit and board[x][y].part_of_ship:
                                    y -= 1
                                elif board[x][y].hit and not board[x][y].part_of_ship:
                                    break
                                else:
                                    return (board[x][y].x_coord, board[x][y].y_coord) 


        
        for ship in ships:
            for row in board:
                for node in row:
                    if node.hit == True and node.part_of_ship == False:
                        continue
                    else:
                        legal_placement(board, ship, [node.x_coord, node.y_coord])
                    
        # return coords of the highest probability node
        highest_node = board[0][0]
        for row in board:
            for node in row:
                if node.hit == True:
                    continue
                if node.prob > highest_node.prob:
                    highest_node = node
                if node.prob == highest_node.prob:
                    switch = random.randint(1,2)
                    if switch == 1:
                        highest_node = node
        
        return (highest_node.x_coord, highest_node.y_coord)
    
    def AI_turn(self, board):
        """
        Executes AI turn, returns true if AI hit a battleship
        false otherwise
        """
        highest_node = self.best_move(board)
        board[highest_node[0]][highest_node[1]].hit = True
        print(f"ENEMY CHOOSES [{highest_node[0]}, {highest_node[1]}]")
        if board[highest_node[0]][highest_node[1]].part_of_ship:
            print("THE ENEMY HAS HIT YOUR BATTLESHIP")
            return True
        else:
            print("THE ENEMY MISSED")
            return False


def legal_placement(board, ship_size, coords):
    """
    Function for the AI to rank remaining nodes in order to choose the best
    next move, function returns a value density
    """
    # pass this check if the north direction does not contain enough spaces for the ship size
    legal_ship_direction = True
    if coords[0]-(ship_size-1) < 0:
        legal_ship_direction = False
    else: 
        for i in range(0, ship_size):
            if board[coords[0]-i][coords[1]].hit == True and board[coords[0]-i][coords[1]].part_of_ship == False:
                legal_ship_direction = False
    
    if legal_ship_direction:
        for i in range(0,ship_size):
            if(board[coords[0]-i][coords[1]].hit == False):
                board[coords[0]-i][coords[1]].prob += 1


    # pass this check if the east direction does not contain enough spaces for the ship size
    legal_ship_direction = True
    if coords[1]+ship_size-1 > 9:
        legal_ship_direction = False
    else:  
        for i in range(0, ship_size):
            if(board[coords[0]][coords[1]+i].hit == True and board[coords[0]][coords[1]+i].part_of_ship == False):
                legal_ship_direction = False

    
    if legal_ship_direction:
        for i in range(0,ship_size):
            if(board[coords[0]][coords[1]+i].hit == False):
                board[coords[0]][coords[1]+i].prob += 1

    # pass this check if the south direction does not contain enough spaces for the ship size
    legal_ship_direction = True
    if coords[0]+ship_size-1 > 9:
        legal_ship_direction = False
    else:    
        for i in range(0, ship_size):
            if(board[coords[0]+i][coords[1]].hit == True and board[coords[0]+i][coords[1]].part_of_ship == False):
                legal_ship_direction = False
        
    if legal_ship_direction:
        for i in range(0,ship_size):
            if(board[coords[0]+i][coords[1]].hit == False):
                board[coords[0]+i][coords[1]].prob += 1


    # pass this check if the west direction does not contain enough spaces for the ship size
    legal_ship_direction = True
    if coords[1]-(ship_size-1) < 0:
        legal_ship_direction = False
    else:    
        for i in range(0, ship_size):
            if(board[coords[0]][coords[1]-i].hit == True and board[coords[0]][coords[1]-i].part_of_ship == False):
                legal_ship_direction = False
        
    if legal_ship_direction:
        for i in range(0,ship_size):
            if(board[coords[0]][coords[1]-i].hit == False):
                board[coords[0]][coords[1]-i].prob += 1


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


def player_turn(board):
    """
    Takes the players turn, returns false if the location hit does not contain
    a battleship, true otherwise
    """
    print("Player's turn, where would you like to hit?")
    x_coord = int(input("Enter X Coordinate: "))
    y_coord = int(input("Enter Y Coordinate: "))

    while(board[x_coord][y_coord].hit):
        print("That location has already been hit - please select a different location")
        x_coord = int(input("Enter X Coordinate: "))
        y_coord = int(input("Enter Y Coordinate: "))
    board[x_coord][y_coord].hit = True
    if(board[x_coord][y_coord].part_of_ship):
        print("YOU HIT AN ENEMY BATTLESHIP")
        return True
    else:
        print("YOU MISSED")
        return False

def single_player_game(board):
    ai_player = AI()
    ai_score = 0
    turns = 0
    while(ai_score < 17):
        ai_takes_turn = ai_player.AI_turn(board)
        turns += 1
        show_ai_view(board)
        x = input("Press any key to continue... ")
        if x == 'q':
            quit()
        if ai_takes_turn:
            ai_score += 1
            
    print(f"The AI has taken {turns} turns to complete the game.")

def show_ai_view(board):
    for row in board:
        for node in row:
            node.view_prob()
            
            
def print_game(board):
    """
    this will print out the board state (without identifying information)
    """
    for row in board:
        for node in row:
            node.print_node()


def print_setup(board):
    """
    This will print out the board state with identifying information
    """
    for row in board:
        for node in row:
            node.view_info()

def play_game(player_board, ai_board):
    ai_player = AI()
    player_score = 0
    ai_score = 0
    
    # setup player board and ai_board
    player_setup(player_board)
    ai_player.set_ai_ships(ai_board)

    # print the initial boards for viewing
    print("INITIAL PLAYER BOARD")
    print_setup(player_board)

    print("INITIAL AI BOARD")
    print_setup(ai_board)
    
    while(player_score != 17 and ai_score != 17):
        print("ENEMY BOARD")
        print_game(ai_board)
        player_takes_turn = player_turn(ai_board)
        print_game(ai_board)
        if(player_takes_turn):
            player_score += 1
        
        x = input("Press any key to continue... ")
        if(x == 'q'):
            quit()
        
        if(x == 'ai'):
            show_ai_view(player_board)
            time.sleep(5)
            x = input("Press any key to continue... ")
        
        
        ai_takes_turn = ai_player.AI_turn(player_board)
        print_game(player_board)
        if(ai_takes_turn):
            ai_score += 1
            
        x = input("Press any key to continue... ")
        if(x == 'q'):
            quit()
        
        if(x == 'ai'):
            show_ai_view(player_board)
            time.sleep(5)
            x = input("Press any key to continue... ")
        
    
def main():
    player_board = []
    ai_board = []
    for i in range(10):
        row = []
        for j in range(10):
            new_node = Node(x_coord=i, y_coord=j, probability=1)
            row.append(new_node)
        player_board.append(copy.deepcopy(row))
        ai_board.append(copy.deepcopy(row))
    print("What game would you like to play:")
    print("1) Two players\n2) Single player (AI only)")
    game = int(input("Selection: "))
    if game == 1:
        play_game(player_board, ai_board)
    else:
        ai_player = AI()
        ai_player.set_ai_ships(player_board)
        print_setup(player_board)
        single_player_game(player_board)


main()