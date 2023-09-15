from tkinter import *
from tkinter import messagebox as mb
import json

root = Tk()
root.geometry("800x500")
root.title("Quiz")

with open('quiz.json') as f:
    obj = json.load(f)

q = obj['ques']
options = obj['options']
a = obj['ans']

# Time limit per question (in seconds)
time_limit = 25  # 2 minutes

# The actual quiz class can be regarded as the main
class Quiz:
    def __init__(self):
        self.qn = 0
        self.opt_selected = IntVar()
        self.ques = self.question(self.qn)
        self.opts = self.radiobtns()
        self.display_options(self.qn)
        self.buttons()
        self.correct = 0
        self.timer_label = Label(root, text="Time Left: 120", font=("times", 16))
        self.timer_label.place(x=600, y=10)
        self.timer_seconds = time_limit
        self.update_timer()

    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.config(text=f"Time Left: {self.timer_seconds}")
            root.after(1000, self.update_timer)
        else:
            self.display_result()

    def question(self, qn):
        t = Label(root, text="CodifyLearn", width=50, bg="blue", fg="white",
                  font=("times", 20, "bold"))
        t.place(x=0, y=2)
        qn = Label(root, text=q[qn], width=60, font=("times", 16, "bold"), anchor="w")
        qn.place(x=70, y=100)
        return qn

    def radiobtns(self):
        val = 0
        b = []
        yp = 150
        while val < 4:
            btn = Radiobutton(root, text=" ", variable=self.opt_selected, value=val + 1, font=("times", 14))
            b.append(btn)
            btn.place(x=100, y=yp)
            val += 1
            yp += 40
        return b

    def display_options(self, qn):
        val = 0
        self.opt_selected.set(0)
        self.ques["text"] = q[qn]
        for op in options[qn]:
            self.opts[val]["text"] = op
            val += 1

    def buttons(self):
        nbutton = Button(root, text="Next", command=self.nextbtn, width=10, bg="green", fg="white",
                         font=("times", 16, "bold"), activebackground="dark green")  # Set button color and hover effect
        nbutton.place(x=200, y=380)
        quitbutton = Button(root, text="Quit", command=root.destroy, width=10, bg="red", fg="white",
                            font=("times", 16, "bold"), activebackground="dark red")  # Set button color and hover effect
        quitbutton.place(x=380, y=380)

    def checkans(self, qn):
        if self.opt_selected.get() == a[qn]:
            return True

    def nextbtn(self):
        if self.checkans(self.qn):
            self.correct += 1
        self.qn += 1
        self.timer_seconds = time_limit  # Reset the timer for the next question
        self.timer_label.config(text=f"Time Left: {self.timer_seconds}")
        if self.qn == len(q):
            self.display_result()
        else:
            self.display_options(self.qn)

    def display_result(self):
        score = int(self.correct / len(q) * 100)
        if score >= 80:
            result = "Score: " + str(score) + "%"
            wc = len(q) - self.correct
            correct = "No. of correct answers: " + str(self.correct)
            wrong = "No. of wrong answers:" + str(wc)
            first = "Congratulations, you passed"
            mb.showinfo("Result", "\n".join([result, correct, wrong, first]))
        else:
            result = "Score: " + str(score) + "%"
            wc = len(q) - self.correct
            correct = "No. of correct answers: " + str(self.correct)
            wrong = "No. of wrong answers:" + str(wc)
            second = "You failed!"
            mb.showinfo("Result", "\n".join([result, correct, wrong, second]))
        root.destroy()

# Initialize the quiz
quiz = Quiz()

root.mainloop()
