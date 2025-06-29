@echo off
REM Переходим в директорию, где лежит этот .bat (корень проекта)
pushd "%~dp0"

REM Создаём виртуальное окружение в папке venv
python -m venv venv
if %errorlevel% neq 0 (
    echo Ошибка: не удалось создать виртуальное окружение.
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

REM Обновляем pip
python -m pip install --upgrade pip

REM Устанавливаем зависимости из requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Файл requirements.txt не найден в %~dp0
)

REM Возвращаемся в предыдущую директорию
popd

echo.
echo Виртуальное окружение создано и зависимости установлены.
pause