import openai
import os
openai.api_key = os.environ.get('MY_KEY', '')


def generate_completion(messages, user_id):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,

        )
        completion_text = response["choices"][0]["message"]["content"]
        print(completion_text)

        return completion_text
    except Exception as e:
        print(e)
        return None
