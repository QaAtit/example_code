import time

import pytest
import random
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import start
import def_setting


@pytest.mark.all_tests
@pytest.mark.notice
class TestsNotifications(start.SettingBrowser):
    @pytest.mark.notice_create_auto
    def test_create_auto_and_edit(self):
        try:
            self.method()
            self.login_app('app_page')
            self.add_machine()
            self.edit_machine()
        finally:
            # Удаляем добавленную технику
            self.clear_auto()
            # Закрываем браузер по окончанию работы
            print('Закрываю браузер')
            self.browser.quit()

    @pytest.mark.notice_button_refresh
    def test_button_refresh(self):
        try:
            self.method()
            self.login_app('app_page')
            self.push_refresh()
        finally:
            self.browser.quit()

    @pytest.mark.checking_notifications_part1
    def test_checking_notification_part1(self):
        try:
            self.checking_notifications_part1()
        finally:
            self.browser.quit()

    @pytest.mark.checking_notifications_part2
    def test_checking_notification_part2(self):
        try:
            self.checking_notifications_part2()
        finally:
            self.browser.quit()

    @pytest.mark.checking_notifications_part3
    def test_checking_notification_part3(self):
        try:
            self.checking_notifications_part3()
        finally:
            self.browser.quit()

    # ==================================================================================================================
    # Функции для проведения проверок
    # ==================================================================================================================

    def add_machine(self, data=None):
        try:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_base_tech).click()
        except StaleElementReferenceException:
            time.sleep(1)
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_base_tech).click()
        self.browser.find_element(By.CSS_SELECTOR, '.Machines-AddButton').click()
        elements_auto = self.browser.find_elements(By.CSS_SELECTOR, 'div.globalVerticalContainer > div > div')
        if data is None:
            while self.browser.find_element(By.CSS_SELECTOR, '.MuiToolbar-gutters > h3').text == 'Выбор типа':
                random.choice(elements_auto).click()
        if data == 666:
            while self.browser.find_element(By.CSS_SELECTOR, '.MuiToolbar-gutters > h3').text == 'Выбор типа':
                elements_auto[3].click()
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
        if data is None:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_cash).send_keys(random.randint(500, 10000))
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_no_vat).send_keys(random.randint(500, 10000))
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_vat).send_keys(random.randint(500, 10000))
        elif data == 666:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_cash).send_keys(666666)
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_no_vat).send_keys(666666)
            self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_vat).send_keys(666666)
        name_auto = self.browser.find_element(By.CSS_SELECTOR, '.machineForm .MuiGrid-item .MuiTypography-root').text
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'button.machineForm--formInput').click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, def_setting.f_alert)))
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление о добавлении техники'
        assert f"{name_auto} добавлен" in self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text, \
            f'В уведомлении о добавлении техники должно быть название техники + добавлен, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def edit_machine(self):
        self.browser.find_element(By.CSS_SELECTOR,
                                  'div:nth-child(2) > .MuiGrid-container > div.MuiGrid-root > div > div:nth-child(1)'
                                  ' > div.MuiGrid-root.MuiGrid-container button').click()
        self.browser.find_element(By.CSS_SELECTOR, '.expandBlock button').click()
        name_auto = self.browser.find_element(By.CSS_SELECTOR, '.machineForm .MuiGrid-item .MuiTypography-root').text
        self.browser.find_element(By.CSS_SELECTOR, def_setting.a_price_cash).send_keys(random.randint(1, 100000000))
        self.browser.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > button > span.MuiButton-label').click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление о редактировании техники'
        assert f"{name_auto} изменён" in self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text, \
            f'В уведомлении о редактировании техники должно быть: "{name_auto} изменён", а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def clear_auto(self):
        self.browser.find_element(By.CSS_SELECTOR,
                                  'div:nth-child(2) > .MuiGrid-container > div.MuiGrid-root > div > div:nth-child(1)'
                                  ' > div.MuiGrid-root.MuiGrid-container button').click()
        self.browser.find_element(By.CSS_SELECTOR, '.expandBlock button').click()
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, def_setting.a_b_del_auto)))
        self.browser.find_element(By.CSS_SELECTOR, def_setting.a_b_del_auto).click()

    def push_refresh(self):
        try:
            self.browser.find_element(By.CSS_SELECTOR, 'h3.MuiTypography-root.header--title')
            time.sleep(1)
            self.add_machine()
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_order).click()
            self.push_refresh_2()
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_base_tech).click()
            self.clear_auto()
        except NoSuchElementException:
            self.push_refresh_2()

    def push_refresh_2(self):
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.task--CenteredRenewButton')))
        self.browser.find_element(By.CSS_SELECTOR, 'button.task--CenteredRenewButton').click()
        wait = WebDriverWait(self.browser, 2)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, def_setting.f_alert)))
        assert "Обновлено" == self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text, \
            f'В уведомлении после нажатия на кнопку обновить должно указываться "Обновлено", а указывается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'

    def notice_create_ind_task(self, time_work=None, artist=None, pay_n=None):
        # переходим в меню еще, потом в базу исполнителей
        try:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_more).click()
            time.sleep(2)
            self.browser.find_element(By.CSS_SELECTOR,
                                      '.MuiGrid-root.MuiGrid-align-items-xs-center:nth-child(3)').click()
        except NoSuchElementException:
            self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_more).click()
            time.sleep(2)
            self.browser.find_element(By.CSS_SELECTOR,
                                      '.MuiGrid-root.MuiGrid-align-items-xs-center:nth-child(3)').click()
        if artist is None:
            self.artist_choice('9522471691')
        else:
            self.artist_choice(artist)
        # ------------------------------------------------------------------------------------------------------------
        # Определяем кол-во техники у исполнителя и рандомно выбираем одну из них
        try:
            count = len(self.browser.find_elements(By.CSS_SELECTOR, def_setting.a_machines))
            if count == 1:
                random_auto = '.machineCard:nth-child(1)'
            else:
                random_auto = '.machineCard:nth-child(' + str(random.randint(1, count)) + ')'
                self.browser.execute_script("arguments[0].scrollIntoView(true);",
                                            self.browser.find_element(By.CSS_SELECTOR, random_auto))
            self.browser.find_element(By.CSS_SELECTOR, random_auto).click()
        except (ValueError, NoSuchElementException):
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.add_machine()
            self.browser.switch_to.window(self.browser.window_handles[0])
            time.sleep(1)
            self.browser.refresh()
            self.browser.find_element(By.CSS_SELECTOR, '.machineCard:nth-child(1)').click()
        # Переходим к заполнению заказа
        self.browser.find_element(By.CSS_SELECTOR, "span.MuiFab-label").click()
        # Адрес работ
        self.browser.find_element(By.CSS_SELECTOR, '.MuiGrid-item > ul > div:nth-child(5)').click()
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_create_task_address).click()
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_services_search).send_keys(
            'ул Новосибирская, д 1, Ленинский р-н, Новосибирск')
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_services_search_1).click()
        wait = WebDriverWait(self.browser, 5)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, def_setting.f_b_next)))
        element.click()
        # ------------------------------------------------------------------------------------------------------------
        # Далее, переходим к заполнению Даты и времени
        # ------------------------------------------------------------------------------------------------------------
        if time_work is None:
            time_work = random.randint(1, 3)
        if time_work == 1 or time_work == 0:
            # Выбираем часы
            self.browser.find_element(By.CSS_SELECTOR,
                                      '.radio-bg button.MuiButton-outlined:nth-child(1)').click()
            self.browser.find_element(By.CSS_SELECTOR,
                                      'div.MuiGrid-align-items-xs-flex-start select.MuiSelect-root').click()
            # Далее составляем css по кол-ву часов и выбираем его
            self.browser.find_element(By.CSS_SELECTOR, 'div.MuiGrid-align-items-xs-flex-start select.MuiSelect-root'
                                                       f' option:nth-child({random.randint(5, 20)})').click()
        elif time_work == 2:
            # Выбираем смены
            self.browser.find_element(By.CSS_SELECTOR,
                                      '.radio-bg button.MuiButton-outlined:nth-child(2)').click()
            self.browser.find_element(By.CSS_SELECTOR,
                                      'div.MuiGrid-align-items-xs-flex-start select.MuiSelect-root').click()
            self.browser.find_element(By.CSS_SELECTOR, 'div.MuiGrid-align-items-xs-flex-start select.MuiSelect-root'
                                                       f' option:nth-child({random.randint(1, 10)})').click()
        elif time_work == 3:
            # Долгосрочный
            self.browser.find_element(By.CSS_SELECTOR, '.formElem-right:nth-child(3) .MuiSwitch-input').click()
        # Кнопка далее
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_b_next).click()
        # ------------------------------------------------------------------------------------------------------------
        # Перешли в блок оплаты, устанавливаем нужные параметры
        self.browser.find_element(By.CSS_SELECTOR, '.last').click()
        if pay_n is None:
            pay_n = random.randint(1, 2)
        if pay_n == 1:
            pay = 'li.MuiListItem-container:nth-child(2)'
        else:
            pay = 'li.MuiListItem-container:nth-child(4)'
        try:
            self.browser.find_element(By.CSS_SELECTOR, pay + ' .Mui-checked')
        except NoSuchElementException:
            self.browser.find_element(By.CSS_SELECTOR, pay + ' .MuiSwitch-input').click()
        # Далее, если безнал, идет выбор НДС или без НДС
        if pay_n == 2:
            # После выбора безналичного способа оплаты выбирает ндс\без ндс
            pay_n_no_cash = random.randint(1, 2)
            if pay_n_no_cash == 1:
                type_pay = '.OrderPayment--prepayment  .MuiButton-root:nth-child(1)'
            else:
                type_pay = '.OrderPayment--prepayment  .MuiButton-root:nth-child(2)'
            type_pay_task = type_pay + '.radioButton-active'
            try:
                self.browser.find_element(By.CSS_SELECTOR, type_pay_task)
            except NoSuchElementException:
                self.browser.find_element(By.CSS_SELECTOR, type_pay).click()
            # Предоплата
            self.browser.find_element(By.CSS_SELECTOR,
                                      '.OrderPayment--taxation.radio-bg > div > button:nth-child(1)').click()
        # Далее, запрос или авто-цена
        type_work = random.randint(1, 2)
        if time_work != 3:
            if time_work == 0:
                type_of_work = '.contractual-switch .MuiButton-root:nth-child(1)'
            elif type_work == 1:
                type_of_work = '.contractual-switch .MuiButton-root:nth-child(2)'
            else:
                type_of_work = '.contractual-switch .MuiButton-root:nth-child(1)'
            type_of_work_task = type_of_work + '.radioButton-active'
            try:
                self.browser.find_element(By.CSS_SELECTOR, type_of_work_task)
            except NoSuchElementException:
                self.browser.find_element(By.CSS_SELECTOR, type_of_work).click()
        # Проверка доступности техники
        time.sleep(1)
        text_start_work = self.browser.find_element(By.CSS_SELECTOR, '.doneButtons-next > span.MuiButton-label').text
        if "Нет техники" == text_start_work:
            print('Добавьте технику пользователю 95222471691 со всеми типами оплаты')
        # Кнопка далее (выходит в настройки карточки заказа)
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_b_next).click()
        # ------------------------------------------------------------------------------------------------------------
        self.browser.find_element(By.CSS_SELECTOR, '.listComment').click()
        comment = "Проверка уведомлений"
        # Отправка заказа в работу
        self.browser.find_element(By.CSS_SELECTOR, 'textarea:nth-child(1)').send_keys(comment)
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_b_next).click()
        self.browser.find_element(By.CSS_SELECTOR, '.mainButton button').click()
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_b_submition).click()

    def artist_choice(self, pn_isp=None):
        if pn_isp is None:
            count = len(self.browser.find_elements(By.CSS_SELECTOR, '.serviceList--element'))
            isp = '.serviceList--element:nth-child(' + str(random.randint(1, count)) + ')'
        else:
            self.browser.find_element(By.CSS_SELECTOR, '.MuiInputBase-inputAdornedEnd').send_keys(pn_isp)
            isp = '.serviceList--element:nth-child(1)'
            try:
                self.browser.find_element(By.CSS_SELECTOR, isp + ' .MuiTypography-subtitle2').text[:-3]
            except NoSuchElementException:
                self.browser.quit()
                x = 2
                assert x == 0, 'По указанному номеру телефона или имени исполнителя не находится ни одного пользователя'
        self.browser.find_element(By.CSS_SELECTOR, isp).click()

    def checking_notifications_part1(self):
        self.method()
        # Открытие страницы браузера
        # Вход в систему find. Ввод логина и пароля и нажатие на кнопку войти.
        self.login_app('find_page', '9537670770')
        # Открываем 2 вкладку, логинимся исполнителем
        self.browser.execute_script("window.open('', 'new_window')")
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.login_app('app_page', '9522471691')
        # Переключаемся обратно на заказчика
        self.browser.switch_to.window(self.browser.window_handles[0])
        # Вызываем функцию создания заказа
        self.notice_create_ind_task(0)
        self.checking_notifications_n1()
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.checking_notifications_n2()
        self.checking_notifications_n3()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.checking_notifications_n4()
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.checking_notifications_n5()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.checking_notifications_n6()
        self.closed_alert()
        self.checking_notifications_n7()
        self.checking_notifications_n8()

    def checking_notifications_part2(self):
        self.method()
        self.login_app('app_page', '9666666666')
        self.add_machine(666)
        # Открываем 2 вкладку, логинимся исполнителем
        self.browser.execute_script("window.open('', 'new_window')")
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.login_app('find_page', '9537670770')
        self.notice_create_ind_task(0, '9666666666')
        self.browser.refresh()
        self.browser.find_element(By.CSS_SELECTOR, f'{def_setting.task_order}:nth-child(2) '
                                                   f'{def_setting.f_button_order_open_card_task}').click()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_bottom_navi_order).click()
        self.browser.refresh()
        self.checking_notifications_n2()
        self.closed_alert()
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.closed_alert()
        self.checking_notifications_n9()
        # self.help_f_1()
        self.checking_notifications_n10()
        self.browser.quit()

    def checking_notifications_part3(self):
        self.method()
        self.login_app('find_page', '9537670770')
        self.notice_create_ind_task(0, '9139494530', 2)
        self.closed_alert()
        self.browser.find_element(By.CSS_SELECTOR, f'{def_setting.task_order}:nth-child(2) '
                                                   f'{def_setting.f_button_order_open_card_task}').click()
        self.browser.find_element(By.CSS_SELECTOR, '.orderInfo--continueButton').click()
        self.closed_alert()
        a = self.browser.find_element(By.CSS_SELECTOR, '.header--title').text
        a = a[-6:] + '-1. '
        if a[0] == ' ':
            a = a[1:]
        wait = WebDriverWait(self.browser, 500)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                     '.orderCard--continue-price > div:nth-child(1)  button')))
        if 'Можно' in self.browser.find_element(By.CSS_SELECTOR,
                                                '.orderCard--continue-price > div:nth-child(1)  button span').text:
            self.browser.find_element(By.CSS_SELECTOR, '.orderCard--continue-price > div:nth-child(1)  button').click()
            assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == \
                f'{a}Вы добавили другой вид налога к условиям заказа' or 'Продолжаю поиск исполнителя', \
                f'Должно быть уведомление вида: №9543-1. Вы добавили другой вид налога к условиям заказа,' \
                f' а отображается: {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
            self.closed_alert()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                               '.orderCard--continue-price > div:nth-child(1)  button')))
        if 'Поднять цену' == self.browser.find_element(
                By.CSS_SELECTOR, '.orderCard--continue-price > div:nth-child(1)  button span').text:
            self.browser.find_element(By.CSS_SELECTOR, '.orderCard--continue-price > div:nth-child(1)  button').click()
            time.sleep(1)
            assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == f'{a}Вы подняли цену' or\
                   'Продолжаю поиск исполнителя', \
                   f'Должно быть уведомление вида: {a}Вы подняли цену, а отображается:' \
                   f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'

    # Test #1 Проверка уведомления у заказчика: "Заказ добавлен! Ждите откликов!"
    def checking_notifications_n1(self):
        wait = WebDriverWait(self.browser, 3)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, def_setting.f_alert)))
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление о создании заказа'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Заказ добавлен! Ждите' \
                                                                                       ' откликов!', \
            f'Должно быть уведомление вида: Заказ добавлен! Ждите откликов!, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    # Test #2 Проверка уведомления у исполнителя: "Заказ забронирован!"
    def checking_notifications_n2(self):
        self.browser.find_element(By.CSS_SELECTOR, f'{def_setting.task_order}:nth-child(2) '
                                                   f'{def_setting.f_button_order_open_card_task}').click()
        self.browser.find_element(By.CSS_SELECTOR, '.layout-main-content div:nth-child(1) > button').click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление о бронировании заказа'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Вы успешно забронировали' \
                                                                                       ' заказ', \
            f'Должно быть уведомление вида: Вы успешно забронировали заказ, а отображается: ' \
            f'{self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def checking_notifications_n3(self):
        self.browser.find_element(By.CSS_SELECTOR, '.taskInfo--takeButton').click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление о взятии заказа'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Вы взяли заказ', \
            f'Должно быть уведомление вида: Вы взяли заказ, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.number_task_f_check = self.browser.find_element(By.CSS_SELECTOR, 'header > div > h3').text

    def checking_notifications_n4(self):
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), 'Отсутствует уведомление о том, ' \
                                                                                'что заказ был принят исполнителем'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == f'{self.number_task_f_check} ' \
                                                                                       f'принят в работу', \
            'Должно быть уведомление вида: Заказ №9484-1 принят в работу, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def checking_notifications_n5(self):
        self.closed_alert()
        self.browser.find_element(By.CSS_SELECTOR, '.taskInfo--refuseButton').click()
        self.browser.find_element(By.CSS_SELECTOR, '.questionPopup--question-div:nth-child(1) > button').click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление о том, что заказ был отменен исполнителем после нажатия на кнопку' \
            ' Отказаться от заказа'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Вы отказались от заказа', \
            'Должно быть уведомление вида: Вы отказались от заказа, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'

    def checking_notifications_n6(self):
        if self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text[-8] == ' ':
            x = 7
        else:
            x = 8
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), 'Отсутствует уведомление о том, ' \
                                                                                'что исполнитель отказался от заказа'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == \
               f'Исполнитель отказался от заказа {self.number_task_f_check[-x:]}!', \
            f'Исполнитель отказался от заказа {self.number_task_f_check[-x:]} ->' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def checking_notifications_n7(self):
        self.closed_alert()
        self.browser.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div > button.orderCard--openInfo').click()
        self.browser.find_element(By.CSS_SELECTOR, 'button.orderInfo--continueButton').click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление после нажатия на кнопку продолжить заказчиком, после отказа от заказа исполнителем'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Продолжаю поиск исполнителя' or\
               'Остальные исполнители получили доступ к задаче', \
               f'Продолжаю поиск исполнителя ->' \
               f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def checking_notifications_n8(self):
        self.closed_alert()
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_cancel_button).click()

        self.browser.find_element(By.CSS_SELECTOR,
                                  '.questions div:nth-child(1) .questionPopup--question-button').click()
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, def_setting.f_alert)))
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Ваш заказ отменён', \
            f'Ваш заказ отменён {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def checking_notifications_n9(self):
        self.browser.find_element(By.CSS_SELECTOR, def_setting.f_cancel_a).click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), 'Отсутствует уведомление после отказа' \
                                                                                ' заказчика от исполнителя'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Вы отказались от заказа', \
            f'Должно быть уведомление вида: Вы отказались от заказа, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'
        self.closed_alert()

    def checking_notifications_n10(self):
        self.closed_alert()
        wait = WebDriverWait(self.browser, 1000)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, def_setting.f_alert)))
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), 'Отсутствует уведомление об' \
                                                                                ' автоматическом повышении цены'
        assert 'Цена поднята автоматически' in self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text, \
            f'Должно быть уведомление вида: Цена поднята автоматически, а отображается:' \
            f' {self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text}'

    def help_f_1(self):
        self.closed_alert()
        self.browser.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div > button.orderCard--openInfo').click()
        self.browser.find_element(By.CSS_SELECTOR, 'button.orderInfo--continueButton').click()
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert), \
            'Отсутствует уведомление после нажатия на кнопку продолжить заказчиком, после отказа от заказа исполнителем'
        assert self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text == 'Остальные исполнители ' \
                                                                                       'получили доступ к задаче', \
            f'Остальные исполнители получили доступ к задаче -> ' \
            f'{self.browser.find_element(By.CSS_SELECTOR, def_setting.f_alert).text} '
