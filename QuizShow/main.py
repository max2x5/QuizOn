import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk

import data

def start_quiz():
    global data_set, current_question, score

    # Determine the selected category
    if bioVar.get():
        data_set = data.bio_data
    elif chemVar.get():
        data_set = data.chem_data
    elif rapVar.get():
        data_set = data.rap_data
    else:
        messagebox.showwarning("Uwaga", "Wybierz kategorię")
        return

    # Destroy the image label
    img_label.destroy()

    # Hide the menu button and start button
    mb.place_forget()
    start_btn.place_forget()
    root.geometry(f"620x600")


    # Initialize the quiz variables
    current_question = 0
    score = 0
    score_label.config(text="Wynik: 0/{}".format(len(data_set)))

    # Show the quiz elements
    qs_label.pack(pady=10)
    for btn in choice_btns:
        btn.pack(pady=5)
    feedback_label.pack(pady=10)
    score_label.pack(pady=10)
    next_btn.pack(pady=10)

    show_question()

def check_answer(choice):
    global score
    question = data_set[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
        score += 1
        score_label.config(text="Wynik: {}/{}".format(score, len(data_set)))
        feedback_label.config(text="Poprawna odpowiedź", foreground="green")
    else:
        feedback_label.config(text="Niepoprawna odpowiedź", foreground="red")

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

def next_question():
    global current_question
    current_question += 1

    if current_question < len(data_set):
        show_question()
    else:
        # Clear all the widgets
        for btn in choice_btns:
            btn.pack_forget()
        qs_label.pack_forget()
        feedback_label.pack_forget()
        next_btn.pack_forget()
        score_label.pack_forget()
        messagebox.showinfo("Quiz Zakończony", "Wynik końcowy: {}/{}".format(score, len(data_set)))
        root.destroy()


def show_question():
    bg_label.place(relwidth=1, relheight=1)
    question = data_set[current_question]
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal")

    feedback_label.config(text="")
    next_btn.config(state="disable")

# Create the main window
root = tk.Tk()
root.title("Quiz On")

# Block the window resizing
root.resizable(False, False)

# Load the logo and background using PIL
image = Image.open("assets/logo2.png")
photo = ImageTk.PhotoImage(Image.open("assets/logo2.png"))
background = ImageTk.PhotoImage(Image.open("assets/background.png"))

# Set the window size to the image size
image_width, image_height = image.size
root.geometry(f"{image_width}x{image_height}")

# Create a Label widget to display the image
img_label = tk.Label(root, image=photo)
img_label.pack()

# Set the window icon
icon = tk.PhotoImage(file="assets/logo2.png")
root.iconphoto(False, icon)

# Set the theme style
style = Style(theme="flatly")

# Create a menu
mb = tk.Menubutton(root, text="Kategoria", relief=tk.RAISED)
mb.menu = tk.Menu(mb, tearoff=0)
mb["menu"] = mb.menu

bioVar = tk.IntVar()
chemVar = tk.IntVar()
rapVar = tk.IntVar()
mb.menu.add_checkbutton(label="Biologia", variable=bioVar)
mb.menu.add_checkbutton(label="Chemia", variable=chemVar)
mb.menu.add_checkbutton(label="Rap", variable=rapVar)

bg_label = tk.Label(root, image=background)

# Position the menu button
mb.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Start button
start_btn = ttk.Button(root, text="Start", command=start_quiz)

# Position the start button slightly below the menu button
start_btn.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

# Configure the font size
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 18))

# Create the question label
qs_label = ttk.Label(root, anchor="center", wraplength=600, padding=10)

# Create the choice buttons
choice_btns = []
for i in range(4):
    button = ttk.Button(root, command=lambda i=i: check_answer(i))
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(root, anchor="center", padding=10)


# Initialize the score
score = 0

# Create the score label
score_label = ttk.Label(root, text="Wynik: 0", anchor="center", padding=10)

# Create next button
next_btn = ttk.Button(root, text="Następne pytanie", command=next_question, state="disable")

# Initialize the current position index
current_question = 0

# Start the main event loop
root.mainloop()
