# Используем образ Ubuntu c зеркала(последняя LTS версия)
FROM mirror.gcr.io/library/ubuntu:latest

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
WORKDIR /SSPT

# Копируем сайт
COPY . .


# Устанавливаем python3-venv (нужен для создания виртуального окружения)
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение
RUN python3 -m venv /venv

# Устанавливаем pip внутри виртуального окружения (обновляем до свежей версии)
RUN /venv/bin/pip install --upgrade pip

# Устанавливаем зависимости через pip из виртуального окружения
RUN /venv/bin/pip install -r requirements.txt

# Добавляем виртуальное окружение в PATH, чтобы команды были доступны
ENV PATH="/venv/bin:$PATH"

# Указываем порт для сайта
EXPOSE 5000

# Команда по умолчанию
CMD ["bash"]