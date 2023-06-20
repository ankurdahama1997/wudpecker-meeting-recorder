import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
status_url = os.getenv("STATUS_URL")
uuid = os.getenv("UUID")

def parse_input(input_str):
    split_input = input_str.split("::::")
    start_time = int(split_input[1])
    speaker_data = split_input[2].split(";;;")
    speaker_dict = {}
    user_id = 0
    json_output = []
    
    for data in speaker_data:
        if not data:  # skip if data is empty
            continue
        speaker_time, speaker_name = data.split("==>")
        speaker_time = int(speaker_time)
        timestamp = (speaker_time - start_time)  # convert milliseconds to seconds

        if speaker_name not in speaker_dict:
            speaker_dict[speaker_name] = user_id
            user_id += 1

        json_output.append({
            "timestamp": timestamp,
            "user_id": speaker_dict[speaker_name],
            "name": speaker_name
        })
        
    return json_output

speakers = []
try:
    with open('speakers.txt', 'r') as file:
        content = file.read()
        speakers = parse_input(content) 
except FileNotFoundError:
    print("The file 'speakers.txt' does not exist in the current directory.")


res = requests.post(status_url+str(uuid)+"/", data={"uuid": uuid, "status": "DONE", "speakers": json.dumps(speakers)})
print(res.text, flush=True)