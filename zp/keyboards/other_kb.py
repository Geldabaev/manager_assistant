from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from zp.data_base import read_sql
from aiogram.types.web_app_info import WebAppInfo

__all__ = ["mark_salary_mk", "ReplyKeyboardMarkup", "mk_groups_kb", "mk_go", "mk_cancel", "start_kb",
           "cancel_mk", "marks_mk", "ready_mk_stat", "mk_all_or_group_stat", "mk_group_stat", "mark_salary_mk_admin"]

from zp.diagrams import res_save_plot

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
conf_btn = KeyboardButton("Настроить 🛠")
run_btn = KeyboardButton("Начать ⚡")
getdoc_btn = KeyboardButton("Получить отчет! 📄")
start_kb.add(run_btn).add(conf_btn).add(getdoc_btn)

mark_salary_mk = InlineKeyboardMarkup(row_width=2)
kb_mark_salary = [InlineKeyboardButton(text="Урок 📚", callback_data="lesson"), InlineKeyboardButton(text="Доп. урок 📝", callback_data='additional')]
mark_salary_mk.row(*kb_mark_salary).row(InlineKeyboardButton(text="Баллы 🥇", callback_data="marks"), InlineKeyboardButton(text="Вывести статистику 📊", callback_data="get_statistic"))


mark_salary_mk_admin = InlineKeyboardMarkup(row_width=2)
kb_mark_salary_admin = [InlineKeyboardButton(text="Урок 📚", callback_data="lesson"), InlineKeyboardButton(text="Доп. урок 📝", callback_data='additional')]
mark_salary_mk_admin.row(*kb_mark_salary).add(InlineKeyboardButton(text="ЗП 💰", callback_data='salary')).row(InlineKeyboardButton(text="Баллы 🥇", callback_data="marks"), InlineKeyboardButton(text="Вывести статистику 📊", callback_data="get_statistic"))


mk_go = InlineKeyboardMarkup(row_width=1)
kb_zp = InlineKeyboardButton(text="Назад 🔙", callback_data="go")
mk_go.add(kb_zp)


async def mk_groups_kb(clb_data_command, webapp=False):
    "Вывод групп из бд в кнопках инлайн"
    read = await read_sql('my_groups')
    groups_inline = []
    if read and not webapp:
        for ret in read:
            groups_inline.append(InlineKeyboardButton(text=ret[1] + " 🎓", callback_data=f"{clb_data_command} {ret[0]}:{ret[1]}"))  # указываем id группы, чтобы выводить потом студентов по их id группы ret[0]
    elif webapp:
        for ret in read:
            groups_inline.append(InlineKeyboardButton(text=ret[1] + " 📊", callback_data=f"open_stat {ret[1]}"))  # указываем id группы, чтобы выводить потом студентов по их id группы ret[0]

    mk_groups = InlineKeyboardMarkup(row_width=2)

    for i in groups_inline:
        mk_groups.add(i)
    mk_groups.add(kb_zp)
    return mk_groups


mk_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Отмена")


ready_mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ready_kb = KeyboardButton("Готово")
cancel_kb = KeyboardButton("Отмена")
ready_mk.add(ready_kb).add(cancel_kb)


cancel_mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_kb_one = KeyboardButton("Отмена")
cancel_mk.add(cancel_kb_one)


marks_mk = InlineKeyboardMarkup(row_width=2)
mark_kb1 = InlineKeyboardButton(text="Поощрить", callback_data="encourage")
mark_kb2 = InlineKeyboardButton(text="Замечание", callback_data="reprimand")
marks_mk.row(mark_kb1, mark_kb2)


ready_mk_stat = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
end_kb_stat = KeyboardButton("Закончить")
ready_mk_stat.add(end_kb_stat).add(cancel_kb)


mk_all_or_group_stat = InlineKeyboardMarkup(row_width=2)
kb_stats = [InlineKeyboardButton(text="Общая статистика 📈", web_app=WebAppInfo(url=f"https://2187-2a03-d000-1481-f3f1-f6c9-2e26-e357-e2a3.ngrok-free.app/reg/other_groups")), InlineKeyboardButton(text="Статистика группы 📉", callback_data="stat_group")]
mk_all_or_group_stat.row(*kb_stats).add(InlineKeyboardButton(text="Общая статистика png", callback_data="jpg_statistic")).add(kb_zp)


def mk_group_stat(name_group):
    mk_group_one = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_group_one = KeyboardButton("Открыть статистику", web_app=WebAppInfo(url=f"https://2187-2a03-d000-1481-f3f1-f6c9-2e26-e357-e2a3.ngrok-free.app/reg/{name_group}"))
    kb_image = KeyboardButton("Статистика группы png")
    mk_group_one.add(kb_group_one).add(kb_image).add(cancel_kb)
    return mk_group_one
