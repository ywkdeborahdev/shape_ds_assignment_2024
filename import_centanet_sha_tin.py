import requests
import certifi
import pandas as pd
import glob

# create log file for recording
file_name = 'Shatin.txt'
# create output file for transaction record
outputFileNamePrefix = "output2/shatin/"
# URL of the website to crawl
url = "https://hk.centanet.com/findproperty/api/Transaction/Search"
# other variables
size = 48
region = "NTE"

def generate_file_name(age_range):
    return f"{outputFileNamePrefix}{age_range}.csv"

# function for writing to log file
def append_to_file(text):
    with open(file_name, 'a') as file:
        file.write(text + "\n")  # Add a newline after each entry

def generate_payload(record_size, to_offset, age_range):
    payload = {"postType": "Both", "day": "Day1095", "sort": "InsOrRegDate", "order": "Descending", "size": record_size, "mtrs": [],
     "primarySchoolNets": [],
     "typeCodes": ["19-HMA187", "19-HMA001", "19-HMA170", "19-HMA062", "19-HMA176", "19-HMA021", "19-HMA106",
                   "19-HMA188", "19-HMA107", "19-HMA996", "19-HMA994", "19-HMA995"], "offset": to_offset,
     "pageSource": "search", "buildingAgeRange": {"min": age_range, "max": age_range}, "universities": [],
     "estateUsages": ["HOS", "PRH", "RE"]}
    return payload

# loop through each age range
for ageRange in range(57):
    # reset page offset
    offset = 0

    ageRangeText = f"This is to record age range of {ageRange}."
    append_to_file(ageRangeText)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    # first payload to obtain count number
    payload = generate_payload(size, offset, ageRange)
    # Get number of records from age range
    ageRangeResponse = requests.post(url, json=payload, headers=header, verify=certifi.where())
    ageRangeResponseData = ageRangeResponse.json()
    totalAgeRangeRecord = ageRangeResponseData["count"]
    noOfLoopsForAgeRange = int(totalAgeRangeRecord / size) + 1
    ageRangeRecordText = f"There are a total of {totalAgeRangeRecord}, number of loops are {noOfLoopsForAgeRange}."
    append_to_file(ageRangeRecordText)
    print(ageRangeRecordText)
    dataList = []
    for i in range(noOfLoopsForAgeRange):
        if i != 0:
            offset = size * i
        payload = generate_payload(size, offset, ageRange)

        # Send a GET request to the website
        r = requests.post(url, json=payload, headers=header, verify=certifi.where())

        # print("Loops: " + str(i) + " offset: " + str(offset) +". status code: " + str(r.status_code))
        # Check if the request was successful
        if r.status_code == 200:
            # Parse the HTML content
            responseData = r.json()
            dataList.extend(responseData["data"])
    afterAgeRangeLoopList = f"There are a total of {len(dataList)} records in ageRange: {ageRange}"
    append_to_file(afterAgeRangeLoopList)
    print(afterAgeRangeLoopList)
    if len(dataList) != 0:
        df = pd.DataFrame(dataList)
        filtered_df = df[
            ["districtName", "bigEstateName", "estateName", "buildingName", "yAxis", "transactionPrice", "postType",
             "nArea", "nUnitPrice", "regDate", "insDate", "dataSource", "firstOrSecondHand"]]
        filtered_df["buildingAgeRange"] = ageRange
        filtered_df["region"] = region
        outputFileName = generate_file_name(ageRange)
        filtered_df.to_csv(outputFileName, index=False)
print("first part done")

# Path to the directory containing your CSV files
path = f"{outputFileNamePrefix}*.csv"

# Use glob to get all the csv files in the directory
csv_files = glob.glob(path)

# Create a list to hold the DataFrames
dfs = []

# Loop through the list of files and read each one
for filename in csv_files:
    df = pd.read_csv(filename)
    dfs.append(df)

# Concatenate all DataFrames in the list
concatenated_df = pd.concat(dfs, ignore_index=True)  # ignore_index resets the index

print("Concatenated DataFrame:")
print(concatenated_df)

# Fill empty cells in 'bigEstateName' first with values from 'estateName', then from 'buildingName'
concatenated_df['bigEstateName'] = concatenated_df['bigEstateName'].fillna(concatenated_df['estateName']).fillna(
    concatenated_df['buildingName'])

output_file = f"{outputFileNamePrefix}concatenated_output.csv"

# Save the concatenated DataFrame to a CSV file
concatenated_df.to_csv(output_file, index=False)
print(f"Concatenated DataFrame saved to {output_file}")