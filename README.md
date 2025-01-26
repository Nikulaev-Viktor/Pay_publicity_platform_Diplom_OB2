# Платформа для публикации платного контента 
## Описание задачи
Реализовать платформу для публикации записей пользователями. Публикация может быть бесплатной, доступной любому пользователю без регистрации, либо платной, доступной только авторизованным пользователям, которые оплатили разовую подписку. Для реализации оплаты подписки используйте Stripe. Регистрация пользователя должна быть по номеру телефона. Платформа должна иметь фронтенд в виде шаблонов с использованием Bootstrap.

   # Технические требования:
**Фреймворк**:

- Для реализации проекта использовать фреймворк Django.

**База данных**:
   
- Использовать PostgreSQL для хранения данных.
  
**ORM**:
   
- Использовать встроенную ORM Django для взаимодействия с базой данных.
  
**Контейнеризация**:
   
- Использовать Docker и Docker-compose для контейнеризации приложения.
  
**Аутентификация и авторизация**:
   
- Реализовать регистрацию пользователей по номеру телефона.
  
- Использовать JWT для защиты API и управления сеансами пользователей.
  
**Платежная система**:

- Интегрировать Stripe для обработки оплат подписки.
  
**Фронтенд**:

- Использовать шаблоны с использованием Bootstrap для создания пользовательского интерфейса.
  
**Документация**:

- В корне проекта должен быть файл README.md с описанием структуры проекта и инструкциями по установке и запуску.
  
**Качество кода**:

- Соблюдать стандарты PEP8.
  
- Весь код должен храниться в удаленном Git репозитории.
  
**Тестирование**:

- Код должен быть покрыт тестами с покрытием не менее 75%

  ## Функционал
1. Реализована функциональность публикации записей:
- Бесплатные записи доступны всем пользователям без регистрации.
- Платные записи доступны только авторизованным пользователям, оплатившим разовую подписку.
2. Реализована регистрацию пользователей по номеру телефона с подтверждением номера с помощью отправки opt-сообщения.
 - Реализована смена пароля пользователей по номеру телефона с подтверждением номера с помощью отправки opt-сообщения.
3. Интегрирована платежная система Stripe для обработки оплат подписки.
4. Создан фронтенд на основе шаблонов с использованием Bootstrap для отображения и взаимодействия пользователей с платформой.
5. Для хранения данных используется база PostgreSQL
6. Для взаимодействия с базой данных используется ORM Django
7. Для контейнеризации приложения используется Dockerfile и Docker-compose

## Для запуска проекта необходимо:
1. Клонируйте репозитории https://github.com/Nikulaev-Viktor/Pay_publicity_platform_Diplom_OB2.git
2. Создайте и активируйте виртуальное окружение.
3. Для работы программы необходимо установить зависимости, указанные в файле pyproject.toml с помощью команды poetry install
4. Создайте файл .env. Введите туда свои настройки как указано в файле .env.sample.

## Для запуска проекта с помощью Docker Compose необходимо:
1. Установите Docker и Docker Compose, если они еще не установлены на вашем компьютере.
2. Соберите и запустите контейнеры Docker.
2.1 команды: docker-compose build, docker-compose up
3. Откройте браузер и перейдите по адресу http://localhost:8000 для доступа к проекту.

## Полезные команды для работы с контейнерами DOCKER:
Сборка образов: docker-compose build

Запуск контейнеров: docker-compose up

Запуск контейнеров в фоне: docker-compose up -d

Сборка образа и запуск в фоне после успешной сборки: docker-compose up -d —build

Выполнение команды внутри контейнера app: docker-compose exec app <здесь ваша команда>

Остановка контейнеров: docker-compose stop

Удаление контейнеров: docker-compose down

Проверка в shell всех запущенных и остановленных контейнеров: docker ps -a

Ссылка на тестовые карты для stripe: https://docs.stripe.com/terminal/references/testing#standard-test-cards
