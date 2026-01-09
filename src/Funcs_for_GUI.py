import tkinter as tk
import sys
import os
from tkinter import ttk, messagebox
from typing import Literal
from PIL import Image, ImageTk

"""
This file will be imported by the GUI file and will contain important functions
"""

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def error(message:str) -> None:
    """
    Opens a popup window with the error
    """
    messagebox.showerror("Error from Chess-bot GUI", message)
    return None


def what_piece_in_which_cell(pieces_LIST, cell_coordinates:tuple[int, int]):
    """
    Finds what piece is in which cell and returns it.
    Returns None when the square is empty.
    """
    for element in pieces_LIST: #To find which piece was selected
        if element.position == cell_coordinates:
            return element
            break
    else:
        return None

def check_check(pieces_LIST, new_pos, element_color, element_type) -> str:
    """
    Says if the configuration puts the opponent's king in danger.
    Returns '+' if it is and '' if it isn't.
    """

    if element_type == 'Pawn':
        
        future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]-1, new_pos[1]+1)) # The piece that will be eaten in the next round. Case 1
        if future_meal != None: #Otherwise makes an error while taking Nonetype.color...
            if element_color == "white" and future_meal.color == "black" and future_meal.type == "King":
                return '+'
        
        #Case 2
        future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]+1, new_pos[1]+1))
        if future_meal != None:
            if element_color == "white" and future_meal.color == "black" and future_meal.type == "King":
                return '+'
        
        #Case 3
        future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]-1, new_pos[1]-1))
        if future_meal != None:
            if element_color == "black" and future_meal.color == "white" and future_meal.type == "King":
                return '+'
        
        #Case 4
        future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]+1, new_pos[1]-1))
        if future_meal != None:
            if element_color == "black" and future_meal.color == "white" and future_meal.type == "King":
                return '+'
        
    if element_type == 'Knight':
        # Instead of checking for all 8 cases, I made a loop that checks for every delta x and y that are of 2 and 1 for the L shape
        
        for x in range(-2, 3): # -2, -1, 1, 2
            if x == 0: #If x=0, then it doesn't execute the rest of code
                continue
            for y in range(-2, 3): #also -2, -1, 1, 2
                if y == 0:
                    continue
                if (abs(x) == 1 and abs(y) == 2) or (abs(y) == 1 and abs(x) == 2) : #L shape -- x and y are like deltas

                    future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]+x, new_pos[1]+y)) #adding x and y to position
                    if future_meal != None:
                        if element_color != future_meal.color and future_meal.type == "King":
                            return '+'

    if element_type == 'Rook':
        
        #Checks in all four directions
        for x_plus in range(7-new_pos[0]): #First direction ->
            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]+x_plus+1, new_pos[1])) #Adding +1 since we want it to look for +1 instead of +0 in the first round
            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 1rst loop
        
        for x_minus in range(new_pos[0]): #Second direction <-

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]-x_minus-1, new_pos[1]))
            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 2nd loop
        
        for y_plus in range(7-new_pos[1]): #Third direction ↑

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0], new_pos[1]+y_plus+1))
            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 3rd loop
        
        for y_minus in range(new_pos[1]): #Fourth direction ↓

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0], new_pos[1]-y_minus-1))
            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 2nd loop

    if element_type == 'Bishop':
        
        #Checks in all four directions
        y = 0 # Index y for vertical

        for x in range(7-new_pos[0]): #First direction ↗

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]+x+1, new_pos[1]+y+1)) #Adding +1 since we want it to look for +1 instead of +0 in the first round
            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 1rst loop
            y += 1
        
        y = 0 #Re-initialize y for next loop
        for x in range(new_pos[0]): #Second direction ↖

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]-x-1, new_pos[1]+y+1))
            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 2nd loop
            y += 1
        
        y = 0
        for x in range(7-new_pos[1]): #Third direction ↘

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]+x+1, new_pos[1]-y-1))

            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 3rd loop
            y += 1
        
        y = 0
        for x in range(new_pos[1]): #Fourth direction ↙

            future_meal = what_piece_in_which_cell(pieces_LIST, (new_pos[0]-x-1, new_pos[1]-y-1))

            if future_meal != None: #If there is a piece
                if element_color != future_meal.color and future_meal.type == "King": #If the piece is the opponent's king
                    return '+'
                else: #If it is another random piece
                    break #Do not continue the 2nd loop
            y += 1

    if element_type == 'Queen':
        return check_check(pieces_LIST, new_pos, element_color, 'Rook') + check_check(pieces_LIST, new_pos, element_color, 'Bishop') #Here, I did a recursion, since the moves of the queen are the moves of the rook and bishop combined. I added the two since they return strings and it is logically impossible to have check in both directions since there's only one king.
    
    return ''

