import os

from src.mover import EmailMover


def test_move_email_to_category(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "message.eml"
    source.write_text("email body", encoding="utf-8")

    result = EmailMover().move(str(source), "Баги")

    destination = tmp_path / "Баги" / "message.eml"
    assert result == os.path.join("Баги", "message.eml")
    assert destination.read_text(encoding="utf-8") == "email body"
    assert not source.exists()


def test_move_email_renames_file_when_destination_exists(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "message.eml"
    source.write_text("new email", encoding="utf-8")

    category_dir = tmp_path / "Срочно"
    category_dir.mkdir()
    existing_file = category_dir / "message.eml"
    existing_file.write_text("old email", encoding="utf-8")

    result = EmailMover().move(str(source), "Срочно")

    renamed_destination = category_dir / "message_1.eml"
    assert result == os.path.join("Срочно", "message_1.eml")
    assert existing_file.read_text(encoding="utf-8") == "old email"
    assert renamed_destination.read_text(encoding="utf-8") == "new email"
    assert not source.exists()


def test_move_broken_email_when_category_is_none(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "broken.eml"
    source.write_text("bad email", encoding="utf-8")

    result = EmailMover().move(str(source), None)

    destination = tmp_path / "broken" / "broken.eml"
    log_path = tmp_path / "run.log"
    assert result == os.path.join("broken", "broken.eml")
    assert destination.read_text(encoding="utf-8") == "bad email"
    assert "Broken file moved: " + str(source) in log_path.read_text(encoding="utf-8")
    assert not source.exists()
