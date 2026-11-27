import random
import tkinter as tk
from PIL import ImageTk, Image 
from tkinter import messagebox
import time 

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("490x480")
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
time_left=30 
time_taken=0
total_time=0
question_start_time=time.time()  
time_id=None
timer_label=None
entry = None #No value assigned yet. 
feedback_label = None

frame = tk.Frame(root, bg='#fbf6f3',
                 highlightbackground='#e3bdb5',
                 highlightcolor='#e3bdb5', 
                 highlightthickness=3)
frame.pack(expand=True, 
           fill="both", 
           padx=25, pady=25)

#A function that generates random numbers based on the difficulty level
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

#Assigns A rank based on the score the user gets. 
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

#A function that clears the contents of your GUI frame. This destroys all the widgets from the GUI when it is called. 
def clearFrame():
    for widget in frame.winfo_children():#Goes through every widget inside the frame one at a time. 
        widget.destroy() #Removes the widget from the GUI.

#the main window and its GUI 
def displayMenu(): 
    clearFrame()
    tk.Label(frame, text="★ Math Quiz ★", 
             font=("Century Gothic", 22, 'bold'), 
             bg='#fbf6f3', fg='#b47878').pack(pady=(10, 5))

    tk.Label(frame,
            text="Welcome to Lianne's Calculator Quiz! Please proceed by choosing a difficulty level.",
            font=("Century Gothic", 11),
            bg='#fbf6f3',
            wraplength=350,
            fg="#8a7a7a",
            justify="center").pack(pady=10)
    
    tk.Label(frame, text="Difficulty Level", 
             font=("Century Gothic", 15, 'bold'), 
             bg='#fbf6f3',fg='#3d2f2f').pack(pady=(10, 5))

    tk.Button(frame, text="1. Easy", 
              width=20, 
              command=lambda: Difficulty("Easy"),
              bg='#cfe3c8', fg='#3d2f2f', font=("Century Gothic", 13, 'bold'), cursor="hand2", pady=5).pack(pady=6)
    
    tk.Button(frame, text="2. Moderate", 
              width=20, 
              command=lambda: Difficulty("Moderate"),
              bg='#f3e1b6', fg='#3d2f2f', font=("Century Gothic", 13, 'bold'), cursor="hand2", pady=5).pack(pady=6)
    
    tk.Button(frame, text="3. Advanced", 
              width=20, 
              command=lambda: Difficulty("Advanced"),
              bg='#e3bdb5', fg='#3d2f2f', font=("Century Gothic", 13, 'bold'), cursor="hand2", pady=5).pack(pady=6)



def Difficulty(chosen_level):
    confirm = messagebox.askyesno( #Displays a pop-up message box that asks the user if they want to proceed with the chosen difficulty 
        "Confirm Difficulty",
        "Are you sure you want to proceed with " + chosen_level + " difficulty?"
    )

    if confirm: 
        startQuiz(chosen_level) #run the function with the chosen difficulty when user presses 'confirm'


#a function that starts the quiz at a new level 
def startQuiz(new_level):
    global level, score, question_num,total_time,question_start_time #The global keyword allows the startQuiz function to store and edit variables outside this specific function

    total_time=0 #resets the total time taken back to 0 for a new quiz
    level = new_level #stores the difficulty level chosen by the user 
    score = 0 #resets the score back to 0 
    question_num = 0 #resets the question number back to 0 
    nextQuestion() #calls on the nextQuestion() function to generate the next question 


#a function that handles the countdown timer for each question 
def countdown(): 
    global time_left, time_id #allows the function to access and modify the timer variables

    timer_label.config(text="Time left: " +str(time_left) + "s") #updates the timer variable to display the remaining time 

    if time_left>0: #checks if there is still remaining time 
        time_left-=1 #decreases the time by 1 
        time_id=root.after(1000,countdown) #calls the countdown function again after 1 second 

    else: #runs if time_left==0 
        showFeedback("Time's up! The correct answer was " + str(answer) + ".", "#b47878")


#a function that proceeds with the next question 
def nextQuestion(): 
    global question_num, attempt, num1, num2, op, answer, time_left, time_id, time_taken,question_start_time
    root.unbind("<Return>") #removes the enter key binding from the previous question 

    question_num += 1 #moves onto the next question 
    attempt = 1 #resets the attempt count to 1 for the new question 
    time_left = 30 #resets the timer for every new question 
    time_taken=time.time() #records the starting time for the new question 
    num1 = randomInt(level) #generates the first number based on the selected difficulty 
    num2 = randomInt(level)
    op = Operation() #calls onto the Operation function to randomly generate either addition or subtraction 


    if time_id is not None: #checks if the previous countdown timer is still running 
        root.after_cancel(time_id) #cancels the previous countdown timer 
        time_id = None #resets the timer_id 

    if question_num >= total_questions: #checks if all the questions have been answered 
        displayResults() #displays the final quiz results 
        return

#checks if either addition or subtraction was selected and performs the needed solutions
    if op == "+":
        answer = num1 + num2
    else:
        answer = num1 - num2

    displayProblem() #calls on the displayProblem() function to display the questions on the GUI 


