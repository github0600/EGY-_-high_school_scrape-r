
from bs4 import BeautifulSoup
import requests


import concurrent.futures
from requests.exceptions import RequestException
import pandas as pd
import csv



'''
input: takes the scraped data table that have students data
output: DataFrame with all scraped data
'''
def scrape_data(table):
    global df
    info = table[2].find_all("td") + table[3].find_all("td")
    h = 0
    data= dict.fromkeys(headers)
    for i in range(len(info)):
        if i % 2 == 1:
            #student info 
            if i <= 17: 
                data[headers[h]]= info[i].text.strip()
                h+=1
            #grades info
            else:
                data[headers[h]]= info[i].text.strip()
                h+=1
    df = df.append(data, ignore_index=True)
    return df



'''
input: takes a lis of seat numbers
output: return a table if the seat number valid 

'''
def request_data(seat_n):
    result = requests.get('https://shbabbek.com/natega/{}'.format(seat_n), timeout=10)
    if result.status_code != 200:
        print('request error')
        return 
    soup = BeautifulSoup(result.content,"lxml")
    table = soup.find_all("div",{"class":"col-lg-6 col-md-12"})
    result = None
    if table:
        result = scrape_data(table)
        print(seat_n)
    return result




#translated headers
headers = ["seat_no","name","school","directorate","division","total_score","percentage","type","status","arabic","1st_language","2nd_language","pure_math","history","geography","philosophy","psychology","chemistry","biology","geology","applied_math","physics","total","religion","citizenship","economics_statistics"]
df = pd.DataFrame(columns=headers)

# takes seat number range
x, y = input("Enter range values x-y: ").split('-')
seat_n = range(int(x),int(y))

# its speed 10 requests per 1.8 sec
MAX_THREADS = 10
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    executor.map(request_data, seat_n)


df.to_csv('grades.csv', encoding='utf-8-sig')
