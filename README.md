### Hexlet tests and linter status:
[![Actions Status](https://github.com/DZharenko/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DZharenko/python-project-83/actions)
[![Python CI](https://github.com/DZharenko/python-project-83/actions/workflows/pyci.yaml/badge.svg)](https://github.com/DZharenko/python-project-83/actions/workflows/pyci.yaml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DZharenko_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DZharenko_python-project-83)

🐍 Python Project 83
# 🔍 Page Analyzer

Live Demo: https://python-project-83-fjtf.onrender.com

## 📋 Описание проекта

**Page Analyzer** — это веб-приложение, которое позволяет добавлять сайты, запускать их проверки и сохранять результаты (код ответа, заголовки, описание). Подходит для анализа SEO-данных и доступности сайтов.

## 🚀 Возможности
- Добавление и нормализация URL-адресов
- Проверка сайтов по HTTP-запросу
- Извлечение и сохранение:
  - Статуса ответа (HTTP Status)
  - `<title>`
  - `<h1>`
  - `<meta name="description">`
- Просмотр истории всех проверок
- Удобный интерфейс с Bootstrap 5

---


## 🚀 Технологии

- Python 3.12.3
- Flask
- PostgreSQL
- BeautifulSoup
- Psycopg2
- Requests

## 🔧 Использование

Чтобы установить проект, клонируйте репозиторий:
```
git clone https://github.com/DZharenko/python-project-83.git
```
Для установки зависимостей запустите:
```
uv run flask --debug --app page_analyzer:app run
```
Инициализируйте базу данных:
```
psql -f database.sql
```
Запустите приложение:
```
uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
```
Для удаления проекта запустите:
```
rm -rf python-project-83
```


## ⭐Star this repo if you found it useful! ⭐
