import random
import time
import datetime
import requests
import data_wa_notice
import data_stress_t

site = 'https://demobk.rentmachina.ru/api/v2/'
phone_logiest = "79537670770"
phone_owner = "79522471691"


# Функция для фиксирования времени начала запроса
def time_log():
    st_t = time.time()
    st = datetime.datetime.now()
    timing = [st_t, st]
    return timing


# Функция для сохранения логов принимает в себя: 1) Список - результат работы функции timing, 2) Вид запроса и к чему
# обращаемся в API 3) Сам запрос
def save_log(t, req, response):
    log = open('logs.txt', 'a')
    st_ms = time.time() - t[0]
    st_ms = format(st_ms, '.3f')
    time_for_log = f'{t[1].hour}:{t[1].minute}:{t[1].second}'
    log.write(f'{req} {st_ms} {time_for_log} {stage} {response}\n')
    log.close()
    return response.json()


# Функция для получения токена логистом
def logiest(phone=None):
    if phone is None:
        phone = phone_logiest
    param_get_token = {"phone": phone, "code": "****", "type": "search"}
    param_request_token = {"phone": phone, "type": "search"}
    a = time_log()
    save_log(a, f'POST user/request-token', (requests.post(f"{site}user/request-token", data=param_request_token)))
    a = time_log()
    r = (requests.post(f'{site}user/get-token', data=param_get_token)).json()
    save_log(a, 'POST user/get-token', (requests.post(f'{site}user/get-token', data=param_get_token)))
    token = {'authorization': 'Bearer ' + r['data']['token']}
    return token


# Функция для получения токена исполнителем
def owner(phone=None):
    if phone is None:
        phone = phone_owner
    param_get_token_app = {"phone": phone, "code": "****", "type": "owner"}
    param_request_token_app = {"phone": phone, "type": "owner"}
    a = time_log()
    save_log(a, 'POST user/request-token', (requests.post(f"{site}user/request-token", data=param_request_token_app)))
    a = time_log()
    r = (requests.post(f'{site}user/get-token', data=param_get_token_app)).json()
    save_log(a, 'POST user/get-token', (requests.post(f'{site}user/get-token', data=param_get_token_app)))
    token = {'authorization': 'Bearer ' + r['data']['token']}
    return token


# Функция для создания техники, если параметр не передается, то техника будет создана на исполнителя: phone_owner
def create_auto(token=None):
    if token is None:
        token = owner()
    for machine in data_stress_t.auto:
        a = time_log()
        save_log(a, 'POST /machine', (requests.post(f"{site}machine", headers=token, json=machine)))
        print('Создал технику')


# Функция для создания заказов
def create_tasks(count):
    token = logiest()
    x = 0
    for i in range(count):
        for task in data_wa_notice.for_test_stress:
            a = time_log()
            save_log(a, 'POST /order', (requests.post(f'{site}order', json=task, headers=token)))
            x += 1
            if x == 10000:
                perf_behavior()
                token = logiest()
                x = 0


# Функция рандомного поведения исполнителем - взятие, бронирование и отказ от заказа.
def perf_behavior():
    token = owner()
    a = time_log()
    s = (requests.get(f'{site}task', headers=token)).json()
    save_log(a, 'GET /task', (requests.get(f'{site}task', headers=token)))
    for xx in s['data']:
        if xx['status'] == 'STATUS_CREATED':
            task_id = xx['id']
            variable = random.randint(1, 3)
            if variable == 1:
                a = time_log()
                save_log(a, f'POST /task/{task_id}/viewed',
                         (requests.post(f'{site}task/{task_id}/viewed', headers=token)))
                a = time_log()
                save_log(a, f'POST /task/{task_id}/skip', (requests.post(f'{site}task/{task_id}/skip', headers=token)))
                print(task_id, ' исполнитель отказался')
            elif variable == 2:
                body_properties = True
                a = time_log()
                save_log(a, f'POST /task/{task_id}/viewed',
                         (requests.post(f'{site}task/{task_id}/viewed', headers=token)))
                a = time_log()
                save_log(a, f'POST /task/{task_id}/reserve',
                         (requests.post(f'{site}task/{task_id}/reserve', headers=token, json=body_properties)))
                a = time_log()
                save_log(a, f'POST /task/{task_id}/approve',
                         (requests.post(f'{site}task/{task_id}/approve', headers=token)))
                print(task_id, ' взял заказ')
            else:
                a = time_log()
                save_log(a, f'POST /task/task{task_id}/viewed',
                         (requests.post(f'{site}task/{task_id}/viewed', headers=token)))
                a = time_log()
                save_log(a, f'POST /task/{task_id}/reserve',
                         (requests.post(f'{site}task/{task_id}/reserve', headers=token, json=True)))
                a = time_log()
                save_log(a, f'POST /task/{task_id}/reserve',
                         (requests.post(f'{site}task/{task_id}/reserve', headers=token, json=False)))
                print(task_id, ' забронировал, отказался')


# Функция удаления заказов у заказчика. Если не передавать токен, то будет удалять у пользователя phone_logiest
def delete_task(token=None):
    if token is None:
        token = logiest()
    a = time_log()
    s = (requests.get(f"{site}order", headers=token)).json()
    save_log(a, 'GET /order', (requests.get(f"{site}order", headers=token)))
    for xx in s['data']:
        if xx['status'] == "":
            a = time_log()
            save_log(a, f'DELETE /order/{xx["id"]}', (requests.delete(f'{site}order/{xx["id"]}', headers=token)))
            print(xx['id'], ' заказчик отменил')


