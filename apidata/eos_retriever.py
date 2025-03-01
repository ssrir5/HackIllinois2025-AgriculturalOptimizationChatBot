import requests



API_KEY = 'apk.55914a899f76dab152d9b7ce70e20de65e0ef85107aecb3e38805f5156b35de9'

















task_status = requests.get(f'https://api-connect.eos.com/api/gdw/api/{TASK_ID}?api_key={API_KEY}')
