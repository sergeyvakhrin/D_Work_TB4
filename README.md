Инструкция по запуску:

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Как это работает:
1. Пользователь отправляет POST-запрос с номером телефона на users/api/authsms/auth/sms/
    {
    "phone": "+71111111114"
    }
2. Если телефон есть в базе:
   - Отправляется SMS-код из 4-х цифр.
   - Возвращается статус 200 OK. "SMS sent to existing user."
3. Если телефона нет:
   - Создается новая запись.
   - Присваивается 6-ти значный инвайт-код.
   - Отправляется SMS-код из 4-х цифр.
   - Возвращается статус 201 Created. "User created and SMS sent."
4. Пользователь отправляет POST-запрос с номером телефона и смс кодом на /api/authsms/login/
    {
    "phone": "+71111111114",
    "password": "1234"
    }
    - В качестве ответа получаем JWT токены.

Получили доступ к ресурсам сервиса.

Пользователь может:
1. Просматривать свой профиль отправив GET-запрос на /api/authsms/{id}/
    - Ответ:    
    {
    "users_list": [],
    "phone": "+71111111112",
    "email": null,
    "first_name": null,
    "last_name": null,
    "avatar": null,
    "self_referral": 3,
    "user_referral": null
    }
2. Ввести один раз инвайт-код другого пользователя отправив PATCH-запрос на /api/authsms/update/{id}/
        {
            "user_referral": "222222"
        }
        Введенный инвайт-код проверяется на существование в базе.
        Если введенный инвайт-код не найден, выведится ошибка "Object with referral=222222 does not exist."
        Если пользователь уже вводил инвайт-код, то выведится ошибка "Referral already input."
3. редактировать свой профиль отправив PUT-запрос на /api/authsms/update/{id}/
        {
        "phone": "+78888888888",
        "email": "admin@sky.pro",
        "first_name": "Admin",
        "last_name": "SkyPro",
        "avatar": null,
        "user_referral": null,
        }
4. Если меняется номер телефона, придет смс-код на новый номер телефона.
5. Что бы номер телефона изменился, необходимо отправить PATCH-запрос на /api/authsms/update/sms/{id}/ с новым номером
   телефона и смс-кодом, который пришел на новый номер телефона.
        {
         "phone": "+78888888888",
         "sms-code": "1234"
        }
   Если вводимые данные будут не верны, выведется ошибка "Incorrect phone/sms pair."
6. удалить свой профиль отправив DELETE-запрос на /api/authsms/delete/{id}/
        
   


Курсовая работа ТВ4
Описание задачи:

 

В рамках данного проекта необходимо разработать реферальную систему, которая позволяет пользователям регистрироваться и авторизовываться по номеру телефона, а также использовать и распространять инвайт-коды. Эта система будет иметь минимальный интерфейс для тестирования, однако вся логика работы с пользователями и их инвайт-кодами должна быть тщательно проработана и задокументирована.

 

Цель проекта — обеспечить простой и надежный механизм авторизации и реферальной системы, который можно будет легко тестировать и интегрировать в другие системы.

 

### Задача:

 

**Реализовать логику и API для следующего функционала:**

 

1. **Авторизация по номеру телефона:** 
   - Пользователь вводит свой номер телефона для авторизации.
   - Система имитирует отправку 4-значного кода авторизации (с задержкой на сервере 1-2 секунды).


:::info
Вместо иммитации можно использовать реальные сервисы по отправке СМС кодов, например, [этот](https://smsaero.ru/integration/api/)

:::

- Пользователь вводит полученный код для завершения процесса авторизации.
- Если пользователь ранее не авторизовывался, его данные записываются в базу данных.

1. **Запрос на профиль пользователя:** 
   - При первой авторизации пользователю присваивается случайно сгенерированный 6-значный инвайт-код, состоящий из цифр и символов.
   - В профиле у пользователя должна быть возможность ввести чужой инвайт-код, при этом проверяется его существование в системе.
   - В профиле можно активировать только один инвайт-код. Если пользователь уже активировал инвайт-код, он должен отображаться в соответствующем поле при запросе профиля пользователя.
   - API профиля должно выводить список пользователей (номеров телефона), которые ввели инвайт-код текущего пользователя.
2. **API документация:** 
   - Реализовать и описать в README.md API для всего функционала, включая примеры запросов и ответов.
   - Создать и прислать Postman коллекцию со всеми запросами для тестирования API.
   - Документировать API с использованием ReDoc для удобной и понятной автодокументации.
3. **Интерфейс:** 
   - Реализовать интерфейс на Django Templates для базового тестирования функционала.
4. **Контейнеризация:** 
   - Проект должен быть завернут в Docker для облегчения развертывания и обеспечения переносимости.

 

### Технические требования:

1. **Язык программирования:** 
   - Python
2. **Фреймворк:** 
   - Django, DRF для реализации веб-сервера
3. **База данных:** 
   - PostgreSQL для хранения данных
4. **Контейнеризация:** 
   - Docker для контейнеризации приложения
5. **Документация:** 
   - В корне проекта должен быть файл README.md с описанием структуры проекта, инструкциями по установке и запуску, а также описанием API.
6. **Качество кода:** 
   - Соблюдать стандарты PEP8 для Python кода.
   - Весь код должен храниться в удаленном Git репозитории.
7. **Тестирование:** 
   - Написать тесты для всех основных функций платформы.
   - Покрытие тестами должно быть минимум 75%.