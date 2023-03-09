from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
word = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    words_dict = original_data.to_dict(orient="records")
else:
    words_dict = data.to_dict(orient="records")

def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = choice(words_dict)
    front.itemconfig(card_title, text="French", fill="black")
    front.itemconfig(card_word, text=word["French"], fill="black")
    front.itemconfig(card_background, image=front_card)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    front.itemconfig(card_title, text="English", fill="white")
    front.itemconfig(card_word, text=word["English"], fill="white")
    front.itemconfig(card_background, image=back_card)

def is_known():
    words_dict.remove(word)
    data = pandas.DataFrame(words_dict)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, func=flip_card)

front_card = PhotoImage(file="card_front.png")
front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = front.create_image(400, 263, image=front_card)
front.grid(row=0, column=0, columnspan=2)

back_card = PhotoImage(file="card_back.png")

right_button_image = PhotoImage(file="right.png")
right_button = Button(image=right_button_image, bg=BACKGROUND_COLOR, width=90, height=90, highlightthickness=0, borderwidth=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_button_image = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_button_image, bg=BACKGROUND_COLOR, width=90, height=90, highlightthickness=0,borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

card_title = front.create_text(400, 150, text="", font=("Impact", 40, "italic"))
card_word = front.create_text(400, 263, text="", font=("Impact", 60, "bold"))

next_card()

window.mainloop()