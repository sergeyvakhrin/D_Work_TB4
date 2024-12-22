Инструкция.

Как это работает:
1. Пользователь отправляет POST-запрос с номером телефона на /auth/sms/
    {
    "phone": "+71111111114"
    }
2. Если телефон есть в базе:
   - Отправляется SMS-код из 4-х цифр.
   - Возвращается статус 200 OK.
3. Если телефона нет:
   - Создается новая запись.
   - Присваивается 6-ти значный инвайт-код.
   - Отправляется SMS-код из 4-х цифр.
   - Возвращается статус 201 Created.
4. Пользователь отправляет POST-запрос с номером телефона и смс кодом на /users/login/
    {
    "phone": "+71111111114",
    "password": "1234"
    }

Получили доступ к ресурсам сервиса.

Пользователь может:
1. просматривать свой профиль на /users/"pk"/
2. ввести один раз инвайт-код другого пользователя на /users/update/"pk"/
        {
            "user_referral": "222222"
        }
        Введенный инвайт-код проверяется на существование в базе.
        Если введенный инвайт-код не найден, выведится ошибка "Object with referral=222222 does not exist."
        Если пользователь уже вводил инвайт-код, то выведится ошибка "Referral already input."
3. редактировать свой профиль /users/update/"pk"/
        {
        "phone": "+78888888888",
        "email": "admin@sky.pro",
        "first_name": "Admin",
        "last_name": "SkyPro",
        "avatar": null,
        "user_referral": null,
        }
   



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