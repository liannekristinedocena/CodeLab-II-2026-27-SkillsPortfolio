import random
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("460x450")
root.resizable(0, 0)
root.configure(bg='#eacdc7')


#Variables that will be used in the Quiz
level = 1
score = 0
question_num = 0
attempt = 1
num1 = 0
num2 = 0
op = "+"
answer = 0
total_questions = 10
entry = None #No value assigned yet. 
feedback_label = None


#Generates random numbers based on the difficulty level
def randomInt(level):

    if level == "Easy":
        return random.randint(1, 9) #random.randit is a built in python function that picks a random whole number from the given range. 

    elif level == "Moderate":
        return random.randint(10, 99)

    elif level == "Advanced":
        return random.randint(1000, 9999)


#Randomly chooses addition(+) or subtraction(-)
def Operation():
    return random.choice(['+', '-'])


#Checks whether user answer is correct. If correct, the message 'Correct!' appears. Else, the message 'wrong answer' prints.
def isCorrect(user_answer, correct_answer):
    if user_answer == correct_answer:
        return True, "Correct!"
    return False, "Sorry, wrong answer!"


def Rank(score):
    if score > 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 50:
        return "D"
    return "F"


#GUI
frame = tk.Frame(root, bg='#fbf6f3')
frame.pack(expand=True, 
           fill="both", 
           padx=25, pady=25)


def clearFrame():
    for widget in frame.winfo_children():
        widget.destroy()

def Difficulty(chosen_level):
    confirm = messagebox.askyesno(
        "Confirm Difficulty",
        "Are you sure you want to proceed with " + chosen_level + " difficulty?"
    )

    if confirm:
        startQuiz(chosen_level)

def displayMenu():
    clearFrame()
    tk.Label(frame, text="Math Quiz", 
             font=("Arial", 22, 'bold'), 
             bg='#fbf6f3', fg='#b47878').pack(pady=(10, 5))

    tk.Label(frame,
            text="Welcome to Lianne's Calculator! Please proceed by choosing a difficulty level.",
            font=("Arial", 11),
            bg='#fbf6f3',
            wraplength=350,
            fg="#8a7a7a",
            justify="center").pack(pady=10)
    
    tk.Label(frame, text="Difficulty Level", 
             font=("Arial", 15, 'bold'), 
             bg='#fbf6f3').pack(pady=(10, 5))

    tk.Button(frame, text="1. Easy", 
              width=20, 
              command=lambda: Difficulty("Easy"),
              bg='#e3bdb5', fg='#3d2f2f', font=("Arial", 13), cursor="hand2", pady=5).pack(pady=6)
    
    tk.Button(frame, text="2. Moderate", 
              width=20, 
              command=lambda: Difficulty("Moderate"),
              bg='#e3bdb5', fg='#3d2f2f', font=("Arial", 13), cursor="hand2", pady=5).pack(pady=6)
    
    tk.Button(frame, text="3. Advanced", 
              width=20, 
              command=lambda: Difficulty("Advanced"),
              bg='#e3bdb5', fg='#3d2f2f', font=("Arial", 13), cursor="hand2", pady=5).pack(pady=6)


def startQuiz(new_level):
    global level, score, question_num #The global keyword allows the startQuiz function to store and edit variables outside this specific function
    level = new_level
    score = 0
    question_num = 0
    nextQuestion()

def nextQuestion():
    global question_num, attempt, num1, num2, op, answer
    root.unbind("<Return>")

    if question_num >= total_questions:
        displayResults()
        return

    question_num += 1
    attempt = 1
    num1 = randomInt(level)
    num2 = randomInt(level)
    op = Operation()

    if op == "+":
        answer = num1 + num2
    else:
        answer = num1 - num2

    displayProblem()


