import os
import argparse
from reader import EmailReader
from classifier import EmailClassifier
from mover import EmailMover
from generate_report import generate_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inbox", default="inbox")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    inbox_path = args.inbox

    reader = EmailReader()
    classifier = EmailClassifier()
    mover = EmailMover()

    stats = {}

    if not os.path.exists(inbox_path):
        print("Inbox folder not found")
        return

    for file_name in os.listdir(inbox_path):
        if not (file_name.endswith('.eml') or file_name.endswith('.txt')):
            continue
        src_path = os.path.join(inbox_path, file_name)

        if not os.path.isfile(src_path):
            continue

        email = reader.read(src_path)

        if email is None:
            category = None
            report_category = "broken"
        else:
            category = classifier.classify(email)
            report_category = category


        if report_category not in stats:
            stats[report_category] = 0

        stats[report_category] += 1

        if args.dry_run:
            print(src_path + " -> " + report_category)
        else:
            mover.move(src_path, category)

    generate_report(stats)

    print("Done")
    print("Report saved to report.txt")


if __name__ == "__main__":
    main()