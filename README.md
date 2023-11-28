# Менеджер вакансий

## Установка:

```
1) https://github.com/Zuhomim/vacancy_manager
2) "Fork" repository
3) git clone созданного репозитория в Вашем Git-аккаунте
```

## Структура:

### 1. JSON - директория хранения файла json со списком полученных по API HH.ru вакансий

### 2. SRC - основная рабочая директория

### 2.1 API_modules - class HeadHunterAPI с методами отправки запросов на API.hh.ru

### 2.2 Config_database:

### - database.ini - файл-инициализатор для СУБД-postgreSQL (host, user, password, port)

### - config.py - парсер для чтения настроек инициализации СУБД и передачи конфигурации в рабочие модули

### 2.3 Database_modules:

### - db_creator.py - class для создания БД в postgreSQL с названием "hh_vacancies" и таблицами (vacancies, employers)

### - db_manager.py - class для отбора и получения данных с БД postgreSQL (включает 5 разных методов)

### 2.4 Utils:

### - json_saver.py - вспомогательный класс для сохранения вакансий в директорию json

### - utils.py - содержит функцию чтения статичного набора (10) компаний (с соответствующими id API.hh.ru), по к-ым происходит отбор

### 3. employers.txt - файл с набором (10) компаний для поиска на API.hh.ru

### 4. main.py - файл для запуска интерактива с пользователем

### 5. requirements.txt - все необходимые зависимости для виртуального окружения:

### - pip install -r requirements.txt

### - poetry add ...

## Запуск программы (интерактив с пользователем через терминал):
```
python3 main.py (запуск происходит из директории проекта "vacancy_manager")
```
