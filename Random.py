buttons[row][col].config(text=currentplayer)
    winner=check_winner()
    if winner=="Tie":
        messagebox.showinfo("Game Over", "It's a tie!")
    elif winner:
        messagebox.showinfo("Game Over", f"Player {winner} wins")
        reset_board()
    else:
        currentplayer="O" if currentplayer=="X" else "X"
        status_label.config(text=f"Player {currentplayer}'s turn")

status_label=tk.Label(root, text=f"Player {currentplayer}'s turn")
status_label.grid(row=0,column=0,columnspan=3,pady=10)
for r in range(3):
    for c in range(3):
        btn=tk.Button(
            root,
            text="",
            font=("Arial",24),
            width=5,
            height=2,
            command=lambda  row=r, col=c: on_click(row,col)
        )
        btn.grid(row=r+1,column=c)
        buttons[r][c]=btn
reset_btn=tk.Button(root, text="Restart",font=("Arial",12),command=reset_board)
reset_btn.grid(row=4,column=0,columnspan=3,pady=10)
root.mainloop()

def check_row():
    for r in range(BOARD_SIZE):
        x=0
        y=0
        for c in range(BOARD_SIZE):
            if board[r][c]=="X":
                x=x+1
            if board[r][c]=="O":
                y=y+1
        if x==BOARD_SIZE:
            return "X"
        if y==BOARD_SIZE:
            return "O"
    return None
def check_column():
    for c in range(BOARD_SIZE):
        x=0
        y=0
        for r in range(BOARD_SIZE):
            if board[r][c]=="X":
                x=x+1
            if board[r][c]=="O":
                y=y+1
        if x==BOARD_SIZE:
            return "X"
        if y==BOARD_SIZE:
            return "O"
    return None
def checkright_diagonal():
    x=0
    y=0
    for i in range(BOARD_SIZE):
        if board[i][i]=="X":
            x=x+1
        if board[i][i]=="O":
            y=y+1
    if x==BOARD_SIZE:
        return "X"
    if y==BOARD_SIZE:
        return "O"
    return None
def checkleft_diagonal():
    x=0
    y=0
    for i in range(BOARD_SIZE):
        if board[i][BOARD_SIZE-1-i]=="X":
            x=x+1
        if board[i][BOARD_SIZE-1-i]=="O":
            y=y+1
    if x==BOARD_SIZE:
        return "X"
    if y==BOARD_SIZE:
        return "O"
    return None


