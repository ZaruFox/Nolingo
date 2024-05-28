from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Question:
    def __init__(self, driver):
        self.questionData = ""
        self.answer = ""
        self.driver = driver

    @classmethod
    def createQuestion(cls, questionType, driver):
        # initializes correct question type class given duolingo's question type
        questionsMap = {"challenge challenge-select": SelectionQuestion}

        if questionType in questionsMap:
            return questionsMap[questionType](driver)
        raise Exception("Question Type not found")


    def recordAnswer(self):
        # saves answer to self.answer, only use when self.isWrong() is true.
        self.answer = self.driver.find_element(By.CSS_SELECTOR, "div._2jz5U.o-3Ru").text
        return True

    def isWrong(self):
        # returns True if current question is wrong
        try:
            self.driver.find_element(By.XPATH, "//img[@src='https://d35aaqx5ub95lt.cloudfront.net/images/bd13fa941b2407b4914296afe4435646.svg']")
            return True
        except:
            return False
        
    def clickNext(self):
        self.driver.find_element(By.XPATH, "//button[@data-test='player-next']").click()

    def solve(self):
        # uses child class definition
        pass

    def guess(self):
        # use child class definition
        pass    

    def recordQuestion(self):
        # uses child class definition
        pass    
    
    def __repr__(self):
        return f"Question Type: {type(self).questionType}\nQuestion: {self.questionData}\nAnswer: {self.answer}"
    
    
class SelectionQuestion(Question):
    questionType = "Selection"
    def recordQuestion(self):
        self.questionData = self.driver.find_element(By.XPATH, "//h1[@data-test='challenge-header']/span").text

    def guess(self):
        self.driver.find_element(By.CSS_SELECTOR, "span._1NM0v").click()
        self.clickNext()

    def solve(self):
        self.driver.find_element(By.XPATH, f"//span[text()='{self.answer}']")
        self.clickNext()