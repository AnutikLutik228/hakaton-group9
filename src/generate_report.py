def generate_report(stats):
    with open("report.txt", "w", encoding="utf-8") as file:
        file.write("Report\n")
        file.write("------\n")

        for category in stats:
            file.write(category + ": " + str(stats[category]) + "\n")