from aiogram import types, Dispatcher
from zp.create_bot import bot
from zp.keyboards import other_kb


async def file_excel_loader(message : types.Message):
    'для отправки файла excel'
    if message.from_user.id == 5295520075:
        try:
            await message.reply_document(open('../zp/data_files/zp_excel.xlsx', 'rb'), reply_markup=other_kb.start_kb)
        except FileNotFoundError as ex:
            await bot.send_message(message.chat.id, "Файл еще не создан!")
    else:
        await message.answer("Доступ запрещен!", reply_markup=other_kb.start_kb)

def register_handlers_excel(dp: Dispatcher):
    dp.register_message_handler(file_excel_loader, text='Получить отчет! 📄')
