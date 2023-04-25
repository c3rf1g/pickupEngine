import openai
openai.api_key = "sk-xXXxa7Hn0wZYi42ASzm8T3BlbkFJaQDwSj5VZdFOp3BaYJ5y"


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
