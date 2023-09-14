import copy

from aiogram import types, Dispatcher
from zp.create_bot import bot
from aiogram.utils.exceptions import MessageNotModified
from ..models import edit_msg_clicked_group, edit_msg_clicked_salary, edit_msg_clicked_back, edit_msg_marks
from ..keyboards import mark_salary_mk, mk_cancel, mark_salary_mk_admin
from ..excel import main_exel, calculate_salary
from zp.keyboards import other_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


list_edit = []
async def start_go(msg: types.Message):
    global edit, list_edit
    if msg.from_user.id == 5295520075:
        edit = await bot.send_message(msg.chat.id, "Добро пожаловать ! Я ваш помощник.\nЯ создан, чтобы вы не забивали свою голову излишней рутиной\nВыберите  один из вариантов ниже:", reply_markup=mark_salary_mk_admin)
    else:
        edit = await bot.send_message(msg.chat.id, "Добро пожаловать ! Я ваш помощник.\nЯ создан, чтобы вы не забивали свою голову излишней рутиной\nВыберите  один из вариантов ниже:", reply_markup=mark_salary_mk)
    list_edit.clear()  # чтобы сново и сново не добавлять
    list_edit.append(edit)   # чтобы передавать этот сообщение в другие модули для изменения


async def request_article(clb: types.CallbackQuery):
    if clb.from_user.id == 5295520075:
        try:
            await edit_msg_clicked_group(edit)
        except MessageNotModified:
            await clb.answer()  # убираем ожидания
    else:
        await clb.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)

async def request_article_plus(clb: types.CallbackQuery):
    "Вывод зп"
    if clb.from_user.id == 5295520075:
        try:
            salary = calculate_salary()
            await edit_msg_clicked_salary(edit, int(salary))
        except (MessageNotModified, FileNotFoundError):
            await edit_msg_clicked_salary(edit, 0)
            await clb.answer()
            # await clb.answer(text="hello")
            # await clb.message.answer(text="hello")
            # await clb.answer(text="hello", show_alert=True)
    else:
        await clb.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


async def request_marks(clb: types.CallbackQuery):
    if clb.from_user.id == 5295520075:
        await edit_msg_marks(edit, "mark_set")
    else:
        await clb.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


async def back_go(msg: types.Message):
    await edit_msg_clicked_back(edit)


class FSMAdditionalLesson(StatesGroup):
    student_additional = State()


async def start_fsm_get_lesson_additional(clb: types.CallbackQuery):
    if clb.from_user.id == 5295520075:
        x = await FSMAdditionalLesson.student_additional.set()
        await bot.send_message(clb.from_user.id, "Введите имя ученика (ков)", reply_markup=mk_cancel)
    else:
        await clb.message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


async def additional_name_student_save(msg: types.Message, state: FSMContext):
    if msg.from_user.id == 5295520075:
        await state.update_data(name_group=msg.text)  # сохраняем в озу
        main_exel(msg.text, 1)  # write to excel
        await msg.answer("Доп. урок записан", reply_markup=other_kb.start_kb)
        await state.finish()
    else:
        await msg.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)


def register_handlers_go(dp: Dispatcher):
    dp.register_message_handler(start_go, text='Начать ⚡')
    dp.register_callback_query_handler(back_go, text='go')
    dp.register_callback_query_handler(request_article, text='lesson')
    dp.register_callback_query_handler(request_marks, lambda c: c.data == 'marks')
    dp.register_callback_query_handler(request_article_plus, lambda c: c.data == 'salary')
    dp.register_callback_query_handler(start_fsm_get_lesson_additional, text='additional', state=None)
    dp.register_message_handler(additional_name_student_save, state=FSMAdditionalLesson.student_additional)
