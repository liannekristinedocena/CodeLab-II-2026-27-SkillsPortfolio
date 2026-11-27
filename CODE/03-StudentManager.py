import os
import tkinter as tk
from PIL import ImageTk, Image 
from tkinter import messagebox

root=tk.Tk()
root.title("Student Manager")
root.geometry("900x620")
root.resizable(0,0)
root.configure(bg='#1f3a5f')

MARKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks (4).txt")

students=[]
marks=160


def loadStudents(filename):
    info=[] #creates an empty list called info
    file = open(filename, encoding="utf-8-sig")
    file.readline()

    for line in file: #runs through all the lines in the studentMarks file 
        line=line.strip() #Removes all whitespace from the beginning and end of the string 
        parts=line.split(",") #Splits the line into seperate values once a comma appears 

        code=int(parts[0]) #Convert student codes from str to int. EX: '1111' becomes 1111
        name=parts[1]
        course=int(parts[2])+int(parts[3])+int(parts[4]) #Converts all three coursemarks into integers and adds for their total
        exam=int(parts[5]) 
        info.append([code, name, course, exam]) #Appends the student info to the info[] list. 
    file.close()
    return info #Allows information collected inside one function to be used somewhere else in the program 

students = loadStudents(MARKS_FILE) #Recieves the the list returned by info 
print("Number of students:", len(students))
print(students)

#A function that gets the total percentage of the students by adding the total course and exam mark together and multipying by 100. 
def getPercentage(student):
    total=student[2]+student[3]
    return total / marks * 100

#Assigns a grade based on the percentage receieved. 
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

#A function that handles how the information will be formatted. 
def format(student):
    code = student[0] #gets the student number from the list
    name = student[1] #gets student name
    course = student[2] #gets students total coursework mark
    exam = student[3] #gets the students exam mark

    percentage = getPercentage(student) #calculates the students overall percentage
    text = "Name: " + student[1] + "\n" #adds the student name to the output text 
    text += "Student Number: " + str(student[0]) + "\n" #adds the student number to the output text 
    text += "Total Coursework Mark: " + str(student[2]) + " / 60\n" #adds the coursework mark out of 60
    text += "Exam Mark: " + str(student[3]) + " / 100\n" #adds the exam mark out of 100
    text += "Overall Percentage: " + str(round(percentage, 1)) + "%\n" #adds the overall percentage rounded off to 1 decimal place
    text += "Grade: " + getGrade(percentage) + "\n" #gets an adds the student grade based on the percentage 
    return text #returns the formatted student information 


def showOutput(text):
    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)


def viewAll():
    text = "" #creates an empty string to store all student information 
    total_avr = 0

    for student in students: #Goes through the student list one record at a time 
        text += format(student) + "\n" #formats the student information and adds it to the text 
        total_avr += getPercentage(student) #calculates student percentage and adds it to the running total 

#calculates the average percentage of the entire class
    avr = total_avr / len(students) #len counts how many student records are in the students list. This divides the total percentage to the number of students in the list 

    text += "Number of students in class: " + str(len(students)) + "\n" #adds the total number of students to the output text
    text += "Average percentage mark: " + str(round(avr, 1)) + "%\n" #adds the total avr percentage to the output text

    showOutput(text) #calls the showOutput function and displays it in the GUI 

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

def highest(): #a function that displays the student with the highest score 
    highest=max(student[2]+student[3] for student in students)
    #adds the course and exam marks and looks for the highest sum from the students in the list. 

#creates a heading 
    text="Student with the highest total score:\n\n"
    for student in students: #goes through the student list one record at a time 
        if student[2] + student[3] == highest: #checks if the students combined marks match the highest score 
            text+=format(student) + "\n" #adds the formatted information to the output text 
    showOutput(text)

def lowest(): #a function that displays the student with the lowest score
    lowest=min(student[2]+student[3] for student in students) 
    text="Student with the lowest total score:\n\n"
    for student in students:
        if student[2] + student[3] == lowest:
            text+=format(student) + "\n"
    showOutput(text)

#a function that loads the original student records from a text file 
def loadRawStudents(filename):
    global file_header

    info = [] #creates an empty list to store all the student records 
    file = open(filename, encoding="utf-8-sig") 

    file_header = file.readline() #reads the first line of the file, which contains all column headings 

    for line in file: #goes through the remaining lines of the file one at a time 
        line = line.strip()

        if line == "": #checks if the line is empty 
            continue #skips the empty line and moves onto the next line 

        parts = line.split(",")

        code = int(parts[0])
        name = parts[1]
        coursework_1 = int(parts[2])
        coursework_2 = int(parts[3])
        coursework_3 = int(parts[4])
        exam = int(parts[5])

#creates a list containing all student info and appends this record into the main list 
        info.append([code, name, coursework_1,
                     coursework_2, coursework_3, exam])

    file.close()
    return info


