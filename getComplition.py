import openai
openai.api_key = "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"


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
