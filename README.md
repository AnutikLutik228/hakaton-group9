# 📬 Post Sorter
 
> Автоматическая классификация и сортировка входящих писем по папкам.
 
**НИУ ВШЭ · Хакатон 2026 · Команда 9**
Аня · Милана · Лиза · Арина · Тимофей
 
---
 
## Установка
 
```bash
git clone https://github.com/AnutikLutik228/hakaton-group9.git
cd hakaton-group9
 
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
 
---
 
## Запуск
 
Положи письма в папку `inbox/`, затем:
 
```bash
# АВТОМАТИЧЕСКИ (macOS, Linux или Windows с установленным Git Bash)
chmod +x run.sh # На Windows (Git Bash) эту строчку можно пропустить
./run.sh
 
# ВРУЧНУЮ (Для любой ОС)
# Если вы на Windows, пишите просто python вместо python3:
python3 src/main.py --inbox inbox
 
# Предпросмотр без перемещения файлов
python3 src/main.py --inbox inbox --dry-run
После запуска письма окажутся в папках по категориям, статистика — в report.txt.
```

---
 
## Тесты
 
```bash
pytest tests/ -v
# 29 passed
```
 
---
 
## Структура
 
```
src/
├── reader.py          # чтение и парсинг писем
├── classifier.py      # классификация по 19 категориям
├── mover.py           # перемещение файлов
├── main.py            # точка входа
└── generate_report.py # статистика
tests/
├── test_classifier.py # 22 теста
├── test_reader.py     # 3 теста
└── test_mover.py      # 3 теста
inbox/                 # входящие письма (не в репо)
```
 
---
 
## Зависимости
 
| Пакет | Версия | Зачем |
|-------|--------|-------|
| `chardet` | 5.2.0 | автоопределение кодировки |
| `pytest` | 9.0.3 | запуск тестов |
