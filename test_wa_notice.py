import time
import pytest
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data_wa_notice
import start
import def_setting


def create_tasks():
    param_get_token = {"phone": "79537670770", "****": "1212", "type": "search"}
    param_request_token = {"phone": "79537670770", "type": "search"}
    for task in data_wa_notice.tasks:
        requests.post("https://demobk.rentmachina.ru/api/v2/user/request-token", data=param_request_token)
        r = (requests.post('https://demobk.rentmachina.ru/api/v2/user/get-token', data=param_get_token)).json()
        token = {'authorization': 'Bearer ' + r['data']['token']}
        requests.post('https://demobk.rentmachina.ru/api/v2/order', json=task, headers=token)


#@pytest.mark.all_tests
@pytest.mark.notice_wa
class TestsNotificationsWA(start.SettingBrowser):
    def test_wa(self):
        self.wa_number = '9522471691'
        self.method()
        self.login_app('app_page', self.wa_number)
        #self.clear_machines()
        machines = [
            ['Разрушитель', [50, 1000, 1500]], ['Колесный', [1500, 2400, 2500]], ['Самосвал', [1100, 1200, 1250]],
            ['Автокран', [1500, 1650, 1500]], ['агп', [1000, 1200, 1400]], ['Манипулятор', [1200, 1300, 1400]],
            ['мини-погрузчик', [1100, 1200, 1250]], ['Длинномер', [1400, 1400, 1550]], ['Трал', [50, 2800, 50]]
        ]
        for i in machines:
            pass
            #self.create_machines(i[0], i[1])
        create_tasks()

    def clear_machines(self):
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_base_tech).click()
        machines = self.browser.find_elements(By.CSS_SELECTOR, def_setting.a_machines)
        x = len(machines)
        while x != 0:
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.element_to_be_clickable(machines[0]))
            machines[0].click()
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_b_red_auto).click()
            self.browser.execute_script("arguments[0].scrollIntoView(true);",
                                        self.browser.find_element(By.CSS_SELECTOR, def_setting.a_b_del_auto))
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_b_del_auto).click()
            machines = self.browser.find_elements(By.CSS_SELECTOR, def_setting.a_machines)
            x -= 1

    def create_machines(self, name_auto, cash=None):
        self.browser.find_element(By.CSS_SELECTOR, def_setting.a_b_add_auto).click()
        self.browser.find_element(By.CSS_SELECTOR, '.MuiInputBase-formControl input').send_keys(name_auto)
        self.browser.find_element(By.CSS_SELECTOR, '.serviceList--element').click()
        self.add_param_auto(cash)

    def add_param_auto(self, cash=None):
        param = self.browser.find_elements(By.CSS_SELECTOR, def_setting.a_select_checkbox)
        param_2 = self.browser.find_elements(By.CSS_SELECTOR, def_setting.a_select_std_required)
        choose_param = 0
        # Устанавливает минимальные параметры для техники.
        while choose_param != len(param):
            Select(param[choose_param]).select_by_index(1)
            choose_param += 1
        choose_param = 0
        while choose_param != len(param_2):
            param_2[choose_param].send_keys(random.randint(1, 100))
            choose_param += 1
        choose_param = 0
        self.browser.find_element(By.CSS_SELECTOR, '#optionsSelect').click()
        param_3 = self.browser.find_elements(By.CSS_SELECTOR, 'div.MuiFormGroup-root label input')
        while choose_param != len(param_3):
            param_3[choose_param].click()
            choose_param += 1
        self.browser.find_element(By.CSS_SELECTOR,
                                  '.MuiDialogActions-spacing > button:nth-child(1) > span.MuiButton-label').click()
        try:
            self.browser.find_element(By.CSS_SELECTOR, '#equipmentSelect').click()
            choose_param = 0
            param_4 = self.browser.find_elements(By.CSS_SELECTOR, '.MuiCheckbox-root  input')
            while choose_param != len(param_4):
                param_4[choose_param].click()
                choose_param += 1
            self.browser.find_element(By.CSS_SELECTOR,
                                      '.MuiDialogActions-spacing > button:nth-child(1) > span.MuiButton-label').click()
        except NoSuchElementException:
            pass
        self.browser.find_element(By.CSS_SELECTOR, def_setting.a_number_auto).send_keys('Н000НН54')
        try:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_address_garage).send_keys(
                'ул Ульяновская, д 1А, Октябрьский р-н, Новосибирск')
            try:
                self.browser.find_element(By.CSS_SELECTOR, def_setting.a_address_garage_opt_1).click()
            except NoSuchElementException:
                self.browser.find_element(By.CSS_SELECTOR, def_setting.a_address_garage).click()
                self.browser.find_element(By.CSS_SELECTOR, def_setting.a_address_garage_opt_1).click()
        except ElementNotInteractableException:
            pass
        if cash is None:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_cash).send_keys(random.randint(500, 10000))
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_no_vat).send_keys(random.randint(500, 10000))
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_vat).send_keys(random.randint(500, 10000))
        else:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_cash).send_keys(cash[0])
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_no_vat).send_keys(cash[1])
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_vat).send_keys(cash[2])
        time.sleep(2)
        try:
            self.browser.execute_script("arguments[0].scrollIntoView(true);",
                                        self.browser.find_element(By.CSS_SELECTOR, 'button.machineForm--formInput'))
        except JavascriptException:
            pass
        self.browser.find_element(By.CSS_SELECTOR, 'button.machineForm--formInput').click()
        self.closed_alert()