def displayProblem():
    global entry, feedback_label
    clearFrame()

    tk.Label(frame, 
             text="Question " + str(question_num) + " of " + str(total_questions),
             font=("Arial", 12),
             bg='#fbf6f3').pack(anchor="w") #Creates a text label that shows the current question number. STR converts the INT into a string value.
    
    tk.Label(frame, 
             text="Score: " + str(score), 
             font=("Arial", 12),
             bg='#fbf6f3').pack(anchor="e")

    tk.Label(frame, text=str(num1) + " " + op + " " + str(num2) + " =",
             font=("Arial", 28, "bold"),
             bg='#fbf6f3').pack(pady=(25, 10))

    entry = tk.Entry(frame, 
                     font=("Arial", 28), 
                     width=8, 
                     justify="center")
    
    entry.pack(pady=10)
    entry.focus_set() #Places the cursor inside the entry box automatically. 
    entry.bind("<Return>", lambda event: submitAnswer())   #Connects the keyboard to a function. When the user clicks enter, python executes the submitAnswer function. 

    feedback_label = tk.Label(frame, text="", 
                              font=("Arial", 14), bg='#fbf6f3')
    feedback_label.pack(pady=8)

    tk.Button(frame, text="Submit", width=14, 
              font=("Arial", 14), bg='#e3bdb5', fg='#3d2f2f', cursor="hand2",
              command=submitAnswer).pack(pady=8)


def submitAnswer():
    global score, attempt

    try:
        user_answer = int(entry.get().strip())
    except ValueError:
        feedback_label.config(text="Please enter a whole number.", 
                              bg="#fbf6f3",
                              fg="#b47878")
        return

    correct, message = isCorrect(user_answer, answer)

    if correct:
        if attempt == 1:
            points = 10
        else:
            points = 5
        score += points
        showFeedback(message + "  +" + str(points) + " points", "#6b8f71")

    elif attempt == 1:
        attempt = 2     # give the user one more chance
        feedback_label.config(text=message + " One more chance.", fg="#b47878")
        entry.delete(0, tk.END)
        entry.focus_set()

    else:
        showFeedback(message + " The correct answer was " + str(answer) + ".", "#b47878")



def showFeedback(text, colour):
    clearFrame()

    tk.Label(frame, 
             text="Score: " + str(score), 
             font=("Arial", 12), 
             bg='#fbf6f3').pack(anchor="e")
    
    tk.Label(frame, 
             text=str(num1) + " " + op + " " + str(num2) + " = " + str(answer),
             font=("Arial", 28, "bold"), 
             bg='#fbf6f3').pack(pady=(25, 10))
    
    tk.Label(frame, text=text, 
             font=("Arial", 14), fg=colour, bg='#fbf6f3',
             wraplength=380).pack(pady=15)
    
    if question_num >= total_questions:
        button_text = "See Results"
    else:
        button_text = "Next Question"

    tk.Button(frame, text=button_text, 
              width=16, 
              font=("Arial", 14), 
              bg='#e3bdb5', fg='#3d2f2f', cursor="hand2",
              command=nextQuestion).pack(pady=10)
    
    root.bind("<Return>", lambda event: nextQuestion())



def displayResults():
    clearFrame()

    tk.Label(frame, 
             text="QUIZ COMPLETE", 
             font=("Arial", 22, "bold"), 
             bg='#fbf6f3', fg='#b47878').pack(pady=(15, 10))
    
    tk.Label(frame, 
             text="Your score: " + str(score) + " / 100",
             font=("Arial", 24, "bold"), 
             bg='#fbf6f3').pack(pady=10)
    
    tk.Label(frame, text="Rank: " + Rank(score),
             font=("Arial", 24, "bold"), 
             bg='#fbf6f3').pack(pady=10)

    tk.Button(frame, text="Play Again", 
              width=16, 
              font=("Arial", 14), 
              bg='#e3bdb5', fg='#3d2f2f', cursor="hand2",
              command=askReplay).pack(pady=(20, 6))
    
    tk.Button(frame, 
              text="Quit", 
              width=16, 
              font=("Arial", 14), 
              bg='#e3d6cc', fg='#3d2f2f', cursor="hand2",
              command=root.destroy).pack(pady=6)


#Asks if the user wants to play again
def askReplay():
    if messagebox.askyesno("Play again?", "Would you like to play again?"):
        displayMenu()
    else:
        root.destroy()


displayMenu()
root.mainloop()