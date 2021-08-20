from tkinter import *
from tkinter import filedialog
import threading
import time
import os
from email_finder import email_finder
from excel_generator import excel_utils


def run_email_finder(search, name, folder):
    button.config(state=DISABLED)
    button2.config(state=DISABLED)

    # Running email finder
    search = str(search)
    name = str(name)
    database_path = folder + "/" + name

    finder = email_finder(search, database_path, 2)
    finder.store_emails()
    excel_utils = excel_utils()
    excel_utils.generate_excel_from_sqlite3_db(database_path + ".db", database_path + ".xlsx")

    # email finder has finished
    button.config(state=NORMAL)
    button2.config(state=NORMAL)


def hola():
    x = threading.Thread(target=run_email_finder, args=(search.get(), name.get(), folder_path.get(),))
    x.start()


def browse_button():
    # Allow user to select a directory and store it in global var called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)

    if len(filename) > 0:
        button.config(state=NORMAL)


# This file won0't show a terminal behind the application because it has the extension *.pyw
root = Tk()
root.title("Emails finder")
root.resizable(0, 0)

search = StringVar()
name = StringVar()
folder_path = StringVar()

Label(root, text="Hola JuanPe, estas son las instrucciones blabla bla bla bla").grid(row=1, columnspan=3, sticky="w")

# Search row
search_text = Label(root, text="Búsqueda")
search_text.grid(row=2, column=0, sticky="w")

search_entry = Entry(root, textvariable=search)
search_entry.grid(row=2, column=1)

# Excel name row
name_text = Label(root, text="Nombre")
name_text.grid(row=3, column=0, sticky="w")

name_entry = Entry(root, textvariable=name)
name_entry.grid(row=3, column=1)

# Browse button
lbl1 = Label(master=root, textvariable=folder_path)
lbl1.grid(row=4, column=1)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=4, column=3)

# Start button
button = Button(root, text="Empezar", command=hola)
button.grid(row=5, column=3)
button.config(state=DISABLED)
button.config(state=DISABLED)

# abort_button

root.mainloop()  # It starts the loop application mode
