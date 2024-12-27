import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage you want to scrap
secondary_school_url = [
    {
        "district": "Sha Tin",
        "url": "https://www.myschool.hk/secondary-school/banding-heatmap.php?did=14"
    },
    {
        "district": "Yuen Long",
        "url": "https://www.myschool.hk/secondary-school/banding-heatmap.php?did=13"
    }
]

final_list = []
for district in secondary_school_url:
    district_name = district['district']
    district_url = district['url']
    response = requests.get(district_url, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the webpage with Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Replace 'your-class-name' with the actual class name you want to scrape
        band_class_name = ['band3', 'band3A', 'band2', 'band2A', 'band1', 'band1A']
        for banding in band_class_name:
            schools_by_banding = soup.find_all(class_=banding)
            for school in schools_by_banding:
                school_detail = {}
                # Initialize a dictionary to store titles and texts
                school_name = school.get('title')

                # Add to dictionary
                school_detail["school_name"] = school_name
                school_detail["banding"] = banding
                school_detail["district"] = district_name
                # Print the resulting dictionary
                print(school_detail)
                final_list.append(school_detail)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# create output file for transaction record
outputFileNamePrefix = "output2/school/"

if len(final_list) != 0:
    df = pd.DataFrame(final_list)
    outputFileName = outputFileNamePrefix + "secondary_school_list_banding.csv"
    df.to_csv(outputFileName, index=False)