def displayProblem():
    global entry, feedback_label, timer_label,question_start_time
    clearFrame()

    top_bar = tk.Frame(frame, bg='#fbf6f3') #a small frame that holds the question counter and score on the same line
    top_bar.pack(fill="x", padx=5, pady=(5, 0))


    tk.Label(top_bar, 
             text="Question " + str(question_num) + " of " + str(total_questions),
             font=("Century Gothic", 12, 'bold'),
             bg='#fbf6f3',fg='#8a7a7a').pack(side="left") #Creates a text label that shows the current question number. STR converts the INT into a string value.
    
    tk.Label(top_bar, 
             text="Score: " + str(score), 
             font=("Century Gothic", 12, 'bold'),
             bg='#fbf6f3', fg='#8a7a7a').pack(side="right")

    tk.Label(frame, text=str(num1) + " " + op + " " + str(num2) + " =",
             font=("Century Gothic", 28, "bold"),
             bg='#fbf6f3',fg="#3d2f2f").pack(pady=(25, 10))

    entry = tk.Entry(frame, 
                     font=("Century Gothic", 28), 
                     width=8, 
                     justify="center")

    timer_label = tk.Label(frame,
                       text="Time left: 30s",
                       font=("Century Gothic", 14, "bold"),
                       fg="#b47878",
                       bg="#fbf6f3")

    timer_label.pack(pady=5)
    
    entry.pack(pady=10)
    entry.focus_set() #Places the cursor inside the entry box automatically. 
    entry.bind("<Return>", lambda event: submitAnswer())   #Connects the keyboard to a function. When the user clicks enter, python executes the submitAnswer function. 

    feedback_label = tk.Label(frame, text="", 
                              font=("Century Gothic", 14), bg='#fbf6f3')
    feedback_label.pack(pady=8)

    tk.Button(frame, text="Submit", width=14, 
              font=("Century Gothic", 14), bg='#e3bdb5', fg='#3d2f2f', cursor="hand2",
              command=submitAnswer).pack(pady=8)
    countdown()



def submitAnswer():
    global score, attempt #allows the function to access the score and attempt variables 

    try:
        user_answer = int(entry.get().strip()) #gets user input, removes extra space, and turns it into an integer. 
    except ValueError:
        feedback_label.config(text="Please enter a whole number.", 
                              bg="#fbf6f3",
                              fg="#b47878")
        return

    correct, message = isCorrect(user_answer, answer) #checks whether the user answer is correct and gets the feedback message 

    if correct: 
        if attempt == 1:
            points = 10 #awards 10 points for a correct answer on the first attempt 
        else:
            points = 5 #awards 5 points for a correct answer on the second attempt 
        score += points
        showFeedback(message + "  +" + str(points) + " points", "#6b8f71")

    elif attempt == 1:
        attempt = 2     #give the user one more chance
        feedback_label.config(text=message + " One more chance.", fg="#b47878") #displays feedback 
        entry.delete(0, tk.END) #clears the entry box
        entry.focus_set() #places the cursor back in the entry box 

    else:
        showFeedback(message + " The correct answer was " + str(answer) + ".", "#b47878") #runs if the answer is incorrect on the second attempt 



def showFeedback(text, colour):
    global time_id, total_time,question_start_time

    #calculates how long the user took to answer the question 
    #adds the time taken for this question to the total time 
    total_time+=time.time()-question_start_time #Created using the help of CLAUDE AI. Prompt: Create a function in my code that will calculate the average time the user spends answering the quiz.
    
    if time_id is not None:
        root.after_cancel(time_id)
    time_id = None
    clearFrame()


    tk.Label(frame, 
             text="Score: " + str(score), 
             font=("Century Gothic", 12), 
             bg='#fbf6f3').pack(anchor="e")
    
    tk.Label(frame, 
             text=str(num1) + " " + op + " " + str(num2) + " = " + str(answer),
             font=("Century Gothic", 28, "bold"), 
             bg='#fbf6f3').pack(pady=(25, 10))
    
    tk.Label(frame, text=text, 
             font=("Century Gothic", 14), fg=colour, bg='#fbf6f3',
             wraplength=380).pack(pady=15)
    
    if question_num >= total_questions:
        button_text = "See Results"
    else:
        button_text = "Next Question"

    tk.Button(frame, text=button_text, 
              width=16, 
              font=("Century Gothic", 14), 
              bg='#e3bdb5', fg='#3d2f2f', cursor="hand2",
              command=nextQuestion).pack(pady=10)
    
    root.bind("<Return>", lambda event: nextQuestion())


def displayResults():
    clearFrame()

    tk.Label(frame, 
             text="★ QUIZ COMPLETE ★", 
             font=("Century Gothic", 22, "bold"), 
             bg='#fbf6f3', fg='#b47878').pack(pady=(15, 10))
    
    tk.Label(frame, 
             text="Your score: " + str(score) + " / 100",
             font=("Century Gothic", 24, "bold"), 
             bg='#fbf6f3',fg='#3d2f2f').pack(pady=10)
    
    tk.Label(frame, text="Rank: " + Rank(score),
             font=("Century Gothic", 24, "bold"), 
             bg='#fbf6f3',fg='#3d2f2f').pack(pady=10)

    average_time = round(total_time / total_questions, 2)

    tk.Label(frame,
         text="Average time: " + str(average_time) + " seconds",
         font=("Century Gothic", 14),
         bg='#fbf6f3',fg='#3d2f2f').pack(pady=10)

    tk.Button(frame, text="Play Again", 
              width=16, 
              font=("Century Gothic", 14), 
              bg='#e3bdb5', fg='#3d2f2f', cursor="hand2",
              command=askReplay).pack(pady=(20, 6))
    
    tk.Button(frame, 
              text="Quit", 
              width=16, 
              font=("Century Gothic", 14), 
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
