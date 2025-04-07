from groq import Groq
import dotenv

import time


client = Groq(
    api_key=dotenv.get_key('.env', 'SECRET_KEY'),
)

with open("AI_shit/you_are.txt", "r") as f1:
    you_are = f1.read()

def chat_with_ai(message):
        
    with open ("AI_shit/memory.peepee_poopoo", "r+") as mem:
        memory = mem.read()

        chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": str(you_are) + "It is: " + str(time.time()) + 
             ".   this is what you remember from our previous conversation: " + str(memory)},

            {"role": "user", "content": message}
        ],
        model="llama3-70b-8192",
        stream=False,
        top_p=1,
        temperature=1.5,
        frequency_penalty=2.0,
        presence_penalty=2.0,
    )

    output = chat_completion.choices[0].message.content

    print("\n", output)
    # pyttsx3_TTS(output)

    with open("AI_shit/memory.peepee_poopoo", "a") as mem:
        mem.write("\nUser: " + message  + "\nYou: " + output)

    return output

if __name__ == "__main__":
    userIn = "-1"
    while userIn != "exit":
        userIn = input(":   ")
        print(chat_with_ai(userIn))