def convert_to_chess_coords(WINDOW, pieces_LIST, position1:tuple[int, int], position2:tuple[int, int], chessboard_orientation:bool) -> str:
    """
    This function will convert simple coordinates on the chessboard to the more official chess coordinates
    """

    promote_to = None #Only used for promotion and will be as a tuple (letter:str, word:str)

    def x_to_letter(x:int) -> str:
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return alphabet[x]
    

    def promotion(promotion_WIN) -> None:
        """
        Opens a GUI menu for the user to choose between the type of piece.
        
        # A Complete explanation of this very chaotic function:
         - First the TopLevel window has to be created externally, then, it has to be passed as an argument in this function
         - This function will then set up the window and at widgets with options of pieces
         - When one piece is clicked it is highlighted in blue (selecting())
         - When "Promote" is clicked, the value is stored in a global variable called `promote_to`, and the window is destroyed
         - When the window gets destroyed the `WINDOW.wait_window(promotion_WIN)` line will stop waiting and the condition after that will be executed.
        """

        list_of_selected_ones = [False, False, False, False]
        
        def selecting(list_of_types, Type:Literal[1, 2, 3, 4]) -> list[bool, bool, bool, bool]:
            """
            Called each time a piece is selected.
            Returns the list of selected ones
            """

            nonlocal list_of_selected_ones
            
            list_of_selected_ones = [False, False, False, False] #To unselect everybody

            list_of_selected_ones[Type-1] = not list_of_selected_ones[Type-1] #Invert boolean from selected one

            _ = 0
            for piece in list_of_types: #For every possible piece
                if list_of_selected_ones[_]: #If their associated boolean is true
                    piece.configure(highlightthickness=5) #It is highlighted
                else: #Otherwise
                    piece.configure(highlightthickness=0) #It is not
                
                _ += 1
            
                    
        def returnType():
            
            nonlocal list_of_selected_ones
            nonlocal promote_to
            
            if list_of_selected_ones[0] == False and list_of_selected_ones[1] == False and list_of_selected_ones[2] == False and list_of_selected_ones[3] == False:
                list_of_selected_ones[0] = True #auto-selection of queen
            
            if list_of_selected_ones[0]: #If first one true -> queen
                promote_to = ("Q", "Queen")
                
            elif list_of_selected_ones[1]:
                promote_to = ("R", "Rook")

            elif list_of_selected_ones[2]:
                promote_to = ("B", "Bishop")
            
            else:
                promote_to = ("N", "Knight")

            promotion_WIN.destroy()
            return None
        

        # Setting up the window
        promotion_WIN.title("GUI of Chess game - Promote your pawn") # To put a title to the window
        if os.name == 'nt': #WINDOWS icon
            promotion_WIN.iconbitmap(Funcs_for_GUI.resource_path("Media/icon.ico")) #To put an icon to the window
        promotion_WIN.resizable(width=False, height=False) #Sets the resizable option for the window to false
        promotion_WIN['bg'] = WINDOW['bg'] #Set the background color of the Window
        win_width = 600
        win_height = 300
        x = (promotion_WIN.winfo_screenwidth()/2) - (win_width/2) # calculate x and y coordinates for the Tk root window
        y = (promotion_WIN.winfo_screenheight()/2) - (win_height/2)
        promotion_WIN.geometry('%dx%d+%d+%d' % (win_width, win_height, x, y)) #And sets the where it is placed on the screen
        
        
        
        #Elements
        TitleLabel = tk.Label(promotion_WIN, text='Click on the type of piece you want to promote to:', bg=WINDOW['bg'], font=('Arial', 18)) #Create the title
        TitleLabel.pack(side='top', pady=20)
        

        img1 = Image.open(resource_path('./Media/Queen_white.png'))
        img1 = img1.resize((129, 117))
        img1 = ImageTk.PhotoImage(img1)
        Queen = tk.Label(promotion_WIN, image=img1, bg=WINDOW['bg'], highlightbackground='#00a2ed')
        Queen.image = img1
        Queen.place(x=20, y=100)
        Queen.bind('<Button-1>', lambda x=1: selecting(list_of_types, 1))
        
        
        img2 = Image.open(resource_path('./Media/Rook_white.png'))
        img2 = img2.resize((115, 117))
        img2 = ImageTk.PhotoImage(img2)
        Rook = tk.Label(promotion_WIN, image=img2, bg=WINDOW['bg'], highlightbackground='#00a2ed')
        Rook.image = img2
        Rook.place(x=40+int((win_width-100)/4), y=100)
        Rook.bind('<Button-1>', lambda x=1: selecting( list_of_types, 2))
        

        img3 = Image.open(resource_path('./Media/Bishop_white.png'))
        img3 = img3.resize((129, 117))
        img3 = ImageTk.PhotoImage(img3)
        Bishop = tk.Label(promotion_WIN, image=img3, bg=WINDOW['bg'], highlightbackground='#00a2ed')
        Bishop.image = img3
        Bishop.place(x=20+(20+int((win_width-100)/4))*2, y=100)
        Bishop.bind('<Button-1>', lambda x=1: selecting(list_of_types, 3))
        

        img4 = Image.open(resource_path('./Media/Knight_white.png'))
        img4 = img4.resize((117, 117))
        img4 = ImageTk.PhotoImage(img4)
        Knight = tk.Label(promotion_WIN, image=img4, bg=WINDOW['bg'], highlightbackground='#00a2ed')
        Knight.image = img4
        Knight.place(x=20+(20+int((win_width-100)/4))*3, y=100)
        Knight.bind('<Button-1>', lambda x=1: selecting(list_of_types, 4))


        list_of_types = [Queen, Rook, Bishop, Knight]

        promotion_WIN.bind('<Return>', lambda x: returnType()) 
        
        style = ttk.Style()
        style.configure('W.TButton', font=("Arial", 13)) #Set the buttons' style
        
        OKLabel = ttk.Button(promotion_WIN, text='Promote', style='W.TButton', default='active', command=returnType) #Creates the 'Ok' button and calling returnType function when pressed
        OKLabel.place(x=487, y=250)
    

        promotion_WIN.protocol("WM_DELETE_WINDOW", lambda: messagebox.showwarning("Nah Bro", 'You silly foul, you really thought you could not choose any promotion! What about a queen?')) #If the user wants to close the window


    if chessboard_orientation: #If the chessboard is oriented as default, I have to invert the y positions
        pos1 = (position1[0], 7 - position1[1])
        pos2 = (position2[0], 7 - position2[1])
    else: # Here, I have to invert the x positions
        pos1 = (7 - position1[0], position1[1])
        pos2 = (7 - position2[0], position2[1])


    element = what_piece_in_which_cell(pieces_LIST, pos1)
    if what_piece_in_which_cell(pieces_LIST, pos1) == None: #If no piece was selected...
        raise Exception("No valid piece was selected!")
    

    if element.type == "Pawn":

        #Moving Pawn
        if (pos2 == (pos1[0], pos1[1]+1) or pos2 == (pos1[0], pos1[1]-1)) and what_piece_in_which_cell(pieces_LIST, pos2) == None: #If where the pawn wants to go is one cell over or under it
            if (pos2[1] == 7 and element.color == "white") or (pos2[1] == 0 and element.color == "black"): # If pawn promotion
                
                promotion_WIN = tk.Toplevel(WINDOW) #Creating the child window

                promotion(promotion_WIN) #Setting the widgets and selection on toplevel window

                WINDOW.wait_window(promotion_WIN) #Wait until the toplevel window is destroyed

                return x_to_letter(pos2[0]) + str(pos2[1]+1) + "=" + promote_to[0] + check_check(pieces_LIST, pos2, element.color, promote_to[1]) #!! piece type as Q, R, N, B Ex: b1=Q+
            else:
                return x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: a2

        #Pawn capturing
        elif what_piece_in_which_cell(pieces_LIST, pos2) != None and ((pos2 == (pos1[0]+1, pos1[1]+1) or pos2 == (pos1[0]-1, pos1[1]+1)) or (pos2 == (pos1[0]+1, pos1[1]-1) or pos2 == (pos1[0]-1, pos1[1]-1))): # When the pawn moves diagonally to capture somebody. !!! It first looks if the cell where it wants to go is not empty
            if (pos2[1] == 7 and element.color == "white") or (pos2[1] == 0 and element.color == "black"):
                
                promotion_WIN = tk.Toplevel(WINDOW) #Creating the child window

                promotion(promotion_WIN)

                WINDOW.wait_window(promotion_WIN)

                return x_to_letter(pos1[0]) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + "=" + promote_to[0] + check_check(pieces_LIST, pos2, element.color, promote_to[1])
            else:
                return x_to_letter(pos1[0]) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type)#Ex: axb3
        
        #En passant
        elif (what_piece_in_which_cell(pieces_LIST, (pos2[0], pos1[1])) != None): #If the cell next to it is not empty
            if ((what_piece_in_which_cell(pieces_LIST, (pos2[0], pos1[1])).type == "Pawn")) and (pos2 == (pos1[0]+1, pos1[1]+1) or pos2 == (pos1[0]-1, pos1[1]+1)) or (pos2 == (pos1[0]+1, pos1[1]-1) or pos2 == (pos1[0]-1, pos1[1]-1)): #It first checks if the cell next to it is containing a pawn, then if it wants to move diagonally
                return x_to_letter(pos1[0]) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + "e.p." + check_check(pieces_LIST, pos2, element.color, element.type)#Ex: axb3e.p.+
        
        #Pawn Promotion -> see in individual moves

        #Moving two squares
        if (pos2 == (pos1[0], pos1[1]+2) or pos2 == (pos1[0], pos1[1]-2)) and what_piece_in_which_cell(pieces_LIST, pos2) == None:

            if (pos2[1] == 7 and element.color == "white") or (pos2[1] == 0 and element.color == "black"): # If pawn promotion
                
                promotion_WIN = tk.Toplevel(WINDOW) #Creating the child window

                promotion(promotion_WIN) #Setting the widgets and selection on toplevel window

                WINDOW.wait_window(promotion_WIN) #Wait until the toplevel window is destroyed

                return x_to_letter(pos2[0]) + str(pos2[1]+1) + "=" + promote_to[0] + check_check(pieces_LIST, pos2, element.color, promote_to[1]) #!! piece type as Q, R, N, B Ex: b3=Q+
            else:
                return x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: a3


    elif element.type == "Knight":
        if (abs(pos2[0]-pos1[0]) == 1 and abs(pos2[1]-pos1[1]) == 2) or (abs(pos2[1]-pos1[1]) == 1 and abs(pos2[0]-pos1[0]) == 2): # L Movement -> delta x = 1 and delta y=2 and vice-versa   --- abs() -> absolute value

            if what_piece_in_which_cell(pieces_LIST, pos2) == None: #If the destination square is empty
                return 'N' + x_to_letter(pos1[0]) + str(pos1[1]+1) + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Ng1h3

            else: # If it's eating somebody
                return 'N' + x_to_letter(pos1[0]) + str(pos1[1]+1) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Ng1xh3
    
    elif element.type == "Rook":
        if (pos1[0] == pos2[0]) or (pos1[1] == pos1[1]): #if the row or the line is the same
            
            if what_piece_in_which_cell(pieces_LIST, pos2) == None: #If the destination square is empty
                return 'R' + x_to_letter(pos1[0]) + str(pos1[1]+1) + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Ra1a3
            
            else: # If it's eating somebody
                return 'R' + x_to_letter(pos1[0]) + str(pos1[1]+1) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Ra1xa3
        
    elif element.type == "Bishop":
        if (abs(pos2[0] - pos1[0]) == abs(pos2[1] - pos1[1])): #If delta x is the same as delta y

            if what_piece_in_which_cell(pieces_LIST, pos2) == None: #If the destination square is empty
                return 'B' + x_to_letter(pos1[0]) + str(pos1[1]+1) + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Bc1d2

            else: # If it's eating somebody
                return 'B' + x_to_letter(pos1[0]) + str(pos1[1]+1) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Rc1xe3

    elif element.type == "Queen":
        if (abs(pos2[0] - pos1[0]) == abs(pos2[1] - pos1[1])) or (pos1[0] == pos2[0]) or (pos1[1] == pos1[1]): #If delta x is the same as delta y or if it moves in the same row or column

            if what_piece_in_which_cell(pieces_LIST, pos2) == None: #If the destination square is empty
                return 'Q' + x_to_letter(pos1[0]) + str(pos1[1]+1) + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Qd4d6

            else: # If it's eating somebody
                return 'Q' + x_to_letter(pos1[0]) + str(pos1[1]+1) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) + check_check(pieces_LIST, pos2, element.color, element.type) #Ex: Qd4xe5
    
    elif element.type == "King":

        #King moving
        if (abs(pos2[0]-pos1[0]) == 1 or abs(pos2[1]-pos1[1]) == 1) and what_piece_in_which_cell(pieces_LIST, pos2) == None: #If delta x or delta y is 1
            # return 'K' + x_to_letter(pos2[0]) + str(pos2[1]+1) #Ex: Kd2 I thought he did it like that
            return 'K' + x_to_letter(pos1[0]) + str(pos1[1]+1) + x_to_letter(pos2[0]) + str(pos2[1]+1) #Ex: Ke1e2

        #King capturing
        elif (abs(pos2[0]-pos1[0]) == 1 or abs(pos2[1]-pos1[1]) == 1) and what_piece_in_which_cell(pieces_LIST, pos2) != None:
            return 'K' + x_to_letter(pos1[0]) + str(pos1[1]+1) + 'x' + x_to_letter(pos2[0]) + str(pos2[1]+1) #Ex: Kd1xd2
        
        #Small Castling -> right
        elif (pos2[0]-pos1[0] == +2) and what_piece_in_which_cell(pieces_LIST, (pos1[0]+1, pos1[1])) == None and what_piece_in_which_cell(pieces_LIST, pos2) == None: #if the king wants to move two cells right and there's no pieces in between

            if what_piece_in_which_cell(pieces_LIST, (pos2[0]+1, pos2[1])) != None and what_piece_in_which_cell(pieces_LIST, (pos2[0]+1, pos2[1])).type == 'Rook': #checks if there's a rook -> wrote it like that so it doesn't return an error
                return 'O-O'
        
        #Big Castling -> left
        elif (pos2[0]-pos1[0] == -2) and what_piece_in_which_cell(pieces_LIST, (pos1[0]-1, pos1[1])) == None and what_piece_in_which_cell(pieces_LIST, pos2) == None: #if the king wants to move two cells left and there's no pieces in between + checks if there's a rook

            if what_piece_in_which_cell(pieces_LIST, (pos2[0]-2, pos2[1])) != None and what_piece_in_which_cell(pieces_LIST, (pos2[0]-2, pos2[1])).type == 'Rook': #checks if there's a rook -> wrote it like that so it doesn't return an error
                return 'O-O-O'

