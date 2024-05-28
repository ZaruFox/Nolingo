from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Question:
    questionType = "Question Base Class"
    def __init__(self, driver):
        self.questionData = ""
        self.answer = ""
        self.driver = driver

    def recordAnswer(self):
        # saves answer to self.answer, only use when self.isWrong() is true.
        self.answer = self.driver.find_element(By.CSS_SELECTOR, "div._2jz5U.o-3Ru").getText()
        return True

    def isWrong(self):
        # returns True if current question is wrong
        try:
            self.driver.find_element(By.XPATH, "//img[@src='https://d35aaqx5ub95lt.cloudfront.net/images/bd13fa941b2407b4914296afe4435646.svg']")
            return True
        except:
            return False

    def solve(self):
        # uses child class definition
        pass

    def trial(self):
        # uses child class definition
        pass    

    def getQuestion(self):
        # uses child class definition
        pass    

    def __hash__(self):
        return hash(self.questionData)
    
    def __repr__(self):
        return f"Question Type: {type(self).questionType}\nQuestion: {self.questionData}\nAnswer: {self.answer}"
    
    
