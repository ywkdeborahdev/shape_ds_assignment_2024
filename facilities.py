import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage you want to scrap
secondary_school_url = [
    {
        "district": "Sha Tin",
        "url": "https://www.lcsd.gov.hk/clpss/en/webApp/PhoneAddress.do?cat=ALL&dist=ST&keyword=&pageNo=1&sortField=&sortOrder="
    },
    {
        "district": "Yuen Long",
        "url": "https://www.lcsd.gov.hk/clpss/en/webApp/PhoneAddress.do?cat=ALL&dist=YL&keyword=&pageNo=1&sortField=&sortOrder="
    }
]

final_list = []
for district in secondary_school_url:
    district_name = district['district']
    district_url = district['url']
    response = requests.get(district_url, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        print("Successfully fetched " + district_name)
        # Parse the content of the webpage with Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Replace 'your-class-name' with the actual class name you want to scrape
        class_name = 'table_head'
        facility_category_list = soup.find_all(class_=class_name)
        for category in facility_category_list:
            print(category)
            category_detail = {}
            # Initialize a dictionary to store titles and texts
            category_name = category.get('title')
            category_count = category.find('p')
            print(category_count)

            # Add to dictionary
            category_detail["category_name"] = category_name
            category_detail["category_count"] = category_count
            category_detail["district"] = district_name
            # Print the resulting dictionary
            final_list.append(category_detail)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# create output file for transaction record
outputFileNamePrefix = "output2/facility/"

if len(final_list) != 0:
    df = pd.DataFrame(final_list)
    outputFileName = outputFileNamePrefix + "facility.csv"
    df.to_csv(outputFileName, index=False)