def bitify(chessboard_alexis) -> list[int]:
    """
    Transforms a normal chessboard into a bitboard. Each entry is a different type of piece and has 8 bytes (64 bits). Every bit is a chessboard square. If the square has a white pawn, for example, it will be 1, and 0 if not.
    The bitboard entries are organized like this: White Pawn ; White Knight ; White Bishop ; White Rook ; White Queen ; White King ; Black Pawn...
    """
    
    #Bitboard -> White Pawn ; White Knight ; White Bishop ; White Rook ; White Queen ; White King ; Black Pawn...
    bitboard = [0b0 for i in range(12)] # For the 6 types of pieces x2 for both colors
    
    bit_index = 0

    for line in chessboard_alexis:
        for piece in line:
            if piece != '.':
                match piece.type:
                    case "P":
                        if piece.Blanc:
                            bitboard[0] = bitboard[0] | (1 << bit_index) # Adding a 1 at the specific bit index -- [0] is for white pawn
                        else:
                            bitboard[6] = bitboard[6] | (1 << bit_index) # Adding a 1 at the specific bit index -- [6] is for black pawn

                    case "N":
                        if piece.Blanc:
                            bitboard[1] = bitboard[1] | (1 << bit_index) 
                        else:
                            bitboard[7] = bitboard[7] | (1 << bit_index)
                    
                    case "B":
                        if piece.Blanc:
                            bitboard[2] = bitboard[2] | (1 << bit_index) 
                        else:
                            bitboard[8] = bitboard[8] | (1 << bit_index) 
                    
                    case "R":
                        if piece.Blanc:
                            bitboard[3] = bitboard[3] | (1 << bit_index) 
                        else:
                            bitboard[9] = bitboard[9] | (1 << bit_index) 

                    case "Q":
                        if piece.Blanc:
                            bitboard[4] = bitboard[4] | (1 << bit_index) 
                        else:
                            bitboard[10] = bitboard[10] | (1 << bit_index) 
                    
                    case "K":
                        if piece.Blanc:
                            bitboard[5] = bitboard[5] | (1 << bit_index) 
                        else:
                            bitboard[11] = bitboard[11] | (1 << bit_index)
                
            bit_index += 1
    return bitboard

