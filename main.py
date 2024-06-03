from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from questiontypes import *

# print colours
RED = "\033[1;31;40m"
GREEN = "\033[1;32;40m"
YELLOW = "\033[1;33;40m"

def main():
    # init driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)

    # open up Duo
    driver.get("https://www.duolingo.com")
    try:
        element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button._1Qh5D._36g4N._2YF0P.-TeUZ._2Ccfj'))
            )
    except:
        print(f"{RED}Unable to access Duolingo. Exiting..")
        exit(0)

    # navigate to login page and login
    element.click()
    login(driver)

    sleep(1)
    # start a lesson
    while True:
        try:
            driver.find_element(By.XPATH, "//div[text()='OPEN']").click()
        except:
            pass

        # detect type of lesson
        isStoryLesson = driver.find_element(By.XPATH, "(//button[@class='_3vGNs _2YF0P _1333i _22TV_ _3Jm09']/img[@class='_1B6UH'])[last()]").get_attribute("src") == "https://d35aaqx5ub95lt.cloudfront.net/images/path/icons/7aa61c3f60bd961a60a46fb36e76c72f.svg"
        
        driver.get("https://www.duolingo.com/lesson")
        print(f"{YELLOW}Starting Lesson..")
        if not isStoryLesson:
            complete_normal_lesson(driver)
        else:
            complete_story_lesson(driver)

        print(f"{GREEN}Lesson Complete!")
        driver.get("https://www.duolingo.com/learn")
        sleep(0.5)
    


def login(driver):
    # get account details
    print(f"{YELLOW}Please login to your Schools Duolingo account. Ensure you are not using a Google/Facebook account.")
    if "duo-user" in os.environ and "duo-pass" in os.environ:
        print(f"{GREEN}Logining in...")
        username = os.environ["duo-user"]
        password = os.environ["duo-pass"]
    else:
        print(f"{YELLOW}To auto-login, add 'duo-user' and 'duo-pass' to env. However, this is not recommended for security concerns.")
        username = input("Username/Email: ")
        password = input("Password: ")

    # login
    driver.find_element(By.ID, "web-ui1").send_keys(username)
    sleep(0.05)
    driver.find_element(By.ID, "web-ui2").send_keys(password)
    sleep(0.05)
    driver.find_element(By.CSS_SELECTOR, 'button.WxjqG._1x5JY._1M9iF._36g4N._2YF0P._1QN-w').click()

    # detect the login
    try:
        WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/learn'][@class='_1Mak3']"))
            )
    except:
        print(f"{RED}Login Failed. Exiting..")
        exit(0)
        
    print(f"{GREEN}Logged In!\n")



def complete_normal_lesson(driver):
    # wait for lesson to load
    try:
        skipButton = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-test='player-next']/span"))
            )
    except:
        print(f"{RED}Lesson load timed out. Exiting..")
        exit(0)

    # get pass challange screen if it shows up
    if "start challenge" in skipButton.text.lower():
        skipButton.click()

    while True:
        sleep(0.45)
        # skip if it is transition screen
        if (skipButton := driver.find_element(By.XPATH, "//button[@data-test='player-next']/span")).text.lower() == "continue":
            skipButton.click()
            continue

        # detect question type
        questionContainer = driver.find_element(By.CSS_SELECTOR, 'div._1fxa4._1Mopf')
        questionType = questionContainer.get_attribute("data-test")

        # solve question
        print(f"{YELLOW}Reading question...")
        question = Question.getQuestion(questionType, driver)
        print(f"{YELLOW}Answering question...")
        question.answerQuestion()
        sleep(0.25)

        if question.isWrong():
            question.recordAnswer()
            print(f"{RED}Question answered wrongly, question saved as:\n{repr(question)}\n")
        else:
            print(f"{GREEN}Question answered correctly!\n")
        question.clickNext()

        # if progress bar is full, break out of the loop
        if driver.find_element(By.XPATH, "//div[@aria-valuemax='1']").get_attribute("aria-valuenow") == "1":
            break

    # wait for duolingo to finish loading
    WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, "//button[@data-test='player-next']/span"), "CONTINUE")
        )
    
def complete_story_lesson(driver):
    # wait for lesson to load
    try:
        skipButton = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-test='player-next']/span"))
            )
    except:
        print(f"{RED}Lesson load timed out. Exiting..")
        exit(0)

    # get pass challange screen if it shows up
    if "start challenge" in skipButton.text.lower():
        skipButton.click()

if __name__ == "__main__":
    main()