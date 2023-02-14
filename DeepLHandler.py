from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import threading

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class DeepLHandlerC:


    def __init__(self):
        # create a ChromeOptions instance
        self.options = Options()
        # set the headless mode to False to run the browser in GUI mode
        self.options.headless = True
        self.options2 = Options()
        self.options2.headless= True
        # create a webdriver instance with the ChromeOptions
        self.driver_norm = uc.Chrome(options=self.options)
        self.driversource = 0
        self.drivertarget = 0
        self.driver_reverse = uc.Chrome(options=self.options2)
        self.start_flag = False
        self.state = "Initializing"
        self.availablelanguages = ["Russian"]

    def SetLanguageInDriver(self, driver, Language0, Language1):
        sourcelanguageClass = driver.find_element(By.CLASS_NAME, "lmt__language_select--source")
        sourcelanguageSelected = sourcelanguageClass.find_element(By.CLASS_NAME, "lmt__language_select__active__title")
        if sourcelanguageSelected.text != Language0:
            sourcelanguageClass.click()
            time.sleep(2)
            sourcelanguageDropdown = driver.find_element(By.CLASS_NAME, "lmt__language_wrapper")

            sourcelanguageDropdownEnglish = sourcelanguageDropdown.find_element(By.XPATH,
                                                                                "//button[contains(., '" + Language0 + "')]")
            image = sourcelanguageDropdownEnglish.screenshot_as_png
            with open("sourcelanguageDropdownEnglish.png", "wb") as f:
                f.write(image)
            sourcelanguageDropdownEnglish.click()
        print(sourcelanguageSelected.text)

        targetlanguageClass = driver.find_element(By.CLASS_NAME, "lmt__language_select--target")
        targetlanguageSelected = targetlanguageClass.find_element(By.CLASS_NAME, "lmt__language_select__active__title")
        if targetlanguageSelected.text != Language1:
            targetlanguageClass.click()
            time.sleep(1)
            targetlanguageDropdown = driver.find_element(By.CLASS_NAME, "lmt__language_wrapper")

            targetlanguageDropdownRus = targetlanguageDropdown.find_element(By.XPATH,
                                                                            "//button[contains(., '" + Language1 + "')]")
            image = targetlanguageDropdownRus.screenshot_as_png
            with open("targetlanguageDropdownEnglish.png", "wb") as f:
                f.write(image)
            targetlanguageDropdownRus.click()
    def getlanguages(self):
        targetlanguageClass = WebDriverWait(self.driver_reverse, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "lmt__language_select--target")))
        sourcelanguageClass = WebDriverWait(self.driver_norm, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "lmt__language_select--source")))
        targetlanguageClass.click()
        sourcelanguageClass.click()
        time.sleep(1)
        sourcelanguageelements =  [element.text for element in self.driver_reverse.find_elements(By.XPATH, "//button[contains(@dl-test, 'translator-lang-option')]")]
        targetlanguageelements = [element.text for element in self.driver_reverse.find_elements(By.XPATH, "//button[contains(@dl-test, 'translator-lang-option')]")]
        while len(targetlanguageelements) == 0:
            try:
                targetlanguageelements = [element.text for element in self.driver_reverse.find_elements(By.XPATH, "//button[contains(@dl-test, 'translator-lang-option')]")]
            except:
                pass

            self.driver_reverse.get("https://www.deepl.com/translator")
            targetlanguageClass = WebDriverWait(self.driver_reverse, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lmt__language_select--target")))
            targetlanguageClass.click()
        sourcelanguages = []
        for element in sourcelanguageelements:
            print(element,"src")
            sourcelanguages.append(element)
        targetlanguages = []
        for element in targetlanguageelements:
            print(element,"trgt")
            targetlanguages.append(element)
        targetlanguages1 = []
        sourcelanguages1 = []
        for string in sourcelanguages:
            sourcelanguages1.append(string.split(" ")[0])
        for string in targetlanguages:
            targetlanguages1.append(string.split(" ")[0])
        bothwaylanguages = list(set(sourcelanguages1) & set(targetlanguages1))
        print(bothwaylanguages)
        self.availablelanguages = bothwaylanguages

    def start(self,sourcelanguage,targetlanguage):
        if self.start_flag == True:
            return
        self.start_flag = True
        self.state = "Starting"
        self.driversource = sourcelanguage
        self.drivertarget = targetlanguage
        # load the web page, click cookies
        self.driver_norm.get("https://www.deepl.com/translator")
        self.driver_reverse.get("https://www.deepl.com/translator")
        self.getlanguages()
        time.sleep(44)
        BothDrivers = [self.driver_norm,self.driver_reverse]
        for driver in BothDrivers:
            try:
                button = driver.find_element("xpath", "/html/body/div[8]/div/div/div/span/div[2]/button[1]")
                print(button)
                button.click()
            except:
                pass
            textinput = 0
            # wait till text area loaded
            while textinput == 0:
                try:
                    textinput = driver.find_element("xpath",
                                                              "/html/body/div[4]/main/div[5]/div[1]/div[2]/section[1]/div[3]/div[2]/d-textarea")
                    # textinput.send_keys("Hello, this is a test")
                except:
                    time.sleep(1)

        self.state = "Setting DeepL languages"
        self.SetLanguageInDriver(self.driver_norm,sourcelanguage,targetlanguage)
        self.SetLanguageInDriver(self.driver_reverse, targetlanguage,sourcelanguage)
        self.state = "Ready"
        self.start_flag = False


    def translate(self,text,reverse):
        driver = 0
        self.state = "Translating"
        if reverse == 1:
            driver = self.driver_reverse
        else:
            driver =self.driver_norm
        textarea = driver.find_element(By.XPATH,
                                                 "//d-textarea[@dl-test='translator-source-input']/div[@contenteditable='true']")
        textarea.clear()
        textarea.send_keys(text)
        time.sleep(2)
        textarea = driver.find_element(By.XPATH,
                                                 "//d-textarea[@dl-test='translator-target-input']/div[@contenteditable='true']")
        text = textarea.text
        self.state = "Ready"
        return text

