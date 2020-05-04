from flask import Flask, request
import logging
from random import shuffle

import json
help(shuffle)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        suggs = [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
                "Зачем он мне?",
                "Он дорогой.",
                "Он слишком большой.",
                "Я боюсь слонов.",
                "А чем его кормить?",
                "Сама купи",
                "Мне не нужен слон.",
                "Слон есть в зоопарке.",
                "Никогда не куплю.",
                "Перестань.",
                "Это надоедает.",
                "Слоны некрасивые",
                "Он опасен.",
                "Слоны не продаются.",
                "Нет.",
                "Да не куплю я!!!",
                "Лучше куплю кота.",
                "Я не знаю где купить.",
                "...",
                "Что?",
                "Какой ещё слон?"
            ]
        shuffle(suggs)
        sessionStorage[user_id] = {
            'suggests': suggs
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    suggests.append({
        "title": "Ладно",
        "url": "https://market.yandex.ru/search?text=слон",
        "hide": True
    })

    session['suggests'] = session['suggests'][1:]

    sessionStorage[user_id] = session

    return suggests


if __name__ == '__main__':
    app.run()
