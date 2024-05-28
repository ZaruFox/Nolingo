from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

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

    # start a lesson
    driver.find_element(By.CSS_SELECTOR, 'div._1DLP9._27IMa').click()
    sleep(0.5)
    driver.find_element(By.XPATH, "//a[@href='/lesson']").click()
    complete_lesson(driver)
    input()
    


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
    driver.find_element(By.ID, "web-ui2").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button.WxjqG._1x5JY._1M9iF._36g4N._2YF0P._1QN-w').click()

    # detect the login
    try:
        WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/learn'][@class='_1Mak3']"))
            )
    except:
        print(f"{RED}Login Failed. Exiting..")
        exit(0)
        
    print(f"{GREEN}Logged In!")

def complete_lesson(driver):
    # wait for lesson to load
    try:
        WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-test='quit-button']"))
            )
    except:
        print(f"{RED}Lesson load timed out. Exiting..")
        exit(0)

    # detect question type
    questionContainer = driver.find_element(By.CSS_SELECTOR, 'div._1fxa4._1Mopf')
    questionType = questionContainer.get_attribute("data-test")

if __name__ == "__main__":
    main()