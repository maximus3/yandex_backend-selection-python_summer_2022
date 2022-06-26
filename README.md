# Mega Market Open API

## Description
Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022

## Run

Запуск сервиса в docker-контейнере:
`make docker-d`

Предварительно необходимо создать папку и доступ pgadmin для работы с ней:
```
mkdir pgadmin
sudo chown -R 5050:5050 pgadmin
```

## Commands

### Docker clean, build, up detach
    make docker-d

### Docker clean, build, up, clean
    make docker

### Up docker container
    make docker-up

### Down docker container
    make docker-down

### Create venv (if no docker)
    make venv

### Run app
    make up

### Run tests
    make test

### Run linters
    make lint

### Run formatters
    make format

### Run format and lint code then run tests
    make check

## Task Description

### Описание

В данном задании вам предлагается реализовать бэкенд для веб-сервиса сравнения цен, аналогичный сервису [Яндекс Товары](https://yandex.ru/products). Обычно взаимодействие с такими сервисами происходит следующим образом:
1. Представители магазинов загружают информацию о своих товарах и категориях. Также можно изменять и удалять информацию о ранее загруженных товарах и категориях.
2. Покупатели, пользуясь веб-приложением, могут искать предложения разных магазинов, сравнивать цены и следить за их динамикой и историей.

Ваша задача - разработать REST API сервис, который позволяет магазинам загружать и обновлять информацию о товарах, а пользователям - смотреть какие товары были обновлены за последние сутки, а также следить за динамикой цен товара или категории за указанный интервал времени.

### Технические требования

Реализуйте сервис на Python или Java в зависимости от выбранного направления школы. Сервис должен удовлетворять следующим требованиям:
- реализует спецификацию API, описанную в файле <code>openapi.yaml</code>, и корректно отвечает на запросы проверяющей системы
- некоторые обработчики из них являются необязательными, их реализация позволит вам набрать дополнительное количество баллов
- сервис должен быть развернут в контейнере на `0.0.0.0:80`
- сервис должен обеспечивать персистентность данных (должен сохранять состояние данных при перезапуске)
- сервис должен обладать возможностью автоматического перезапуска при рестарте контейнера, в котором работает ваш бэкенд (этого можно достичь настройкой контейнера)
- после запуска сервиса время ответа сервиса на все методы API не должно превышать 1 секунду
- время полного старта сервиса не должно превышать 1 минуту
- импорт и удаление данных не превосходит 1000 элементов в 1 минуту
- RPS (Request per second) получения  статистики, недавних изменений и информации об элементе суммарно не превосходит 100 запросов в секунду

#### Тестирование

В качестве предварительного тестирования мы подготовили для вас юнит-тест <code>unit_test.py</code>, написанный на Python. Он позволит проверить минимальную работоспособность вашего бэкенда до отправки решения на проверку.

Для прохождения проверки обратите внимание на следующее:
- Коды ответа HTTP.
- Корректность JSON структуры запроса и ответа.
- Типы данных (строки, числа).
- Формат даты.
- Проведение необходмых валидаций входных данных.
- Краевые случаи.
- Формат и коды ошибок.

Рекомендуется написать свои тесты для проверки разработанной функциональности.

#### Развёртывание приложения
На выделенном контейнере вы можете:
1. Работать с вашим приватным репозиторием.
2. Использовать средства контейнеризации, например Docker, он уже установлен.
3. Устанавливать программное обеспечение для сборки и запуска вашего приложения, используя Интернет. Например, для реализации задания на языке Java вы можете использовать Maven или Gradle. Явных требований по сборке и развертыванию приложения нет.
4. Настраивать контейнер по своему усмотрению (например, настройки автозапуска или версии Java).

#### Оценивание решения
Оценивание решения будет проходить после отправки решения кандидатом на проверку в несколько этапов.
1. Автоматическое тестирование. Проверяющей системой будут выполнятся запросы к вашему бэкенду. Будет проверятся корректность ответов, их коды ответа HTTP и тела.
2. Ручная проверка решения проверяющими Школы бэкенд-разработки. Будут учитываться различные особенности вашего решения:
   - Способ решения.
   - Качество решения.
   - Возможность обработки нескольких запросов сервисом одновременно.
   - Покрытие тестами.
   - Документация описывающая код, сборку, запуск и работу приложения.

### Полезные материалы
1. Подробнее про спецификацию OpenAPI вы можете узнать здесь [Спецификация OpenAPI](https://swagger.io/specification/)
2. [Практическое руководство по разработке бэкенд-сервиса на Python](https://habr.com/ru/company/yandex/blog/499534/)
3. Как реализовать автозапуск программы при рестарте контейнера вы можете узнать в [Практическом руководстве по разработке бэкенд-сервиса на Python](https://habr.com/ru/company/yandex/blog/499534/) в разделе "Деплой".
4. [Визуализация файла спецификации Open API](https://editor.swagger.io)
5. [Автозапуск сервера при рестарте контейнера](https://habr.com/ru/company/southbridge/blog/255845/)

### FAQ
**Как обратиться к моему приложению с рабочего компьютера?**

Как и проверяющая система, вы можете сделать запрос по адресу <code> https://hostname.usr.yandex-academy.ru </code> для проверки своего решения, где hostname - это название вашего контейнера (можно получить войдя в контейнер).

**Как подключиться к базе данных внутри моего контейнера?**

Вы можете развернуть требуемую базу данных внутри Docker (или другой программы для контейнеризации) или на выданном вам контейнере. В качестве примера вы можете изучить статью на [Habr](https://habr.com/ru/post/578744/) , рассказывающую о развёртывании PostgreSQL в Docker контейнере.

**Почему не использовали oneOf в спецификации OpenAPI?**

Поскольку у OpenAPI в последних версиях есть [нерешенные проблемы с кодогенерацией oneOf классов](https://github.com/OpenAPITools/openapi-generator/issues/15), мы решили отказаться от использования такой функциональности.

### Правки
Здесь будут описаны внесенные изменения/правки в задание.
