from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import requests
from time import sleep
import sys

def process(website):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path='geckodriver')
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://transparencyreport.google.com/safe-browsing/search")
    except WebDriverException:
        for i in range(3):
            try:
                WebDriverWait(driver, 10).until(EC.title_is('Google Safe Browsing – Google Laporan Transparansi'))
                break
            except TimeoutException:
                driver.get("https://transparencyreport.google.com/safe-browsing/search")
    try:
        sleep(2)
        driver.find_element(By.XPATH , "/html/body/app/site-layout/mat-sidenav-container/mat-sidenav-content/safe-browsing-report/ng-component/section/div/search-box/input").send_keys(website)
        sleep(2)
        driver.find_element(By.XPATH , '/html/body/app/site-layout/mat-sidenav-container/mat-sidenav-content/safe-browsing-report/ng-component/section/div/search-box/i').click()
    except NoSuchElementException:
        sleep(2)
        driver.get("https://transparencyreport.google.com/safe-browsing/search")  
    try:
        try:
            first_result = wait.until( presence_of_element_located((By.XPATH, "/html/body/app/site-layout/mat-sidenav-container/mat-sidenav-content/safe-browsing-report/ng-component/site-status-result/report-section/section/div/data-tile/div[2]/span")) )
            fix_result = first_result.get_attribute('textContent')
            driver.delete_all_cookies()
            driver.close()
            driver.quit()
            return(fix_result)
        except:
                driver.close()
                driver.quit()
                return ('RF')
    except:
        driver.close()
        driver.quit()

while(True):
    try:
        list = open('list.txt','r')
        emailnya = list.readline()
    except Exception as Err:
        print('Pastiin ada list websitenya tanpa https:// ')
        sys.exit()



    loop = 1
    for line in list:
        result = process(line)
        print(result)
        if line != "\n":
            if result == 'No unsafe content found':
                print("AMAN")
                pass
            # jika mokad
            elif result == 'This site is unsafe':
                # print("RF")
                text = f"RF{line}"
                TOKEN = "1448616115:AAF4nYNFAf6Gib_fJtEXLKcHCQvEYwP37kY"
                chat_id = "-1001568937743"
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
                # print(url)
                r = requests.get(url)
                pass
            elif result == 'No available data':
                print("KOSONG")
                pass
            else :
                print("ERROR")
                pass
            loop += 1

        print('done')
        sleep(60)
    sleep(60)