def convert_bot_to_coords(pieces_before, pieces_after, turn:bool, mv:str) -> list[tuple[int, int]]:
    """
    Will output relative coords when the robot played.
    The first coordinates will be the previous position of the piece that moved; the second will be where the piece has moved.
    To do this, it will take Alexis' chessboard before the move, and after the move. It will then figure out the difference.
    """
    # Exceptions - castling
    if mv == 'O-O':
        if turn:
            return [(4, 0), (6, 0)] # White small castling
        else:
            return [(4, 7), (6, 7)] # Black small castling
    elif mv == 'O-O-O':
        if turn:
            return [(4, 0), (2, 0)] # White big castling
        else:
            return [(4, 7), (2, 7)] # Black big castling


    range_turn = 0 if turn else 6 # Will be added to the range to only look at the robot's color

    for i in range(range_turn, int(len(pieces_before)/2) + range_turn):
        if (pieces_before[i] ^ pieces_after[i]) != 0:
            bit_piece = (pieces_before[i] ^ pieces_after[i]) & pieces_before[i] #To know what piece moved on the chessboard (XOR for finding the differences, and AND for taking off the position after)
            piece_pos, piece_new_pos = [0, 0], [0, 0]

            for bit in range(64):
                if bit_piece & (1 << bit):
                    piece_pos[1] = bit // 8 #byte, entire division
                    piece_pos[0] = bit % 8 #bit, rest of entire division
                    break
            
            bit_new_piece = (pieces_before[i] ^ pieces_after[i]) & pieces_after[i] #To know what piece moved on the chessboard (XOR for finding the differences, and AND for taking off the position after)

            for bit in range(64):
                if bit_new_piece & (1 << bit):
                    piece_new_pos[1] = bit // 8 #byte, entire division
                    piece_new_pos[0] = bit % 8 #bit, rest of entire division
                    break
            
            if '=' in mv: # If pawn promotion, then it will do the loop again to search for the difference in the other pieces, ex:Q
                for j in range(range_turn+1, int(len(pieces_before)/2) + range_turn):
                    if (pieces_before[j] ^ pieces_after[j]) != 0:

                        bit_new_piece1 = (pieces_before[j] ^ pieces_after[j]) & pieces_after[j] #To know what piece moved on the chessboard (XOR for finding the differences, and AND for taking off the position after)

                        for bit in range(64):
                            if bit_new_piece1 & (1 << bit):
                                piece_new_pos[1] = bit // 8 #byte, entire division
                                piece_new_pos[0] = bit % 8 #bit, rest of entire division
                                break

            return [(piece_pos[0], piece_pos[1]), (piece_new_pos[0], piece_new_pos[1])] #Sending out tuples

    return None
