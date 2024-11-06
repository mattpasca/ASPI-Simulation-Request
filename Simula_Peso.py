import lxml
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import time


# I. Parsing della trasmissione ASPI

# Dati convoglio da estrarre (riprendo i nomi dal xml)
class Veicolo:
    def __init__(self, tara, numAssi, lungh, largh, portataUtile, massaCarico, pesoRim, massaRalla):
        # Initialize instance variables
        self.tara = tara
        self.numAssi = numAssi
        self.lungh = lungh
        self.largh = largh
        self.portataUtile = portataUtile
        self.massaCarico = massaCarico
        self.pesoRim = pesoRim
        self.massaRalla = massaRalla

    def __repr__(self):
        return f"Veicolo(tara={self.tara}, numAssi={self.numAssi}, lungh={self.lungh}, largh={self.largh}, portataUtile={self.portataUtile}, massaCarico={self.massaCarico}, pesoRim={self.pesoRim}, massaRalla={self.massaRalla})"

class Asse:
    def __init__(self, tipo, massa, distanza):
        self.tipo = tipo
        self.massa = massa
        self.distanza = distanza

    def __repr__(self):
        return f"Asse(tipo={self.tipo}, massa={self.massa}, distanza={self.distanza})"

class Convoglio:
    def __init__(self, lungMax, largMax, altMax, massa, altTerra, spoAnt, spoPos, velCC):
        self.lungMax = lungMax
        self.largMax = largMax
        self.altMax = altMax
        self.massa = massa
        self.altTerra = altTerra
        self.spoAnt = spoAnt
        self.spoPos = spoPos
        self.velCC = velCC

# Funzioni di estrazione
#Assi
def estrai_assi(file_xml):
    tree = ET.parse(file_xml)
    root = tree.getroot()

    assi = []

    # Estraiamo sottotipi
    for assi_elem in root.findall('.//assi'):
        tipo = assi_elem.find('tipo').text
        massa = float(assi_elem.find('massa').text)
        distanza = assi_elem.find('distanza').text

        assi.append(Asse(tipo=tipo, massa=massa, distanza = distanza))

    return assi

# Veicoli
def estrai_veicoli(file_xml):
    tree = ET.parse(file_xml)
    root = tree.getroot()

    veicoli = []

    # Estraiamo sottotipi
    for datiVeicolo_elem in root.findall('.//datiVeicolo'):
        tara = float(datiVeicolo_elem.find('tara').text)
        numAssi = int(datiVeicolo_elem.find('numAssi').text)
        lungh = float(datiVeicolo_elem.find('lungh').text)
        largh = float(datiVeicolo_elem.find('largh').text)
        portataUtile = float(datiVeicolo_elem.find('portataUtile').text)
        massaCarico = datiVeicolo_elem.find('massaCarico')
        massaCarico_value = float(massaCarico.text) if massaCarico is not None else 0.0
        pesoRim = float(datiVeicolo_elem.find('pesoRim').text)
        massaRalla = datiVeicolo_elem.find('massaRalla')
        massaRalla_value = float(massaRalla.text) if massaRalla is not None else 0.0 # Semirimorchio

        veicoli.append(Veicolo(tara=tara, numAssi=numAssi, lungh=lungh, largh=largh, portataUtile=portataUtile, massaCarico=massaCarico_value, pesoRim=pesoRim, massaRalla=massaRalla_value))

    return veicoli

# Convoglio
def estrai_convoglio(file_xml):
    tree = ET.parse(file_xml)
    root = tree.getroot()

    convoglio = []

    # Estraiamo sottotipi
    for totaliVeicolo_elem in root.findall('.//totaliVeicolo'):
        lungMax = float(totaliVeicolo_elem.find('lungMax').text)
        largMax = float(totaliVeicolo_elem.find('largMax').text)
        altMax = float(totaliVeicolo_elem.find('altMax').text)
        massa = float(totaliVeicolo_elem.find('massa').text)
        altTerra = float(totaliVeicolo_elem.find('altTerra').text) #tanto ET segna sempre 0
        spoAnt = float(totaliVeicolo_elem.find('spoAnt').text)
        spoPos = float(totaliVeicolo_elem.find('spoPos').text)
        velCC = int(totaliVeicolo_elem.find('velCC').text)

        convoglio.append(Convoglio(lungMax=lungMax, largMax=largMax, altMax=altMax, massa=massa, altTerra=altTerra, spoAnt=spoAnt, spoPos=spoPos, velCC=velCC))

    return convoglio

file_xml = 'trasmissione.xml'
assi_lista = estrai_assi(file_xml)
print (*assi_lista)
veicoli_lista = estrai_veicoli(file_xml)
convoglio_lista = estrai_convoglio(file_xml)

# Calcoliamo il peso su trattore e su Semirimorchio
peso_trattore = 0.0
peso_rimorchio = 0.0

for i in range(veicoli_lista[0].numAssi):
    peso_trattore += assi_lista[i].massa

for i in range(veicoli_lista[0].numAssi, veicoli_lista[0].numAssi + veicoli_lista[1].numAssi):
    peso_rimorchio += assi_lista[i].massa

# II. Compilazione online

