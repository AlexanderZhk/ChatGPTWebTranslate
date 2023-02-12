import tkinter as tk
from tkinter import *

class ChatWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Window")
        self.master.geometry("400x600")

        chatframe= tk.Frame(master)
        chatframe.pack(side=tk.BOTTOM)

        self.scrollbar = Scrollbar(chatframe)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_area = Text(chatframe, height=20, width=45, yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill=BOTH)
        self.text_area.config(state=DISABLED)

        self.scrollbar.config(command=self.text_area.yview)

        self.entry = Entry(chatframe, width=45)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.user_message)

        self.send_button = Button(chatframe, text="Send", command=self.user_message)
        self.send_button.pack()

    def user_message(self,event=None):
        message = self.entry.get()
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, "You: " + message + "\n")
        self.text_area.config(state=DISABLED)
        self.entry.delete(0, END)
        self.text_area.see(END)
