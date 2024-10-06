# Сервис управления рассылками на Django

## Реализованная логика работы рассылки
- доступ к сервису возможен только для авторизованных пользователей
- пользователю доступны создание, редактирование и удаление расслок, сообщений, клиентов
  -рассылки могут быть с разной периодичностью: однокртано, ежедевно, еженедельно, ежемесячно
  -по умолчанию рассылки не активны
  -при изменении статуса рассылки на активную она начинает выполняться

- Автоматическая рассылка реализована с помощью библиотеки django-crontab. По умолчанию система проверяет наличие новых рассылок раз в минуту. (настройку можно изменить в config/settings.py -> CRONJOBS).
- Добавление автоматической рассылки
  - python manage.py crontab add

- Рассылка может быть запущена в любое время из командной строки с помощью кастомной команды
  python manage.py send_mailing

## Запуск проекта:
- Необходимые переменные окружения перечислены в файле .env.sample
- Файл с зависимостями - pyproject.toml
- Установка зависимостей выполняется командой
  poetry install
- Необходимо применить миграции командой
  python3 manage.py migrate
- Запуск WEB-приложения командой
  python manage.py runserver

## Пользователи:
### Администратор системы (суперпользователь)
- Команда для создания суперпользователя
  python manage.py create_su
- Откроется страница авторизации, можно авторизироваться аккаунтом суперпользователя для доступа в административную панель, либо перейти к регистрации пользователя сервиса.

## Интерфейс пользователя системы
- Расширена модель пользователя для регистрации по почте, а также верификации электронного адреса. Добавлен интерфейс для входа, регистрации и подтверждения почтового ящика, редактирования профиля.
- Пользователь может создавать рассылки, клиентов, сообщения, управлять своими рассылками и списком клиентов.
- Каждый пользователь системы имеет доступ только к своему списку рассылок и подписчиков.

### Функционал менеджеров рассылки
- Может просматривать любые рассылки.
- Может просматривать список пользователей сервиса.
- Может просматривать отменять рассылки (изменять их статус).

### Блог
В сущность блога добавлены следующие поля:
- заголовок,
- содержимое статьи,
- изображение,
- количество просмотров,
- дата публикации,
- автор.

### Главная страница
На главной странице отображается информация:
- количество рассылок всего,
- количество сообщений
- количество уникальных клиентов для рассылок,
- количество попыток рассылок.
