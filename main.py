import json
from time import sleep

# Used in order to bypass cloudflare's protection from bots
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# CREDENTIALS
email = 'YOUR EMAIL HERE'
password = 'YOUR PASSWORD HERE'

# VESSEL NAME LIST
vessels = ['KRITI VIGOR', 'DALI', 'QUEEN MARY 2', 'EVER GIVEN', 'QUEEN ELIZABETH', 'ECLIPSE', 'OASIS OF THE SEAS',
           'TIME BANDIT', 'DISNEY MAGIC']


def findVesselInfo(search_bar, vessel_name):
    imo = ''
    mmsi = ''
    speed = ''
    course = ''
    search_bar.send_keys(vessel_name)
    sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'body > div.MuiDialog-root.MuiModal-root.css-126xj0f > '
                                         'div.MuiDialog-container.MuiDialog-scrollPaper.css-16u656j > div > '
                                         'div.mtapp4 > div.simplebar-wrapper > div.simplebar-mask > div > div > div > '
                                         'div > li:nth-child(1) > a').click()
    sleep(5)
    table_rows = driver.find_elements(By.TAG_NAME, 'tr')
    for row in table_rows:
        try:
            if row.find_element(By.TAG_NAME, 'th').text == 'IMO':
                imo = row.find_element(By.TAG_NAME, 'td').text
            elif row.find_element(By.TAG_NAME, 'th').text == 'MMSI':
                mmsi = row.find_element(By.TAG_NAME, 'td').text
            elif row.find_element(By.TAG_NAME, 'th').text == 'Speed':
                speed = row.find_element(By.TAG_NAME, 'td').text
            elif row.find_element(By.TAG_NAME, 'th').text == 'Course':
                course = row.find_element(By.TAG_NAME, 'td').text
        except NoSuchElementException:
            continue
        if imo and mmsi and speed and course:
            break
    return {'name': vessel_name, 'imo': imo, 'mmsi': mmsi, 'speed': speed, 'course': course}


def getSearchBar(driver):
    driver.find_element(By.ID, 'searchMarineTraffic').click()
    sleep(2)
    return driver.find_element(By.ID, 'searchMT')


if __name__ == '__main__':
    scrapped_data = []
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)

    driver.get("https://www.marinetraffic.com")

    sleep(5)
    driver.find_element(By.ID, 'login').click()
    sleep(2)

    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login_form_submit').click()
    sleep(5)

    for vessel in vessels:
        search_bar = getSearchBar(driver)
        scrapped_data.append(findVesselInfo(search_bar, vessel))
        driver.back()
        sleep(3)

    with open('output.json', 'w', encoding='utf-8') as output:
        json.dump(scrapped_data, output, ensure_ascii=False, indent=4)
    driver.quit()
