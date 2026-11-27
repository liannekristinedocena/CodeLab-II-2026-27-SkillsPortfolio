import os
import random
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox

root = tk.Tk()
root.title("Joke Assistant")
root.geometry("520x570")
root.resizable(0, 0)
root.configure(bg='#f3d9b8')


jokes = [] #creates an empty jokes list         
current_punchline = "" #creates an empty string variable that will store the punchline of the current joke 

JOKES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "randomJokes.txt")


def loadJokes(filename):
    loaded = [] #Creates an empty list to store all the jokes in 
    file = open(filename, encoding="utf-8") #Tells python to open a specific file. UTF=8 allows the program to load special characters 
    for line in file: #Goes through the file one line at a time. 
        parts = line.strip().split("?") #.strip() removes whitespaces at the start and end of a string. .split() seperates the text whenever it finds a question mark. 
        setup = parts[0] + "?" #Takes the first part of the joke and adds a question mark. This is then stored in the setup variable.
        punchline = parts[1] #Second part of the joke placed in the variable named 'punchline'
        #Python now creates a list with two items. These are parts[0] which is the question, and parts[1] which are the answers. 
        loaded.append((setup, punchline)) #Adds the joke to the list using the .append function.
    file.close()
    return loaded


def confirmJoke():
    confirm = messagebox.askyesno(
        "Proceed?",
        "Would you like to hear a joke?"
    )

    if confirm:
        tellJoke()


def confirmQuit():
    confirm = messagebox.askyesno(
        "Quit?",
        "Are you sure you want to leave Mr. Fox?"
    )

    if confirm:
        root.destroy()


def tellJoke():
    global current_punchline

    setup, current_punchline = random.choice(jokes) #Picks a random joke and seperates the two items as two variables, setup and current punchline. 
    setup_label.config(text=setup) #Displays the question on the tkinter window. 
    mascot_label.config(text="🤔") #the fox starts thinking
    punchline_label.config(text="") #Clears the punchline label

    tell_button.pack_forget() #Hides the tell joke button 
    punchline_button.config(state="normal") #enables the showpunchline button 
    punchline_button.pack(pady=6)
    next_button.pack(pady=6)
    quit_button.pack_forget() #Takes Quit off the screen...
    quit_button.pack(pady=6) #...and puts it back underneath the other buttons


def showPunchline():
    mascot_label.config(text=random.choice(["😂", "🤣", "😆", "😹"])) #Picks a random laughing face
    punchline_label.config(text=current_punchline) #Displays the answer stored in current_punchline onto the program using the punchline label 


#GUI
frame = tk.Frame(root, 
                 bg='#fffaf2')
frame.pack(expand=True, 
           fill="both", 
           padx=25, 
           pady=25)

mascot_label = tk.Label(frame, text="🦊", font=("Century Gothic", 36), bg='#fffaf2')
mascot_label.pack()


tk.Label(frame, text="Joke Assistant ₊ ⊹", font=("Century Gothic", 22, "bold"),
         bg='#fffaf2', fg='#d62828').pack(pady=(5, 10))

setup_label = tk.Label(frame, 
                       text="Are you having a bad day? Allow Mr. Fox to take over and make you laugh. Press the button to hear a joke!",
                       font=("Arial", 14), 
                       fg='#3b2a1e', 
                       bg='#fffaf2', 
                       wraplength=380,
                       width=36,
                       padx=15,
                       pady=10,
                       height=3)
setup_label.pack(pady=5)

punchline_label = tk.Label(frame, text="", 
                           font=("Century Gothic", 14, "bold"),
                           fg='#c2571a', 
                           bg='#fffaf2', 
                           wraplength=440,
                            width=36, 
                           padx=15, 
                           pady=10,
                           height=3)
punchline_label.pack(pady=5)

tell_button = tk.Button(frame, 
                        text="Mr Fox, tell me a Joke!", 
                        width=22,
                        font=("Century Gothic", 13, 'bold'), 
                        bg='#d62828', 
                        fg='white', 
                        cursor="hand2", 
                        command=confirmJoke)
tell_button.pack(pady=6)

punchline_button = tk.Button(frame, 
                             text="What, why, how?", 
                             width=22,
                             font=("Century Gothic", 13, 'bold'), 
                             bg='#6a4c93', 
                             fg='white', 
                             cursor="hand2", 
                             command=showPunchline)

next_button = tk.Button(frame, 
                        text="One more, one more!", 
                        width=22,
                        font=("Century Gothic", 13, 'bold'), 
                        bg='#2a9d8f', 
                        fg='white', 
                        cursor="hand2", 
                        command=tellJoke)

quit_button = tk.Button(frame, text="I'm done for today", 
                        width=22,
                        font=("Century Gothic", 13, 'bold'), 
                        bg='#8d99ae', 
                        fg='white', 
                        cursor="hand2", 
                        command=confirmQuit)

quit_button.pack(pady=6)



jokes = loadJokes(JOKES_FILE)

root.mainloop()
