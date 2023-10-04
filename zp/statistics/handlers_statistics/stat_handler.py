from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from zp.create_bot import bot
from zp.data_base import read_sql, sql_delete_group
from zp.diagrams import res_save_plot
from zp.handlers.go import list_edit
from zp.keyboards import mk_groups_kb, other_kb
from zp.models.models_edit_kb import edit_all_or_groups, edit_msg_marks

name_image = []


async def stat_all_or_groups(clb: types.CallbackQuery):
    global name_image
    name_image.clear()
    name_image.append("other_groups.png")
    try:
        await edit_all_or_groups(list_edit[0])
    except MessageNotModified:
        await clb.answer()  # убираем ожидания
    finally:
        res_save_plot()  # создаем графику общую


async def stat_groups(clb: types.CallbackQuery):
    # Вывод групп с clb stat для вывода нужной для группы графики
    await edit_msg_marks(list_edit[0], "stat", webapp=True)  # второй агрумент это команда для кнопки на что это кнопка будет реагировать


async def open_stat(clb: types.CallbackQuery):
    global name_group
    name_group = clb.data.replace("open_stat", "").strip().replace(" ", "_")
    res_save_plot(name_group)  # сохраняем картинку под нужным названием
    await bot.send_message(clb.from_user.id, f'Открыть статистику группы {clb.data.replace("open_stat", "").strip()}', reply_markup=other_kb.mk_group_stat(name_group))


async def send_jpg_group(msg: types.Message):
    await bot.send_document(msg.from_user.id, open(f'../flask_app/static/image/{name_group}.png', 'rb'), reply_markup=other_kb.start_kb)


async def send_jpg_other(msg: types.Message):
    await bot.send_document(msg.from_user.id, open(f'../flask_app/static/image/other_groups.png', 'rb'), reply_markup=other_kb.start_kb)

def register_handlers_stat(dp: Dispatcher):
    dp.register_callback_query_handler(stat_all_or_groups, text='get_statistic')
    dp.register_callback_query_handler(stat_groups, text='stat_group')
    dp.register_callback_query_handler(send_jpg_other, text='jpg_statistic')
    dp.register_callback_query_handler(open_stat, lambda x: x.data and x.data.startswith('open_stat '))
    dp.register_message_handler(send_jpg_group, lambda msg: 'Статистика группы png' in msg.text)
