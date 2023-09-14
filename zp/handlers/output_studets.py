import json

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from zp.create_bot import bot
from zp.keyboards import other_kb
from zp.data_base import join_table
from ..models import edit_status_student, edit_status_mark
from ..excel import main_exel
from datetime import datetime
from ..statistics.models import creating_csv
from zp.diagrams import res_save_plot


id_msg_del: list = []
async def output_students_group(callback_query: types.CallbackQuery):
    global msg_edit, name_group, count_student
    if callback_query.from_user.id == 5295520075:
        count_student = ""  # если статус студента не меняли, во второй урок, то сохранится данные из первого урока
        # чтобы этого избежать очищаем количество, и берем количество учеников прямо из сообщения, и не из этого (count_student)
        name_group_and_students = await join_table(callback_query.data.replace("output ", "").split(":")[0]) # split(":") берем id группы
        if name_group_and_students:
            msg_edit = {}  # ключ текст сообщения, значения id сообщения, что по значению редактировать сообщения
            for ret in name_group_and_students:
                id_msg = await bot.send_message(callback_query.from_user.id, text=ret[0].title() + "\nСтатус: присутствует ✅", reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(text=f'Отсутствует {ret[0].title()} ✖', callback_data=f"status {ret[0].title()}")))
                msg_edit[ret[0].title()] = id_msg
            name_group = ret[1]
            await callback_query.answer("Выбрана группа " + name_group)  # вплывающая подсказка
            await bot.send_message(callback_query.from_user.id, f"Ученики группы {name_group} ☝", reply_markup=other_kb.ready_mk)
        else:
            await bot.send_message(callback_query.from_user.id, "У вас нет ни одного ученика в этой группе", reply_markup=ReplyKeyboardRemove())
    else:
        await callback_query.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


data_sudents: str = ''  # если статус не будет изменен, чтобы не стало not defined
async def absent_attend_student(clb: types.CallbackQuery):
    global count_student, data_sudents
    if clb.from_user.id == 5295520075:
        "Вывести для добавлении или отсутвовании"
        "рекция на кнопки отсутсвует (присутсвует)"
        txt_msg = clb.message.text.split(":")[1].strip()
        txt_clb = clb.data.replace("status", "").strip().title()  # берем текст с кнопки, убирая лишнее
        count_student, data_sudents = await edit_status_student(msg_edit, txt_clb, txt_msg, len(msg_edit))
    else:
        await clb.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


async def ready_to_write_exel(msg: types.callback_query):
    global count_student, msg_edit
    if msg.from_user.id == 5295520075:
        date_list = []
        names_list = []
        status_list = []
        groups_list = []
        try:
            if not count_student: # если статус студента не меняли
                raise NameError
            # сохраняет полученные данные в excel
            main_exel(name_group, count_student)
        except NameError:  # если статус студента не меняли
            count_student = len(msg_edit)
            main_exel(name_group, count_student)
            count_student = ''  # очищаем, чтобы не было в следющий раз как будно мы не меняли статус, хотя и меняли
        finally:
            date = datetime.now().strftime("%d_%m_%Y")
            creating_csv().create_csv_headers()
            if data_sudents:  # был ли статус изменен
                for name, status in data_sudents.items():
                    if isinstance(status['text'], str):
                        if status['text'].split(":")[1].strip() == "присутствует ✅":
                            data_sudents[name]['text'] = 1
                for name, status in data_sudents.items():
                    names_list.append(name)
                    status_list.append(status['text'])
                    date_list.append(date)
                    groups_list.append(name_group)
            else:  # если статус не был изменен
                for name, status in msg_edit.items():
                    if isinstance(status['text'], str):
                        if status['text'].split(":")[1].strip() == "присутствует ✅":
                            msg_edit[name]['text'] = 1
                for name, status in msg_edit.items():
                    date_list.append(date)
                    groups_list.append(name_group)
                    names_list.append(name)
                    status_list.append(status['text'])
            creating_csv().create_df(date_list, names_list, groups_list, status_list)
        await msg.answer("Данные сохранены!", reply_markup=other_kb.start_kb)
    else:
        await msg.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


