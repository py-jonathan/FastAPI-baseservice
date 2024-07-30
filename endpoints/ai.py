import openai
from config import app_config

openai.api_key = app_config["OPENAI"]["api_key"]

async def chat_with_ai(model: str, message: str):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
        return {"message": response.choices[0].message.content}
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")
