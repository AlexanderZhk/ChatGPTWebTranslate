from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import ChatGPTHandler
import tkinter as tk
from tkinter import *
import GUI
import threading
from DeepLHandler import DeepLHandlerC
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ChatGPT = ChatGPTHandler.ChatGPTHandlerC()
    root = Tk()
    window = GUI.ChatWindow(root,ChatGPT)
    ChatGPT_start_thread = threading.Thread(target=ChatGPT.start)
    ChatGPT_start_thread.start()
    root.mainloop()


    inputtext = 8

    Deepl = DeepLHandlerC()
    Deepl.start("English","Russian")
    #GUI.RunGUI(Deepl)
    while inputtext !="e":
        inputtext = input()
        translatedtext = Deepl.translate(inputtext,1)
        ChatGPTAnswer = ChatGPT.Query(translatedtext)
        print( Deepl.translate(ChatGPTAnswer,0))
    input()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
