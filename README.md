# Инструкция по установке автотеста

## Установка Python

1. Находим в меню Пуск **"Microsoft Store"**
2. В поиске ищем **"Python 3.10"**
3. Нажимаем кнопку "Установить", ждем окончания установки

## Установка Git

1. Проходим на сайт (Git)[https://git-scm.com/]
2. Нажимаем на кнопку "Download for Windows" и ждем окончания загрузки
3. Устанавливаем, везде прожимая "Next"

## Установка автотеста

1. Ищем в меню Пуск **"Windows PowerShell"** и запускаем его
2. Пропишите команду `mkdir Documets\PyScripts\Testing`
3. Пропишите команду `cd Documets\PyScripts\Testing`
4. Пропишите команду `git clone https://github.com/AnvarShagvaleev/AutoTestingForPochta.git`
5. Пропишите команду 'cd .\AutoTestingForPochta\'
6. Пропишите команду `python3.10 -m venv venv`
7. Пропишите команду `.\venv\Scripts\activate`
8. Пропишите команду `pip3 install -r .\requirements.txt`
9. Закрываем **"Windows PowerShell"**
10. Далее откройте папку `c:/Users/user_name/Documents/PyScripts/Testing/AutoTestingForPochta` и найдите в папке Excel-файл `input.xlsx`. Откройте её и на листе `Авторизация` введите свой логин и пароль от учетной записи. Сохраните и закройте файл.

## Запуск автотеста
1. Ищем в меню Пуск **"Windows PowerShell"** и запускаем его
2. Пропишите команду `cd Documets\PyScripts\Testing\AutoTestingForPochta\`
3. Пропишите команду `.\venv\Scripts\activate`
4. **"Windows PowerShell"** не закрываем. Далее откройте папку `c:/Users/user_name/Documents/PyScripts/Testing/AutoTestingForPochta` и найдите в папке Excel-файл `input.xlsx`. Откройте её и на листе `Таблицы` введите сущности, которые вы хотите протестировать. Сохраните и закройте файл.
5. Переходим обратно в **"Windows PowerShell"** прописываем команду `c:/Users/user_name/Documents/PyScripts/Testing/AutoTestingForPochta/venv/Scripts/python.exe c:/Users/user_name/Documents/PyScripts/Testing/AutoTestingForPochta/main.py`. Ждем окончания тестов.
6. После окончания тестов в папке `c:/Users/user_name/Documents/PyScripts/Testing/AutoTestingForPochta` появится Excel-файл `Report.xlsx` с результатами тестов.