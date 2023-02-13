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
    Deepl = DeepLHandlerC()
    window = GUI.ChatWindow(root,ChatGPT,Deepl)
    ChatGPT_start_thread = threading.Thread(target=ChatGPT.start)
    DeepL_start_thread = threading.Thread(target=Deepl.start,args=("English","Russian",))
    ChatGPT_start_thread.start()
    DeepL_start_thread.start()
    root.mainloop()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
