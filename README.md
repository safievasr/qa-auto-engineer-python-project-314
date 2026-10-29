# Тестирование канбан-доски с Selenium (Python)

[![hexlet-check](https://github.com/safievasr/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/safievasr/qa-auto-engineer-python-project-314/actions)

[![Quality gate status](https://sonarcloud.io/api/project_badges/measure?project=safievasr_qa-auto-engineer-python-project-314&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=safievasr_qa-auto-engineer-python-project-314)

Напишите тесты для проверки работы приложения

Учебный проект Хекслета: https://ru.hexlet.io/programs/qa-auto-engineer-python

## Описание проекта

Task Manager напоминает знакомые трекеры вроде Redmine: в системе есть пользователи, статусы, метки и задачи. Каждая задача привязана к статусу (колонке доски) и исполнителю, а работа строится вокруг перемещения карточек между этапами. Приложение развёрнуто в Docker-образе и доступно как SPA без отдельного бэкенда — все проверки выполняются на уровне клиентского интерфейса.

Что предстоит сделать:

Настроить окружение: поднять фронтенд в Docker, подготовить Python-проект через uv, установить Selenium, pytest и вспомогательные инструменты
Построить инфраструктуру тестов: фикстуры, конфигурации, Page Object-классы и утилиты
Описать сквозные сценарии: от запуска приложения до CRUD-операций с пользователями, статусами, метками и задачами
Реализовать проверки канбан-доски: фильтрацию, смену статуса, перетаскивание карточек
Провести рефакторинг: вынести повторяющиеся шаги, оптимизировать ожидания, обезопасить тесты от флаки

## Стек

- Python

## Установка

<!-- Опишите установку: клонирование, зависимости, переменные окружения -->

```bash
git clone https://github.com/safievasr/qa-auto-engineer-python-project-314.git
cd qa-auto-engineer-python-project-314
```

## Использование

<!-- Добавьте примеры запуска и запись asciinema — именно это смотрит работодатель -->

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
