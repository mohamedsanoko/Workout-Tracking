import os
import requests
import datetime as dt

NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID", "Key does not exist")
NUTRITIONIX_APP_KEY = os.environ.get("NUTRITIONIX_APP_KEY", "Key does not exist")
SHEETY_AUTHENTICATION_TOKEN = os.environ.get("SHEETY_AUTHENTICATION_TOKEN", "Key does not exist")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "Content-Type": "application/json",
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_APP_KEY
}

input_text = input("Tell me which exercises you did: ")

data = {
    "query": input_text
}

response = requests.post(url=nutritionix_endpoint, headers=headers, json=data)
exercise_data = response.json()['exercises']
today_date = dt.date.today().strftime("%d/%m/%Y")
time = dt.datetime.now().time().strftime("%H:%M:%S")
sheety_headers = {
    "Authorization": SHEETY_AUTHENTICATION_TOKEN
}
for exercise in exercise_data:
    exercise_name = exercise['name'].title()
    duration = round(exercise['duration_min'])
    calories = round(exercise['nf_calories'])
    row_data = {
        "workout": {
            "date": today_date,
            "time": time,
            "exercise": exercise_name,
            "duration": duration,
            "calories": calories
        }
    }
    sheet_response = requests.post(SHEETY_ENDPOINT, json=row_data, headers=sheety_headers)
    print(sheet_response.status_code)
    json_data = sheet_response.json()
    print(json_data)



