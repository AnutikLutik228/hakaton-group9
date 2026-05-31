from scr.reader import EmailReader

def test_reader_reads_normal_email(tmp_path):
    email_file = tmp_path / "email.eml"
    email_file.write_text(
        "From: user@example.com\n"
        "To: support@example.com\n"
        "Subject: Test subject\n"
        "\n"
        "Hello from test body",
        encoding="utf-8",
    )

    reader = EmailReader()

    result = reader.read(str(email_file))

    assert result["from"] == "user@example.com"
    assert result["to"] == "support@example.com"
    assert result["subject"] == "Test subject"
    assert "Hello from test body" in result["body"]
    assert result["attachments"] == []


def test_reader_returns_none_for_missing_file(tmp_path):
    reader = EmailReader()
    missing_file = tmp_path / "missing.eml"

    result = reader.read(str(missing_file))

    assert result is None


def test_reader_empty_file_does_not_crash(tmp_path):
    email_file = tmp_path / "empty.eml"
    email_file.write_text("", encoding="utf-8")

    reader = EmailReader()

    result = reader.read(str(email_file))

    assert result["from"] == ""
    assert result["to"] == ""
    assert result["subject"] == ""
    assert result["attachments"] == []


def test_reader_file_without_subject_does_not_crash(tmp_path):
    email_file = tmp_path / "no_subject.eml"
    email_file.write_text(
        "From: user@example.com\n"
        "To: support@example.com\n"
        "\n"
        "Text without subject",
        encoding="utf-8",
    )

    reader = EmailReader()

    result = reader.read(str(email_file))

    assert result["subject"] == ""
    assert "Text without subject" in result["body"]


def test_reader_bad_bytes_do_not_crash(tmp_path):
    email_file = tmp_path / "bad_bytes.eml"
    email_file.write_bytes(b"\xff\xfe\x00\x00bad email")

    reader = EmailReader()

    result = reader.read(str(email_file))

    assert result is not None