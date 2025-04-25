import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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
        locator = (By.ID, 'make-incl-0')
        make_select_elmt = self._get_and_move_to_element(locator, EC.presence_of_element_located)
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
        locator = (By.ID, 'model-incl-0')
        model_select_elmt = self._get_and_move_to_element(locator, EC.presence_of_element_located)
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
        locator = (By.CSS_SELECTOR, 'input[data-testid="first-registration-filter-min-input"]')
        input_elem = self._get_and_move_to_element(locator, EC.visibility_of_element_located)
        input_elem.click()
        input_elem.send_keys(str(value)) 

    def fill_first_registration_max(self, value):
        locator = (By.CSS_SELECTOR, 'input[data-testid="first-registration-filter-max-input"]')
        input_elem = self._get_and_move_to_element(locator, EC.visibility_of_element_located)
        input_elem.click()
        input_elem.send_keys(str(value)) 

    def fill_mileage_min(self, value):
        locator = (By.CSS_SELECTOR, 'input[data-testid="mileage-filter-min-input"]')
        input_elem = self._get_and_move_to_element(locator, EC.visibility_of_element_located)
        input_elem.click()
        input_elem.send_keys(str(value)) 

    def fill_mileage_max(self, value):
        locator = (By.CSS_SELECTOR, 'input[data-testid="mileage-filter-max-input"]')
        input_elem = self._get_and_move_to_element(locator, EC.visibility_of_element_located)
        input_elem.click()
        input_elem.send_keys(str(value)) 

    def check_fuel_type(self, fuel_types):
        fuel_type_options_locator = (By.CSS_SELECTOR, 'div[data-testid="fuel-type-filter"]')
        fuel_type_options_elem = self._get_and_move_to_element(fuel_type_options_locator, EC.presence_of_element_located)
        for fuel_type in fuel_types:
            fuel_type_options_elem.find_element(By.XPATH, f'//div//label[text()="{fuel_type}"]').click()

    def check_offer_details(self, offer_details):
        offer_details_options_locator = (By.ID, 'section-offerDetails')
        offer_detail_options_elem = self._get_and_move_to_element(offer_details_options_locator, EC.presence_of_element_located)
        for offer_detail in offer_details:
            locator = (By.XPATH, f".//div//label/div[text()='{offer_detail}']")
            self._get_and_move_to_element(locator, EC.visibility_of_element_located, offer_detail_options_elem).click()

    def click_on_search(self):
        locator = (By.CSS_SELECTOR, 'button[data-testid="belowFilter-submit-search"]')
        self._move_and_click_on(locator)
        painel_search_filters_elem =self._get_and_move_to_element((By.CSS_SELECTOR, 'article[data-testid="result-list-container"]'), EC.visibility_of_element_located)
        search_title = painel_search_filters_elem.find_element(By.XPATH, '//*[@data-testid="srp-title"]').text
        if search_title[0] == '0':
            print('No results found')
        else:
            print(search_title)
        
        return search_title

    def browser_on_results(self):
        while True:
            page_number_elem = self.driver.find_element(By.XPATH, '//button[@disabled and not(contains(normalize-space(.), "Previous"))]')
            print(page_number_elem.get_attribute('aria-label'))
            locator = (By.CSS_SELECTOR, 'button[data-testid="pagination:next"]')
            has_next_page = self._element_exists(locator)
            if not has_next_page:
                break
            self._move_and_click_on(locator)
            from time import sleep
            sleep(3)

    def _move_and_click_on(self, locator, expected_condition=EC.element_to_be_clickable):
        bellow_search_button_elem = self._get_and_move_to_element(locator, expected_condition)
        bellow_search_button_elem.click()

    def _element_exists(self, locator, expected_condition=EC.presence_of_element_located, parent_element=None, timeout=2):
        if parent_element is not None:
            try:
                elem = parent_element.find_element(*locator)
                if expected_condition == EC.presence_of_element_located:
                    return True
                else:
                    return expected_condition(locator)(elem)
            except NoSuchElementException:
                return False
        else:
            try:
                WebDriverWait(self.driver, timeout).until(expected_condition(locator))
                return True
            except TimeoutException:
                return False

    def _element_in_viewport(self, locator):
        element = self.driver.find_element(*locator)
        return self.driver.execute_script("""
            var elem = arguments[0],
                box = elem.getBoundingClientRect(),
                cx = box.left + box.width / 2,
                cy = box.top + box.height / 2,
                e = document.elementFromPoint(cx, cy);
            for (; e; e = e.parentElement) {
                if (e === elem)
                    return true;
            }
            return false;
        """, element)

    def _get_and_move_to_element(self, locator, expected_condition=EC.presence_of_element_located, parent_element=None):
        search_context = parent_element if parent_element is not None else self.driver
        # Custom wait for element within the context
        def find_in_context(driver):
            # If using EC, call it with the context
            return expected_condition(locator)(search_context)
        element = self.wait.until(find_in_context)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(lambda d: self._element_in_viewport(locator) if parent_element is None else self._element_in_viewport_within(locator, parent_element))
        return element

    def _element_in_viewport_within(self, locator, parent_element):
        element = parent_element.find_element(*locator)
        return self.driver.execute_script("""
            var elem = arguments[0],
                box = elem.getBoundingClientRect(),
                cx = box.left + box.width / 2,
                cy = box.top + box.height / 2,
                e = document.elementFromPoint(cx, cy);
            for (; e; e = e.parentElement) {
                if (e === elem)
                    return true;
            }
            return false;
        """, element)

    def close(self):
        self.driver.quit()
