from time import sleep
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import os
import datetime
import logging


def get_calendar(
    start_date: datetime.datetime = None,
    end_date: datetime.datetime = None,
    download_location: str = os.getcwd(),
    wait_time: int = 5,
):
    logging.info("Getting calendar...")
    """Récupère automatiquement le calendrier de l'IUT INFO de l'ULCO. Peut ne pas enregistrer le ISC si jamais il n'y a pas de cours sur la période demandée.

    Args:
        start_date (datetime.datetime, optional): Date du début des évennements à récupérer. Par défaut la date du jour. Defaults to None.
        end_date (datetime.datetime, optional): Date de fin des évennements à récupérer. Par défaut 7 jours après la date du début. Defaults to None.
        download_location (str, optional): Chemin du dossier dans lequel enregistrer le calendrier. Defaults to CWD.
        wait_time (int, optional): Temps d'attente entre chaque action, à ajuster selon la connexion et la charge du serveur. Defaults to 5.
    """
    if start_date is None:
        start_date = datetime.datetime.now()
    if end_date is None:
        end_date = start_date + datetime.timedelta(days=7)

    # Download driver if necessary
    if not os.path.exists("geckodriver.exe"):
        import requests

        print("Downloading driver...")
        url = "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-win64.zip"

        res = requests.get(url)

        with open("geckodriver.zip", "wb") as f:
            f.write(res.content)

        # unzip
        import zipfile

        with zipfile.ZipFile("geckodriver.zip", "r") as zip_ref:
            zip_ref.extractall(".")

        # Delete zip file
        os.remove("geckodriver.zip")

    # Set download folder to be the current one
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.set_preference("browser.download.dir", download_location)
    firefox_options.set_preference("browser.download.folderList", 2)

    driver = webdriver.Firefox(options=firefox_options)

    # Connect to page http://edt.univ-littoral.fr/public/iut-info
    driver.get("http://edt.univ-littoral.fr/public/iut-info")
    sleep(wait_time)

    # If the page contains "Ouvrir un projet"
    if "Ouvrir un projet" in driver.execute_script(
        "return document.documentElement.outerHTML"
    ):
        # find the last element ".thumb-wrap"
        last_thumb = driver.find_elements(By.CSS_SELECTOR, ".thumb-wrap")[-1]
        last_thumb.click()

        # Click on the button containing "ouvrir"
        driver.find_element(By.XPATH, "//button[contains(text(), 'Ouvrir')]").click()
        sleep(wait_time)

    # expand the tree by clicking on the .x-tree3-node-joint
    driver.find_element(By.CSS_SELECTOR, ".x-tree3-node-joint").click()

    # Click on "IUT INFO"
    driver.find_element(By.XPATH, "//span[contains(text(), 'IUT INFO')]").click()

    sleep(wait_time)
    # Select the 2nd button from the 2nd .x-toolbar-left (the one with the calendar)
    tool_bar = driver.find_elements(By.CSS_SELECTOR, ".x-toolbar-left")[1]

    tool_bar.find_elements(By.CSS_SELECTOR, "button")[1].click()

    sleep(wait_time)

    # Modify the value of the input
    driver.execute_script(
        f"document.querySelectorAll('input')[1].value = '{start_date.strftime('%d/%m/%Y')}'"
    )

    # Same for the #x-auto-189-input one week later
    driver.execute_script(
        f"document.querySelectorAll('input')[2].value = '{end_date.strftime('%d/%m/%Y')}'"
    )

    # Update the software by clicking on #x-auto-190 (calendar icon), then on the selected date
    driver.find_element(By.CSS_SELECTOR, "#x-auto-190").click()
    driver.find_element(By.CSS_SELECTOR, ".x-date-selected").click()

    # click on the button "OK"
    driver.find_element(By.XPATH, "//button[contains(text(), 'Ok')]").click()

    sleep(wait_time)

    driver.close()

    # Clean geckodriver.log file
    os.remove("geckodriver.log")


if __name__ == "__main__":
    get_calendar(
        datetime.datetime(2023, 9, 3),
        download_location=os.path.join(os.getcwd(), "Calendars"),
    )
