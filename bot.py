import asyncio
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import WebAppInfo
from amplitude import Amplitude
from amplitude import BaseEvent
from bot_bd import db

bot_token = "###"

openai.api_key = '###'

bot = Bot(bot_token)

dp = Dispatcher(bot)

amplitude = Amplitude("f03339a75d031e4bf4d534afe518f34e")


class CharacterState(StatesGroup):
    ChoosingCharacter = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    track_amplitude("Sign Up", str(message['from']['id']))

    date_to_bd = [el[1] for el in message['from'] if el[0] not in ['is_bot', 'language_code']]
    date_to_bd.append(message.date)
    db.insert_full_data_users(date_to_bd)

    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Выбрать персонажа', web_app=WebAppInfo(url='https://127.0.0.1:5000')))
    await message.reply('Привет! Это бот в котором ты можешь пообщаться с разными персонажами.')


@dp.message_handler(content_types=['web_app_data'])
async def processing_data(message: types.Message, state: FSMContext):
    character = message.web_app_data.data

    track_amplitude('Pick character', str(message['from']['id']))
    db.update_character(message['from']['id'], str(character))
    print(character)

    hello_message = db.get_hello_message(str(character))
    await state.update_data()
    await message.reply(hello_message)

    await state.update_data(character=character)
    await CharacterState.next()


@dp.message_handler()
async def handle_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    character = data.get('character')

    user_id = str(message['from']['id'])

    if character == 'mario':
        character += 'from super mario game'

    user_message = str(message.text)

    db.insert_user_message(user_id, user_message)

    track_amplitude("User send call", user_id)

    response = generate_character_response(user_message, character, user_id)

    await message.reply(response)

    db.insert_character_response(character, response, user_id)

    track_amplitude('Get response from openai api', user_id)


def generate_character_response(user_message, character, user_id):
    message = f'Respond as if you are {character}, here is the message to reply to: {user_message}'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=100,
        temperature=0.8,
        n=1,
        stop=None,
    )

    if response.choices[0].text.strip():
        track_amplitude('Get response from openai api', user_id)
        return response.choices[0].text.strip()

    else:
        return 'OpenAI is currently unavailable or has sent an empty message'


def track_amplitude(event, user_id):
    amplitude.track(
        BaseEvent(
            event_type=event,
            user_id=user_id,
            event_properties={
                "source": "notification"
            }
        )
    )
    amplitude.shutdown()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
