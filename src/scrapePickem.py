import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

loginUrl = "https://www.nfl.com/account"
url = "http://weeklypickem.fantasy.nfl.com/group/152180"
week = 10
# users = ["VernacularRaptor", "Kzprzn", "ndjolt02", "Dick_Beaterson"]
numPeople = 7

def main():
   scores = []
   driver = webdriver.Chrome()

   logIn(driver)

   # Go to Weekly
   navigateToWeek(driver)

   for i in range(1, numPeople+1):
      time.sleep(1)
      xpath = '//*[@id="group-entries"]/div/div/div[2]/table/tbody/tr[{0}]/td[2]/a'.format(i)
      user = driver.find_element_by_xpath(xpath).text.split("'")[0]
      score = getScore(driver, xpath)
      scores.append(tuple([str(user), score]))

   print scores

   driver.quit()

def logIn(driver):
   driver.get(loginUrl)

   emailBox = driver.find_element_by_id("fanProfileEmailUsername").send_keys("EMAIL_HERE")
   pwBox = driver.find_element_by_id("fanProfilePassword").send_keys("PW_HERE")
   driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div/div/div[2]/main/div/div[2]/div[2]/form/div[3]/button').click()
   time.sleep(1)
   
   
def navigateToWeek(driver):
   driver.get(url)

   # Click on weekly
   driver.find_element_by_css_selector("#group-entries > div > div.bd > div.section-header > div.widget-wrap > div > a:nth-child(2)").click()
   time.sleep(0.5)

   currentWeek = driver.find_element_by_css_selector("#group-entries > div > div.bd > div.section-header > div.week-selector.selector > span.label").text
   weekText = currentWeek.split(" ")
   weekNum = int(weekText[1])

   if(weekNum == week):
      print "Current Week!"
   else:
      driver.find_element_by_css_selector("#group-entries > div > div.bd > div.section-header > div.week-selector.selector > span.btn-wrap > span").click()
      time.sleep(0.1)
      
      driver.find_element_by_class_name("week-selector").find_element_by_class_name("menu").find_element_by_css_selector("ul > li:nth-child({0}) > a".format(week)).click()
      time.sleep(0.4)

def getScore(driver, xpath):
   driver.find_element_by_xpath(xpath).click()
   # WebDriverWait(driver, 3).until(expected_conditions.text_to_be_present_in_element((By.XPATH, '//*[@id="primary-inner"]/div[1]/div/div[2]/h1'), "WEEK {0} PICKS".format('\[0-9]+')))
   WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="primary-inner"]/div[1]/div/div[2]/h1')))
   time.sleep(0.3)
   weekHeader = driver.find_element_by_xpath('//*[@id="primary-inner"]/div[1]/div/div[2]/h1')
   weekNum = str(weekHeader.text).split(" ")[1]
   backCount = 0
   
   while(int(weekNum) != week):
      back = driver.find_element_by_xpath('//*[@id="primary-inner"]/div[1]/div/div[2]/a[1]').click()

      WebDriverWait(driver, 10).until(expected_conditions.text_to_be_present_in_element((By.XPATH, '//*[@id="primary-inner"]/div[1]/div/div[2]/h1'), str(int(weekNum)-1)))
      weekHeader = driver.find_element_by_xpath('//*[@id="primary-inner"]/div[1]/div/div[2]/h1')
      weekNum = str(weekHeader.text).split(" ")[1]
      backCount += 1

   games = driver.find_elements_by_class_name("pick-module")
   correct = 0
   incorrect = 0

   for game in games:
      slider = game.find_element_by_xpath('//*[@id="{0}"]/div[1]/div[2]'.format(game.get_property("id")))
      sliderText = slider.get_attribute("class")
      if sliderText.find("slider-incorrect") != -1:
         # print "incorrect {0}".format(sliderText)
         incorrect += 1
      elif sliderText.find("slider-correct") != -1:
         # print "correct {0}".format(sliderText)
         correct += 1
      else:
         incorrect += 1

   for i in range(backCount):
      driver.back()

   driver.back()
   
   # driver.back()
   # time.sleep(0.3)
   # driver.back()
   # return tuple([str(user), correct])
   return correct
   


if __name__ == "__main__":
    main()