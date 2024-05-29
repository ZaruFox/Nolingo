from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Question:
    questionType = "Base Question"
    allQuestions = {}

    def __init__(self, driver):
        self.driver = driver
        self.questionData = ""
        self.answer = ""
        self.recordQuestion()

    @classmethod
    def getQuestion(cls, newQuestionType, driver):
        # initializes correct question type class given duolingo's question type
        # OR if question was seen before, return the question object

        questionsMap = {"challenge challenge-dialogue": GapFillQuestion, "challenge challenge-listenIsolation": ListenQuestion, "challenge challenge-select": SelectionQuestion, "challenge challenge-translate": TranslationQuestion, "challenge challenge-listenTap": ListenQuestion, "challenge challenge-tapComplete": TapCompleteQuestion, "challenge challenge-match": MatchQuestion, "challenge challenge-assist": AssistQuestion, "challenge challenge-listenMatch": ListenQuestion, "challenge challenge-speak": ListenQuestion, "challenge challenge-listenComplete": ListenQuestion, "challenge challenge-completeReverseTranslation": TextTranslationQuestion, "challenge challenge-gapFill": GapFillQuestion}
        if newQuestionType not in questionsMap:
            raise Exception(f"Question Type not found: {newQuestionType}")
        
        newQuestion = questionsMap[newQuestionType](driver)
        if str(newQuestion) in cls.allQuestions:
            return cls.allQuestions[str(newQuestion)]
        cls.allQuestions[str(newQuestion)] = newQuestion
        return newQuestion

    def recordAnswer(self):
        # saves answer to self.answer, only use when self.isWrong() is true.
        self.answer = self.driver.find_element(By.CSS_SELECTOR, "div._2jz5U.o-3Ru").text
        return True

    def isWrong(self):
        # returns True if current question is wrong
        element = self.driver.find_element(By.XPATH, "//div[@class='_1k6eg']")
        return element.get_attribute("data-test") == "blame blame-incorrect"
        
    def clickNext(self):
        self.driver.find_element(By.XPATH, "//button[@data-test='player-next']").click()

    def answerQuestion(self):
        if self.answer:
            self.solve()
        else:
            self.guess()

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
    
    def __str__(self):
        return f"{type(self).questionType}{self.questionData}"
    
    
class SelectionQuestion(Question):
    questionType = "Selection"
    def recordQuestion(self):
        self.questionData = self.driver.find_element(By.XPATH, "//h1[@data-test='challenge-header']/span").text

    def guess(self):
        self.driver.find_element(By.XPATH, "//div[@data-test='challenge-choice']").click()
        self.clickNext()

    def solve(self):
        self.driver.find_element(By.XPATH, f"//span[text()='{self.answer}']").click()
        self.clickNext()


class TranslationQuestion(Question):
    questionType = "Translation"
    def recordQuestion(self):
        tmp = self.driver.find_elements(By.XPATH, "//span[@class='_5HFLU']/span/span")
        self.questionData = "".join([x.text for x in tmp])
        
    def guess(self):
        self.driver.find_element(By.XPATH, "//span[@data-test='challenge-tap-token-text']").click()
        self.clickNext()

    def solve(self):
        # matches largest choice to target string
        choices = self.driver.find_elements(By.XPATH, "//span[@data-test='challenge-tap-token-text']")
        choices.sort(key=lambda x:len(x.text), reverse=True)
        target = " ".join([s.strip(",.!?:;") for s in self.answer.split()])

        i = 0
        while i < len(target):
            if target[i] == " ":
                i += 1

            for j, choice in enumerate(choices):
                if choice.text == target[i:i+len(choice.text)]:
                    choice.click()
                    i += len(choice.text)
                    choices.pop(j)
                    break
        self.clickNext()


class ListenQuestion(Question):
    questionType = "Listen"
    def guess(self):
        # just skip the question
        self.driver.find_element(By.XPATH, "//button[@data-test='player-skip']").click()


class TapCompleteQuestion(Question):
    questionType = "Tap Complete"
    def recordQuestion(self):
        sentence = self.driver.find_elements(By.XPATH, "//span[@class='_5HFLU']/span/span")

        for ele in sentence:
            if ele.text == "":
                self.questionData += " "
            else:
                self.questionData += ele.text

        self.questionData = self.questionData.strip(".!?")

    def guess(self):
        [x.click() for x in self.driver.find_elements(By.XPATH, "//div[@data-test='word-bank']/div/span/button/span/span[@data-test='challenge-tap-token-text']")]
        self.clickNext()

    def solve(self):
        choices = self.driver.find_elements(By.XPATH, "//div[@data-test='word-bank']/div/span/button/span/span[@data-test='challenge-tap-token-text']")
        choices.sort(key=lambda x:len(x.text), reverse=True)
        self.answer = self.answer.strip(".?!")

        i = 0
        j = 0
        while i < len(self.answer) and j < len(self.questionData):
            if self.answer[i] == self.questionData[j]:
                i += 1
                j += 1
            else:
                for k, choice in enumerate(choices):
                    if choice.text == self.answer[i:i+len(choice.text)]:
                        choice.click()
                        i += len(choice.text)
                        choices.pop(k)
                        break

        self.clickNext()

class MatchQuestion(Question):
    questionType = "Match"
    def guess(self):
        choices = self.driver.find_elements(By.CSS_SELECTOR, "span button")
        choices1 = choices[:len(choices)//2]
        choices2 = choices[len(choices)//2:]
        for c1 in choices1:
            for c2 in choices2:
                if c2.get_attribute("aria-disabled") == "false":
                    c1.click()
                    c2.click()

                if c1.get_attribute("aria-disabled") == "true":
                    break
        
class AssistQuestion(Question):
    questionType = "Assist"
    def recordQuestion(self):
        self.questionData = self.driver.find_element(By.CSS_SELECTOR, "div._2L10X").text
    def guess(self):
        self.driver.find_element(By.XPATH, "//span[@data-test='challenge-judge-text']").click()
        self.clickNext()
    def solve(self):
        self.driver.find_element(By.XPATH, f"//span[@data-test='challenge-judge-text'][text()='{self.answer}']").click()
        self.clickNext()

class TextTranslationQuestion(Question):
    questionType = "TextTranslation"
    def recordQuestion(self):
        try:
            toggle = self.driver.find_element(By.XPATH, "//button[@data-test='player-toggle-keyboard']")
            if "harder" in toggle.text.lower():
                toggle.click()
        except:
            pass

        tmp = self.driver.find_elements(By.XPATH, "//span[@class='_5HFLU']/span/span")
        self.questionData = "".join([x.text for x in tmp])

    def guess(self):
        textarea = self.driver.find_element(By.XPATH, "//textarea[@data-test='challenge-translate-input']")
        textarea.send_keys("a")
        self.clickNext()

    def solve(self):
        textarea = self.driver.find_element(By.XPATH, "//textarea[@data-test='challenge-translate-input']")
        textarea.send_keys(self.answer)
        self.clickNext()

class GapFillQuestion(AssistQuestion):
    def recordQuestion(self):
        tmp = self.driver.find_elements(By.XPATH, "//span[@class='_5HFLU']/span/span")
        self.questionData = "".join([x.text for x in tmp])