#a function that saves student info in the text file 
def saveStudents(): 
    global students #allows the function to update the global students list 

    file = open(MARKS_FILE, "w", encoding="utf-8-sig")
    file.write(file_header)

    for student in rawStudents:
        file.write(
            str(student[0]) + "," + student[1] + "," +
            str(student[2]) + "," + str(student[3]) + "," +
            str(student[4]) + "," + str(student[5]) + "\n"
        ) #writes each students information into the file, seperating each value with a comma 

    file.close() #closes the file after writing all student records 

    students = loadStudents(MARKS_FILE) #reloads the updated file to refresh the students list 


def addStudent(): #a function that creates a new window for adding student information 
    form=tk.Toplevel(root) #creates a new window connected to the main application 
    form.title("Add Student") 
    form.geometry("300x400")

    entries=[] #creates an empty list to the store the entry widgets 

    labels=["Student Code", "Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam"] #stores the name of the information list required by the user 

    for label in labels: #Loops through each label 
        tk.Label(form,text=label).pack() #and creates and displays a label in the form 
        entry=tk.Entry(form) #creates an input box where the user can input information 
        entry.pack(pady=5) 
        entries.append(entry) #stores each entry widget in the entries list so its value can be retrieved later 

    def submit(): #a function that handles the information submitted by the user 
        try:
            code = int(entries[0].get()) #retrieves the student code and converts it into an integer 
            name = entries[1].get().strip() #retrieves student name 
            coursework_1 = int(entries[2].get()) #retrieves the first coursework mark 
            coursework_2 = int(entries[3].get()) #retrieves the second coursework mark 
            coursework_3 = int(entries[4].get()) #retrieves the third coursework mark 
            exam = int(entries[5].get()) #retrieves the exam mark

    
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return #runs when the user fails to enter a valid whole number 

        rawStudents.append([code, name, coursework_1, coursework_2, coursework_3, exam]) #appends the new values into the new text file
        saveStudents() #calls the function to save new student information into the text file 
        showOutput("Student added successfully!")

    tk.Button(form, text="Add Student", command=submit).pack(pady=15) #creates a button that runs the submit function when clicked 


#a function that deletes a student based on a given student code
def deleteStudent():  
    form = tk.Toplevel(root)
    form.title("Delete Student")
    form.geometry("300x150")

    tk.Label(form, text="Enter Student Code:").pack(pady=5) #tells the user to enter a student code

    entry = tk.Entry(form) #creates an input box 
    entry.pack(pady=5) #displays input box in the window 


#a nested function that handles the deletion of the student 
    def delete(): 
        try:
            code=int(entry.get()) #gets the number inputted by the user
        except ValueError:
             messagebox.showerror("Error," "Enter a valid student code!") #runs if the user input is invalid
             return

        for student in rawStudents: 
            if student[0]==code: #checks if the user inputted code matches a code in the rawStudent list
                rawStudents.remove(student) #deletes the student with the matching code
                saveStudents() #saves the file
                showOutput("Student deleted.")
                form.destroy()
                return

        messagebox.showerror("Error", "Student not found.") #runs if user inputted code does not match a code from the rawStudents file.

    tk.Button(form, text="Delete", command=delete).pack(pady=10)


def updateStudent(): # a function that updates a student in the student records 
    form = tk.Toplevel(root)
    form.title("Update Student")
    form.geometry("300x180")

    tk.Label(form, text="Enter Student Code:").pack(pady=5)

    entry = tk.Entry(form)
    entry.pack(pady=5)

    def findStudent(): 
        try:
            code=int(entry.get()) #gets the number inputted by the user
        except ValueError:
            messagebox.showerror("Error," "Enter a valid student code!") #runs if the user input is invalid
            return

        for student in rawStudents: #loops through the rawStudents file 
            if student[0] == code: #checks whether user input matches any student code
                form.destroy()

                edit = tk.Toplevel(root)
                edit.title("Edit Student")
                edit.geometry("300x400")

                entries = [] #creates an empty list to store the input boxes 
                labels = ["Student Code", "Name", "Coursework 1",
                          "Coursework 2", "Coursework 3", "Exam"] #stores the label for each student details 

                for i in range(6): #repeats 6 times to create an input box for each detail 
                    tk.Label(edit, text=labels[i]).pack() #displays the label for each current detail 
                    box = tk.Entry(edit) #creates an input box 
                    box.pack(pady=5)
                    box.insert(0, str(student[i])) #fills the input box with a students current information 
                    entries.append(box) #adds the input box to the entry list 

                def saveUpdate():
                    try:
                        code = int(entries[0].get()) #gets all the updated information 
                        name = entries[1].get().strip()
                        coursework_1 = int(entries[2].get())
                        coursework_2 = int(entries[3].get())
                        coursework_3 = int(entries[4].get())
                        exam = int(entries[5].get())
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input.")
                        return

                    student[0] = code #updates the student code, name, courseworks, and exams
                    student[1] = name
                    student[2] = coursework_1
                    student[3] = coursework_2
                    student[4] = coursework_3
                    student[5] = exam

                    saveStudents() #saves the updated student records to the file 
                    showOutput("Student updated successfully!")
                    edit.destroy() #closes the editing window 

                tk.Button(edit, text="Save Changes",
                          command=saveUpdate).pack(pady=15) #creates a button that saves the updated details 

                return #stops searching once the matching student has been found 

        messagebox.showerror("Error", "Student not found.")

    tk.Button(form, text="Find Student",
              command=findStudent).pack(pady=10) #creates a button that searches for the student 


