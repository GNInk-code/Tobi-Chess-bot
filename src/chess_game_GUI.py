try:
    import tkinter as tk # I can't do much here without that
    from tkinter import ttk, messagebox, filedialog # For some few useful utils
    from PIL import Image, ImageTk # For the images
    from webbrowser import open as wbopen #To open lichess and the github repo
    import threading #To launch the robot on a separate thread
    import sys #Used to relaunch the program (executable details) -> menu()/key_manager()/
    import os #Used for changing dirs... & to relaunch the program if reset
    import time #To put the date on the exported file
    from random import randint # random moves at the beginning
    from math import log # For some predictions about the depth used
except Exception as err:
    raise ImportError("Can't load necessary modules for this ui") from err

try:
    import Funcs_for_GUI
    import Chess_fct
    import ROBOTTT as Robot
except Exception as err:
    raise ImportError("Can't load Python files that are needed for this ui") from err

try:
    import pyi_splash # For a splash screen -- ONLY used for PyInstaller
except:
    pass

""" To do:
[x] Import button and function
[x] Robot is thinking label
"""

try:
    #To be in the right dir, otherwise it won't find the pictures
    if os.getcwd()[-4:] != "Code": #os.getcwd() = get current working directory && -4: -> last 4 chars
        os.chdir("./Code") #os.chdir(pathname:str) = change directory
        # There's no dark magic in this that will open ports on your computer :) Hein Alexis!!!
except:
    pass


#Settings

HEIGHT = 720
WIDTH = 900 #Initially done like that; used for chessboard things and pieces
Left_space = 160 #Since then added things like text on the left

BOARD_HEIGHT = 600
BOARD_WIDTH = 600

WhiteX = "#f8f8f8"
RedX = "#bd0000"
BlueX = "#236aa5"
BlackX = "#1f1f1f"
PurpleX = "#aa336a"
BordeauX = "#6f0618"
Light_GreyX = "#777"
GreenX = "#1e6933"

square_size = 75
square_colors = ("#ffcf9f", "#d28c45", "#cdd16a", "#aaa23a") # 0-light ; 1-dark ; 2-light-selected ; 3-dark-selected

Latency_move = 500 #Time waited before unselecting the cells and executing the move (in ms)

#Robot settings
Max_depth = 8
Min_depth = 4
Depth_increase_coefficient = 1.5
Max_time = 60 # in seconds

Max_length_history_of_boards = 15

WINDOW = tk.Tk() #To create the main window

x = (WINDOW.winfo_screenwidth()/2) - (WIDTH/2) # calculate x and y coordinates for the Tk root window -> center
y = (WINDOW.winfo_screenheight()/2) - (HEIGHT/2)
WINDOW.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y)) #And sets the where it is placed on the screen
WINDOW.resizable(width=False, height=False) #Sets the resizable option for the window to false
WINDOW.title("GUI of Chess game") # To put a title to the window
WINDOW['bg'] = WhiteX #Set the background color of the Window

BOARD = tk.Canvas(WINDOW, width=BOARD_WIDTH, height=BOARD_HEIGHT, bd=0, highlightthickness=0)

game = False
has_played = False

Turn = True #White's turn (True) or Black's turn (False)

Type_of_game = 0 # 0->human vs human  ;  1-> bot white  ;  2 -> bot black  ;  3 -> bot vs bot


#-----------------------------------------------------------------

BOARD.place(x=int(((WIDTH+Left_space) - BOARD_WIDTH)/2), y=int((HEIGHT-BOARD_HEIGHT)/2))

