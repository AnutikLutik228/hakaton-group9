from email.parser import Parser
from email.policy import default
import os
from email import message_from_file
from email.header import decode_header
import chardet

parser = Parser(policy=default)


class EmailReader:
    def normalize_letter_to_russian_language(self, text: str) -> str:
        replacements = {
            'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
            'x': 'х', 'y': 'у', 'A': 'А', 'E': 'Е', 'O': 'О',
            'P': 'Р', 'C': 'С', 'X': 'Х', 'B': 'В', 'M': 'М',
            'T': 'Т', 'H': 'Н', 'K': 'К'
        }
        normalized_text = ''.join(replacements.get(ch, ch) for ch in text)
        return normalized_text

    def get_header(self, message, header_name):
        header = message.get(header_name, '')
        if not header:
            return ''
        header = self.normalize_letter_to_russian_language(header)
        decoded_elements = decode_header(header)
        decoded_string = ''
        for content, encoding in decoded_elements:
            if isinstance(content, bytes):
                decoded_string += content.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += content
        return decoded_string

    def read(self, path: str) -> dict:
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as file:
            raw_data = file.read(50000)
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if not encoding:
            encoding = 'utf-8'

        with open(path, 'r', encoding=encoding) as f:
            message = message_from_file(f)

        email_dict = {
            "from": self.get_header(message, 'From'),
            "to": self.get_header(message, 'To'),
            "subject": self.get_header(message, 'Subject'),
            "body": self.get_body(message),
            "attachments": self.get_attachments(message)
        }

        return email_dict

    def get_body(self, message) -> str:
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    charset = part.get_content_charset() or 'utf-8'
                    payload = part.get_payload(decode=True).decode(charset, errors='ignore')
                    return self.normalize_letter_to_russian_language(payload)
        return self.normalize_letter_to_russian_language(message.get_payload())

    def get_attachments(self, message) -> list:
        attachments = []
        if not message.is_multipart():
            return attachments
        for part in message.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    attachments.append(filename)
        return attachments
