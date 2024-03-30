from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

YELLOW = "#f7f5dd"
GREEN = "#9bdeac"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
           'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def gen_password():
    pw_entry.delete(0, END)
    nr_letters = random.randint(8, 12)
    nr_symbols = random.randint(1, 3)
    nr_numbers = random.randint(1, 3)

    password_list = []
    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = web_entry.get()
    email = email_entry.get()
    password = pw_entry.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }
    if len(website)*len(password) == 0:
        messagebox.showinfo(message="Please don't leave any fields empty!", title="Failed")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        web_entry.delete(0, END)
        pw_entry.delete(0, END)
# ----------------------- SEARCH FOR A PASSWORD ----------------------- #


def find_password():
    website = web_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            if website in data:
                email = data[website]["Email"]
                password = data[website]["Password"]
                messagebox.showinfo(message=f"Email: {email}\n Password: {password}", title=website)
            else:
                messagebox.showerror(title="Error!", message="No such website")
    except FileNotFoundError:
        messagebox.showinfo(title="Error!", message="No data file found!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
web_label = Label(text="Website:", bg=YELLOW, font=("Courier", 10))
web_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg=YELLOW, font=("Courier", 10))
email_label.grid(row=2, column=0)

pw_label = Label(text="Password: ", bg=YELLOW, font=("Courier", 10))
pw_label.grid(row=3, column=0)

# Buttons
gen_button = Button(text="Generate", width=15, command=gen_password, bg=YELLOW)
gen_button.grid(column=2, row=3)

search_button = Button(text="Search", width=15, command=find_password, bg=YELLOW)
search_button.grid(column=2, row=1)

add_button = Button(text="Add", width=36, command=add_password, bg=YELLOW)
add_button.grid(column=1, row=4, columnspan=2)

# Entries
web_entry = Entry(width=24)
web_entry.focus()
web_entry.grid(column=1, row=1)

email_entry = Entry(width=43)
email_entry.insert(0, "email@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

pw_entry = Entry(width=24)
pw_entry.grid(column=1, row=3)

window.mainloop()
