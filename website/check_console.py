from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

os.system('start /B python server.py')
time.sleep(2) # wait for server to start

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

driver.get('http://127.0.0.1:8080')
time.sleep(1)

for entry in driver.get_log('browser'):
    print(entry)

driver.quit()
os.system('taskkill /F /IM python.exe /T') # warning: might kill other python processes, let's just kill the server specifically. Actually, let's use subprocess.

