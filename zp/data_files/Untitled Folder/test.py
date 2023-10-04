# import pandas as pd
# import csv
# import datetime
#
#
# class PaymentTime:
#     def __init__(self):
#         self.payment_time = "payment_time.csv"
#         self.counting_lessons = "counting_lessons.csv"
#
#     def open_df(self):
#         self.df3 = pd.read_csv("counting_lessons.csv")
#         self.df4 = pd.read_csv("payment_time.csv")
#
#     def create_files(self):
#         with open(self.counting_lessons, "w") as file:
#             "Подсчет кол. уроков ученика"
#             write = csv.writer(file)
#
#             write.writerow(
#                 (
#                     "Ученики",
#                     "Кол. уроков",
#                 )
#             )
#
#         with open(self.payment_time, "w") as file:
#             """Время и статус оплаты"""
#             write = csv.writer(file)
#
#             write.writerow(
#                 (
#                     "Ученики",
#                     "Время оплаты",
#                     "Дата",
#                     "Статус"
#                 )
#             )
#
#     def is_summ_counting(self, row):
#         "Изменения кол. уроков ученика"
#         if row['Кол. уроков'] and row['Ученики'] == self.name:
#             return row['Кол. уроков'] + 1
#         return row['Кол. уроков']
#
#     def write_students_counting(self, name='Yunus'):
#         self.open_df()
#         self.name = name
#         self.df3['Кол. уроков'] = self.df3.apply(self.is_summ_counting, axis=1)
#         print(self.df3)
#         self.update_status()
#
#     def update_status(self):
#
#         names = self.df3[self.df3['Кол. уроков'] == 9]['Ученики'].to_list()
#         if names:
#             len_names = len(names)
#             df = pd.DataFrame({
#                 "Ученики": names,
#                 "Время оплаты": ["Да"] * len_names,
#                 "Дата": [datetime.datetime.now().strftime("%d_%m_%Y")] * len_names,
#                 "Статус": ["Нет"] * len_names
#             })
#
#             df.to_csv("payment_time.csv", mode='a', header=False, index=False)  # пишем что ему пора оплатить
#
#             'удаляем его из списков после того как записали в другой докумен, что ему нужно оплатить, чтобы начать новый отчет'
#             self.df3.set_index("Ученики", inplace=True)
#             self.df3.drop(names, inplace=True)
#             self.df3 = self.df3.reset_index()
#             self.df3.to_csv("counting_lessons.csv", mode='w', header=True, index=False)
#
#
# payment_time = PaymentTime()
# # payment_time.create_files()
# payment_time.write_students_counting("Yunus")


# n = int(input())
# m = int(input())
# c2 = int(input())
# c5 = int(input())
#
# remainder = m - (n-1)
# cost = 0
#
# if m <= n:
#     cost = 0
# else:
#     if c2 * 4 < c5:
#         cost = (m - n) * c2
#     else:
#         while remainder > 0:
#             if remainder >= 4:
#                 cost += remainder // 4 * c5
#                 remainder %= 4
#             elif remainder * c2 < c5:
#                 cost += remainder * c2
#                 remainder = 0
#             else:
#                 cost += c5
#                 remainder = 0
# print(cost)

n = {"online"}
print(n.intersection({}))