class chessboard(): #The chessboard is actually a class. Therefore it has properties and functions
    def __init__(self):
        self.selected1 = [None, None] #pos of selected squares
        self.selected2 = [None, None] #=> Default for no selection

        self.last_selected_squares = [(None, None), (None, None)] #Will contain the coordinates of the last selected squares
        self.check = 0 #0-> None ; 1-> Whites ; 2-> Blacks

        self.highlight_width = 6

        self.chessboard_orientation = True # True -> white down -- False -> black down
        self.turn_around_IMAGE = Image.open(Funcs_for_GUI.resource_path("Media/Turn_around.png"))
        self.turn_around_IMAGE = self.turn_around_IMAGE.resize((50, 70))
        self.turn_around_IMAGE = ImageTk.PhotoImage(self.turn_around_IMAGE)
        self.turn_around_BUTTON = tk.Button(WINDOW, 
                                image=self.turn_around_IMAGE, 
                                command=self.turn_around,
                                relief="flat", 
                                background=WhiteX,
                                highlightthickness=0,
                                bd=0)
        self.turn_around_BUTTON.place(x=(WIDTH - (WIDTH-Left_space-BOARD_WIDTH)/2)+10, y=HEIGHT/2 - 35) #- 25 and -35 -> half of image width/height


        self.create_Chessboard()
        WINDOW.bind('<Button-1>', self.select)
        
    def create_Chessboard(self) -> None:
        x = 0
        y = 0
        alternation = False # For having each time a different color --> will be the element of the colors tuple

        #Saving the checked king cell according to the chessboard orientation
        if self.check == 1:
            for piece in pieces_LIST:
                if piece.id == "Kw1":
                    check_cell = (piece.position[0] if chessboard.chessboard_orientation else 7 - piece.position[0], 7 -piece.position[1] if chessboard.chessboard_orientation else piece.position[1]) #finds king's cell
        elif self.check == 2:
            for piece in pieces_LIST:
                if piece.id == "Kb1":
                    check_cell = (piece.position[0] if chessboard.chessboard_orientation else 7 - piece.position[0], 7 -piece.position[1] if chessboard.chessboard_orientation else piece.position[1]) #finds king's cell
        else:
            check_cell = (-1, -1) #If there is no check

        for row in range(8):
            for item in range(8):

                if [item, row] == self.selected1 or [item, row] == self.selected2: #If it is a selected cell
                    
                    if (item, row) == check_cell: #If it is a king in check
                        fill_color = RedX

                    elif (item, row) in self.last_selected_squares: #If it was a last selected cell and first orientation
                        fill_color = square_colors[int(alternation)+2]
                    
                    else:
                        fill_color = square_colors[int(alternation)]
                    
                    BOARD.create_rectangle(x + self.highlight_width//2, 
                    y + self.highlight_width//2, 
                    x + square_size - self.highlight_width//2, 
                    y + square_size - self.highlight_width//2, 
                    fill=fill_color, 
                    width=self.highlight_width,
                    outline=WhiteX)
    

                elif (item, row) in self.last_selected_squares : #If it was a last played square or ((7 - item, 7 - row) in self.last_selected_squares and not self.chessboard_orientation)
                    BOARD.create_rectangle(x, y, x+square_size, y+square_size, fill=square_colors[int(alternation)+2], width=0)
                    #int(alternation) +2 for last selected colors ==> With orientation=True

                elif (item, row) == check_cell: #If it was the checked king's square
                    BOARD.create_rectangle(x, y, x+square_size, y+square_size, fill=RedX, width=0)
                    #int(alternation) +2 for last selected colors ==> With orientation=True

                
                else: #If it's a normal square
                    BOARD.create_rectangle(x, y, x+square_size, y+square_size, fill=square_colors[int(alternation)], width=0)
                
                x += square_size
                alternation = not alternation
            x = 0
            y += square_size
            alternation = not alternation

        return None

    def select(self, event) -> None: #called each time the board is clicked
        global game, Type_of_game
        
        if not game or (Type_of_game == 1 and Turn) or (Type_of_game == 2 and not Turn) or Type_of_game == 3: # When the user cannot select a square
            return None

        x = event.x_root - WINDOW.winfo_x() #Otherwise doesn't calculate position relative to window
        y = event.y_root - WINDOW.winfo_y()

        x -= int((WIDTH+Left_space-BOARD_WIDTH)/2) #taking out board x padding
        y -= int((HEIGHT-BOARD_HEIGHT)/2) #taking out board y padding

        if x < 0 or y <0 or x > BOARD_WIDTH or y > BOARD_HEIGHT: #If it is outside of the canvas, it will automatically deselect
            self.deselect()
            return None

        x //= square_size #Performing entire division
        y //= square_size

        if self.selected1 == [None, None]: #If None are selected already
            self.selected1 = [x, y]
        
        elif self.selected2 == [None, None]: #If the second is not yet selected
            if self.selected1 != [x, y]: #We don't want to enable two selections for the same square
                self.selected2 = [x, y]
                WINDOW.after(Latency_move, lambda: self.move_piece(self.selected1, self.selected2))
        
        #ATTENTION: these are not real coordinates, there are relative to the chessboard not to its orientation

        self.create_Chessboard()

        return None

    def deselect(self, event=0) -> None:
        self.selected1 = [None, None]
        self.selected2 = [None, None]

        self.create_Chessboard()

        return None

    def turn_around(self) -> None:
        self.chessboard_orientation = not self.chessboard_orientation
        
        self.deselect()

        if not self.chessboard_orientation: # Placing the pieces according to the chessboard orientation
            for element in pieces_LIST:
                element.place((7 - element.position[0], 7 - element.position[1]))
        else:
            for element in pieces_LIST:
                element.place(element.position)
        
        try: #Won't like doing 7-None at the beginning
            self.last_selected_squares[0] = ( 7 - self.last_selected_squares[0][0], 7 - self.last_selected_squares[0][1]) #Re inverting last selected squares positions
            self.last_selected_squares[1] = ( 7 - self.last_selected_squares[1][0], 7 - self.last_selected_squares[1][1]) #Re inverting position 1 #Saving the last selected squares
        except:
            pass

        self.create_Chessboard() #Re-creating the chessboard with new colored cells

        menu.captured() #Change white and black text orientation

        return None

    def bot_call(self):
        """
        Calls the bot and then calls the function to play
        """

        def sub_call(): # I did a sub call so that I can send this into another process
            # Some experimental calculations to estimate what depth it is supposed to search to
            estimated_time_depth_4 = 0.063 * (32-(len(menu.black_captured)//2 + len(menu.white_captured)//2)) + 0.01 * len(Chess_fct.listage_coup_possible(Chess_fct.n, Turn, False)) -0.4

            if estimated_time_depth_4 == 0: # To avoid an error when taking its logarithm
                estimated_time_depth_4 = 0.1

            estimated_depth = Min_depth + int(abs(1.074-2.967*log(abs(estimated_time_depth_4)))*Depth_increase_coefficient)
            if estimated_depth > Max_depth:
                estimated_depth = Max_depth
            print(f"Depth: {estimated_depth}, with ({estimated_time_depth_4})")

            before = time.time()

            mv, depth = Robot.ROBOT(Chess_fct.n, Turn, estimated_depth, Max_time)
            
            print(time.time()-before)

            WINDOW.after(0, chessboard.bot_play(mv, int(depth)))

        if Type_of_game == 0: # If it a human vs human game
            return None

        if Type_of_game == 1 and not Turn: #If the robot is white and the turn is for blacks...
            return None
        if Type_of_game == 2 and Turn:
            return None

        try:
            menu.thinking.place(x=10, y=10)

            num = randint(0, 10)
            if len(menu.moves_LIST) < 6 and Robot.possible_ouverture_moves(Turn, menu.moves_LIST, num) != False: # Opening from list of possible openings
                mv = Robot.possible_ouverture_moves(Turn, menu.moves_LIST, num)
                self.bot_play(mv, 0)
            else:
                t = threading.Thread(target=sub_call, daemon=True).start() # Starting a thread so that the process is independent and so that the GUI doesn't freeze
        
        except Exception as err:
            Funcs_for_GUI.error("Something went wrong with the robot\nException: " + str(err))
            print(err)
            menu.thinking.place_forget()
            return None

    def bot_play(self, mv, depth):
        
        menu.thinking.place_forget()

        Alexis_chessboard = Funcs_for_GUI.bitify(Chess_fct.n) # Fetching Alexis' list and copying it so it doesn't change locally

        Chess_fct.n = Chess_fct.jouer_le_coup(mv, Turn, Chess_fct.n)
        
        coords = Funcs_for_GUI.convert_bot_to_coords(Alexis_chessboard, Funcs_for_GUI.bitify(Chess_fct.n), Turn, mv)

        menu.depth(depth)

        WINDOW.after(0, lambda: self.move_piece(coords[0], coords[1], mv))

    def move_piece(self, position1:tuple[int, int], position2:tuple[int, int], bot_move:str=None): #Bot coords is used if the bot directly wants to move a piece

        global Turn, game, has_played

        self.deselect()
             
        try: #can return an error (if no valid piece is selected)
            if bot_move == None:
                move = Funcs_for_GUI.convert_to_chess_coords(WINDOW, pieces_LIST, position1, position2, self.chessboard_orientation) #Calling external function to translate the position change into chess coordinates
                
                if self.chessboard_orientation: #If the chessboard is oriented as default, I have to invert the y positions
                    position1 = (position1[0], 7 - position1[1])
                    position2 = (position2[0], 7 - position2[1])
                else: # Here, I have to invert the x positions
                    position1 = (7 - position1[0], position1[1])
                    position2 = (7 - position2[0], position2[1])
            else:
                move = str(bot_move)

        except Exception as error: # the error can only be raised by the "convert_to_chess_coords" function if no piece is selected
            print("Exception: ", end="")
            print(error)
            Funcs_for_GUI.error("No valid piece was selected")
            return None
        

        piece_that_will_move = Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, position1)

        if bot_move == None: #If the bot played, it won't check if the move is feasible
            try:
                if (piece_that_will_move.color == "white" and not Turn) or (piece_that_will_move.color == "black" and Turn): #If the wrong color is playing
                    raise Exception("The wrong color is playing!")

                if move != None:
                    for possible_move in Chess_fct.listage_coup_possible(Chess_fct.n, Turn, False): # Checks for every possible move of this piece from Chess_fct
                        if move == possible_move or move[:-1] + "#" == possible_move or move + "#" == possible_move or move + "*" == possible_move: # "#" instead of "+" maybe
                            move = possible_move #In case there is a # for checkmate
                            break

                    else: # If the loop didn't break -> nothing did correspond
                        raise Exception(f"Sorry, this move doesn't seem to work: {move}\nIf it is supposed to, please report this issue on our repository, by clicking 'p', (along with this error message).")

                else:
                    raise Exception("Sorry, I can't recognize your move.\nIf your sure this move exists, please report this issue on our repository, by clicking 'p', (along with this error message).")
                    
            except Exception as error: #Handling errors raised earlier
                print("Exception: ", end="")
                print(error)
                Funcs_for_GUI.error(error)
                return None


        menu.move(move) #Change Leftward label with current move

        if 'x' in move: #Calling the captured function from the captured piece.

            if 'e.p.' in move: # Special case for en passant since the captured piece isn't on the same square as the opponent pawn
                if Turn: # If whites are playing, the captured piece is just below where the white pawn wants to go
                    Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, (position2[0], position2[1]-1)).captured()
                else: # If blacks are playing, the captured piece is just on top of where the black pawn wants to go
                    Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, (position2[0], position2[1]+1)).captured()

            else: # If it is not a en passant move
                Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, position2).captured()
        if '+' in move:
            self.check = int(Turn) + 1
        elif self.check != 0: #If a turn has been played after being checked -> no check
            self.check = 0


        if move == 'O-O': #I have to move the rook if castling
            if Turn: #If whites
                Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, (7, 0)).change_position(((5, 0)), 1)
            else:
                Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, (7, 7)).change_position(((5, 7)), 1)
        elif move == 'O-O-O':
            if Turn: #If whites
                Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, (0, 0)).change_position(((3, 0)), 1) #Special != None since we don't want its background to be green
            else:
                Funcs_for_GUI.what_piece_in_which_cell(pieces_LIST, (0, 7)).change_position(((3, 7)), 1)

        if '=' in move: #If promotion
            _letter = move[-2] if '+' in move else move[-1] #Find the letter -> and getting rid of '+'
            piece_that_will_move.change_position(position2, promotion=_letter) #Move piece and change image...
        else:
            piece_that_will_move.change_position(position2) #Move actual piece on chessboard

        if bot_move == None: # If the bot played, it already changes the list, sadly
            Chess_fct.n = Chess_fct.jouer_le_coup(move, Turn, Chess_fct.n) # Changing Alexis' pieces list
        
        Chess_fct.previous_boards.append(Funcs_for_GUI.bitify(Chess_fct.n)) # Adding board to history
        if len(Chess_fct.previous_boards) > Max_length_history_of_boards: # So that the program only keeps the last 15 boards in memory
            del Chess_fct.previous_boards[0]
        
        self.last_selected_squares[0] = (position1[0], 7 - position1[1]) if self.chessboard_orientation else  (7 - position1[0], position1[1]) #Re inverting position 1
        self.last_selected_squares[1] = (position2[0], 7 - position2[1]) if self.chessboard_orientation else  (7 - position2[0], position2[1]) #Re inverting position 1 #Saving the last selected squares

        self.create_Chessboard() #Re-draw the chessboard with new selected colors

        Turn = not Turn #Inverting Turn
        has_played = True
        
        if '#' in move:
            if Turn:
                tk.messagebox.showinfo("End of game", message="Blacks won the game!") # Blacks since the turn was inverted just before
                menu.result = '0-1'
            else:
                tk.messagebox.showinfo("End of game", message="Whites won the game!")
                menu.result = '1-0'
            game = False
            return None

        elif '*' in move:
            tk.messagebox.showinfo("End of game", message="Draw!")
            menu.result = '1/2-1/2'
            game = False
            return None
        
        
        WINDOW.after(0, chessboard.bot_call())


