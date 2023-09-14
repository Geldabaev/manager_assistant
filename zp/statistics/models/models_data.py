import csv
import pandas as pd
import os.path


class CreatingCsv:
    def __init__(self):
        "создаем заголовки"
        self.create_csv_headers()
        self.create_csv_headers_stat()

    def create_csv_headers(self):
        'Для учета поссещаемости'
        if not os.path.isfile('../zp/data_files/attendance.csv'):
            with open("../zp/data_files/attendance.csv", "w") as file:
                write = csv.writer(file)

                write.writerow(
                    (
                        "Date",
                        "Name",
                        "Group",
                        "Status"
                    )
                )

    def create_df(self, date, names, group, status):
        'Для учета поссещаемости'
        df = pd.DataFrame({
                      "date": date,
                      "name": names,
                      "group": group,
                      "status": status
                        })

        df.to_csv("../zp/data_files/attendance.csv", mode='a', header=False, index=False)

    def create_csv_headers_stat(self):
        "Для ввода статистики"
        if not os.path.isfile('../zp/data_files/statistics.csv'):
            with open("../zp/data_files/statistics.csv", "w") as file:
                write = csv.writer(file)

                write.writerow(
                    (
                        "Date",
                        "Name",
                        "Group",
                        "Encouragement",
                        "Reprimand",
                    )
                )

    def create_stat_df(self, date, names, group, encouragement, reprimand):
        print(len(date))
        print(len(names))
        print(len(group))
        print(len(encouragement))
        print(len(reprimand))
        "Для ввода статистики"
        df = pd.DataFrame({
                      "date": date,
                      "name": names,
                      "group": group,
                      "encouragement": encouragement,
                      "reprimand": reprimand
                           })

        df.to_csv("../zp/data_files/statistics.csv", mode='a', header=False, index=False)


def creating_csv():
    return CreatingCsv()
