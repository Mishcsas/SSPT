# Используем официальный образ Ubuntu (последняя LTS версия)
FROM ubuntu:22.04

# Предотвращаем интерактивные запросы при установке пакетов
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем список пакетов и устанавливаем необходимое
RUN apt-get update && apt-get install -y \
    # Базовые утилиты
    wget \
    curl \
    git \
    nano \
    vim \
    # Для C++ (компиляторы и инструменты)
    g++ \
    gcc \
    make \
    cmake \
    gdb \
    # Для Python
    python3 \
    python3-pip \
    python3-dev \
    # Дополнительные полезные библиотеки
    build-essential \
    # Очищаем кэш apt для уменьшения размера образа
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем символическую ссылку, чтобы 'python' работал (по умолчанию только python3)
RUN ln -s /usr/bin/python3 /usr/bin/python

# Устанавливаем рабочую директорию
WORKDIR /project

# Копируем сайт
COPY . .

# Качаем зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Указываем порт для сайта
EXPOSE 5000

# Команда по умолчанию
CMD ["bash"]