class piece():
    def __init__(self, type:str, color:bool, position:tuple[int, int], id:str):
        '''
        - type:str -> must be full and capitalized -- example: `Pawn`
        important for file path!!

        - id:str -> will be useful to recognize which piece it is, since I now put all pieces in `pieces_LIST`
        
        ## Output
        This will create pieces that are in fact `tk.Label`'s!
        '''
        self.type = type
        self.position = position
        self.id = id
        if color:
            self.color = "white"
        else:
            self.color = "black"

        self.image = Image.open(Funcs_for_GUI.resource_path("Media/" + self.type + "_" + self.color + ".png"))
        self.image = self.image.resize((50, 60))
        self.image = ImageTk.PhotoImage(self.image)
        self.size = (self.image.width(), self.image.height())

        self.widget = tk.Label(WINDOW, image=self.image, background=square_colors[not (position[0]+position[1])%2]) #Very difficult formula: if the sum of the coords is even -> color 2; if it is odd -> color1. (the `not is to take the opposite value, since the colors are inverted)

        self.place(self.position)

    def change_position(self, new_position:tuple[int, int], special=None, promotion:str=None) -> tuple[int, int]: #special-> if castling no need to color piece background ; promotion-> the letter to promote to
        self.position = new_position
    
        if promotion != None:
            match promotion: #Since I have to change the letters to the words...
                case "Q":
                    self.type = "Queen"
                case "B":
                    self.type = "Bishop"
                case "R":
                    self.type = "Rook"
                case "N":
                    self.type = "Knight"

            self.image = Image.open(Funcs_for_GUI.resource_path("Media/" + self.type + "_" + self.color + ".png"))
            self.image = self.image.resize((50, 60))
            self.image = ImageTk.PhotoImage(self.image)
            self.widget.config(image=self.image)

        if chessboard.chessboard_orientation: #I still have to invert, since the next function takes positions relative to the chessboard
            new_position = (new_position[0], new_position[1])
        else: # Here, I have to invert the x positions
            new_position = (7 - new_position[0], 7 - new_position[1])

        self.place(new_position)

        for piece in pieces_LIST: #Put all pieces to default background color
            if piece.position[0] != -1: #if the piece is out, it won't do it
                piece.widget.config(background=square_colors[not (piece.position[0] + piece.position[1]) % 2])

            if piece.type == "King" and piece.color == "white" and chessboard.check == 1: #The king's cell becomes red if his in check
                piece.widget.config(background=RedX)
            elif piece.type == "King" and piece.color == "black" and chessboard.check == 2:
                piece.widget.config(background=RedX)

        if special == None:
            self.widget.config(background=square_colors[(not (self.position[0] + self.position[1]) % 2) + 2]) #To change the background color to the cell color

        return self.position

    def place(self, position:tuple[int, int], highlight_width:int=0) -> None:

        if self.position[0] == -1: #Out
            self.widget.destroy()
            return None

        board_0 = (int(((WIDTH+Left_space) - BOARD_WIDTH)/2), int((HEIGHT-BOARD_HEIGHT)/2)) #Canva coords

        x = board_0[0] + (position[0])*square_size + int((square_size-self.size[0])/2) - highlight_width #space before canvas + squares + in the middle of its square
        y = board_0[1] + (7 - position[1])*square_size + int((square_size-self.size[1])/2) - highlight_width #space before canvas + squares + in the middle of its square [IMPORTANT]: 7- is used to invert the positions in y. Since with default white at the bottom, 0, 0, is for the grid 0, 7

        self.widget.place(x=x, y=y)

        return None

    def captured(self) -> None:
        self.position = (-1, 0 if self.color=="white" else 1) #-1 -> means out; 1/0 for which team
        self.place(self.position)

        if self.color == "white":
            if self.type == "Pawn":
                menu.captured("♙", False) #False because the blacks took the piece
            elif self.type == "Rook":
                menu.captured("♖", False)
            elif self.type == "Knight":
                menu.captured("♘", False)
            elif self.type == "Bishop":
                menu.captured("♗", False)
            elif self.type == "Queen":
                menu.captured("♕", False)
        else:
            if self.type == "Pawn":
                menu.captured("♟", True) #True because the whites took the piece
            elif self.type == "Rook":
                menu.captured("♜", True)
            elif self.type == "Knight":
                menu.captured("♞", True)
            elif self.type == "Bishop":
                menu.captured("♝", True)
            elif self.type == "Queen":
                menu.captured("♛", True)

        return None


