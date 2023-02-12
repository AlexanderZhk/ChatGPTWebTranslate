from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import json

def save_list_of_dicts(file_name, the_list):
    with open(file_name, 'w') as f:
        json.dump(the_list, f)

def load_list_of_dicts(file_name):
    with open(file_name, 'r') as f:
        try:
            loaded_list = json.load(f)
        except:
            print("Error cookie load")
            return [0]
    return loaded_list

import time

class ChatGPTHandlerC:

    def __init__(self):
        self.options = Options()
        # set the headless mode to False to run the browser in GUI mode
        self.options.headless = False
        self.options.add_argument("--app=https://chat.openai.com/chat")
        self.options.add_argument("--incognito")
        self.options.add_argument('--disable-blink-features=AutomationControlled')

        # create a webdriver instance with the ChromeOptions
        self.driver = uc.Chrome(options=self.options)
    def start(self):

        self.driver.get("https://chat.openai.com/chat")
        cookieslist = load_list_of_dicts("cookies.txt")
        for d in cookieslist:
            try:
                self.driver.add_cookie(d)
            except:
                print("FAIL COOKIE",d)

        self.driver.set_window_size(800, 600)
        found = 0
        while found == 0:
            try:
                element = self.driver.find_element(By.XPATH, "//*[text()='Clear conversations']")
                print("Element with the text 'Clear Conversations' is present on the page")
                found = 1

                NextButtons = 1
                while NextButtons == 1:
                    time.sleep(1)
                    try:
                        element = self.driver.find_element(By.XPATH,
                                                      "//div[@id='headlessui-dialog-:r0:' and @role='dialog']")
                        self.driver.execute_script("arguments[0].remove();", element)
                        print("click")
                    except:
                        NextButtons=0
                        print(self.driver.get_cookies())
                        save_list_of_dicts("cookies.txt",self.driver.get_cookies())
                        print(type(self.driver.get_cookies()))
                #self.driver.minimize_window()
            except:
                print("Element with the text 'Clear Conversations' is not present on the page")
                time.sleep(1)

    def Query(self,text):
        try:
            textarea = self.driver.find_element(By.XPATH, "//textarea")
            textarea.clear()
            textarea.send_keys(text)
            textarea.send_keys(Keys.RETURN)
        except:
            url = self.driver.current_url
            self.driver.get(url)
            return "Error"
        generating = True
        answer = "Internal Application Error"
        time.sleep(3)
        while generating == True:
            print("11")
            elements = self.driver.find_elements(By.XPATH,'//*[@class="markdown prose w-full break-words dark:prose-invert light"]')
            if elements:
                try:
                    self.driver.find_element(By.XPATH,'//*[@class="text-2xl"]')
                except:
                    generating = False
                answer = elements[-1].text
                print("4")
            time.sleep(1)
            try:
                element = self.driver.find_element(By.XPATH,
                                                   '//*[text()="An error occurred. If this issue persists please contact us through our help center at help.openai.com."')
                url = self.driver.current_url
                self.driver.get(url)
            except:
                pass
            try:
                element = self.driver.find_element(By.XPATH,
                                                   '//*[text()="Too many requests in 1 hour. Try again later."')
                answer = "Too many requests in 1 hour. Try again later."
                after = ""
            except:
                pass
        #print(answer)


        with open("elements.txt", "w") as f:
            for element in elements:
                # Get the element's XPath
                # Get the element's text and class name
                element_text = element.text
                class_name = element.get_attribute('class')
                # Write the element text and class name to the file
                f.write(f'Element Text: {element_text}\nClass Name: {class_name}\n\n')
        return answer

