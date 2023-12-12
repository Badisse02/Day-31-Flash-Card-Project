from tkinter import *
from pandas import *
from random import *
ident = 0
key = 0
value = 0
word = {}
data = []
BACKGROUND_COLOR = "#B1DDC6"
try:
    data = read_csv("data/words_to_learn.csv")
    if len(data) == 0:
        data = read_csv("data/french_words.csv")
except FileNotFoundError:
    data = read_csv("data/french_words.csv")
    print(len(data))
finally:
    french_words = data.French.to_list()
    english_words = data.English.to_list()
    words = [{french_words[i]: english_words[i]} for i in range(len(french_words))]


def counter(n):
    count = n
    if count >= 0:
        window.after(1000, counter, count - 1)


def display_answer(x):
    counter(3)
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(language, text="English", fill="white", font=("ariel", 40, "italic"))
    canvas.itemconfig(canvas_word, text=f"{x}", fill="white", font=("ariel", 60, "bold"))


def click_button():
    global ident, key, value, word
    try:
        window.after_cancel(ident)
    except ValueError:
        pass
    finally:
        canvas.itemconfig(canvas_image, image=front_card)
        word = choice(words)
        for item in word:
            key = item
            value = word[key]
        canvas.itemconfig(language, text="French", fill="black", font=("ariel", 40, "italic"))
        canvas.itemconfig(canvas_word, text=f"{key}", fill="black", font=("ariel", 60, "bold"))
        ident = window.after(3000, display_answer, value)


def right_button():
    try:
        words.remove(word)
    except ValueError:
        pass
    finally:
        click_button()


def wrong_button():
    click_button()


window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
back_card = PhotoImage(file="images/card_back.png")
front_card = PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_card)
canvas.grid(row=1, column=1, columnspan=2)
language = canvas.create_text(400, 150, text="Welcome to the Flash Card Game", font=("ariel", 20, "italic"))
canvas_word = canvas.create_text(400, 263, text="Press any button to start the game", font=("ariel", 30, "bold"))


right_pic = PhotoImage(file="images/right.png")
right_button = Button(image=right_pic, highlightthickness=0, bg=BACKGROUND_COLOR, command=right_button)
right_button.grid(row=2, column=2)

wrong_pic = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_pic, highlightthickness=0, bg=BACKGROUND_COLOR, command=wrong_button)
wrong_button.grid(row=2, column=1)


window.mainloop()
french_words = []
english_words = []
for dic in words:
    for key in dic:
        french_words.append(key)
        english_words.append(dic[key])
unknown_words = {
    "French": french_words,
    "English": english_words,
}
df = DataFrame(unknown_words)
df.to_csv("data/words_to_learn.csv", index=False)
