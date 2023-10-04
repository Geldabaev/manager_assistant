import csv
import pandas as pd
import os.path
import datetime


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


class PaymentTime:
    def __init__(self):
        self.payment_time = "payment_time.csv"
        self.counting_lessons = "counting_lessons.csv"
        self.create_files()

    def open_df(self):
        self.df3 = pd.read_csv(f'../zp/data_files/{self.counting_lessons}')
        self.df4 = pd.read_csv(f'../zp/data_files/{self.payment_time}')

    def create_files(self):
        if not os.path.isfile(f'../zp/data_files/{self.counting_lessons}'):
            with open(self.counting_lessons, "w") as file:
                "Подсчет кол. уроков ученика"
                write = csv.writer(file)

                write.writerow(
                    (
                        "Ученики",
                        "Кол. уроков",
                    )
                )

        if not os.path.isfile(f'../zp/data_files/{self.payment_time}'):
            with open(self.payment_time, "w") as file:
                """Время и статус оплаты"""
                write = csv.writer(file)

                write.writerow(
                    (
                        "Ученики",
                        "Время оплаты",
                        "Дата",
                        "Статус"
                    )
                )

    def is_summ_counting(self, row):
        "Изменения кол. уроков ученика"
        if row['Кол. уроков'] and row['Ученики'] == self.name:
            return row['Кол. уроков'] + 1
        return row['Кол. уроков']

    def write_students_counting(self, name):
        self.open_df()
        self.name = name
        if self.df3[self.df3["Ученики"] == name]['Ученики'].to_list():
            self.df3['Кол. уроков'] = self.df3.apply(self.is_summ_counting, axis=1)
            self.df3.to_csv(f'../zp/data_files/{self.counting_lessons}', mode='w', header=True, index=False) # сохраняем изменения кол. уроков
            self.update_status()  # проверка прошли ли все 9 уроков
        else:  # если ученика там нет, записываем
            df = pd.DataFrame([{
                "Ученики": name,
                "Кол. уроков": 1,
            }])

            df.to_csv(f'../zp/data_files/{self.counting_lessons}', mode='a', header=False, index=False)  # пишем что ему пора оплатить

    def update_status(self):
        names = self.df3[self.df3['Кол. уроков'] == 9]['Ученики'].to_list()
        if names:
            len_names = len(names)
            df = pd.DataFrame({
                "Ученики": names,
                "Время оплаты": ["Да"] * len_names,
                "Дата": [datetime.datetime.now().strftime("%d_%m_%Y")] * len_names,
                "Статус": ["Нет"] * len_names
            })

            df.to_csv(f'../zp/data_files/{self.payment_time}', mode='a', header=False, index=False)  # пишем что ему пора оплатить

            'удаляем его из списков после того как записали в другой докумен, что ему нужно оплатить, чтобы начать новый отчет'
            self.df3.set_index("Ученики", inplace=True)
            self.df3.drop(names, inplace=True)
            self.df3 = self.df3.reset_index()
            self.df3.to_csv(f'../zp/data_files/{self.counting_lessons}', mode='w', header=True, index=False)


def write_payment_time(student_names: list):
    payment_time = PaymentTime()
    for i in student_names:
        payment_time.write_students_counting(i)

