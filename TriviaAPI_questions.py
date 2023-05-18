import requests
import random

def request_q(topic, qtype):
    url = 'https://opentdb.com/api.php'
    params = {
        'amount': 1, # количество вопросов
        'category': topic, # категория
        'difficulty': 'medium', # уровень сложности
        'type': qtype # тип вопросов
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            result = data['results'][0]
            question = result['question']
            correct_answer = result['correct_answer']
            if qtype == 'multiple':
                # для множественного выбора
                options = result['incorrect_answers'] + [correct_answer]
                random.shuffle(options)
                return [question, options, correct_answer]
            elif qtype == 'boolean':
                # для вопроса да/нет
                options = ['True', 'False']
                correct_index = options.index(correct_answer)
                return [question, options, options[1] if correct_index == 0 else options[0]]
        else:
            return None
    else:
        return None


# generated = request_q(12, 'boolean')
# print(generated[2])
