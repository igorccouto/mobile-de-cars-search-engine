from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import os

class MobileDeBrowser:
    def __init__(self, headless: bool = True, timeout: int = 15):
        """
        Initializes a Firefox browser instance using geckodriver from the parent folder.
        :param headless: Whether to run browser in headless mode.
        :param timeout: Default timeout for WebDriverWait.
        """
        geckodriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        service = Service(executable_path=geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, timeout)

        # Instance variable
        self.make_options_elmts = []

    def go_to_search(self):
        self.driver.get('https://suchen.mobile.de/fahrzeuge/detailsuche?lang=en&s=Car&vc=Car')
        self.wait_for_consent_dialog()

    def wait_for_consent_dialog(self):
        try:
            consent_dialog = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'mde-consent-modal-dialog'))
            )
            accept_button = consent_dialog.find_element(By.XPATH, ".//button[contains(., 'Accept')]")
            accept_button.click()
        except TimeoutException:
            pass

    def select_make(self, make_name):
        make_select_elmt = self.wait.until(
            EC.presence_of_element_located((By.ID, 'make-incl-0'))
        )
        make_select_elmt.click()
        options = make_select_elmt.find_elements(By.TAG_NAME, 'option')
        found = False
        for option in options:
            if option.text.strip().lower() == make_name.strip().lower():
                option.click()
                found = True
                break
        if not found:
            raise RuntimeError(f'Make name "{make_name}" not found in options.')

    def select_model(self, model_name):
        model_select_elmt = self.wait.until(
            EC.presence_of_element_located((By.ID, 'model-incl-0'))
        )
        model_select_elmt.click()
        options = model_select_elmt.find_elements(By.TAG_NAME, 'option')
        found = False
        for option in options:
            if option.text.strip().lower() == model_name.strip().lower():
                option.click()
                found = True
                break
        if not found:
            raise RuntimeError(f'Model name "{model_name}" not found in options.')

    def fill_first_registration_min(self, value):
        input_elem = self.wait.until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, 'input[data-testid="first-registration-filter-min-input"]').find_element(By.XPATH, '..')
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_elem)
        self.action.click(input_elem).perform()
        input_elem.clear()
        input_elem.send_keys(str(value))

    def close(self):
        self.driver.quit()
