import tkinter as tk    #Imported Library for GUI
from tkinter import messagebox
import random   #Imported library to generate random variable
import json     #Imported library to save data after a session
import os
import pygame
SAVE_FILE="save_data.json"
DIFFICULTY_REWARDS={    #Reward for defeating a specific difficulty
    "Easy":50,
    "Medium":150,
    "Impossible":300
}#Reward for playing against AI
CHARACTERS={    #All characters you can get
    "default":{
        "name":"Tung Tung Sahur",
        "x_file":"x_image.png",
        "o_file":"o_image.png",
        "cost":0
    },
    "ballerina":{
        "name":"Ballerina Cappuccina",
        "x_file":"ballerina.jpg",
        "o_file":"ballerina.jpg",
        "cost": 500
    },
    "patapim":{
        "name":"Brr Brr Patapim",
        "x_file":"patapim.jpg",
        "o_file":"patapim.jpg",
        "cost":1000
    },
    "bombardino":{
        "name":"Bombardino Crocodillo",
        "x_file":"bombardino.webp",
        "o_file":"bombardino.webp",
        "cost":1500
    },
    "lirili":{
        "name":"Lirili Larila",
        "x_file":"lirili.webp",
        "o_file":"lirili.webp",
        "cost": 2000
    },
    "trippi":{
        "name":"Trippi Troppi",
        "x_file":"trippi.webp",
        "o_file":"trippi.webp",
        "cost":2500
    },
    "tatatasahur":{
        "name":"Ta Ta Ta Sahur",
        "x_file":"tatatasahur.webp",
        "o_file":"tatatasahur.webp",
        "cost":3000
    },
    "trulimero":{
        "name":"Trulimero Trulichina",
        "x_file":"trulimero.jpg",
        "o_file":"trulimero.jpg",
        "cost":3500
    },
    "chimpanzinibananini":{
        "name":"Chimpanzini Bananini",
        "x_file":"chimpanzini bananini.jpg",
        "o_file":"chimpanzini bananini.jpg",
        "cost":4000
    }
}#All characters you can unlock
#Mechanism to save coins after every session.
def load_save_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE,"r") as f:
            data=json.load(f)
    else:
        data={"coins":0,"unlocked":["default"],"selected":"default"}
    data.setdefault("stats",{"played":0,"won":0,"lost":0,"tied":0})
    data.setdefault("unlocked_themes",["default"])
    data.setdefault("selected_theme","default")
    return data
def write_save_data():
    with open(SAVE_FILE,"w") as f:
        json.dump(save_data,f)
save_data=load_save_data()
selected_character=save_data.get("selected","default")

PLAYER_NAMES={  #Default playable characters
    "X": "TUNG TUNG TUNG SAHUR",
    "O": "CAPPUCCINO ASSASSINO"
     }
BOARD_THEMES={
    "default":{
        "name":"Midnight Purple",
        "board_bg":"#12002f",
        "cell_bg":"#ffa3ff",
        "border":"#3a1a5c",
        "cost":0
    },
    "crimson":{
        "name":"Crimson Night",
        "board_bg":"#2a0000",
        "cell_bg":"#ffe0e0",
        "border":"#7a1a1a",
        "cost":600
    },
    "emerald":{
        "name":"Emerald Depths",
        "board_bg":"#00230f",
        "cell_bg":"#50c878",
        "border":"#1a5c33",
        "cost":1000
    },
    "ocean":{
        "name":"Ocean Blue",
        "board_bg":"#001a33",
        "cell_bg":"#0077be",
        "border":"#1a3f5c",
        "cost":1500
    },
    "gold":{
        "name":"Golden Hour",
        "board_bg":"#ffd700",
        "cell_bg":"#ffd300",
        "border":"#8a6a1a",
        "cost":2000
    },
}
currentplayer="X"   #Variable used for comparisons
Human="X"
AI="O"      #Variable used for AI moves
board=[["" for i in range(3)]for j in range(3)]         #FOR COMPARING CONDITIONS
buttons=[[None for i in range(3)]for j in range(3)]     #FOR GUI BUTTONS
game_mode=None  #PVP OR P VS B
difficulty="Impossible"   #EASY/MEDIUM/Impossible
games_played=0
games_won=0
games_lost=0
games_tied=0
FRAME_LIST=[]
BOARD_SIZE=3

def hide_all_frames():
    for f in FRAME_LIST:
        f.pack_forget()

