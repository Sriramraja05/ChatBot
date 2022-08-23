from ast import main
import os
import openai
import threading
from twilio.rest import Client 

openai.api_key = "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"
completion = openai.Completion()


start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
''' 
account_sid = 'ACbb361f9aa316de065bbd10465fed8ae4' 
auth_token = 'fd5432aefb778c946b5ccca84efc1792'
client = Client(account_sid, auth_token) 

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer



def main():
    threading.Timer(3.0, main).start()
    messages = client.messages.list(limit=1)
    import re
    for record in messages:
        last_message = record.body
        user_message = re.search(r"You said :([\w\W]*)",str(last_message))
        if user_message:
            try:
                user_message = user_message.group(1)
                user_message = user_message.replace("Configure your WhatsApp Sandbox's Inbound URL to change this message.","")
                #invokes Gpt3
                answer = ask(user_message)
                message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=answer,      
                                to='whatsapp:+917806944588' 
                            )
            except Exception:
                print("Exception:",Exception)

if __name__ == "__main__":
    main()