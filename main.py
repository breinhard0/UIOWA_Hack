import json
import time
import random
import requests
import pandas as pd
from taipy.gui import Gui, notify

API_KEY = "ADD YOUR OPENAI API KEY HERE"
INITIAL_PROMPT = "N/A"
MAX_TOKENS = 150
Filament_Type = ''
answer = ''
result = ''

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
def generate_completion(messages, model="gpt-3.5", temperature=1):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    data["max_tokens"] = MAX_TOKENS

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "I'm sorry, GPT-4 is not available right now."


saved_messages = [
    {"role": "system", "content": INITIAL_PROMPT},
]

user_message = ""
user_message2 = ""
def messages_to_data(messages):
    result = []
    for message in messages:
        result_message = {}
        result_message["Role"] = message["role"]
        result_message["Message"] = message["content"]
        if result_message["Role"] == "system":
            result_message["Role"] = "Result: "
        else:
            result_message["Role"] = "You"
        result.append(result_message)
    return pd.DataFrame(result)


def on_send_click(state):
    notify(state, "info", "Generating response...")
    message = state.user_message
    state.saved_messages.append({"role": "user", "content": message})
    state.saved_messages = state.saved_messages
    state.user_message = ""
    time.sleep(0.1)
    response = generate_completion(state.saved_messages)
    state.saved_messages.append({"role": "system", "content": response})
    state.saved_messages = state.saved_messages
    notify(state, "success", "GPT-4 generated a response!")


def get_data(path_to_csv: str):
    # pandas.read_csv() returns a pd.DataFrame
    dataset = pd.read_csv(path_to_csv)
    dataset["Date"] = pd.to_datetime(dataset["Date"])
    return dataset

path_to_csv = "out.csv"
dataset = get_data(path_to_csv)

path_to_csv = "dataset.csv"
datasetTable = get_data(path_to_csv)

page = """
# **FilamentFinancer**{: .color-primary}

<|PLA|button|on_action=change_toPLAaction|>
<|PETG|button|on_action=change_toPETGaction|>
<|ABS|button|on_action=change_toABSaction|>


<|{user_message2}|input|multiline=false|lines_shown=2|label=Input Grams|on_action=on_send_click|class_name=smaller-input-box|>

<|Enter|button|on_action=button_Action|>

<br/>
<br/>
<br/>
### <p style="text-align: center;">What can I help you with?</p>
<|{messages_to_data(saved_messages)}|table|show_all|width=100%|>

<|{user_message}|input|multiline=True|lines_shown=2|label=Your Message|on_action=on_send_click|class_name=fullwidth|>

<|Send|button|on_action=on_send_click|>

### <p style="text-align: center;">Average Cost of Filament</p>
<|{dataset[1000:]}|chart|type=bar|x=Date|y=Cost|>

<|{datasetTable}|table|width=100%|>
"""
def change_toPLAaction(state):
    notify(state, 'info', f'The filiament type is: {state.Filament_Type}')
    state.Filament_Type = "PLA"
    Filament_Type = "PLA"

def change_toPETGaction(state):
    notify(state, 'info', f'The filiament type is: {state.Filament_Type}')
    state.Filament_Type = "PETG"
    Filament_Type = "PETG"

def change_toABSaction(state):
    notify(state, 'info', f'The filiament type is: {state.Filament_Type}')
    state.Filament_Type = "ABS"
    Filament_Type = "ABS"

def button_Action(state):
    notify(state, "info", "Generating response...")
    answer = state.user_message2
    result = answer
    print(result)

def filament(Filament):
    PricePerGram = (random.randint(9, 17) * int(result)) / 1000
    if(Filament == "PLA"):
        PricePerGram = (random.randint(9, 17) * int(result))/1000
    if (Filament == "PETG"):
        PricePerGram = (random.randint(17, 34) * int(result))/1000
    if (Filament == "PLA"):
        PricePerGram = (random.randint(34, 51) * int(result))/1000



Gui(page).run()