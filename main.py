from tkinter import *
from tkinter import messagebox
import pyperclip
import json

TEXT = None
EMAIL = ""

# Password Generator
def generated_password():
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)
    if len(entry3.get()) == 0:
        entry3.insert(END, password)
    else:
        entry3.delete(0, END)
        entry3.insert(END, password)

# Copy the Password
def copy():
    pyperclip.copy(entry3.get())
    pyperclip.paste()

# Tkinter Screen
window = Tk()
window.title("Password Manager")
window.config(padx=70, pady=30)

# Image
canvas = Canvas(width=200, height=200)
image = PhotoImage(file="<ENTER YOUR IMAGE FILE LOCATION>")
canvas.create_image(100, 100, image=image)
canvas.grid(column=0, row=0, columnspan=3)

def enter(_):
    entry3.focus()
    canvas.itemconfig(TEXT, text="")

window.bind('<Return>', enter)

# Label's
text1 = Label(text="Website:", font=('Arial', 10, 'normal'))
text1.grid(column=0, row=1)
text2 = Label(text="Email/Username:", font=('Arial', 10, 'normal'))
text2.grid(column=0, row=2)
text3 = Label(text="Password:", font=('Arial', 10, 'normal'))
text3.grid(column=0, row=3)

# Entry's
entry1 = Entry(width=21)
entry1.focus()
entry1.grid(column=1, row=1)
entry2 = Entry(width=41)
entry2.insert(END, EMAIL)
entry2.grid(columnspan=2, column=1, row=2)
entry3 = Entry(width=21)
entry3.grid(column=1, row=3)

# To add the data into text file
def record_data():
    global TEXT
    website = entry1.get().capitalize()
    email = entry2.get()
    password = entry3.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning("Warning", "Please don't leave any of the fields empty!")
        entry1.delete(0, END)
        entry3.delete(0, END)
        entry1.focus()
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            entry1.delete(0, END)
            entry3.delete(0, END)
            entry1.focus()
            TEXT = canvas.create_text(100, 190, text="Data Saved Successfully", fill="green2", font=("Courier", 10, "bold"))

# To find the email and password of the desire website
def find_password():
    try:
        with open("data.json") as data:
            file_data = json.load(data)
            email = file_data[entry1.get().capitalize()]["email"]
            password = file_data[entry1.get().capitalize()]["password"]
            messagebox.askquestion(title=entry1.get().capitalize(), message=f"Email: {email} \n\nPassword: {password}")
    except TypeError:
        messagebox.showwarning(title="Data Not Found", message="No Data File Found")
    except KeyError:
        messagebox.showwarning(title="Empty Field", message="Your Website Field is Empty")

# Button's
button1 = Button(text="Generate Password", width=15, command=generated_password)
button1.grid(column=2, row=3)
button2 = Button(text="Copy Password", width=17, command=copy)
button2.grid(column=1, row=4)
button3 = Button(text="Add", width=34, command=record_data)
button3.grid(columnspan=2, column=1, row=5)
button4 = Button(text="Search", width=15, command=find_password)
button4.grid(column=2, row=1)

mainloop()