from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time

#Login data
USERNAME = "your_username"
PASSWORD = "your_password"

# The default view of chrome used by webdriver always asks to choose a search engine. This is disabled for better user-experience
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the login page and insert credentials
login_url = "https://www2.autostrade.it/BVS/newUE/menu.jsp"
driver.get(login_url)

# The different use of XPATH or ID is simply motivated by trial and error
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.XPATH, "//input[@name='password']")

username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

login_button = driver.find_element(By.ID, "login-button")
login_button.click()


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "principale2"))  # principale2 is the name of a form in the homepage
)

# Navigate to simulation page

new_simulation_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:goto('./informativa.jsp?tipo=3');\"]"))
)
new_simulation_button.click()

driver.switch_to.frame("contenuto")

# Before every simulation there is a privacy info modal that has to be red
read_info_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='JavaScript:leggi();']"))
)
read_info_button.click()

# Privacy info is in a new window
original_window = driver.current_window_handle
all_windows = driver.window_handles

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

for handle in all_windows:
        driver.switch_to.window(handle)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Doesn't work without scrolling

# Accept the conditions of use
accept_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='JavaScript:goAction();']"))
)
accept_button.click()

time.sleep(2)

driver.switch_to.window(original_window)
driver.switch_to.frame("contenuto")

proceed_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='JavaScript:goAction();']"))
)
proceed_button.click()

time.sleep(2)

# First step of the simulation: insert general info about the vehicles and of the convoy (dimensions, weight etc.)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:document.forms[0].azione.value='3';checkValidForm(false,'A', '1');\"]"))
)

# Here we compile the table. These are standard values chosen in such a way that the only exception (in terms of exceptional transports) is the height
input_element = driver.find_element(By.NAME, "mTara")
input_element.send_keys("8,52")

input_element = driver.find_element(By.NAME, "rTara")
input_element.send_keys("10,67")

input_element = driver.find_element(By.NAME, "mAssiNum")
input_element.send_keys("2")

input_element = driver.find_element(By.NAME, "rAssiNum")
input_element.send_keys("3")

input_element = driver.find_element(By.NAME, "mLength")
input_element.send_keys("6")

input_element = driver.find_element(By.NAME, "rLength")
input_element.send_keys("16")

input_element = driver.find_element(By.NAME, "mWidth")
input_element.send_keys("2,55")

input_element = driver.find_element(By.NAME, "rWidth")
input_element.send_keys("2,55")

input_element = driver.find_element(By.NAME, "mWeight")
input_element.send_keys("17,50")

input_element = driver.find_element(By.NAME, "rWeight")
input_element.send_keys("22,50")

input_element = driver.find_element(By.NAME, "veicMaxLength")
input_element.send_keys("19")

input_element = driver.find_element(By.NAME, "veicMaxWidth")
input_element.send_keys("2,55")

input_element = driver.find_element(By.NAME, "veicMaxHeight")
input_element.send_keys("6") # This is a very high value. We want to trigger all possible alerts on the route

input_element = driver.find_element(By.NAME, "sporgAnt")
input_element.send_keys("0")

input_element = driver.find_element(By.NAME, "sporgPost")
input_element.send_keys("0")

input_element = driver.find_element(By.NAME, "floorHeight")
input_element.send_keys("1")

input_element = driver.find_element(By.NAME, "veicMaxSpeedCarta")
input_element.send_keys("65")

time.sleep(2)

next1_button = driver.find_element(By.XPATH, "//a[text()='Successiva']")
next1_button.click()


time.sleep(2)

# Second step of the simulation: select start/end dates and route

driver.switch_to.default_content()
driver.switch_to.frame("contenuto") # refreshing the content
# Here we insert start and end date
date_begin_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:document.forms[0].dataFineValidita.value='';calIniVal.popup(document.forms[0].dataInizioValidita.value, '../');\"]")
date_begin_button.click()

# Calendar options are in a new window
original_window = driver.current_window_handle
all_windows = driver.window_handles

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

for handle in all_windows:
        driver.switch_to.window(handle)
        print(f"Window Handle: {handle}, URL: {driver.current_url}") # Just for debug
new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)


# It is better to set the start date in the future. Reason: transports are planned in advance and there could be already scheduled worksites
today = datetime.today()

if today.day > 13:
    # Click the "next month" button
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='next month']"))
    )
    next_button.click()
    if today.month == 12:
        target_date = today.replace(year=today.year + 1, month=1, day=15)
    else:
        target_date = today.replace(month=today.month + 1, day=15)
    next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//img[@alt='next month']"))
    )
else:
    # Set the target date to the 15th of the current month
    target_date = today.replace(day=15)

# Convert the target day to string (for matching with calendar elements)
target_date_str = str(target_date.day)
print (str(target_date_str))
date_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//a[font/text()='{target_date_str}']"))
)
date_element.click()
time.sleep(2)
driver.switch_to.window(original_window)
driver.switch_to.frame("contenuto")

# The website offers the option to automatically determine the end date
date_end_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:if(transformStringToDate($('dataNuovoMetodo').value)<transformStringToDate(document.forms[0].dataInizioValidita.value))setFinDateNewMode('S');else setFinDate('S');\"]")
date_end_button.click()

# Open the route selection modal
route_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:nuovoPercorso();\"]")
route_button.click()
# Here we switch to the new window
original_window = driver.current_window_handle
all_windows = driver.window_handles

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

route_start_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:openNuovaRete('optionsFrom','E',0);\"]")
route_start_button.click()

# Here we have the only part of the compilation that the user has to define: the desired route

print("Almeno il percorso tu lo puoi inserire te. E anche inviare il modulo dopo.")
input()  # Wait for user input before proceeding

exit()