class menu():
    def __init__(self):
        self.moves_LIST = [] #Will store all moves

        self.result = ''

        self.move_LABEL = tk.Label(WINDOW, bg=WhiteX, text="Move: ", font=("Arial", 22), foreground=BlueX)
        self.move_LABEL.place(x=10, y=HEIGHT/2-60)

        self.depth_LABEL = tk.Label(WINDOW, bg=WhiteX, text="Depth: ", font=("Arial", 22), foreground=PurpleX)

        self.export_BUTTON = tk.Button(WINDOW, bg=WhiteX, text="Export", font=("Arial", 22), foreground=BordeauX, state="disabled", relief="flat", command=self.export, highlightbackground="#bbb", highlightthickness=2, activeforeground=BordeauX)
        self.export_BUTTON.place(x=Left_space/2-25, y=HEIGHT/2+160)

        self.import_BUTTON = tk.Button(WINDOW, bg=WhiteX, text="Import", font=("Arial", 22), foreground=BordeauX, state="normal", relief="flat", command=self.import_, highlightbackground=BordeauX, highlightthickness=3, activeforeground=BordeauX)
        self.import_BUTTON.place(x=Left_space/2-25, y=HEIGHT/2+220)
        if os.name == 'nt': #For Windows
            self.export_BUTTON.config(relief='solid')
            self.import_BUTTON.config(relief='solid')

        self.white_FRAME = tk.Frame(WINDOW, background=WhiteX, bd=0, borderwidth=0, height=(HEIGHT-BOARD_HEIGHT)/2-20, width=BOARD_WIDTH)
        self.white_text_LABEL = tk.Label(self.white_FRAME, bg=WhiteX, fg=BlackX, text="White:", font=("Arial", 18))
        self.white_text_LABEL.grid(column=0, row=0)
        self.white_captured_LABEL = tk.Label(self.white_FRAME, bg=WhiteX, fg=BlackX, font=("Arial", 22))
        self.white_captured_LABEL.grid(column=1, row=0)
        self.white_captured = ""

        self.black_FRAME = tk.Frame(WINDOW, background=WhiteX, bd=0, borderwidth=0, height=(HEIGHT-BOARD_HEIGHT)/2-20, width=BOARD_WIDTH)
        self.black_text_LABEL = tk.Label(self.black_FRAME, bg=WhiteX, fg=BlackX, text="Black:", font=("Arial", 18))
        self.black_text_LABEL.grid(column=0, row=0)
        self.black_captured_LABEL = tk.Label(self.black_FRAME, bg=WhiteX, fg=BlackX, font=("Arial", 22))
        self.black_captured_LABEL.grid(column=1, row=0)
        self.black_captured = ""

        self.thinking = tk.Label(WINDOW, bg=WhiteX, fg="#777", font=("Arial", 16), text="Robot is thinking...")

        self.max_depth_LABEL = tk.Label(WINDOW, bg=WhiteX, text="Max Depth: ", font=("Arial", 16), foreground=GreenX)
        self.max_depth_Spin = tk.Spinbox(WINDOW, bg=WhiteX,font=("Arial", 14), foreground=BlackX, from_=2, to=16, increment=1, textvariable=Max_depth, state="normal", cursor="hand2", bd=3, justify="center", wrap=True, width=3, command=self.update_depth_specs)

        self.min_depth_LABEL = tk.Label(WINDOW, bg=WhiteX, text="Min Depth: ", font=("Arial", 16), foreground=GreenX)
        self.min_depth_Spin = tk.Spinbox(WINDOW, bg=WhiteX,font=("Arial", 14), foreground=BlackX, from_=1, to=15, increment=1, textvariable=Min_depth, state="normal", cursor="hand2", bd=3, justify="center", wrap=True, width=3, command=self.update_depth_specs)
        self.min_depth_Spin.delete(0, 1) #Putting desired values
        self.min_depth_Spin.insert(0, Min_depth)

        self.max_depth_Spin.delete(0, 1)
        self.max_depth_Spin.insert(0, Max_depth)

        self.captured() #To place the labels

        WINDOW.bind('<KeyPress>', self.key_manager)
        WINDOW.after(0, lambda: menu.mode())
        
    def move(self, move:str):
        self.move_LABEL.config(text="Move: " + move)

        self.export_BUTTON.config(state="normal", highlightthickness=3, bd=0, highlightbackground=BordeauX) #Enabling the export button
        self.moves_LIST.append(move) #Adding current move to the list

        self.import_BUTTON.config(state="disabled", highlightthickness=2, highlightbackground="#bbb") # Disabling the import button

    def depth(self, depth:int):

        self.depth_LABEL.place(x=10, y=HEIGHT/2)
        self.depth_LABEL.config(text='Depth: ' + str(depth))

        self.min_depth_LABEL.place(x=10, y=HEIGHT/2-250)
        self.min_depth_Spin.place(x=130, y=HEIGHT/2-250, height=30)

        self.max_depth_LABEL.place(x=10, y=HEIGHT/2-200)
        self.max_depth_Spin.place(x=130, y=HEIGHT/2-200, height=30)

    def update_depth_specs(self):
        global Min_depth, Max_depth

        local_min = int(self.min_depth_Spin.get())
        local_max = int(self.max_depth_Spin.get())

        if local_max <= local_min:
            self.min_depth_Spin.delete(0, 15)
            self.min_depth_Spin.insert(0, Min_depth)

            self.max_depth_Spin.delete(0, 15)
            self.max_depth_Spin.insert(0, Max_depth)
        else:
            Min_depth = local_min
            Max_depth = local_max

    def export(self):
        """
        Will export current game as pgn
        """

        if self.export_BUTTON['state'] == 'disabled': #If no one has played
            return None

        self.metadata = {"Event": "Casual Game with Chess-bot",
                        "Site": "?",
                        "Date": "????.??.??",
                        "Round": "?",
                        "White": "?",
                        "Black": "?",
                        "Result": "?"}
        
        #Metadata configuration
        self.metadata['Date'] = time.strftime('%Y.%m.%d')
        match Type_of_game: #White & Black
            case 0:
                self.metadata['Black'], self.metadata['White'] = "Human", "Human"
            case 1:
                self.metadata['Black'], self.metadata['White'] = "Human", "Robot"
            case 2:
                self.metadata['Black'], self.metadata['White'] = "Robot", "Human"
            case 3:
                self.metadata['Black'], self.metadata['White'] = "Robot", "Robot"
        self.metadata['Result'] = self.result if self.result != '' else '*'        

        
        try: #Could cause an error
            moves_export_STR = "" #It will locally be stored as a string to send it to the web browser

            with open("Moves_export.pgn", "w", encoding="UTF-8") as file:
                # Metadata
                for key in self.metadata.keys():
                    file.write('[' + key + ' \"' + self.metadata[key] + '\"' + ']' + '\n')
                else:
                    file.write('\n')

                #Moves
                move_index = 1 # On which move number we are (1 mov = black + white)
                for move in self.moves_LIST:
                    if move_index > 0: #if move_index is positive (since it can be negative if we want to ignore this step)
                        file.write(str(move_index) + '. ')
                        moves_export_STR += str(move_index) + '.+' #Saving the same data but replacing the ' ' with '+'

                        move_index += 1

                    file.write(move + ' ') #separating each value with a whitespace
                    moves_export_STR += move + '+'

                    move_index = -move_index #At each repetition it will change from negative to positive and vice-versa
                file.close()

                wbopen('https://lichess.org/paste?pgn=' + moves_export_STR[:-1]) #[:-1] To take everything except the final '+' automatically added
                
                del moves_export_STR # To save some space

        except PermissionError:
            messagebox.showerror('Error while writing file', message="This OS seems not to allow this little innocent program to write a file in this directory.")
        except OSError:
            messagebox.showerror('Error while writing file', message="Your OS seems not to be able to write this file. \nMaybe no space is left on your disk.")
        except Exception as e:
            messagebox.showerror('Error while writing file', message="A random error occurred: " + str(e))

        else: #If everything goes OK -> little text for 2s
            temp_widget = tk.Label(WINDOW, bg=WhiteX, foreground=BlackX, text="Successfully saved file", font=('Arial', 12))
            temp_widget.place(x=23, y=HEIGHT/2+210)
            WINDOW.after(2000, lambda: temp_widget.destroy())

        return None

    def import_(self, file_=None):
        """
        Will be called when 'o' is pressed and will play the moves stored in a .pgn file
        """
        global Turn, has_played, game

        if has_played == True:
            Funcs_for_GUI.error("Please restart this window in order to import and start a new game!")
            return None

        if file_== None:
            file = filedialog.askopenfile('r',
                                    filetypes=[('Portable Game Notation', '.pgn'), ('Text file', '.txt')],
                                    title='Choose the game you want to open',
                                    parent=WINDOW)
        else:
            file = open(file_, 'r')


        if file == None:
            return None

        file_text = file.readlines()
        file.close()

        moves_text = ''
        for line in file_text: # Getting out the line with the moves
            if line[0] == '1':
                moves_text = line
                break

        moves_text.strip() # Taking of trailing whitespaces
        if moves_text == '':
            Funcs_for_GUI.error("It would be better if you actually had put some moves in this file")
            return None
        _temp_moves_LIST = []
        
        temp_text = ''
        for letter in moves_text: # Creating list from str taking spaces as separator
            if letter == ' ':
                _temp_moves_LIST.append(temp_text)
                temp_text = ''
            else:
                temp_text += letter
        else:
            if temp_text != '' and temp_text != ' ':
                _temp_moves_LIST.append(temp_text)
        for move in _temp_moves_LIST: # Removing move number indications
            if move[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                _temp_moves_LIST.remove(move)
        if len(_temp_moves_LIST) == 0:
            Funcs_for_GUI.error("It would be better if you actually had put some moves in this file")

        #Testing if the moves work
        test_board = Chess_fct.nouveau_plateau(Chess_fct.n) # test board to test all the moves and see if there is an error
        local_turn = True
        try: # First testing all moves before actually moving the graphical pieces
            for move in _temp_moves_LIST:
                test_board = Chess_fct.jouer_le_coup(move, local_turn, test_board)
                local_turn = not local_turn
        except Exception as err:
            Funcs_for_GUI.error("The program encountered a problem while reading the moves.\n Make sure the moves are stored in the long algebraic format!")
            return None
        else:
            del test_board, local_turn


        if '#' in _temp_moves_LIST[-1] or '*' in _temp_moves_LIST[-1]:
            self.mode_WINDOW.destroy() # It won't be able to move any pieces any more
        
        
        #Moving the pieces
        game = True # So that it can move the pieces
        for move in _temp_moves_LIST:

            Alexis_chessboard = Funcs_for_GUI.bitify(Chess_fct.n) # Fetching Alexis' list and copying it so it doesn't change locally

            Chess_fct.n = Chess_fct.jouer_le_coup(move, Turn, Chess_fct.n)
            
            coords = Funcs_for_GUI.convert_bot_to_coords(Alexis_chessboard, Funcs_for_GUI.bitify(Chess_fct.n), Turn, move)
            
            chessboard.move_piece(coords[0], coords[1], move)

        if self.mode_WINDOW.winfo_exists():
            game = False
            self.mode_WINDOW.grab_set()

        return None

    def captured(self, piece:str=None, color:bool=None) -> None:

        if chessboard.chessboard_orientation:
            self.white_FRAME.place(x=int(((WIDTH+Left_space) - BOARD_WIDTH)/2), y=HEIGHT-(HEIGHT-BOARD_HEIGHT)/2+10)
            self.black_FRAME.place(x=int(((WIDTH+Left_space) - BOARD_WIDTH)/2), y=10)
        else:
            self.white_FRAME.place(x=int(((WIDTH+Left_space) - BOARD_WIDTH)/2), y=10)
            self.black_FRAME.place(x=int(((WIDTH+Left_space) - BOARD_WIDTH)/2), y=HEIGHT-(HEIGHT-BOARD_HEIGHT)/2+10)
        
        if piece != None:
            if color:
                self.white_captured += " " + piece
                self.white_captured_LABEL.config(text=self.white_captured)
            else:
                self.black_captured += " " + piece
                self.black_captured_LABEL.config(text=self.black_captured)
        
        Robot.nbPieces -= 1

    def info(self):
        info_WINDOW = tk.Toplevel(WINDOW)
        info_WINDOW.grab_set()
        info_WINDOW.bind('<FocusOut>', lambda x: info_WINDOW.lift()) #So it appears at the top

        info_WINDOW.title("Info about Chess-bot GUI") # To put a title to the window
        if os.name == "nt": #Only for Windows
            info_WINDOW.iconbitmap(Funcs_for_GUI.resource_path("Media/icon.ico")) #To put an icon to the window
        info_WINDOW.resizable(width=False, height=False) #Sets the resizable option for the window to false
        info_WINDOW['bg'] = WINDOW['bg'] #Set the background color of the Window
        win_width = 300
        win_height = 350
        x = (info_WINDOW.winfo_screenwidth()/2) - (win_width/2) # calculate x and y coordinates for the Tk root window
        y = (info_WINDOW.winfo_screenheight()/2) - (win_height/2)
        info_WINDOW.geometry('%dx%d+%d+%d' % (win_width, win_height, x, y)) #And sets the where it is placed on the screen
        
        self.icon = Image.open(Funcs_for_GUI.resource_path('./Media/Icon.png'))
        self.icon = self.icon.resize((80, 80))
        self.icon = ImageTk.PhotoImage(self.icon)
        Icon_LABEL = tk.Label(info_WINDOW, bg=info_WINDOW['bg'], border=0,width=80, height=80, fg=BlackX, image=self.icon)
        Icon_LABEL.pack(anchor="n", pady=7)

        dev_LABEL = tk.Label(info_WINDOW, bg=info_WINDOW['bg'], bd=0, text="~Alexis2010CM", font=('Arial', 17), justify="center", cursor="hand2")
        dev_LABEL.pack(anchor='n', pady=0)
        dev_LABEL.bind("<Button-1>", lambda x: wbopen("https://github.com/Alexis2010CM")) #So that one can open my GitHub account
        dev_LABEL.bind('<Enter>', lambda x: WINDOW.config(cursor="hand2"))#change cursor
        dev_LABEL.bind('<Leave>', lambda x: WINDOW.config(cursor="arrow"))

        dev_LABEL2 = tk.Label(info_WINDOW, bg=info_WINDOW['bg'], bd=0, text="~GNInk-code", font=('Arial', 17), justify="center", cursor="hand2")
        dev_LABEL2.pack(anchor='n', pady=0)
        dev_LABEL2.bind("<Button-1>", lambda x: wbopen("https://github.com/GNInk-code"))#So that one can open my GitHub account
        dev_LABEL2.bind('<Enter>', lambda x: WINDOW.config(cursor="hand2"))#change cursor
        dev_LABEL2.bind('<Leave>', lambda x: WINDOW.config(cursor="arrow"))

        date_LABEL = tk.Label(info_WINDOW, bg=info_WINDOW['bg'], bd=0, text="(2025)", font=('Arial', 13), justify="center")
        date_LABEL.pack(anchor='n', pady=2)

        info_LABEL = tk.Label(info_WINDOW, bg=info_WINDOW['bg'], bd=0, text="Press 'r' to reset the game\nPress 'e' to export the moves \ninto a csv file\nPress 'o' to open a PGN file\nPress 'i' or 'h' to get info\nPress 'p' to report an issue", font=('Arial', 15), justify="left")
        info_LABEL.pack(anchor='c', pady=8, padx=10, side="top")

    def key_manager(self, event):

        if event.char == 'r':
            on_closing(game) # Close all threads if active
            os.execl(sys.executable, sys.executable, *sys.argv) #When key `r` is pressed, the program will be relaunched

        elif event.char == 'e':
            self.export()
        
        elif event.char == "i" or event.char == "h":
            self.info()
        
        elif event.char == 'p':
            wbopen("https://github.com/GNInk-code/Chess-bot/issues/new")
        
        elif event.char == 'o':
            self.import_()

    def mode(self):

        self.mode_WINDOW = tk.Toplevel(WINDOW)
        self.mode_WINDOW.transient(WINDOW) # Be on top of the main window
        self.mode_WINDOW.focus_get() # Get focus

        self.mode_WINDOW.title("Chess mode") # To put a title to the window
        if os.name == 'nt':
            self.mode_WINDOW.iconbitmap(Funcs_for_GUI.resource_path("Media/icon.ico")) #To put an icon to the window
        self.mode_WINDOW.resizable(width=False, height=False) #Sets the resizable option for the window to false
        self.mode_WINDOW['bg'] = WINDOW['bg'] #Set the background color of the Window
        win_width = 300
        win_height = 320
        x = (self.mode_WINDOW.winfo_screenwidth()/2) - (win_width/2) # calculate x and y coordinates for the Tk root window
        y = (self.mode_WINDOW.winfo_screenheight()/2) - (win_height/2)
        self.mode_WINDOW.geometry('%dx%d+%d+%d' % (win_width, win_height, x, y)) #And sets the where it is placed on the screen
        
        title_LABEL = tk.Label(self.mode_WINDOW, bg=self.mode_WINDOW['bg'], bd=0, text="Select your game mode", font=('Arial', 17), justify="center")
        title_LABEL.pack(anchor='n', pady=10)

        board_canvas = tk.Canvas(self.mode_WINDOW, bd=0, width=200, height=200)
        board_canvas.pack(pady=20, side="top")

        x = 0
        y = 0
        alternation = False # For having each time a different color --> will be the element of the colors tuple

        for row in range(8):
            for item in range(8):
                board_canvas.create_rectangle(x, y, x+25, y+25, fill=square_colors[int(alternation)], width=0)
                x += 25
                alternation = not alternation
            x = 0
            y += 25
            alternation = not alternation

        b= ttk.Style()
        w = ttk.Style() # I wanted to setup styles so that one border could appear black while the other appears white; however it doesn't seem to work on Ubuntu
        b = b.configure('black.TCombobox', bordercolor=BlackX, borderwidth=3, foreground=BlackX, relief="solid")
        w = w.configure('white.TCombobox', bordercolor=WhiteX, borderwidth=3, foreground=BlackX, relief="solid")

        black_COMBOBOX = ttk.Combobox(self.mode_WINDOW, values=["Human", "Robot"], state="readonly", width=10, height=25, style="black.TCombobox", font=('Arial', 13))
        black_COMBOBOX.set("Black will be a...") #Sets default text so that the user knows who's who
        black_COMBOBOX.place(x=80, y=80, width=150)

        white_COMBOBOX = ttk.Combobox(self.mode_WINDOW, values=["Human", "Robot"], state="readonly", width=10, height=25, style="white.TCombobox", font=('Arial', 13))
        white_COMBOBOX.set("White will be a...")
        white_COMBOBOX.place(x=80, y=220, width=150)
        
        style = ttk.Style()
        style.configure('W.TButton', font=("Arial", 13)) #Set the buttons' style
        
        OKLabel = ttk.Button(self.mode_WINDOW, text='Configure', style='W.TButton', default='active', command=lambda: self.start_game(black_COMBOBOX.get(), white_COMBOBOX.get())) #Creates the 'Ok' button and calling returnType function when pressed
        OKLabel.place(x=100, y=280, height=30)

        self.mode_WINDOW.bind('<KeyPress>', self.key_manager)

        self.mode_WINDOW.protocol("WM_DELETE_WINDOW", lambda: self.start_game()) # If one closes without choosing

        if len(sys.argv) > 1: # If someone opened a .pgn file with the app
            if sys.argv[1][-4:] == ".pgn":
                WINDOW.after(0, self.import_(sys.argv[1]))

    def start_game(self, black="Human", white="Human"):
        """
        Changes the global Type of game variable according to what the user entered for the game mode
        """

        global Type_of_game, game

        if black not in ['Human', 'Robot']:
            black = 'Human'
        if white not in ['Human', 'Robot']:
            white = 'Human'
        
        if black == 'Human' and white == 'Robot':
            Type_of_game = 1
        elif black == 'Robot' and white == 'Human':
            Type_of_game = 2
        elif black == 'Robot' and white == 'Robot':
            Type_of_game = 3
        
        self.mode_WINDOW.destroy()
        WINDOW.focus_get()

        game = True

        if Type_of_game == 1 or Type_of_game == 3: #If the robot has to play first, otherwise directly initiated after the other played
            chessboard.bot_call()

        return None


def on_closing(game:bool, message:bool=False) -> None:
    """
    Literally like when you want to close the window.
    `message` is boolean argument that sends a confirmation message to the user if true.
    """
    if game:
        if message:
            if messagebox.askyesno("Quit", "Are you so disgusted of this terrible UI that you want to leave without even finishing your game?") :
                messagebox.showinfo(message='Thanks for the feedback!')
            else: # If the user finally doesn't want to quit
                return None

        try:
            for thread in Robot.threads: # Killing all threads before ending the program, for avoiding any bugs or unfinished processes
                thread.kill()
            else:
                if len(Robot.threads) != 0:
                    print("Successfully ended all robot threads")
        except:
            print("Unsuccessfully ended robot threads")

        WINDOW.destroy()
    else:
        WINDOW.destroy()


pieces_LIST = [piece("Pawn", 1, (0, 1), "pw1"), #White Pawns
                piece("Pawn", 1, (1, 1), "pw2"),
                piece("Pawn", 1, (2, 1), "pw3"),
                piece("Pawn", 1, (3, 1), "pw4"),
                piece("Pawn", 1, (4, 1), "pw5"),
                piece("Pawn", 1, (5, 1), "pw6"),
                piece("Pawn", 1, (6, 1), "pw7"),
                piece("Pawn", 1, (7, 1), "pw8"),
                
                piece("Rook", 1, (0, 0), "rw1"), #White pieces
                piece("Knight", 1, (1, 0), "kw1"),
                piece("Bishop", 1, (2, 0), "bw1"),
                piece("Queen", 1, (3, 0), "Qw1"),
                piece("King", 1, (4, 0), "Kw1"),
                piece("Bishop", 1, (5, 0), "bw2"),
                piece("Knight", 1, (6, 0), "kw2"),
                piece("Rook", 1, (7, 0), "rw2"),
                
                piece("Pawn", 0, (0, 6), "pb1"), #Black pawns
                piece("Pawn", 0, (1, 6), "pb2"),
                piece("Pawn", 0, (2, 6), "pb3"),
                piece("Pawn", 0, (3, 6), "pb4"),
                piece("Pawn", 0, (4, 6), "pb5"),
                piece("Pawn", 0, (5, 6), "pb6"),
                piece("Pawn", 0, (6, 6), "pb7"),
                piece("Pawn", 0, (7, 6), "pb8"),
                
                piece("Rook", 0, (0, 7), "rb1"), #Black pieces
                piece("Knight", 0, (1, 7), "kb1"),
                piece("Bishop", 0, (2, 7), "bb1"),
                piece("Queen", 0, (3, 7), "qb1"),
                piece("King", 0, (4, 7), "Kb1"),
                piece("Bishop", 0, (5, 7), "bb2"),
                piece("Knight", 0, (6, 7), "kb2"),
                piece("Rook", 0, (7, 7), "rb2")]

chessboard = chessboard()
menu = menu()


WINDOW.protocol("WM_DELETE_WINDOW", lambda: on_closing(game))

if __name__ == "__main__":

    try:
        pyi_splash.update_text('Loading...')
        pyi_splash.close() # Closing splash screen -- ONLY for PyInstaller
    except:
        pass

    Robot.freeze_support() # To magically make multiprocessing work with PyInstaller
    
    if os.name == 'nt': #Windows icon
        WINDOW.iconbitmap(Funcs_for_GUI.resource_path("Media/icon.ico"))

    WINDOW.mainloop()
