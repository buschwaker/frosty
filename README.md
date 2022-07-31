# Тестовое задание

## Задача

Написать модели, которые позволят:

1) Делить юзеров на продавцов и покупателей(продавцы не могут быть покупателями)
2) Создавать продавцам лоты с информацией о виде цветка(ромашка/тюльпан и т.п.), его оттенка(перечень оттенков ограничен и известен заранее), количестве товара этого вида, цене за один товар
3) Продавец может выбирать: отображать выбранный лот покупателям или нет
4) Покупатели могут оставлять отзывы на лоты и на продавца
5) Отслеживать сделки

В конце написать скрипт, который будет возвращать информацию в виде списка продавцов с перечнем покупателей, совершивших покупку у этого продавца и общей суммой покупок

## Инструкция по запуску проекта на своей машине:
1. Скачиваем репозиторий
2. Устанавливаем и активируем виртуальное окружение  
3. Устанавливаем зависимости `pip install -r requirements.txt`
4. В директории проекта `python manage.py loaddata db.json` для dummy data
5. Устанавливаем миграции `python manage.py migrate`
6. Запускаем проект `python manage.py runserver`

## Запуск скрипта

Для запуска скрипта, выводящего информацию о продавцах, их покупателях и заработанной сумме, нужно:

1. В директории проекта `python manage.py shell`.
2. Импортируем класс сделок 'from flower.models import Deal'
3. Вызываем метод класса full_info `Deal.full_info()`

## Данные администратора
Логин/Пароль: `admin/admin`
