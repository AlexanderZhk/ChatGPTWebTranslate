from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import threading





class DeepLHandlerC:


    def __init__(self):
        # create a ChromeOptions instance
        options = Options()
        # set the headless mode to False to run the browser in GUI mode
        options.headless = False
        # create a webdriver instance with the ChromeOptions
        self.driver_norm = webdriver.Chrome(options=options)
        self.driversource = 0
        self.drivertarget = 0
        self.driver_reverse = webdriver.Chrome(options=options)
        self.start_flag = False
        self.state = "Initializing"

    def SetLanguageInDriver(self, driver, Language0, Language1):
        sourcelanguageClass = driver.find_element(By.CLASS_NAME, "lmt__language_select--source")
        sourcelanguageSelected = sourcelanguageClass.find_element(By.CLASS_NAME, "lmt__language_select__active__title")
        if sourcelanguageSelected.text != "English":
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
        if targetlanguageSelected.text != "Russian":
            targetlanguageClass.click()
            time.sleep(1)
            targetlanguageDropdown = driver.find_element(By.CLASS_NAME, "lmt__language_wrapper")

            targetlanguageDropdownRus = targetlanguageDropdown.find_element(By.XPATH,
                                                                            "//button[contains(., '" + Language1 + "')]")
            image = targetlanguageDropdownRus.screenshot_as_png
            with open("targetlanguageDropdownEnglish.png", "wb") as f:
                f.write(image)
            targetlanguageDropdownRus.click()

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

