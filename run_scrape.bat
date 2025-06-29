@echo off
REM ==========================================================
REM  run_scrape.bat
REM  Автоматический запуск scrape_made_in_china.py из корня проекта
REM ==========================================================

REM Перейти в директорию, где лежит этот .bat (корень проекта)
pushd "%~dp0"

REM Проверка наличия виртуального окружения
if not exist venv\Scripts\activate.bat (
    echo Внимание: виртуальное окружение не найдено.
    echo Запустите setup_venv.bat для его создания, затем повторите запуск.
    popd
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Ошибка: не удалось активировать виртуальное окружение.
    popd
    pause
    exit /b 1
)

REM Проверяем наличие скрипта scrape_made_in_china.py
if not exist scrape_made_in_china.py (
    echo Ошибка: файл scrape_made_in_china.py не найден в текущей директории.
    popd
    pause
    exit /b 1
)

REM Запуск парсинга
echo Запускаем парсинг компаний...
python scrape_made_in_china.py

REM Сохраняем код возврата
set "RC=%errorlevel%"

REM Деактивация виртуального окружения
deactivate 2>nul

REM Возвращаемся в исходную директорию
popd

REM Вывод результата
echo.
if %RC% equ 0 (
    echo Парсинг завершен успешно.
) else (
    echo Парсинг завершился с ошибкой (код %RC%).
)
echo.
pause
