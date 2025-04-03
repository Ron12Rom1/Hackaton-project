from groq import Groq

from secret import GROQ_API_KEY

import time


client = Groq(
    api_key=GROQ_API_KEY,
)

with open("you_are.txt", "r") as f1:
    you_are = f1.read()

def send_to_AI(message):
        
    with open ("memory.peepee_poopoo", "r+") as mem:
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

    with open("memory.peepee_poopoo", "a") as mem:
        mem.write("\nUser: " + message  + "\nYou: " + output)

    return output

if __name__ == "__main__":
    userIn = "-1"
    while userIn != "exit":
        userIn = input(":   ")
        print(send_to_AI(userIn))