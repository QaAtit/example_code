from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
import def_setting
from selenium.webdriver.common.by import By
import random


class SettingBrowser:
    # ==================================================================================================================
    # Функция method - определяет настройки браузера
    def method(self):
        # Присоединяем к Selenium
        self.options = webdriver.ChromeOptions()
        # Опция во весь экран (если вдруг нужно будет не в фоновом режиме запустить)
        self.options.add_argument("start-maximized")
        # строка отключает панель автоматизации, всплывающее окно расширение режима разработчика, логи консоли
        self.options.add_experimental_option(
            'excludeSwitches', ['load-extension', 'enable-automation', 'enable-logging'])
        # Отключение предотвращения обнаружения (необходимо для проверок кнопок позвонить, чтобы вытягивать номера)
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('useAutomationExtension', False)
        # Отключение уведомлений
        self.options.add_argument("--disable-notifications")
        # Фоновый режим
        # self.options.add_argument('--headless')
        # Отключение gpu
        self.options.add_argument('--disable-gpu')
        # Включение javascript
        self.options.add_argument('--enable-javascript')
        # Присваиваем настройки к объекту
        self.browser = webdriver.Chrome(options=self.options)
        # Устанавливаем время ожидания для поиска элемента и взаимодействия с ним. В секундах
        self.browser.implicitly_wait(7)
        # Страницы app, find, bk. (Для индивидуальных заказов переход в панель администратора через детали заказа)

    # ==================================================================================================================
    # Вход в систему
    def login(self, phone):
        self.browser.find_element(By.CSS_SELECTOR, '#phone').send_keys(phone)
        self.browser.find_element(By.CSS_SELECTOR, 'span.MuiButton-label').click()
        self.browser.find_element(By.CSS_SELECTOR, '#code').send_keys('****')
        self.browser.find_element(By.CSS_SELECTOR, 'span.MuiButton-label').click()

    def login_app(self, page, phone_number=None):
        if phone_number is None:
            phone_number = random.randint(1111111111, 9999999999)
        if page == 'app_page':
            self.browser.get(def_setting.app_page)
        elif page == 'find_page':
            self.browser.get(def_setting.find_page)
        self.login(phone_number)
        try:
            self.browser.find_element(By.CSS_SELECTOR, '#userName').send_keys('Test User')
            self.browser.find_element(By.CSS_SELECTOR, '#root > main > div > form > button').click()
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

    # Закрывает уведомления
    def closed_alert(self):
        try:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert_b).click()
        except NoSuchElementException:
            pass
        try:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert_b).click()
        except NoSuchElementException:
            pass

    # Логин в админку
    def login_bk(self):
        self.browser.get(def_setting.bk_page)
        self.browser.find_element(By.CSS_SELECTOR, '#loginform-phone').send_keys("80008008888")
        self.browser.find_element(By.CSS_SELECTOR, '#loginform-password').send_keys("*****")
        self.browser.find_element(By.CSS_SELECTOR, '#login-form > div.row > div.col-xs-4 > button').click()

    # Функция очистки поля ввода
    def clear_field(self, css_selector):
        self.browser.find_element(By.CSS_SELECTOR, css_selector).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(By.CSS_SELECTOR, css_selector).send_keys(Keys.DELETE)