def build_board_grid():
    global buttons,board
    for widget in board_frame.winfo_children():
        widget.destroy()        #Clear old 3x3 or 4x4 buttons
    board=[["" for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
    buttons=[[None for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    cell_size=get_cell_size()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            btn=tk.Button(board_frame,image=blank_image,width=cell_size,height=cell_size,highlightthickness=0,command=lambda row=r,col=c: on_click(row,col))
            btn.grid(row=r,column=c,sticky="nsew")
            buttons[r][c]=btn
    for i in range(BOARD_SIZE):
        board_frame.grid_columnconfigure(i,minsize=cell_size)
        board_frame.grid_rowconfigure(i,minsize=cell_size)
def get_cell_size():
    return 90 if BOARD_SIZE==3 else 65
def reload_images():
    global blank_image,x_image,o_image,DISPLAY_IMAGE
    size=(get_cell_size(),get_cell_size())
    blank_image_pil=Image.new("RGBA",size,(0,0,0,0))
    blank_image=ImageTk.PhotoImage(blank_img)
    char=CHARACTERS[selected_character]
    x_image=load_Image(char["x_file"],size=size)
    o_image=load_Image(char["o_file"],size=size)
    DISPLAY_IMAGE["X"]=x_image
    DISPLAY_IMAGE["O"]=o_image
    DISPLAY_IMAGE[""]=blank_image

def get_current_theme():
    return BOARD_THEMES[save_data.get("selected_theme","default")]
def apply_board_theme():
    theme=get_current_theme()
    board_frame.config(bg=theme["board_bg"])
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if buttons[r][c]:
                buttons[r][c].config(bg=theme["cell_bg"],activebackground=theme["cell_bg"])
    if mini_frames:                      #<- now runs once, after the board loop finishes
        for br in range(3):
            for bc in range(3):
                mini_frames[br][bc].config(bg=theme["board_bg"])
                for r in range(3):
                    for c in range(3):
                        ultimate_buttons[br][bc][r][c].config(bg=theme["cell_bg"],activebackground=theme["cell_bg"])


#Subroutine which checks for winner conditions after every move
def check_winner():
    WIN_LENGTH=3

    #Horizontal Check
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE-WIN_LENGTH+1):
            cells=[board[r][c+i] for i in range(WIN_LENGTH)]
            if cells==["X"]*WIN_LENGTH:
                return "X"
            if cells==["O"]*WIN_LENGTH:
                return "O"

    #Vertical Check
    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE-WIN_LENGTH+1):
            cells=[board[r+i][c] for i in range(WIN_LENGTH)]
            if cells==["X"]*WIN_LENGTH:
                return "X"
            if cells==["O"]*WIN_LENGTH:
                return "O"

    #Right Diagonal Check
    for r in range(BOARD_SIZE-WIN_LENGTH+1):
        for c in range(BOARD_SIZE-WIN_LENGTH+1):
            cells=[board[r+i][c+i] for i in range(WIN_LENGTH)]
            if cells==["X"]*WIN_LENGTH:
                return "X"
            if cells==["O"]*WIN_LENGTH:
                return "O"
    #Left Diagonal Check
    for r in range(BOARD_SIZE-WIN_LENGTH+1):
        for c in range(WIN_LENGTH-1,BOARD_SIZE):
            cells=[board[r+i][c-i] for i in range(WIN_LENGTH)]
            if cells==["X"]*WIN_LENGTH:
                return "X"
            if cells==["O"]*WIN_LENGTH:
                return "O"
    #Tie Check
    if all(board[r][c]!= "" for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return "Tie"
    return None
#Subroutine which returns empty cells after every move
def get_empty_cells():
    return[(r,c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c]==""]
#Places users character on the board
def make_move(row,col,player):
    board[row][col]=player
    buttons[row][col].config(image=DISPLAY_IMAGE[player])
    play_sound(place_sound)



#Subroutine which checks who has won the game and shows corresponding message
def handle_game_over(winner):
    if winner=="Tie":
        add_games_played()
        add_games_tied()
        if game_mode=="PVB" and difficulty=="Impossible":
            reward=20
            save_data["coins"]+=reward
            write_save_data()
            show_win_screen("IT'S A TIE!",confetti=False,coins_earned=reward)
        else:
            write_save_data()
            show_win_screen("IT'S A TIE!", confetti=False)
    elif game_mode=="PVB":
        who="You" if winner==Human else "The bot"
        add_games_played()
        if winner==Human:
            add_games_won()
            reward=DIFFICULTY_REWARDS.get(difficulty,0)
            save_data["coins"]+=reward
            write_save_data()
            message=f"{who} win{'s' if winner==AI else ''}!\n({PLAYER_NAMES[winner]})"
            show_win_screen(message,winner_image=DISPLAY_IMAGE[winner],coins_earned=reward)
            play_sound(win_sound)
        else:
            add_games_lost()
            write_save_data()
            message=f"{who} win{'s' if winner==AI else ''}!\n({PLAYER_NAMES[winner]})"
            show_win_screen(message,winner_image=DISPLAY_IMAGE[winner])
            play_sound(lose_sound)
    else:
        show_win_screen(f"{PLAYER_NAMES[winner]}\nWINS!",winner_image=DISPLAY_IMAGE[winner])
#For PVB bot ,to skip human turn when its bot's turn
def on_click(row,col):
    global currentplayer
    if board[row][col]!="":
        return #cell occupied
    if game_mode=="PVB" and currentplayer!=Human:
        return #not human turn so skip
    make_move(row,col,currentplayer)
    winner=check_winner()
    if winner:
        handle_game_over(winner)
        return
    if game_mode=="PVP":
        currentplayer="O" if currentplayer=="X" else "X"
        status_label.config(text=f"{PLAYER_NAMES[currentplayer]}'s turn")
    else:   #PVB
        currentplayer=AI
        status_label.config(text="Bot is thinking...")
        root.after(400,ai_move)

#----AI LOGIC----#
MEDIUM_SEARCH_DEPTH=2
IMPOSSIBLE_SEARCH_DEPTH=4

def get_max_search_depth():
    if BOARD_SIZE<=3:
        return None
    return MEDIUM_SEARCH_DEPTH if difficulty=="Medium" else IMPOSSIBLE_SEARCH_DEPTH
#Tries every possible path but chooses best outcome
def best_ai_move():
    best_score=-float("inf")
    best_move=None
    alpha=-float("inf")
    beta=float("inf")
    max_depth=get_max_search_depth()
    for r , c in get_empty_cells():
        board[r][c]=AI
        score=minmax(0,False,alpha, beta,max_depth)
        board[r][c]=""
        if score>best_score:
            best_score=score
            best_move=(r,c)
        alpha=max(alpha,best_score)
    return best_move
#Ai tries to maximize its score against human
def minmax(depth,is_maximizing,alpha=-float("inf"),beta=float("inf"),max_depth=None):
    result=check_winner()
    if result==AI:
        return 1000-depth
    elif result==Human:
        return depth-1000
    elif result=="Tie":
        return 0
    if max_depth is not None and depth>=max_depth:
        return evaluate_board()
    if is_maximizing:
        best_score=-float("inf")
        for r,c in get_empty_cells():
            board[r][c]=AI
            score=minmax(depth+1,False,alpha, beta,max_depth)
            board[r][c]=""
            best_score=max(score,best_score)
            alpha=max(alpha,best_score)
            if beta<=alpha:
                break
        return best_score
    else:
        best_score=float("inf")
        for r , c in get_empty_cells():
            board[r][c]=Human
            score=minmax(depth+1,True,alpha,beta,max_depth)
            board[r][c]=""
            best_score=min(score,best_score)
            beta=min(beta,best_score)
            if beta<=alpha:
                break
        return best_score
def get_all_lines():
    WIN_LENGTH=3
    lines=[]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE-WIN_LENGTH+1):
            lines.append([board[r][c+i] for i in range(WIN_LENGTH)])
    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE-WIN_LENGTH+1):
            lines.append([board[r+i][c] for i in range(WIN_LENGTH)])
    for r in range(BOARD_SIZE-WIN_LENGTH+1):
        for c in range(BOARD_SIZE-WIN_LENGTH+1):
            lines.append([board[r+i][c+i] for i in range(WIN_LENGTH)])
    for r in range(BOARD_SIZE-WIN_LENGTH+1):
        for c in range(WIN_LENGTH-1,BOARD_SIZE):
            lines.append([board[r+i][c-i] for i in range(WIN_LENGTH)])
    return lines
def evaluate_board():
    score=0
    for line in get_all_lines():
        ai_count=line.count(AI)
        human_count=line.count(Human)
        if ai_count and human_count:
            continue
        if ai_count:
            score+=10**ai_count
        elif human_count:
            score-=10**human_count
    return score



#Makes AI move according to its difficulty set
def ai_move():
    global currentplayer
    empty=get_empty_cells()
    move=None
    if difficulty=="Easy":
        move=random.choice(empty)
    elif difficulty=="Medium":
        move=best_ai_move() if random.random()<0.6 else random.choice(empty)
    else:
        move=best_ai_move()
    if move:
        make_move(move[0],move[1],AI)
    winner=check_winner()
    if winner:
        handle_game_over(winner)
        return
    currentplayer=Human
    status_label.config(text=f"{PLAYER_NAMES[currentplayer]}'s turn")

#-----General------#
#Subroutine to reset board after every game
def reset_board():
            global board,currentplayer
            board=[["" for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
            currentplayer="X"
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    buttons[r][c].config(image=blank_image)
            if game_mode=="PVB":
                status_label.config(text=f"Your turn ({PLAYER_NAMES[Human]})")
            else:
                status_label.config(text=f"{PLAYER_NAMES['X']}'s turn")
#Subroutine which helps with initial startup of game
def start_game(mode,chosen_difficulty=None):
    global game_mode,difficulty
    game_mode=mode
    if chosen_difficulty:
        difficulty=chosen_difficulty
    reload_images()
    build_board_grid()
    apply_board_theme()
    if mode=="PVB":
        bot_choices=[key for key in CHARACTERS if key!=selected_character]
        bot_character=random.choice(bot_choices)
        PLAYER_NAMES["O"]=CHARACTERS[bot_character]["name"]
        bot_image=load_Image(CHARACTERS[bot_character]["o_file"],size=(get_cell_size(),get_cell_size()))
        DISPLAY_IMAGE["O"]=bot_image
    else:
        PLAYER_NAMES["O"]="CAPPUCINO ASSASSINO"
        o_default_image=load_Image(CHARACTERS["default"]["o_file"],size=(get_cell_size(),get_cell_size()))
        DISPLAY_IMAGE["O"]=o_default_image
    menu_frame.pack_forget()
    difficulty_frame.pack_forget()
    game_frame.pack(pady=10,expand=True)
    mode_label.config(text="Human vs Human" if mode=="PVP" else f"Human vs Bot({difficulty})")
    reset_board()

#Resets attributes before start of a game.
def back_to_menu():
    game_frame.pack_forget()
    difficulty_frame.pack_forget()
    coins_label.config(text=f"Coins: {save_data['coins']}")
    menu_frame.pack(pady=20,expand=True)
#Displays AI difficulty screen
def show_difficulty_menu():
    hide_all_frames()
    difficulty_frame.pack(pady=20,expand=True)
    menu_frame.pack_forget()
#Displays options menu
def show_options_menu():
    hide_all_frames()
    options_frame.pack(pady=20,expand=True)
    menu_frame.pack_forget()
#Displays screen when user comes back from options
def back_from_options():
    options_frame.pack_forget()
    coins_label.config(text=f"Coins: {save_data['coins']}")
    menu_frame.pack(pady=20,expand=True)
#Play winscreen once the game ends
def show_win_screen(message,confetti=True,winner_image=None,coins_earned=None):
    overlay_canvas.place(x=0,y=0,relwidth=1,relheight=1)
    root.update_idletasks()
    overlay_canvas.tk.call("raise",overlay_canvas._w)
    overlay_canvas.delete("text")
    overlay_canvas.delete("confetti")
    overlay_canvas.update_idletasks()
    cx=overlay_canvas.winfo_width()//2
    cy=overlay_canvas.winfo_height()//2
    text_y=cy-40
    if winner_image:
        overlay_canvas.create_image(cx,cy-140,image=winner_image,tags="text")
        text_y=cy-20
    overlay_canvas.create_text(
        cx,text_y,text=message,fill="#FF0000",font=("Arial",20,"bold"),justify="center",width=650,tags="text")
    button_y=text_y+120
    if coins_earned:
        overlay_canvas.create_text(cx,text_y+60,text=f"🪙 +{coins_earned} coins!",fill="#ffe600",font=("Arial",22,"bold"),justify="center",tags="text")
        button_y=text_y+130
    play_again_btn=tk.Button(
    overlay_canvas,text="Play Again",font=("Arial",16,"bold"),bg="#e806cb",fg="white",command=hide_win_screen
    )
    overlay_canvas.create_window(cx,button_y,window=play_again_btn,tags="text")
    if confetti:
        spawn_confetti()
        animate_confetti()
    overlay_canvas.tag_raise("text")
#Hides winscreen once the user restarts or clicks menu
def hide_win_screen():
    global confetti_job
    if confetti_job:
        root.after_cancel(confetti_job)
        confetti_job=None
    overlay_canvas.delete("confetti")
    overlay_canvas.place_forget()
    reset_board()

#--------Game Data-------#

def add_games_played():
    save_data["stats"]["played"]+=1
def add_games_won():
    save_data["stats"]["won"]+=1
def add_games_lost():
    save_data["stats"]["lost"]+=1
def add_games_tied():
    save_data["stats"]["tied"]+=1
def win_rate():
    played=save_data["stats"]["played"]
    if played==0:
        return 0
    return (save_data["stats"]["won"]/played)*100





#------ULTIMATE TIC TAC TOE MODE------#
ultimate_cell_size=40   #px per cell inside a mini board
ultimate_board=None     #3x3 grid of 3x3 grids:The ultimate board
macro_board=None        #3x3 grid:Stores status of each mini board
ultimate_buttons=None   #matching structure for GUI
mini_frames=None        #3x3 grid of the mini-board container frames
active_boards=None      #Coordinate of miniboard selected by user
ultimate_currentplayer="X"

def new_mini_board():
    return[["" for _ in range(3)]for _ in range(3)]
def reset_ultimate_state():
    global ultimate_board,macro_board,active_boards,ultimate_currentplayer
    ultimate_board=[[new_mini_board() for _ in range(3)]for _ in range(3)]
    macro_board=[["" for _ in range(3)] for _ in range(3)]
    active_boards=None
    ultimate_currentplayer="X"

def check_mini_winner(cells):
    lines=[]
    for i in range(3):
        lines.append([cells[i][0],cells[i][1],cells[i][2]])    #rows
        lines.append([cells[0][i],cells[1][i],cells[2][i]])
    lines.append([cells[0][0],cells[1][1],cells[2][2]])
    lines.append([cells[0][2],cells[1][1],cells[2][0]])
    for line in lines:
        if line==["X","X","X"]:
                return "X"
        if line==["O","O","O"]:
                return "O"
    if all(cells[r][c]!="" for r in range(3) for c in range(3)):
        return "Tie"
    return None

#Checks the 3x3 macro board
def check_macro_winner():
    lines=[]
    for i in range(3):
        lines.append([macro_board[i][0],macro_board[i][1],macro_board[i][2]])
        lines.append([macro_board[0][i],macro_board[1][i],macro_board[2][i]])
    lines.append([macro_board[0][0],macro_board[1][1],macro_board[2][2]])
    lines.append([macro_board[0][2],macro_board[1][1],macro_board[2][0]])
    for line in lines:
        if line==["X","X","X"]:
            return "X"
        if line==["O","O","O"]:
            return "O"
    if all(macro_board[r][c]!="" for r in range(3) for c in range(3)):
        return "Tie"
    return None

def build_ultimate_grid():
    global ultimate_buttons,mini_frames
    for widget in ultimate_board_frame.winfo_children():
        widget.destroy()
    ultimate_buttons=[[[[None]*3 for _ in range(3)] for _ in range(3)]for _ in range(3)]
    mini_frames=[[None for _ in range(3)]for _ in range(3)]
    for br in range(3):
        for bc in range(3):
            mini=tk.Frame(ultimate_board_frame,bg="#12002f",highlightthickness=3,highlightbackground="#3a1a5c")
            mini.grid(row=br,column=bc,padx=3,pady=3)
            mini_frames[br][bc]=mini
            for r in range(3):
                for c in range(3):
                    btn=tk.Button(mini,image=blank_image,width=ultimate_cell_size,height=ultimate_cell_size,highlightthickness=0,command=lambda br=br,bc=bc,r=r,c=c: on_ultimate_click(br,bc,r,c))
                    btn.grid(row=r,column=c,sticky="nsew")
                    ultimate_buttons[br][bc][r][c]=btn

#Border color on each mini board shows who won it
def refresh_mini_highlights():
    for br in range(3):
        for bc in range(3):
            status=macro_board[br][bc]
            frame=mini_frames[br][bc]
            if status=="X":
                frame.config(highlightbackground="#00b300")
            elif status=="O":
                frame.config(highlightbackground="#ff5252")
            elif status=="Tie":
                frame.config(highlightbackground="#555555")
            elif active_boards is None or active_boards==(br,bc):
                frame.config(highlightbackground="#ffe600")
            else:
                frame.config(highlightbackground="#3a1a5c")

def on_ultimate_click(br,bc,r,c):
    global active_boards,ultimate_currentplayer
    if active_boards is not None and active_boards!=(br,bc):
        return #not the mini board you are focused to play in
    if macro_board[br][bc]!="" or ultimate_board[br][bc][r][c]!="":
        return  #mini board already decided,or cell already taken
    ultimate_board[br][bc][r][c]=ultimate_currentplayer
    ultimate_buttons[br][bc][r][c].config(image=DISPLAY_IMAGE[ultimate_currentplayer])
    play_sound(place_sound)
    mini_result = check_mini_winner(ultimate_board[br][bc])
    if mini_result:
        if mini_result == "Tie":
            clear_mini_board(br, bc)
        else:
            macro_board[br][bc] = mini_result
            paint_mini_board(br, bc, mini_result)
    macro_result=check_macro_winner()
    if macro_result:
        handle_ultimate_game_over(macro_result)
        return
    #Wherever you clicked  (r,c) is the mini board your opponent must play in next
    #unless that mini board is already decided, in which case they are free to pick any open one
    next_board=(r,c)
    active_boards=next_board if macro_board[r][c]=="" else None
    refresh_mini_highlights()
    ultimate_currentplayer="O" if ultimate_currentplayer=="X" else "X"
    ultimate_status_label.config(text=f"{PLAYER_NAMES[ultimate_currentplayer]}'s turn"+("" if active_boards else " (any open board)"))

#Stamps a big mark across a mini board once it's won,so it reads clearly at a glance
def paint_mini_board(br,bc,winner):
    mini=mini_frames[br][bc]
    for widget in mini.winfo_children():
        widget.destroy()
    big_label=tk.Label(mini,image=ULTIMATE_BIG_IMAGE[winner],bg="#12002f")
    big_label.image=ULTIMATE_BIG_IMAGE[winner]
    big_label.grid(row=0,column=0)


def handle_ultimate_game_over(winner):
    add_games_played()
    if winner=="Tie":
        add_games_tied()
        write_save_data()
        show_win_screen("IT'S A TIE!",confetti=False)
        return
    if winner==Human:
        add_games_won()
    else:
            add_games_lost()
    write_save_data()
    message=f"{PLAYER_NAMES[winner]}\nWINS THE ULTIMATE BOARD!"
    show_win_screen(message,winner_image=DISPLAY_IMAGE[winner])
    play_sound(win_sound if winner==Human else lose_sound)

def reset_ultimate_board():
    reset_ultimate_state()
    build_ultimate_grid()
    refresh_mini_highlights()
    ultimate_status_label.config(text=f"{PLAYER_NAMES['X']}'s turn")

def start_ultimate_game():
    reload_images()
    reload_ultimate_images()
    PLAYER_NAMES["O"]="CAPPUCCINO ASSASSINO"
    DISPLAY_IMAGE["O"]=load_Image(CHARACTERS["default"]["o_file"],size=(get_cell_size(),get_cell_size()))
    menu_frame.pack_forget()
    ultimate_frame.pack(pady=10,expand=True)
    reset_ultimate_board()
    apply_board_theme()
def clear_mini_board(br,bc):
    ultimate_board[br][bc]=new_mini_board()
    for r in range(3):
        for c in range(3):
            ultimate_buttons[br][bc][r][c].config(image=ULTIMATE_DISPLAY_IMAGE[""])

def back_to_menu_from_ultimate():
    ultimate_frame.pack_forget()
    coins_label.config(text=f"Coins: {save_data['coins']}")
    menu_frame.pack(pady=20,expand=True)

ULTIMATE_DISPLAY_IMAGE={}
ULTIMATE_BIG_IMAGE={}

def reload_ultimate_images():
    global ULTIMATE_DISPLAY_IMAGE,ULTIMATE_BIG_IMAGE
    size=(ultimate_cell_size,ultimate_cell_size)
    blank_pil=Image.new("RGBA",size,(0,0,0,0))
    char=CHARACTERS[selected_character]
    ULTIMATE_DISPLAY_IMAGE["X"]=load_Image(char["x_file"],size=size)
    ULTIMATE_DISPLAY_IMAGE["O"]=load_Image(CHARACTERS["default"]["o_file"],size=size)
    ULTIMATE_DISPLAY_IMAGE[""]=ImageTk.PhotoImage(blank_pil)

    big_size=(ultimate_cell_size*3,ultimate_cell_size*3)
    ULTIMATE_BIG_IMAGE["X"]=load_Image(char["x_file"],size=big_size)
    ULTIMATE_BIG_IMAGE["O"]=load_Image(CHARACTERS["default"]["o_file"],size=big_size)   #<- this line specifically












#-----GUI setup-----
pygame.mixer.init()
click_sound=pygame.mixer.Sound("click.wav")
place_sound=pygame.mixer.Sound("place.wav")
buy_sound=pygame.mixer.Sound("buy.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
error_sound=pygame.mixer.Sound("error.wav")
place_sound.set_volume(1.0)
win_sound.set_volume(1.0)
lose_sound.set_volume(1.0)
buy_sound.set_volume(1.0)
error_sound.set_volume(1.0)
click_sound.set_volume(1.0)

def play_sound(sound):
    if sound_on and sound:
        sound.play()
def button_click(command):
    play_sound(click_sound)
    root.after(50,command)
root=tk.Tk()
root.geometry("700x700")
from PIL import Image,ImageTk
blank_img=Image.new("RGBA",(90,90),(0,0,0,0))
blank_image=ImageTk.PhotoImage(blank_img)
def load_Image(path,size=(90,90)):
    img=Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)
x_image=load_Image("x_image.png",size=(90,90))
o_image = load_Image("o_image.png",size=(90,90))
DISPLAY_IMAGE={
    "X":x_image,
    "O":o_image,
    "":blank_image
    }

root.title("Tic Tac Toe")
pygame.mixer.music.load("menu_music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)     #Loop forever



#-----Main Menu-----#
menu_frame =tk.Frame(root)
tk.Label(menu_frame, text="Tic Tac Toe" , font=("Arial",40,"bold"),bg="#12002F",fg="#F5F3FF").pack(pady=(0,15))
coins_label=tk.Label(menu_frame,text="",font=("Arial",16,"bold"),bg="#12002f",fg="#ffe600")
coins_label.pack(pady=(0,10))
tk.Button(menu_frame, text="Human vs Human", font=("Arial", 18,"bold"), width=25,bg="#e806cb",fg="#F5F3FF",activebackground="#ff822d",command=lambda: button_click(lambda :start_game("PVP"))).pack(pady=5)
tk.Button(menu_frame, text ="Human vs Bot", font=("Arial",18,"bold"),width=25,bg="#e806cb",fg="#F5F3FF",activebackground="#ff822d",command=lambda :button_click(show_difficulty_menu)).pack(pady=10)
tk.Button(menu_frame,text="Ultimate Mode",font=("Arial",18,"bold"),width=25,bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda:button_click(start_ultimate_game)).pack(pady=10)
tk.Button(menu_frame,text="Options",font=("Arial",18,"bold"),width=25,bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(show_options_menu)).pack(pady=10)
menu_frame.pack(pady=20)
root.configure(bg="#12002F")           # dark blue-gray background
menu_frame.configure(bg="#12002F")
tk.Button(menu_frame,text="Board Colors",font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(show_board_themes_menu)).pack(pady=4)
coins_label.config(text=f"Coins: {save_data['coins']}")
tk.Button(menu_frame,text="Statistics",font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(show_statistics_menu)).pack(pady=4)
board_size_btn=tk.Button(menu_frame,text="Board Size:3x3",font=("Arial",14,"bold"),bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(toggle_board_size))
board_size_btn.pack(pady=(0,10))
def toggle_board_size():
    global BOARD_SIZE
    BOARD_SIZE=4 if BOARD_SIZE==3 else 3
    board_size_btn.config(text=f"Board Size: {BOARD_SIZE}x{BOARD_SIZE}"
                          )
#-----Difficulty selection frame----#
difficulty_frame =tk.Frame(root,bg="#12002F")
tk.Label(difficulty_frame,text="Choose Difficulty", font=("Arial", 25, "bold"),bg="#12002F",fg="#F5F3FF").pack(pady=(0, 15))
tk.Button(difficulty_frame, text="Easy", font=("Arial",18,"bold"),width=15,bg="#e806cb",fg="#F5F3FF",activebackground="#ff822d",command=lambda: button_click(lambda :start_game("PVB", "Easy"))).pack(pady=4)
tk.Button(difficulty_frame,text="Medium", font=("Arial", 18,"bold"), width=15,bg="#e806cb",fg="#F5F3FF",activebackground="#ff822d",command=lambda: button_click(lambda :start_game("PVB", "Medium"))).pack(pady=4)
tk.Button(difficulty_frame,text="Impossible",font=("Arial",18,"bold"),width=15,bg="#e806cb",fg="#F5F3FF",activebackground="#ff822d",command=lambda : button_click(lambda :start_game("PVB","Impossible"))).pack(pady=4)
tk.Button(difficulty_frame,text="Back",font=("Arial",15,"bold"),bg="#e806cb",fg="#F5F3FF",activebackground="#ff822d",command=lambda :button_click(back_to_menu)).pack(pady=(15,0))

#------Options Menu----#

#------Characters Frame-----#
character_frame=tk.Frame(root,bg="#12002f")
#Shows character buying screen
def show_characters_menu():
    hide_all_frames()
    for widget in character_frame.winfo_children():
        widget.destroy()

    tk.Label(character_frame, text=f"Coins:{save_data['coins']}", font=("Arial", 16, "bold"), bg="#12002f",fg="white").grid(row=0, column=0, columnspan=3, pady=(0,10))
    tk.Label(character_frame,text="Choose Character",font=("Arial",22,"bold"),bg="#12002f",fg="#F5F3FF").grid(row=1, column=0, columnspan=3, pady=(0,15))

    row_num=2
    col_num=0

    for key,char in CHARACTERS.items():
        unlocked=key in save_data["unlocked"]
        is_selected=key==selected_character
        if is_selected:
            label_text=f"✓ {char['name']}"
            btn_color="#00b300"
        elif unlocked:
            label_text=char["name"]
            btn_color="#e806cb"
        else:
            label_text=f"🔒 {char['cost']} coins"
            btn_color="#555555"

        def make_command(k=key,u=unlocked):
            return lambda: select_character(k) if u else buy_or_select_character(k)

        cell=tk.Frame(character_frame,bg="#12002f")
        cell.grid(row=row_num,column=col_num,padx=10,pady=10)

        thumb=load_Image(char["x_file"],size=(100,100))
        thumb_label=tk.Label(cell,image=thumb,bg="#12002f")
        thumb_label.image=thumb
        thumb_label.pack()

        tk.Button(cell,text=label_text,font=("Arial",11,"bold"),width=16,bg=btn_color,fg="#f5f3ff",activebackground="#ff822d",command=make_command()).pack(pady=(4,0))

        col_num=col_num+1
        if col_num==3:
            col_num=0
            row_num=row_num+1

    row_num=row_num+1
    tk.Button(character_frame,text="Back",font=("Arial",15,"bold"),bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=back_from_characters).grid(row=row_num, column=0, columnspan=3, pady=(15,0))

    character_frame.pack(pady=20,expand=True)
    options_frame.pack_forget()
#Changes users selected character
def select_character(key):
    global selected_character,x_image,o_image,DISPLAY_IMAGE
    selected_character=key
    char=CHARACTERS[key]
    x_image=load_Image(char["x_file"],size=(90,90))
    o_image=load_Image(char["o_file"],size=(90,90))
    DISPLAY_IMAGE["X"]=x_image
    save_data["selected"]=key
    PLAYER_NAMES["X"]=CHARACTERS[key]["name"]
    write_save_data()
    show_characters_menu()
#Deals with purchasing of characters
def buy_or_select_character(key):
    char=CHARACTERS[key]
    if save_data["coins"]>=char["cost"]:
        save_data["coins"]-=char["cost"]
        play_sound(buy_sound)
        save_data["unlocked"].append(key)
        write_save_data()
        select_character(key)
    else:
        play_sound(error_sound)
        messagebox.showinfo("Not enough coins",f"You need {char['cost']} coins to unlock {char['name']}.")

def back_from_characters():
    character_frame.pack_forget()
    options_frame.pack(pady=20,expand=True)

theme_menu_frame=tk.Frame(root,bg="#12002f")
def show_board_themes_menu():
    hide_all_frames()
    for widget in theme_menu_frame.winfo_children():
        widget.destroy()

    tk.Label(theme_menu_frame,text=f"Coins:{save_data['coins']}",font=("Arial",16,"bold"),bg="#12002f",fg="white").grid(row=0,column=0,columnspan=2,pady=(0,10))
    tk.Label(theme_menu_frame,text="Choose Board Color",font=("Arial",22,"bold"),bg="#12002f",fg="#F5F3FF").grid(row=1,column=0,columnspan=2,pady=(0,15))

    row_num=2
    col_num=0
    for key,theme in BOARD_THEMES.items():
        unlocked=key in save_data["unlocked_themes"]
        is_selected=key==save_data["selected_theme"]
        if is_selected:
            label_text=f"✓ {theme['name']}"
            btn_color="#00b300"
        elif unlocked:
            label_text=theme["name"]
            btn_color=theme["board_bg"]
        else:
            label_text=f"🔒 {theme['name']} ({theme['cost']} coins)"
            btn_color="#555555"

        def make_command(k=key,u=unlocked):
            return lambda: select_board_theme(k) if u else buy_or_select_board_theme(k)

        tk.Button(theme_menu_frame,text=label_text,font=("Arial",13,"bold"),width=22,bg=btn_color,fg="#f5f3ff",activebackground="#ff822d",command=make_command()).grid(row=row_num,column=col_num,padx=10,pady=8)

        col_num+=1
        if col_num==2:
            col_num=0
            row_num+=1

    row_num+=1
    tk.Button(theme_menu_frame,text="Back",font=("Arial",15,"bold"),bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=back_from_board_themes).grid(row=row_num,column=0,columnspan=2,pady=(15,0))

    theme_menu_frame.pack(pady=20,expand=True)
    options_frame.pack_forget()

def select_board_theme(key):
    save_data["selected_theme"]=key
    write_save_data()
    apply_board_theme()          #recolors whatever board is currently built, if any
    show_board_themes_menu()     #refresh the checkmark

def buy_or_select_board_theme(key):
    theme=BOARD_THEMES[key]
    if save_data["coins"]>=theme["cost"]:
        save_data["coins"]-=theme["cost"]
        play_sound(buy_sound)
        save_data["unlocked_themes"].append(key)
        write_save_data()
        select_board_theme(key)
    else:
        play_sound(error_sound)
        messagebox.showinfo("Not enough coins",f"You need {theme['cost']} coins to unlock {theme['name']}.")

def back_from_board_themes():
    theme_menu_frame.pack_forget()
    options_frame.pack(pady=20,expand=True)













#------Settings Menu------#
music_on=True
sound_on=True
settings_frame=tk.Frame(root,bg="#12002f")
def update_settings_button():
    music_btn.config(text=f"Music: {'ON' if music_on else 'OFF'}")
    sound_btn.config(text=f"Sound Effects:{'ON' if sound_on else 'OFF'}")
def toggle_music():
    global music_on
    music_on=not music_on
    if music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    update_settings_button()
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    update_settings_button()
def show_settings_menu():
    hide_all_frames()
    options_frame.pack_forget()
    update_settings_button()
    settings_frame.pack(pady=20,expand=True)
def back_from_settings():
    settings_frame.pack_forget()
    menu_frame.pack_forget()
    options_frame.pack(pady=20,expand=True)
tk.Label(settings_frame,text="Settings",font=("Arial",24,"bold"),bg="#12002f",fg="#f5f3ff").pack(pady=(0,20))
music_btn=tk.Button(settings_frame,font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",command=lambda :button_click(toggle_music))
music_btn.pack(pady=5)
sound_btn=tk.Button(settings_frame,font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",command=lambda :button_click(toggle_sound))
sound_btn.pack(pady=5)
tk.Button(settings_frame,text="Back",font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",command=lambda :button_click(back_from_settings)).pack(pady=(20,0))



options_frame=tk.Frame(root,bg="#12002F")
tk.Button(options_frame,text="Settings",font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(show_settings_menu)).pack(pady=4)
tk.Button(options_frame,text="Characters",font=("Arial",18,"bold"),width=20,bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(show_characters_menu)).pack(pady=4)
tk.Button(options_frame,text="Back",font=("Arial",16,"bold"),bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=lambda :button_click(back_from_options)).pack(pady=(15,0))

#------Statistics Panel------#
def show_statistics_menu():
    stats_win=tk.Toplevel(root)
    stats_win.title("Statistics")
    stats_win.geometry("400x400")
    stats_win.configure(bg="#12002f")
    stats_win.resizable(False,False)
    tk.Label(stats_win,text="Statistics",font=("Arial",24,"bold"),bg="#12002f",fg="#f5f3ff").pack(pady=(20,20))
    stats=save_data["stats"]
    played_label=tk.Label(stats_win,text=f"Games Played: {stats['played']}",font=("Arial",16,"bold"),bg="#12002f",fg="#f5f3ff")
    played_label.pack(pady=3)
    won_label=tk.Label(stats_win,text=f"Games Won: {stats['won']}",font=("Arial",16,"bold"),bg="#12002f",fg="#00e676")
    won_label.pack(pady=3)
    lost_label=tk.Label(stats_win,text=f"Games Lost: {stats['lost']}",font=("Arial",16,"bold"),bg="#12002f",fg="#ff5252")
    lost_label.pack(pady=3)
    tied_label=tk.Label(stats_win,text=f"Games Tied: {stats['tied']}",font=("Arial",16,"bold"),bg="#12002f",fg="#ffe600")
    tied_label.pack(pady=3)
    tk.Label(stats_win,text=f"Win Rate: {win_rate():.1f}%",font=("Arial",18,"bold"),bg="#12002f",fg="#00e5ff").pack(pady=(10,3))
    def reset_and_close():
        if messagebox.askyesno("Reset Statistics","Are you sure you want to reset your statistics?"):
            save_data["stats"]={"played":0,"won":0,"lost":0,"tied":0}
            write_save_data()
            stats_win.destroy()
            show_statistics_menu()

    tk.Button(stats_win,text="Reset Stats",font=("Arial",14,"bold"),bg="#555555",fg="#f5f3ff",command=reset_and_close).pack(pady=(15,4))
    tk.Button(stats_win,text="Close",font=("Arial",16,"bold"),bg="#e806cb",fg="#f5f3ff",activebackground="#ff822d",command=stats_win.destroy).pack(pady=(4,10))







game_frame=tk.Frame(root,bg="#12002F",width=400,height=550)
game_frame.grid_propagate(False)
top_frame=tk.Frame(game_frame,bg="#12002f",width=270,height=100)
top_frame.grid(row=0,column=0,columnspan=3)
top_frame.grid_propagate(False)
mode_label=tk.Label(top_frame,text="",font=("Arial",18,"italic"),bg="#12002F",fg="#F5F3FF")
mode_label.pack()
status_label=tk.Label(top_frame,text="",font=("Arial",18),bg="#12002F",fg="#F5F3FF",wraplength=380)
status_label.pack(pady=10)

overlay_canvas=tk.Canvas(root,bg="#12002F",highlightthickness=0)
confetti_particles=[]
confetti_colors=["#e806cb","#ff822d","#00e5ff","#ffe600","#7cfc00"]
confetti_job=None
#Creates confetti particles when someone wins
def spawn_confetti():
    global confetti_job
    confetti_particles.clear()
    overlay_canvas.update_idletasks()
    canvas_width=overlay_canvas.winfo_width()
    for _ in range(54):
        x=random.randint(0,canvas_width)
        y=random.randint(-800,-20)
        size=random.randint(8,14)
        color=random.choice(confetti_colors)
        speed=random.uniform(2,6)
        piece=overlay_canvas.create_rectangle(x,y,x+size,y+size,fill=color,outline="",tags="confetti")
        confetti_particles.append({"id":piece,"speed":speed})
#Move confetti
def animate_confetti():
    global confetti_job
    if not overlay_canvas.winfo_ismapped():
        return
    for p in confetti_particles:
        overlay_canvas.move(p["id"],0,p["speed"])
        coords=overlay_canvas.coords(p["id"])
        if coords and coords[1]>600:
            overlay_canvas.move(p["id"],0,-600)
    confetti_job=root.after(30,animate_confetti)

board_frame=tk.Frame(game_frame,bg="#12002f")
board_frame.grid(row=1,column=0,columnspan=3)

for r in range(3):
    for c in range(3):
        btn=tk.Button(
            board_frame,
            image=blank_image,
            width=90,
            height=90,
            highlightthickness=0,
            command=lambda row=r,col=c: on_click(row,col)
        )
        btn.grid(row=r+2,column=c,sticky="nsew")
        buttons[r][c]=btn


#----Ultimate Frame-----#
ultimate_frame=tk.Frame(root,bg="#12002f")
ultimate_top=tk.Frame(ultimate_frame,bg="#12002f")
ultimate_top.pack(pady=(0,10))
tk.Label(ultimate_top,text="Ultimate Tic Tac Toe",font=("Arial",18,"bold"),bg="#12002f",fg="#f5f3ff").pack()
ultimate_status_label=tk.Label(ultimate_top,text="",font=("Arial",16),bg="#12002f",fg="#f5f3ff")
ultimate_status_label.pack(pady=6)
ultimate_board_frame=tk.Frame(ultimate_frame,bg="#12002f")
ultimate_board_frame.pack()
ultimate_button_row=tk.Frame(ultimate_frame,bg="#12002f")
ultimate_button_row.pack(pady=10)
tk.Button(ultimate_button_row,text="Restart",font=("Arial",18,"bold"),bg="#e806cb",fg="#f5f3ff",command=lambda :button_click(reset_ultimate_board)).pack(side="left",padx=5)
tk.Button(ultimate_button_row,text="Main Menu",font=("Arial",18,"bold"),bg="#e806cb",fg="#f5f3ff",command=lambda:button_click(back_to_menu_from_ultimate)).pack(side="left",padx=5)



FRAME_LIST[:]=[menu_frame,difficulty_frame,options_frame,character_frame,settings_frame,game_frame,ultimate_frame,theme_menu_frame]
button_row=tk.Frame(game_frame,bg="#12002F")
button_row.grid(row=2,column=0,columnspan=3,pady=10)
game_frame.grid_rowconfigure(0,minsize=100)
game_frame.grid_columnconfigure(0,minsize=133)
game_frame.grid_columnconfigure(1,minsize=133)
game_frame.grid_columnconfigure(2,minsize=133)
tk.Button(button_row,text="Restart",font=("Arial",18,"bold"),bg="#e806cb",fg="#F5F3FF",command=lambda :button_click(reset_board)).pack(side="left",padx=5)
tk.Button(button_row,text="Main Menu ",font=("Arial",18,"bold"),bg="#e806cb",fg="#F5F3FF", command=lambda :button_click(back_to_menu)).pack(side="left",padx=5)
root.mainloop()
