# 🎮 Tic-Tac-Toe

A feature-packed Tic-Tac-Toe game built from scratch in Python using Tkinter, with AI opponents, Ultimate Tic-Tac-Toe, unlockable characters, board themes, sounds, statistics, and persistent game data.

## 📖 Why I Built This

Well this project started as a joke.

While I was studying Python, my teacher gave us a challenge question as a joke because he thought we could not complete it: make a Tic-Tac-Toe game. I decided to take the challenge seriously and spent the next **6 hours building one from scratch**.

That first version made me realize how much could actually be done with a simple game. So this summer, I wanted to raise the stakes. Instead of making another basic Tic-Tac-Toe program, I decided to turn it into a proper playable game while learning how to build graphical user interfaces with Python.

What started as a classroom challenge eventually grew into a project with multiple game modes and many other fun additions to the game giving it an exciting new experience to the old boring 3x3 tic tac toe.

## ✨ Features

* 🧑‍🤝‍🧑 **Human vs Human** mode
* 🤖 **Human vs Bot** with 3 difficulty levels
* 🧠 AI using **Minimax with Alpha-Beta Pruning**
* 🎯 **3×3 and 4×4** standard boards
* 🏆 **Ultimate Tic-Tac-Toe** mode
* 🪙 Coin-based reward and progression system
* 🎭 **9 unlockable characters**
* 🎨 **5 unlockable board themes**
* 📊 Persistent game statistics
* 💾 Save data between sessions using JSON
* 🔊 Background music and sound effects
* ⚙️ Music and sound-effect controls
* 🎉 Animated victory screen with confetti
* 🔄 Restart and main-menu functionality

## 🎮 Game Modes

### Human vs Human

Play a traditional game of Tic-Tac-Toe against another player on the same computer.

The game supports both **3×3 and 4×4 boards**, with three matching symbols required to win.

### Human vs Bot

Play against an AI opponent with three difficulty levels:

| Difficulty | Behavior                                               |    Reward |
| ---------- | ------------------------------------------------------ | --------: |
| Easy       | Makes random moves                                     |  50 coins |
| Medium     | Uses strategic search but sometimes makes random moves | 150 coins |
| Impossible | Uses the strongest available search strategy           | 300 coins |

The AI uses **Minimax** to evaluate possible moves. Alpha-beta pruning is used to eliminate branches that do not need to be searched.

For the larger 4×4 board, the search depth is limited to keep the game responsive.

### 🏆 Ultimate Tic-Tac-Toe

Ultimate Tic-Tac-Toe expands the normal game into a **3×3 grid of nine smaller Tic-Tac-Toe boards**.

Winning a small board claims that section of the larger board. The location of your move determines which small board your opponent has to play in next.

This creates a much more strategic version of Tic-Tac-Toe where every move affects both the current small board and the future game state.

## 🪙 Coins & Unlockables

Winning against the AI awards coins based on the difficulty.

Coins can be spent to unlock:

### 🎭 Characters

The game includes **9 playable characters**, each with its own visual assets.

### 🎨 Board Themes

There are **5 board themes**:

* Midnight Purple
* Crimson Night
* Emerald Depths
* Ocean Blue
* Golden Hour

Unlocked characters and themes remain available after closing the game.

## 📊 Statistics

The game tracks:

* Games played
* Games won
* Games lost
* Games tied
* Win rate

Statistics can also be reset from the Statistics panel.

## 💾 Save System

The game uses a JSON save file to persist player progress.

It stores information such as:

* Coin balance
* Unlocked characters
* Selected character
* Unlocked themes
* Selected theme
* Game statistics

If no save file exists, the game automatically creates a new starting state.

## 🔊 Audio

The game uses **Pygame** for audio.

It includes:

* Menu background music
* Button click sounds
* Piece placement sounds
* Purchase sounds
* Victory sounds
* Loss sounds
* Error sounds

Music and sound effects can be independently enabled or disabled through the Settings menu.

## 🛠️ Built With

* **Python**
* **Tkinter** — graphical user interface
* **Pygame** — music and sound effects
* **Pillow** — image loading and resizing
* **JSON** — persistent save data

## 📦 Installation

### 1. Install Python

Install Python 3 from the official Python website.

### 2. Clone or download the project

Download the repository and open it in your preferred Python IDE.

### 3. Install dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python "Base Game.py"
```

## 🎯 How to Play

### Standard Mode

1. Choose **Human vs Human** or **Human vs Bot**.
2. If playing against the Bot, choose a difficulty.
3. Click an empty square to place your character.
4. Get three matching symbols in a row to win.
5. On a 4×4 board, you still need three in a row.
6. If the board fills without a winner, the game ends in a tie.

### Ultimate Mode

1. Start **Ultimate Mode** from the main menu.
2. Choose an empty cell in any available mini-board.
3. Your chosen cell determines the mini-board your opponent must play in.
4. Win mini-boards to claim them on the larger board.
5. Get three claimed mini-boards in a row to win the Ultimate game.

## 📁 Project Structure

```text
Tic-Tac-Toe/
│
├── Base Game.py
├── requirements.txt
├── .gitignore
│
├── Character Images
├── Sound Effects
├── Menu Music
│
└── save_data.json
```

> `save_data.json` is generated automatically when the game is run and stores the player's local progress.

## 🎮 Play the Game

[⬇️ Download the Windows Demo](YOUR_RELEASE_LINK)

Download the ZIP, extract it, and run `Base Game.exe`.
## 📚 What I Learned

Building this project helped me move beyond writing small Python programs and start thinking about how a complete application is structured.

Some of the main things I learned were:

* Building graphical interfaces with Tkinter
* Working with buttons, frames, labels, and event-driven programming
* Implementing game-state management
* Designing AI using Minimax
* Improving Minimax with Alpha-Beta Pruning
* Creating and managing persistent save data with JSON
* Working with images using Pillow
* Adding music and sound effects with Pygame
* Building a more complex game mode with Ultimate Tic-Tac-Toe
* Organizing a larger Python project
* Debugging and iterating on features over time

## 🙏 Credits

The game was designed and programmed from scratch as a personal Python project.

Character names and artwork are based on the **Italian Brainrot** meme trend. The project is not affiliated with the creators or owners of those characters.

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
