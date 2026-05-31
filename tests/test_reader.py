from src.reader import EmailReader


def test_read_email(tmp_path):
    file = tmp_path / "mail.eml"

    file.write_text(
        "From: user@test.ru\n"
        "To: support@test.ru\n"
        "Subject: Ошибка в работе сервиса\n"
        "\n"
        "Сервис не открывается после обновления",
        encoding="utf-8",
    )

    result = EmailReader().read(str(file))

    assert result["subject"] == "Ошибка в работе сервиса"
    assert "Сервис не открывается" in result["body"]


def test_no_file(tmp_path):
    result = EmailReader().read(str(tmp_path / "no.eml"))

    assert result is None


def test_empty_file(tmp_path):
    file = tmp_path / "empty.eml"
    file.write_text("", encoding="utf-8")

    result = EmailReader().read(str(file))

    assert result["subject"] == ""