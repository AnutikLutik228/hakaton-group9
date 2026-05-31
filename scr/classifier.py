import re
import logging

logger = logging.getLogger(__name__)


class EmailClassifier:
    def classify(self, email: dict) -> str:
        if email is None:
            return "Корзина"
        text = self._get_full_text(email)

        checks = [
            self._is_trash,
            self._is_spam,
            self._is_urgent,
            self._is_bugs,
            self._is_access,
            self._is_it,
            self._is_git,
            self._is_contract,
            self._is_changes,
            self._is_finance,
            self._is_vacation,
            self._is_procurement,
            self._is_security,
            self._is_analytics,
            self._is_logistics,
            self._is_external,
            self._is_digest,
            self._is_reminder,
            self._is_auto,
        ]

        for check in checks:
            result = check(email, text)
            if result:
                logger.info(f"Письмо классифицировано: {result}")
                return result

        logger.warning(f"Категория не определена, отправлено в unknown")
        return "unknown"

    def _get_full_text(self, email: dict) -> str:
        subject = email.get("subject", "") or ""
        body = email.get("body", "") or ""
        sender = email.get("from", "") or ""
        return (subject + " " + body + " " + sender).lower()

    def _is_trash(self, email: dict, text: str):
        if not email.get("body", "").strip() and not email.get("subject", "").strip():
            return "Корзина"

    def _is_spam(self, email: dict, text: str):
        keywords = ["spam", "вы стали победителем", "для получения приза",
                    "введите данные банковской карты"]
        if any(kw in text for kw in keywords):
            return "Спам"
        if re.search(r'https?://', email.get("body", "")):
            if any(kw in text for kw in ["приз", "выигрыш", "акция"]):
                return "Спам"

    def _is_urgent(self, email: dict, text: str):
        keywords = ["срочно", "срочная", "помощь", "критичный",
                    "alert", "внимание!", "немедленно", "второй запрос"]
        if any(kw in text for kw in keywords):
            return "Срочно"

    def _is_bugs(self, email: dict, text: str):
        keywords = ["не работает", "ошибка", "перестал открываться",
                    "сломался", "не включается", "падает", "зависает",
                    "неисправность", "ремонт", "недоступен", "недоступна"]
        attachments = email.get("attachments", [])
        bug_files = ["error.log", "error_log.txt"]
        if any(kw in text for kw in keywords):
            return "Баги"
        if any(f in bug_files for f in attachments):
            return "Баги"

    def _is_access(self, email: dict, text: str):
        keywords = ["новый сотрудник", "приступает к работе",
                    "временный сотрудник", "временного сотрудника",
                    "требуется доступ", "нужны права", "выдать права",
                    "пропал доступ", "запрос доступа"]
        if any(kw in text for kw in keywords):
            return "Выдача доступов"

    def _is_it(self, email: dict, text: str):
        keywords = ["bi-система", "[it] [info]", "сервис", " it ",
                    "тикет", "active directory", "it security team",
                    "техническое"]
        attachments = email.get("attachments", [])
        if any(kw in text for kw in keywords):
            return "Отдел IT"
        if "error_log.txt" in attachments:
            return "Отдел IT"

    def _is_git(self, email: dict, text: str):
        if "gitlab" in text:
            return "git"

    def _is_contract(self, email: dict, text: str):
        keywords = ["договор", "договоры", "подписать", "подписью"]
        if any(kw in text for kw in keywords):
            return "Договоры"

    def _is_changes(self, email: dict, text: str):
        keywords = ["правки", "правка", "новая версия"]
        if any(kw in text for kw in keywords):
            return "Правки"

    def _is_finance(self, email: dict, text: str):
        keywords = ["финансы", "бухгалтерия", "счёт", "оплата", "оплаты", "счёта"]
        if any(kw in text for kw in keywords):
            return "Бухгалтерия"

    def _is_vacation(self, email: dict, text: str):
        keywords = ["больничный лист", "отпуск", "отпуска"]
        if any(kw in text for kw in keywords):
            return "Отпуска"

    def _is_procurement(self, email: dict, text: str):
        if "закупки" in text and "отдел" in text:
            return "Закупки"

    def _is_security(self, email: dict, text: str):
        if "безопасность" in text and "отдел" in text:
            return "Безопасность"

    def _is_analytics(self, email: dict, text: str):
        if "аналитика" in text and "отдел" in text:
            return "Отдел Аналитики"

    def _is_logistics(self, email: dict, text: str):
        if "логистика" in text:
            return "Отдел Логистики"

    def _is_external(self, email: dict, text: str):
        if "запрос от внешнего пользователя" in text:
            return "Внешнее"

    def _is_digest(self, email: dict, text: str):
        if "корпоративный дайджест" in text:
            return "Корпоративный дайджест"

    def _is_reminder(self, email: dict, text: str):
        keywords = ["напоминание", "напоминаем"]
        if any(kw in text for kw in keywords):
            return "Напоминания"

    def _is_auto(self, email: dict, text: str):
        keywords = ["автоматическое уведомление", "автоматические уведомления",
                    "это письмо сгенерировано автоматически"]
        if any(kw in text for kw in keywords):
            return "Автоуведомления"
        if re.search(r'(время|метрика)\s*:', text):
            return "Автоуведомления"
