import pytest

from src.classifier import EmailClassifier


def make_email(subject="", body="", sender="", attachments=None):
    if attachments is None:
        attachments = []

    return {
        "subject": subject,
        "body": body,
        "from": sender,
        "to": "support@company.ru",
        "attachments": attachments,
    }


@pytest.mark.parametrize(
    "email, expected_category",
    [
        (make_email(subject="Вы стали победителем", body="Введите данные банковской карты"), "Спам"),
        (make_email(subject="Срочно", body="Нужна помощь немедленно"), "Срочно"),
        (make_email(subject="Ошибка", body="Сервис не работает"), "Баги"),
        (make_email(subject="Доступ", body="Новый сотрудник приступает к работе, нужны права"), "Выдача доступов"),
        (make_email(subject="[IT] [INFO]", body="Техническое уведомление"), "Отдел IT"),
        (make_email(subject="GitLab", body="GitLab pipeline failed"), "git"),
        (make_email(subject="Договор", body="Нужно подписать договор"), "Договоры"),
        (make_email(subject="Правки", body="Новая версия документа"), "Правки"),
        (make_email(subject="Оплата", body="Бухгалтерия просит проверить счёт"), "Бухгалтерия"),
        (make_email(subject="Отпуск", body="Заявление на отпуск"), "Отпуска"),
        (make_email(subject="Отдел закупки", body="Запрос в отдел закупки"), "Закупки"),
        (make_email(subject="Отдел безопасность", body="Письмо в отдел безопасность"), "Безопасность"),
        (make_email(subject="Отдел аналитика", body="Письмо в отдел аналитика"), "Отдел Аналитики"),
        (make_email(subject="Логистика", body="Нужна логистика по доставке"), "Отдел Логистики"),
        (make_email(subject="Внешний запрос", body="Запрос от внешнего пользователя"), "Внешнее"),
        (make_email(subject="Дайджест", body="Корпоративный дайджест за неделю"), "Корпоративный дайджест"),
        (make_email(subject="Напоминание", body="Напоминаем о встрече"), "Напоминания"),
        (make_email(subject="Авто", body="Это письмо сгенерировано автоматически"), "Автоуведомления"),
    ],
)
def test_classifier_categories(email, expected_category):
    classifier = EmailClassifier()
    result = classifier.classify(email)
    assert result == expected_category


def test_classifier_empty_email_goes_to_trash():
    classifier = EmailClassifier()
    email = make_email()
    result = classifier.classify(email)
    assert result == "Корзина"


def test_classifier_none_email_goes_to_trash():
    classifier = EmailClassifier()
    result = classifier.classify(None)
    assert result == "Корзина"


def test_classifier_unknown_email_goes_to_unknown():
    classifier = EmailClassifier()
    email = make_email(subject="Обычное письмо", body="Просто текст без ключевых слов")
    result = classifier.classify(email)
    assert result == "unknown"


def test_classifier_detects_bug_by_attachment():
    classifier = EmailClassifier()
    email = make_email(subject="Лог", body="Посмотрите файл", attachments=["error.log"])
    result = classifier.classify(email)
    assert result == "Баги"
