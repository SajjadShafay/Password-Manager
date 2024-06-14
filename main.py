import tkinter
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = ([random.choice(letters) for _ in range(random.randint(8, 10))] +
                     [random.choice(numbers) for _ in range(random.randint(2, 4))] +
                     [random.choice(symbols) for _ in range(random.randint(2, 4))])  # list comprehension
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)  # Automatically copy password


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        tkinter.messagebox.showinfo(message="Please complete all fields!")
    else:
        try:
            with open('data.json', mode='r') as file:
                #Reading old data
                data = json.load(file)
                #Updating old data with new data
                data.update(new_data)
        except FileNotFoundError:
            data = new_data
        finally:
            with open('data.json', mode='w') as file:
                # Saving updated data
                json.dump(data, file, indent=4)
                website_entry.delete(0, tkinter.END)
                password_entry.delete(0, tkinter.END)


# ---------------------------- SEARCH LOGIN DETAILS ----------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open('data.json', mode='r') as file:
            data = json.load(file)

            username = data[website]['username']
            password = data[website]['password']
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title='Error', message="No data file found")
    except KeyError:
        tkinter.messagebox.showinfo(title='Error', message="No details for the website exist")#
    else:
        tkinter.messagebox.showinfo(title=website, message=f"username: {username}\n"
                                                           f"password: {password}")

# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=35, pady=35)

canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
logo_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = tkinter.Label(text="Website:    ")
website_label.grid(column=0, row=1)
username_label = tkinter.Label(text="Email/Username:    ")
username_label.grid(column=0, row=2)
password_label = tkinter.Label(text="Password:  ")
password_label.grid(column=0, row=3)

website_entry = tkinter.Entry(width=33)
website_entry.grid(column=1, row=1, pady=3)
website_entry.focus()  # App will start with entry box already selected to type in
username_entry = tkinter.Entry(width=52)
username_entry.grid(column=1, row=2, columnspan=2, pady=3)
username_entry.insert(0, "shafaysajjad@outlook.com")  # app will start with email entry already filled.
password_entry = tkinter.Entry(width=33)
password_entry.grid(column=1, row=3, pady=3)

search_button = tkinter.Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)
generate_password_button = tkinter.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = tkinter.Button(text="Add", width=44, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, pady=3)

window.mainloop()