async def output_students_group_mark(callback_query: types.CallbackQuery):
    "Для вывода фукции с кнопка поощерение, замечание"
    global msg_edit_mark, group_name
    if callback_query.from_user.id == 5295520075:
        group_name = callback_query.data.replace("mark_set ", "").strip().split(":")[1]
        name_group_and_students = await join_table(callback_query.data.replace("mark_set ", "").split(":")[0])  # берем id группы
        if name_group_and_students:
            msg_edit_mark = {}  # ключ текст сообщения, значения id сообщения, что по значению редактировать сообщения
            for ret in name_group_and_students:
                id_msg = await bot.send_message(callback_query.from_user.id, text=ret[0].title() + " 🟡", reply_markup=InlineKeyboardMarkup().row(
                    InlineKeyboardButton(text=f'Поощрить', callback_data=f"status_mark plus {ret[0].title()}"), InlineKeyboardButton(text=f'Замечание', callback_data=f"status_mark minus {ret[0].title()}")))
                msg_edit_mark[ret[0].title()] = id_msg
            name_group_mark = ret[1]
            await bot.send_message(callback_query.from_user.id, f"Ученики группы {name_group_mark} ☝", reply_markup=other_kb.ready_mk_stat)
        else:
            await bot.send_message(callback_query.from_user.id, "У вас нет ни одного ученика в этой группе", reply_markup=ReplyKeyboardRemove())
    else:
        await callback_query.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)

async def encourage_reprimand_student(clb: types.CallbackQuery):
    "Вывести для поощерении или замечании"
    global count_student, data_sudents_marks
    if clb.from_user.id == 5295520075:
        "рекция на кнопки замечание и поощерение"
        txt_msg = clb.message.text.strip()
        # txt_clb = clb.data.replace("status_mark", "").strip().title()  # берем текст с кнопки, убирая лишнее
        txt_clb = clb.data # берем текст с кнопки, убирая лишнее
        # data_sudents_marks = await edit_status_mark(msg_edit_mark, txt_clb)
        await edit_status_mark(msg_edit_mark, txt_clb)
    else:
        await clb.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


async def ready_to_write_statistics(msg: types.callback_query):
    json_data = json.load(open("data_files/json_status_students.json", encoding='utf-8'))
    if msg.from_user.id == 5295520075:
        names_list = []
        mark_minis = []
        mark_plus = []
        names_groups = []
        date_list = []
        date = datetime.now().strftime("%d_%m_%Y")
        print(json_data, "json")
        for dicts in json_data:
            """
            За поощерение 1, замечание -0.5.
            Если число, то какое:
                Занчит есть либо замечание или поощерение
            Иначе:
                0 ничего

            в другом документе за пропуски 0, на графие пропус должно быть -1
            
            """

            names_list.append(list(dicts.keys())[0])
            match list(dicts.values())[0]:
                case 1:
                    mark_plus.append(list(dicts.values())[0])
                    mark_minis.append(0)
                case 0.5:
                    mark_minis.append(list(dicts.values())[0])
                    mark_plus.append(0)

            date_list.append(date)
            names_groups.append(group_name)

        creating_csv().create_stat_df(date_list, names_list, names_groups, mark_plus, mark_minis)

        await msg.answer("Данные сохранены!", reply_markup=other_kb.start_kb)
    else:
        await msg.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


def register_handlers_output_students(dp: Dispatcher):
    dp.register_callback_query_handler(output_students_group, lambda x: x.data and x.data.startswith('output '))
    dp.register_callback_query_handler(absent_attend_student, lambda x: x.data and x.data.startswith('status '))
    dp.register_callback_query_handler(output_students_group_mark, lambda x: x.data and x.data.startswith('mark_set '))
    dp.register_callback_query_handler(encourage_reprimand_student, lambda x: x.data and x.data.startswith('status_mark '))
    dp.register_message_handler(ready_to_write_exel, text='Готово')
    dp.register_message_handler(ready_to_write_statistics, text='Закончить')
