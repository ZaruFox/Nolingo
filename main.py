from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    driver.find_element(By.PARTIAL_LINK_TEXT, 'START').click()
    input()
    


def login(driver):
    # ask user to login
    print(f"{YELLOW}Please login to your Schools Duolingo account. Ensure you are not using a Google/Facebook account.")
    username = driver.find_element(By.ID, "web-ui1")
    username.send_keys(input("Username/Email: "))
    password = driver.find_element(By.ID, "web-ui2")
    password.send_keys(input("Password: "))
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


if __name__ == "__main__":
    main()