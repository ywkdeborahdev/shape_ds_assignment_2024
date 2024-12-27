import requests
import certifi
import pandas as pd
import json
import time

# create log file for recording
file_name = 'Shatin.txt'

# function for writing to log file
def append_to_file(text):
    with open(file_name, 'a') as file:
        file.write(text + "\n")  # Add a newline after each entry

# URL of the website to crawl
url = "https://hk.centanet.com/findproperty/api/Transaction/Search"

# variables for handling page number
size = 48

# create dict to store has for each building age range
ageRangeDictList = [
    {'min': 0, 'max': 4},
    {'min': 5, 'max': 9},
    {'min': 10, 'max': 19},
    {'min': 20, 'max': 29},
    {'min': 30, 'max': 39},
    {'min': 40, 'max': 56},
]

# loop through each age range
for ageRange in ageRangeDictList:
    min = ageRange["min"]
    max = ageRange["max"]
    # reset page offset
    offset = 0

    ageRangeText = f"This is to record age range from {min} to {max}."
    append_to_file(ageRangeText)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    # first payload to obtain count number
    ageRangePayload = {"postType": "Both", "day": "Day1095", "sort": "InsOrRegDate", "order": "Descending", "size": size,
               "offset": 0, "pageSource": "search", "currency": "HKD",
               "typeCodes": ["19-HMA001", "19-HMA021", "19-HMA062", "19-HMA106", "19-HMA107", "19-HMA170", "19-HMA176",
                             "19-HMA187", "19-HMA188", "19-HMA994", "19-HMA995", "19-HMA996"], "areaUnit": "Feet",
               "buildingAgeRange": {"min": min, "max": max},
               "hmas": ["HMA001", "HMA021", "HMA062", "HMA106", "HMA107", "HMA170", "HMA176", "HMA187", "HMA188", "HMA994",
                        "HMA995", "HMA996"]}
    # Get number of records from this API call
    ageRangeResponse = requests.post(url, json=ageRangePayload, headers=header, verify=certifi.where())
    ageRangeResponseData = ageRangeResponse.json()
    totalAgeRangeRecord = ageRangeResponseData["count"]
    noOfLoopsForAgeRange = int(totalAgeRangeRecord / size) + 1
    ageRangeRecordText = f"There are a total of {totalAgeRangeRecord}, number of loops are {noOfLoopsForAgeRange}."
    append_to_file(ageRangeRecordText)
    dataList = []
    for i in range(noOfLoopsForAgeRange):
        if i != 0:
            offset = size * i
        payload = {"postType": "Both", "day": "Day1095", "sort": "InsOrRegDate", "order": "Descending", "size": size,
                   "offset": offset, "pageSource": "search", "currency": "HKD",
                   "typeCodes": ["19-HMA001", "19-HMA021", "19-HMA062", "19-HMA106", "19-HMA107", "19-HMA170", "19-HMA176",
                                 "19-HMA187", "19-HMA188", "19-HMA994", "19-HMA995", "19-HMA996"], "areaUnit": "Feet",
                   "buildingAgeRange": {"min": min, "max": max},
                   "hmas": ["HMA001", "HMA021", "HMA062", "HMA106", "HMA107", "HMA170", "HMA176", "HMA187", "HMA188", "HMA994",
                            "HMA995", "HMA996"]}

        # Send a GET request to the website
        r = requests.post(url, json=payload, headers=header, verify=certifi.where())

        loopText = f"Loops: {str(i)}. offset: {str(offset)}. Status Code: {str(r.status_code)}"
        append_to_file(loopText)
        # print("Loops: " + str(i) + " offset: " + str(offset) +". status code: " + str(r.status_code))
        # Check if the request was successful
        if r.status_code == 200:
            # Parse the HTML content
            responseData = r.json()
            dataList.extend(responseData["data"])
    afterAgeRangeLoopList = f"There are a total of {len(dataList)} records in this ageRange"
    append_to_file(afterAgeRangeLoopList)
    df = pd.DataFrame(dataList)
    outputFileName = f"output_shatin_{min}_{max}.csv"
    df.to_csv(outputFileName, index=False)