# Функция удаления всей техники у исполнителя. Если не передавать токен, то будет браться у phone_owner
def del_auto():
    token = owner()
    a = time_log()
    s = (requests.get(f"{site}machine", headers=token)).json()
    save_log(a, 'GET /machine', (requests.get(f"{site}machine", headers=token)))
    for xx in s['data']:
        a = time_log()
        save_log(a, f'DELETE /machine/{xx["id"]}', (requests.delete(f"{site}machine/{xx['id']}", headers=token)))
        print('Удалил технику')


# Функция для создания пользователей. Принимает на вход кол-во пользователей для создания и номер с которого начнет
# создавать пользователей. Пользователя создаются по порядку от переданного значения.
def create_user(count, phone):
    for i in range(count):
        ii = list(str(i))
        phone = int(str(phone)[:-(len(ii))] + str(i))
        param_request_token_app = {"phone": phone, "type": "owner"}
        a = time_log()
        save_log(a, 'POST /user/request-token',
                 (requests.post(f"{site}user/request-token", data=param_request_token_app)))
        param_get_token_app = {"phone": str(phone), "code": "****", "type": "owner"}
        a = time_log()
        save_log(a, 'POST /user/get-token', (requests.post(f'{site}user/get-token', data=param_get_token_app)))
        print(f'Создан пользователь: {phone}')


# Функция для создания техники. Принимает 2 значения: 1) кол-во пользователей, которым будет создана техника.
# 2) Телефон (на который\начиная с которого) эта техника будет создаваться. Создается по порядку от переданного телефона
def create_auto_module_owner(count, phone):
    for i in range(count):
        print(f'Добавляю технику исполнителю: {phone + i}')
        param_get_token_app = {"phone": phone + i, "code": "****", "type": "search"}
        param_request_token_app = {"phone": phone + i, "type": "search"}
        a = time_log()
        save_log(a, 'POST /user/request-token',
                 (requests.post(f"{site}user/request-token", data=param_request_token_app)))
        a = time_log()
        # r = (requests.post(f'{site}user/get-token', data=param_get_token_app)).json()
        r = save_log(a, 'POST /user/get-token', (requests.post(f'{site}user/get-token', data=param_get_token_app)))
        token = {'authorization': 'Bearer ' + r['data']['token'], 'executor-id': '445'}
        create_auto(token)


# Функция тестирования модуля поиска исполнителей (рандом поведение).
# Принимает 3 значения: 1) Кол-во пользователей, по которым будут производиться действия. 2) Кол-во различных поведений
# 3) Номер с которого будут эти поведения начинаться.
def module_owner_random(user_count, count, phone):
    for i in range(count):
        behavior = random.randint(1, 4)
        # behavior = 1
        user = random.randint(phone, phone + user_count - 1)
        # Редактирование техники, меняет цену по всем типам оплаты, рандом.
        if behavior == 1:
            token = owner(user)
            a = time_log()
            machine = requests.get(f'{site}machine', headers=token).json()
            print(f'Запросил список техники у исполнителя: {user}')
            save_log(a, 'GET /machine', (requests.get(f'{site}machine', headers=token)))
            auto = random.choice(machine['data'])
            auto['priceVat'] = random.randint(1, 1000000000)
            auto['priceNoVat'] = random.randint(1, 100000000)
            auto['priceCash'] = random.randint(1, 1000000)
            a = time_log()
            requests.post(f'{site}machine/{auto["id"]}', headers=token, json=auto).json()
            save_log(a, f"POST machine/{auto['id']}",
                     (requests.post(f'{site}machine/{auto["id"]}', headers=token, json=auto)))
            print(f'Отредактировал технику исполнителю: {user}')
        # Запрашивает заказы у логиста
        elif behavior == 2:
            token = logiest()
            a = time_log()
            save_log(a, 'GET /order', (requests.get(f'{site}order', headers=token)))
            print(f'Запросил заказы у логиста: {phone_logiest}')
        # Запрашивает задачи у исполнителя. Исполнитель - рандом от переданного phone до phone+user_count
        elif behavior == 3:
            token = owner(user)
            a = time_log()
            save_log(a, 'GET /task', (requests.get(f'{site}task', headers=token)))
            print(f'Запросил задачи для исполнителя: {user}')
        # Запрашивает список техники у исполнителя. Исполнитель - рандом.
        else:
            token = owner(user)
            a = time_log()
            save_log(a, 'GET /machine', (requests.get(f'{site}task', headers=token)))
            print(f'Запросил список техники у исполнителя: {user}')


stage = 'CreateUser'
create_user(1000, 71000000000)
# 1 запуск create_auto_module_owner = 20 видам техники
# добавить еще 9 видов техники
stage = 'CreateAuto'
create_auto_module_owner(2200, 71000000000)
# 1 запуск create_task = 11 заказам. По типу авто-цена
stage = 'CreateTasks'
create_tasks(4600)
# Рандомное поведение пользователя. (кол-во пользователей, кол-во действий, номер с которого начинается)
stage = 'Behavior'
module_owner_random(1000, 50000, 71000000000)