def sortStudents(order): 

#Created with the help of CLAUDE AI. PROMPT USED: "How do I make an ascending and descending list in python tkinter?"
    if order == "ascending":
        sorted_student = sorted(students, key=lambda s: s[2] + s[3]) #sorts students from lowest to highest based on the total of coursework 1 and 2 
    else:
        sorted_student = sorted(students, key=lambda s: s[2] + s[3], reverse=True) #sorts from highest to lowest 

    text = "" #creates an empty string to store student info 
    total_avr = 0 #initialises the variable to store the class average

    for student in sorted_student: #loops through the sorted student records 
        text += format(student) + "\n" #adds each student information to the text output 
        total_avr += getPercentage(student) #adds each student percentage to the total 

    avr = total_avr / len(sorted_student) #calculates the average percentage of the class

    text += "\nNumber of students in class: " + str(len(sorted_student)) #adds the total number of students to the output 
    text += "\nAverage percentage mark: " + str(round(avr, 1)) + "%" #adds the class average. rounded to 1 decimal place

    showOutput(text) #displays all the student info 


#GUI
panel = tk.Frame(root, bg="#f4f6f9")
panel.pack(expand=True, fill="both", padx=25, pady=25)

sidebar = tk.Frame(root, bg="#1f3a5f", width=240)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False) #stops the sidebar shrinking to fit its buttons, so it keeps a fixed width

def menuButton(text, command):
    tk.Button(sidebar,
              text=text,
              anchor="w",
              padx=15,
              font=("Arial", 10, "bold"),
              bg="#2a4a75",
              fg="white",
              cursor="hand2",
              activebackground="#3b5f93",
              activeforeground="white",
              command=command).pack(fill="x", padx=15, pady=3)

def menuHeading(text):
    tk.Label(sidebar,
             text=text,
             font=("Arial", 8, "bold"),
             bg="#1f3a5f",
             fg="#9fb3cc").pack(anchor="w", padx=18, pady=(14, 2))

menuHeading("RECORDS")
menuButton("View All Student Records", viewAll)
menuButton("Highest Total Score", highest)
menuButton("Lowest Total Score", lowest)

menuHeading("SORT")
menuButton("Sort Ascending", lambda: sortStudents("ascending"))
menuButton("Sort Descending", lambda: sortStudents("descending"))

menuHeading("MANAGE")
menuButton("Add Student", addStudent)
menuButton("Update Student", updateStudent)
menuButton("Delete Student", deleteStudent)

tk.Button(sidebar,
          text="Quit",
          font=("Arial", 10, "bold"),
          bg="#6b7684",
          fg="white",
          cursor="hand2",
          activebackground="#8793a3",
          activeforeground="white",
          command=root.destroy).pack(side="bottom", fill="x", padx=15, pady=20)


#RIGHT SIDE: the main window
main = tk.Frame(root, bg="#f4f6f9")
main.pack(side="left", expand=True, fill="both")

tk.Label(main,
         text="Student Records",
         font=("Georgia", 22, "bold"),
         bg="#f4f6f9",
         fg="#1f3a5f").pack(anchor="w", padx=30, pady=(25, 5))

#Search bar
search_frame = tk.Frame(main, bg="#f4f6f9")
search_frame.pack(anchor="w", padx=30, pady=(5, 10))

tk.Label(search_frame,
         text="Name / Student Code:",
         font=("Arial", 11, "bold"),
         bg="#f4f6f9",
         fg="#1f2933").pack(side="left")

search_entry = tk.Entry(search_frame,
                        font=("Arial", 11),
                        width=22)

search_entry.pack(side="left", padx=10)

tk.Button(search_frame,
          text="Search",
          font=("Arial", 10, "bold"),
          bg="#1f3a5f",
          fg="white",
          cursor="hand2",
          activebackground="#2d4f7c",
          activeforeground="white",
          command=search).pack(side="left")

search_entry.bind("<Return>", lambda event: search())


#Output box 
output_frame = tk.Frame(main, bg="#f4f6f9")
output_frame.pack(expand=True, fill="both", padx=30, pady=(0, 25))

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output = tk.Text(output_frame,
                 font=("Arial", 11),
                 wrap="word",
                 bg="#ffffff",
                 fg="#1f2933",
                 padx=15,
                 pady=15,
                 yscrollcommand=scrollbar.set)

output.pack(side="left", expand=True, fill="both")

scrollbar.config(command=output.yview)


rawStudents=loadRawStudents(MARKS_FILE)
showOutput("Choose an option above.")

root.mainloop()
