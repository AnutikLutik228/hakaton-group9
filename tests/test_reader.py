from email.message import EmailMessage

from src.reader import EmailReader


def test_read_simple_email(tmp_path):
    email_path = tmp_path / "simple.eml"
    email_path.write_text(
        "\n".join(
            [
                "From: user@example.com",
                "To: support@company.ru",
                "Subject: Test request",
                "",
                "Need help with the service.",
            ]
        ),
        encoding="utf-8",
    )

    reader = EmailReader()

    result = reader.read(str(email_path))

    assert result == {
        "from": reader.normalize_letter_to_russian_language("user@example.com"),
        "to": reader.normalize_letter_to_russian_language("support@company.ru"),
        "subject": reader.normalize_letter_to_russian_language("Test request"),
        "body": reader.normalize_letter_to_russian_language("Need help with the service."),
        "attachments": [],
    }


def test_read_multipart_email_with_attachment(tmp_path):
    message = EmailMessage()
    message["From"] = "manager@example.com"
    message["To"] = "support@company.ru"
    message["Subject"] = "Service error"
    message.set_content("Сервис не работает")
    message.add_attachment(
        b"traceback",
        maintype="text",
        subtype="plain",
        filename="error.log",
    )

    email_path = tmp_path / "with_attachment.eml"
    email_path.write_text(message.as_string(), encoding="utf-8")

    reader = EmailReader()

    result = reader.read(str(email_path))

    assert result["from"] == reader.normalize_letter_to_russian_language("manager@example.com")
    assert result["to"] == reader.normalize_letter_to_russian_language("support@company.ru")
    assert result["subject"] == reader.normalize_letter_to_russian_language("Service error")
    assert result["body"] == "Сервис не работает\n"
    assert result["attachments"] == ["error.log"]


def test_read_missing_file_returns_none(tmp_path):
    missing_email_path = tmp_path / "missing.eml"

    result = EmailReader().read(str(missing_email_path))

    assert result is None

