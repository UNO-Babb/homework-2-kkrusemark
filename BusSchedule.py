#BusSchedule.py
#Name: Kylie Krusemark
#Date: 10/21/25
#Assignment: Homework 2

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def getHours(time):
  """
  Take a time in the format "HH:MM AM" and return hour in 24-hour format"
  """
  splitTime = time.split(":") #separates hours from minutes
  hour = int(splitTime[0])

  #determine AM or PM
  if "PM" in time and hour != 12:
    hour = hour + 12
  elif "AM" in time and hour == 12:
    hour = 0

  return hour 

def getMinutes(time):
  """Take a time in the format "HH:MM AM" and returns just the minutes"""
  splitTime = time.split(":")
  minutePart = splitTime[1] #should get MM AM or MM PM

  #cycle through minutePart and only get the numbers
  minutes = ""
  for ch in minutePart:
    if ch.isdigit():
      minutes = minutes + ch

  return int(minutes)

def isLater(time1, time2) :
  """determine if next stop time is later than current time"""
  h1 = getHours(time1)
  m1 = getMinutes(time1)
  h2 = getHours(time2)
  m2 = getMinutes(time2)

  if h1 > h2:
    return True
  elif h1 == h2 and m1 > m2:
    return True
  else:
    return False

def main():

  stopNumber = 1151
  routeNumber = 8
  direction = "WEST"

  #get the date automatically
  today = datetime.date.today()
  date = str(today)

  url = "https://myride.ometro.com/Schedule?stopCode=" + str(stopNumber) + "&date=" + date + "&routeNumber=" + str(routeNumber) + "&directionName=" + str(direction)
  
  c1 = loadURL(url) #loads the web page
  #c1 = loadTestPage() #loads the test page

#split all words in text page
  words = c1.split()

#find word that looks like a time, using : and AM/PM as determining factors
  times = []
  for word in words:
    if ":" in word and ("AM" in word or "PM" in word) :
      times.append(word)

#get current time
  now = datetime.datetime.now()
  currentHour = (now.hour - 5) % 24
  currentMinute = now.minute

#figure out AM or PM
  meridiem = "AM"
  if currentHour >= 12:
    meridiem = "PM"
  if currentHour > 12:
    displayHour = currentHour - 12
  elif currentHour == 0:
    displayHour = 12
  else:
    displayHour = currentHour

  #ensure 0 zero shows before minutes if needed
  if currentMinute < 10:
    displayMinute = "0" + str(currentMinute)
  else:
    displayMinute = str(currentMinute)

  currentTime = str(displayHour) + ":" + displayMinute + " " + meridiem
  print("Current Time: " + currentTime)

#Find next bus
  upcoming = []
  for t in times:
    if isLater(t, currentTime):
      upcoming.append(t)
  
#find minutes until arrival

  def minutesUntil(busTime, currentTime):
    """returns how many minutes from current time to bus time"""
    busHour = getHours(busTime)
    busMinute = getMinutes(busTime)
    currHour = getHours(currentTime)
    currMinute = getMinutes(currentTime)

    totalBusMins = busHour * 60 + busMinute
    totalCurrMins = currHour * 60 + currMinute

    return totalBusMins - totalCurrMins

#find specific bus minutes away
  if len(upcoming) >=1:
    nextBus = upcoming[0]
    minsAway = minutesUntil(nextBus, currentTime)
    print("The next bus will arrive in " + str(minsAway) + " minutes.")
  else:
    print("No more buses today.")
  
  if len(upcoming) >= 2:
    nextBus2 = upcoming[1]
    minsAway2 = minutesUntil(nextBus2, currentTime)
    print("The following bus will arrive in " + str(minsAway2) + " minutes.")

  
main()
