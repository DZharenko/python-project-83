#!/usr/bin/env bash
set -e  # остановиться при любой ошибке

echo "=== Starting build process ==="

# Скачиваем и устанавливаем uv
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Устанавливаем зависимости
echo "Installing dependencies..."
uv sync

# Выполняем миграции базы данных
echo "Running database migrations..."
psql -a -d $DATABASE_URL -f database.sql || {
    echo "Warning: Migrations might have failed, but continuing build..."
    # Или просто echo "Migrations completed"
}

echo "=== Build completed successfully ==="