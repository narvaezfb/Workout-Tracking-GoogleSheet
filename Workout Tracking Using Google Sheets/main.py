import requests
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")
SHEETY_ENDPOINT = "https://api.sheety.co/7269c1cedc011e77d60fe35eb9da9a1b/fabianWorkouts/workouts"
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"


def estimateCaloriesBurnedRequest(userInput):
    try:
        auth_headers = {
            "x-app-id": API_ID,
            "x-app-key": API_KEY,
            "Content-Type": "application/json"
        }
        body = {
            "query": userInput,
            "gender": "male",
            "weight_kg": 72.5,
            "height_cm": 167.64,
            "age": 23
        }

        response = requests.post(
            url=NUTRITIONIX_ENDPOINT, json=body, headers=auth_headers)
        response.raise_for_status()
    except:
        print("something went wrong ")
    else:
        print(response.text)
        return response.json()


def formatDataReponse(response):
    date = dt.datetime.now().strftime("%d/%m/%Y")
    time = dt.datetime.now().strftime("%H:%M:%S")
    exercise = response["exercises"][0]["name"]
    duration = response["exercises"][0]["duration_min"]
    calories = response["exercises"][0]["nf_calories"]

    body_data = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }
    return body_data


def askUserForInput():
    try:
        userInput = input("Tell me which exercises you did today: ")
    except:
        print("something went wrong with user's input")
    else:
        return userInput


def postDataToGoogleSheet(data):
    try:
        sheety_endpoint = SHEETY_ENDPOINT
        response = requests.post(url=sheety_endpoint, json=data)
        response.raise_for_status()
    except:
        print("Something went wrong in posting data to sheety")
    else:
        return response.text


def main():
    userInput = askUserForInput()
    calories_response = estimateCaloriesBurnedRequest(userInput)
    formattedData = formatDataReponse(calories_response)
    sheety_response = postDataToGoogleSheet(formattedData)
    print(sheety_response)


main()
