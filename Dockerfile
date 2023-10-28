# Используем официальный образ Python
FROM python:3.10

# Установим зависимости
# Установим зависимости

# Создадим рабочую директорию в контейнере

WORKDIR /app
COPY . /app/
# Копируем файлы зависимостей
# Копируем requirements.txt и устанавливаем зависимости
RUN pip install -r requirements.txt

# Запускаем бота
CMD ["python3", "main.py"]