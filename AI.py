from groq import Groq

from secret import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY,
)

def send_to_AI(message):
        
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a fluent Hebrew speaker you never replay in English",
                "role": "user",
                "content": message

            }
        ],
        model="gemma2-9b-it",
    )

    return(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    userIn = "-1"
    while userIn != "exit":
        userIn = input(":   ")
        print(send_to_AI(userIn))