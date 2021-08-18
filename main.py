import requests
from bs4 import BeautifulSoup
import pandas as pd

#extract data from website
def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=python%20developer&l=Brooklyn%2C%20NY&start={page}&vjk=55336e6a8815f65f'
    res = requests.get(url,headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    #return data into html form
    return soup

#transform data - passed in html form data
def transform(soup):
    # divs = soup.find_all('div', class_='job_seen_beacon')
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('h2', class_='jobTitle').text.strip()
        company = item.find('span', class_='companyName').text.strip()
        location = item.find('div', class_='companyLocation').text.strip()

        try:
            salary = item.find('span', 'salary-snippet').text.strip().replace('\n', ' ')
        except:
            salary = ''
        summary = item.find('div', class_='job-snippet').text.strip()

        #create the dictionary
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return

# create a blank list to append each job
joblist = []

#go through the pages now
for i in range(0,100,10):
    print(f'Getting page, {i}')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('indeed.csv')

