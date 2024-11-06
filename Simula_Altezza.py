from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time

# Dati di accesso aggiornati al 18/10/2024
USERNAME = "90513786"
PASSWORD = "Martellini6++"

# Step 1: Set up the WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
driver = webdriver.Chrome(options=chrome_options)

# Step 2: Navigate to the login page
login_url = "https://www2.autostrade.it/BVS/newUE/menu.jsp"
driver.get(login_url)

# Step 3: Enter the login credentials
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.XPATH, "//input[@name='password']")

username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

# Step 4: Submit the login form
login_button = driver.find_element(By.ID, "login-button")
login_button.click()

# Step 5: Wait for the dashboard or main page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "principale2"))  # Replace with an element that confirms login
)

# Step 6: Now that we're logged in, simulation

# Navigate to the route selection page (if necessary)
# <a href="javascript:goto('./informativa.jsp?tipo=3');"><img src="img/simula.gif" border="0"><span> Nuova simulazione</span></a>
new_simulation_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:goto('./informativa.jsp?tipo=3');\"]"))
)
new_simulation_button.click()

driver.switch_to.frame("contenuto")

# Step 6.1: Click on the "Read the Info" button to open the privacy info modal
read_info_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='JavaScript:leggi();']"))
)
read_info_button.click()

# passiamo alla nuova finestra
original_window = driver.current_window_handle
all_windows = driver.window_handles

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

for handle in all_windows:
        driver.switch_to.window(handle)
        print(f"Window Handle: {handle}, URL: {driver.current_url}")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Accetta le condizioni
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

# First step of the simulation
# Wait for the table to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:document.forms[0].azione.value='3';checkValidForm(false,'A', '1');\"]"))
)

# Here we compile the table porcoddio
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
input_element.send_keys("6")

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

# Wait a bit to ensure that the action is completed
time.sleep(2)

# Second step of the simulation
# refresh del frame
driver.switch_to.default_content()
driver.switch_to.frame("contenuto")
# data inizio validità
date_begin_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:document.forms[0].dataFineValidita.value='';calIniVal.popup(document.forms[0].dataInizioValidita.value, '../');\"]")
date_begin_button.click()

# passiamo alla nuova finestra
original_window = driver.current_window_handle
all_windows = driver.window_handles

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

for handle in all_windows:
        driver.switch_to.window(handle)
        print(f"Window Handle: {handle}, URL: {driver.current_url}")
new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)


#determina data (quindici giorni da oggi)
today = datetime.today()
#un po' di casistica per passare al mese successivo
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
# Click on the date
date_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//a[font/text()='{target_date_str}']"))
)
date_element.click()
time.sleep(2)
driver.switch_to.window(original_window)
driver.switch_to.frame("contenuto")

#calcola data fine validità
date_end_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:if(transformStringToDate($('dataNuovoMetodo').value)<transformStringToDate(document.forms[0].dataInizioValidita.value))setFinDateNewMode('S');else setFinDate('S');\"]")
date_end_button.click()

# Open the route selection modal
route_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:nuovoPercorso();\"]")
route_button.click()
#cambia finestra
original_window = driver.current_window_handle
all_windows = driver.window_handles

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

new_window = [handle for handle in all_windows if handle != original_window][0]
driver.switch_to.window(new_window)

route_start_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:openNuovaRete('optionsFrom','E',0);\"]")
route_start_button.click()

# Qui facciamo inserire la partenza all'utente

print("Almeno il percorso tu lo puoi inserire te. E anche inviare il modulo dopo.")
input()  # Wait for user input before proceeding

exit()
