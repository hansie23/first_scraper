from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import pandas as pd

# url = 'https://uk.indeed.com/jobs?q=Graduate&start=00'

job_title = []
companies = []
location = []
salary = []

pages = pd.Series(range(0,760,10))

for a in pages:
    url = f'https://uk.indeed.com/jobs?q=Graduate&start={a}'
    s = HTMLSession()
    r = s.get(url)
    soup = bs(r.text, 'html.parser')
    
    containers = soup.find_all('div',{'class':'job_seen_beacon'})
    
    for container in containers:
        job = container.find('h2', {'class':'jobTitle'}).text
        company = container.find('span', {'class':'companyName'}).text
        loc = container.find('div', {'class':'companyLocation'}).text
        
        job_title.append(job)
        companies.append(company)
        location.append(loc)
            
        try:
            sal = container.find('div', {'class':'salary-snippet'}).text
            salary.append(sal)
        except AttributeError:
            salary.append('N/A')

data_dict = {
    'Job_titles':job_title,
    'Companies':companies,
    'Location':location,
    'Salary':salary
    }

df = pd.DataFrame(data_dict)

df.to_csv('indeed_jobs.csv', index=False, header=True)  # exported to .csv file