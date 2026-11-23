import os
import tkinter as tk
from tkinter import messagebox

root=tk.Tk()
root.title("Student Manager")
root.geometry("640x560")
root.resizable(0,0)
root.configure(bg='#1f3a5f')

MARKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks.txt")

students=[]
marks=160

#code = student[0]
#name = student[1]
#course = student[2]
#exam = student[3]

def loadStudents(filename):
    info=[] #creates an empty list called info
    file = open(filename, encoding="utf-8-sig")
    file.readline()

    for line in file:
        line=line.strip()
        parts=line.split(",")

        code=int(parts[0])
        name=parts[1]
        course=int(parts[2])+int(parts[3])+int(parts[4])
        exam=int(parts[5])
        info.append([code, name, course, exam])
    file.close()
    return info

def getPercentage(student):
    total=student[2]+student[3]
    return total / marks * 100

def getGrade(percentage):
    if percentage >= 70:
        return "A"
    if percentage >= 60:
        return "B"
    if percentage >= 50:
        return "C"
    if percentage >= 40:
        return "D"
    return "F"

def format(student):
    code = student[0]
    name = student[1]
    course = student[2]
    exam = student[3]

    percentage = getPercentage(student)
    text = "Name: " + student[1] + "\n"
    text += "Student Number: " + str(student[0]) + "\n"
    text += "Total Coursework Mark: " + str(student[2]) + " / 60\n"
    text += "Exam Mark: " + str(student[3]) + " / 100\n"
    text += "Overall Percentage: " + str(round(percentage, 1)) + "%\n"
    text += "Grade: " + getGrade(percentage) + "\n"
    return text


def showOutput(text):
    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)


def viewAll():
    text = ""
    total_avr = 0

    for student in students:
        text += format(student) + "\n"
        total_avr += getPercentage(student)

    avr = total_avr / len(students)

    text += "Number of students in class: " + str(len(students)) + "\n"
    text += "Average percentage mark: " + str(round(avr, 1)) + "%\n"

    showOutput(text)

def search():
    word=search_entry.get().strip().lower()
    #search_entry.get retrieves what the user types into the search box 
    #.strip() removes all uneeded spaces
    #.lower() converts user input into all lowercase letters. 

    if word=="":
        showOutput("Please type student name or number.")
        return

    text="" #creates an empty string called 'text'
    for student in students: #creates a list that goes through every student in the students list one at a time. 
        if word==str(student[0]) or word in student[1].lower():  

            #student[0] accesses the first item in the list (student code)
            #str converts the student code into a string & checks whether it matches the user input 
            #student[1] accesses the second item in the list (student name)

            text+=format(student) + "\n"

    if text == "":
        text="No student found."
    showOutput(text)

def highest():
    highest=max(student[2]+student[3] for student in students)
    #adds the course and exam marks and looks for the highest sum from the students in the list. 

    text="Student with the highest total score:\n\n"
    for student in students:
        if student[2] + student[3] == highest:
            text+=format(student) + "\n"
    showOutput(text)

def lowest():
    lowest=min(student[2]+student[3] for student in students)
    text="Student with the lowest total score:\n\n"
    for student in students:
        if student[2] + student[3] == lowest:
            text+=format(student) + "\n"
    showOutput(text)


#GUI
panel = tk.Frame(root, bg="#f4f6f9")
panel.pack(expand=True, fill="both", padx=25, pady=25)


# Main title
title = tk.Label(panel, 
                 text="STUDENT MANAGER",
                 font=("Georgia", 22, "bold"),
                 bg="#f4f6f9",
                 fg="#1f3a5f",
                 padx=15, pady=8)
title.pack(pady=(15, 12))


# Menu buttons
button_frame = tk.Frame(panel, bg="#f4f6f9", padx=10, pady=8)
button_frame.pack(pady=5)

tk.Button(button_frame,
          text="View All Student Records",
          width=28,
          font=("Arial", 10, "bold"),
          bg="#1f3a5f",
          fg="white",
          cursor="hand2",
          activebackground="#2d4f7c",
          activeforeground="white",
          command=viewAll).grid(row=0, column=0, padx=5, pady=5)

tk.Button(button_frame,
          text="Highest Total Score",
          width=28,
          font=("Arial", 10, "bold"),
          bg="#1f3a5f",
          fg="white",
          cursor="hand2",
          activebackground="#2d4f7c",
          activeforeground="white",
          command=highest).grid(row=0, column=1, padx=5, pady=5)

tk.Button(button_frame,
          text="Lowest Total Score",
          width=28,
          font=("Arial", 10, "bold"),
          bg="#1f3a5f",
          fg="white",
          cursor="hand2",
          activebackground="#2d4f7c",
          activeforeground="white",
          command=lowest).grid(row=1, column=0, columnspan=2, padx=5, pady=5)



search_frame = tk.Frame(panel, bg="#f4f6f9", padx=10, pady=8)
search_frame.pack(pady=8)

tk.Label(search_frame,
         text="Name / Student Code:",
         font=("Arial", 11, "bold"),
         bg="#f4f6f9",
         fg="#1f2933").pack(side="left", padx=5)

search_entry = tk.Entry(search_frame,
                        font=("Arial", 11),
                        width=20)

search_entry.pack(side="left", padx=5)

tk.Button(search_frame,
          text="Search",
          font=("Arial", 10, "bold"),
          bg="#1f3a5f",
          fg="white",
          cursor="hand2",
          activebackground="#2d4f7c",
          activeforeground="white",
          command=search).pack(side="left", padx=5)

search_entry.bind("<Return>", lambda event: search())


# Output box
output_frame = tk.Frame(panel, 
                        bg="#f4f6f9", 
                        padx=8, 
                        pady=8)
output_frame.pack(expand=True, 
                  fill="both", 
                  padx=15, 
                  pady=5)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output = tk.Text(output_frame,
                 font=("Arial", 11),
                 wrap="word",
                 bg="#ffffff",
                 fg="#1f2933",
                 padx=10,
                 pady=10,
                 yscrollcommand=scrollbar.set)

output.pack(side="left", expand=True, fill="both")

scrollbar.config(command=output.yview)



tk.Button(panel,
          text="Quit",
          width=14,
          font=("Arial", 10, "bold"),
          bg="#6b7684",
          fg="white",
          cursor="hand2",
          activebackground="#2d4f7c",
          activeforeground="white",
          command=root.destroy).pack(pady=(5, 12))


# Load student records
students = loadStudents(MARKS_FILE)
showOutput("Choose an option above.")

root.mainloop()