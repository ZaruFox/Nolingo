from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# print colours
RED = "\033[1;31;40m"
GREEN = "\033[1;32;40m"
YELLOW = "\033[1;33;40m"

# open up Duolingo
driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://www.duolingo.com")
assert "Duolingo" in driver.title

# navigate to login page
driver.find_element(By.CSS_SELECTOR, 'button._1Qh5D._36g4N._2YF0P.-TeUZ._2Ccfj').click()

# ask user to login
print(f"{YELLOW}Please login to your Schools Duolingo account. Ensure you are not using a Google/Facebook account.")
username = driver.find_element(By.ID, "web-ui1")
username.send_keys(input("Username/Email: "))
password = driver.find_element(By.ID, "web-ui2")
password.send_keys(input("Password: "))
driver.find_element(By.CSS_SELECTOR, 'button.WxjqG._1x5JY._1M9iF._36g4N._2YF0P._1QN-w').click()

# detect the login
try:
    element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/learn'][@class='_1Mak3']"))
        )
except:
    print(f"{RED}Login Failed.")
    exit(0)
    
print(f"{GREEN}Logged In!")
input()