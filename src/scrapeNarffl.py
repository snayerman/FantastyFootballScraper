import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

url = "http://www.narffl.com/games/accuracy_challenge"
users = ["VernacularRaptor", "Kzprzn", "ndjolt02", "Dick_Beaterson"]

def main():
   driver = webdriver.Chrome()
   driver.get(url)

   searchBox = driver.find_element_by_css_selector("#cumulative-table_filter > label > input")
   scores = getScores(searchBox, driver)
   return zip(users, scores)
   # print scores

   driver.quit()

def getScores(searchBox, driver):
   scores = []

   for user in users:
      searchBox.clear()
      searchBox.send_keys(user)
      WebDriverWait(driver, 100).until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "#cumulative-table > tbody > tr:nth-child(1) > td:nth-child(1)"), user))
      score = driver.find_element_by_css_selector("#cumulative-table > tbody > tr > td:nth-child(3)")
      scores.append(int(score.text))
   
   return scores
   

if __name__ == "__main__":
    main()