# Dati di accesso aggiornati al 18/10/2024
USERNAME = "your_username"
PASSWORD = "your_password"

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

driver.switch_to.window(original_window)
driver.switch_to.frame("contenuto")

proceed_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='JavaScript:goAction();']"))
)
proceed_button.click()


# First step of the simulation
# Wait for the table to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:document.forms[0].azione.value='3';checkValidForm(false,'A', '1');\"]"))
)
# Here we compile the table porcoddio
input_element = driver.find_element(By.NAME, "mTara")
input_element.send_keys(str(veicoli_lista[0].tara))

input_element = driver.find_element(By.NAME, "rTara")
input_element.send_keys(str(veicoli_lista[1].tara))

input_element = driver.find_element(By.NAME, "mAssiNum")
input_element.send_keys(str(veicoli_lista[0].numAssi))

input_element = driver.find_element(By.NAME, "rAssiNum")
input_element.send_keys(str(veicoli_lista[1].numAssi))

input_element = driver.find_element(By.NAME, "mLength")
input_element.send_keys(str(veicoli_lista[0].lungh))

input_element = driver.find_element(By.NAME, "rLength")
input_element.send_keys(str(veicoli_lista[1].lungh))

input_element = driver.find_element(By.NAME, "mWidth")
input_element.send_keys(str(veicoli_lista[0].largh))

input_element = driver.find_element(By.NAME, "rWidth")
input_element.send_keys(str(veicoli_lista[1].largh))

input_element = driver.find_element(By.NAME, "mWeight")
input_element.send_keys("{:.2f}".format(peso_trattore))


input_element = driver.find_element(By.NAME, "rWeight") # incongruenze nei nomi
input_element.send_keys("{:.2f}".format(peso_rimorchio))

input_element = driver.find_element(By.NAME, "veicMaxLength")
input_element.send_keys(str(convoglio_lista[0].lungMax))

input_element = driver.find_element(By.NAME, "veicMaxWidth")
input_element.send_keys(str(convoglio_lista[0].largMax))

input_element = driver.find_element(By.NAME, "veicMaxHeight")
input_element.send_keys(str(convoglio_lista[0].altMax))

input_element = driver.find_element(By.NAME, "sporgAnt")
input_element.send_keys(str(convoglio_lista[0].spoAnt))

input_element = driver.find_element(By.NAME, "sporgPost")
input_element.send_keys(str(convoglio_lista[0].spoPos))

input_element = driver.find_element(By.NAME, "floorHeight")
input_element.send_keys("0,90")

input_element = driver.find_element(By.NAME, "veicMaxSpeedCarta")
input_element.send_keys(str(convoglio_lista[0].velCC))


next1_button = driver.find_element(By.XPATH, "//a[text()='Successiva']")
next1_button.click()

# data inizio validità

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
# Click on the date
date_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//a[font/text()='{target_date_str}']"))
)
date_element.click()

driver.switch_to.window(original_window)
driver.switch_to.frame("contenuto")

#calcola data fine validità
date_end_button = driver.find_element(By.XPATH, "//a[@href=\"javascript:if(transformStringToDate($('dataNuovoMetodo').value)<transformStringToDate(document.forms[0].dataInizioValidita.value))setFinDateNewMode('S');else setFinDate('S');\"]")
date_end_button.click()

driver.switch_to.window(original_window)
driver.switch_to.frame("contenuto")

tabella = driver.find_element(By.XPATH, "//form[@name='Form1']")

# distribuzione pesi
# Assi Trattore
for i in range(veicoli_lista[0].numAssi):
    tag_peso = "//input[@id='mPesoAsse" + str(i + 1) + "']"
    input_element = tabella.find_element(By.XPATH, tag_peso)
    input_element.send_keys(assi_lista[i].massa)

    tag_tipo = "//select[@id='mTipoAsse" + str(i + 1) + "']"
    dropdown = tabella.find_element(By.XPATH, tag_tipo)
    select = Select(dropdown)
    select.select_by_value(assi_lista[i].tipo)

    tag_interasse = "//input[@id='mInterasse" + str(i + 1) + "']"
    input_element = tabella.find_element(By.XPATH, tag_interasse)
    input_element.send_keys(assi_lista[i].distanza)

# Assi Semirimorchio
for i in range(veicoli_lista[0].numAssi, veicoli_lista[1].numAssi + veicoli_lista[0].numAssi):
    h = i - veicoli_lista[0].numAssi + 1 # Hilfsvariable

    tag_peso = "//input[@id='rPesoAsse" + str(h) + "']"
    input_element = tabella.find_element(By.XPATH, tag_peso)
    input_element.send_keys(assi_lista[i].massa)

    if assi_lista[i].tipo != 'C4V':
       tag_tipo = "//select[@id='rTipoAsse" + str(h) + "']"
       dropdown = tabella.find_element(By.XPATH, tag_tipo)
       select = Select(dropdown)
       select.select_by_value(assi_lista[i].tipo)

    if h is not veicoli_lista[1].numAssi:
                tag_interasse = "//input[@id='rInterasse" + str(h) + "']"
                input_element = tabella.find_element(By.XPATH, tag_interasse)
                input_element.send_keys(str(assi_lista[i].distanza))


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

input()  # Wait for user input before proceeding

exit()


