#!/bin/bash

cd "$(dirname "$0")"


if ! command -v python3 &> /dev/null; then
    echo "Ошибка: python3 не найден"
    exit 1
fi


if [ ! -d "inbox" ]; then
    echo "Ошибка: папка inbox не найдена"
    exit 1
fi


source venv/bin/activate


python3 src/main.py --inbox inbox "$@" 2>>run.log


if [ $? -eq 0 ]; then
    echo "Готово! Письма разобраны по папкам."
    echo "Статистика сохранена в report.txt"
else
    echo "Ошибка при выполнении. Подробности в run.log"
    exit 1
fi