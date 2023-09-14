import pandas as pd
import matplotlib.pyplot as plt


__all__ = ["res_save_plot"]


def is_result_marks(row):
    return (row['Status'] + row["Encouragement"]) - row['Reprimand']


def res_save_plot(name_group=''):
    df1 = pd.read_csv("../zp/data_files/attendance.csv")
    df2 = pd.read_csv("../zp/data_files/statistics.csv")
    df3 = pd.merge(df1, df2, how='outer')
    df3 = df3.fillna(0)
    df3['result'] = df3.apply(is_result_marks, axis=1)
    try:
        if name_group and name_group != 'other_groups':  # групповая статистика
            # df3[df3["Group"] == name_group]['Name'].value_counts().plot(kind='bar', figsize=(20, 10))
            d = df3[df3["Group"] == name_group.replace("_", " ")].pivot_table(index='Date', columns='Name', values="result", aggfunc='sum')[::-1]
            d.plot(kind='bar', figsize=(13, 15))
            plt.savefig(f'../flask_app/static/image/{name_group}.png')
            plt.close()
        else:  # общая статистика
            df4 = df3.groupby(by="Name")['result'].sum().sort_values(ascending=False)
            df4[::-1].plot(kind='barh', figsize=(20, 10))
            plt.savefig('../flask_app/static/image/other_groups.png')
            plt.close()
    except Exception as ex:
        print(ex)
        print("Статитики еще нет для этой группы")
    # d.plot(kind='barh', figsize=(13, 15))
    # d.plot(kind='barh', figsize=(13, 15))

    # plt.show()


