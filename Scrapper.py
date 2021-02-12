#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 22:45:07 2021

@author: ismail
"""

import requests
import pprint
from bs4 import BeautifulSoup
import pandas as pd 
#import matplotlib.pyplot as plt 
#import numpy as np 

# def scrab_jobs(job_title,location=None):
#     """scrab jobs in the desired location
#     param: job_title : string the job title 
#     location : string the location where to search"""

#     if location:
#         URL= 'https://www.monster.com/jobs/search/?q=+'+job_title+'&where='+location
#     else :
#         URL= 'https://www.monster.com/jobs/search/?q=+'+job_title+'&where=France'

        
pp = pprint.PrettyPrinter(indent=4)

URL = 'https://fr.indeed.com/jobs?q=data+scientist+junior&fromage=1'
page = requests.get(URL)

#pp.pprint(page.content)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='resultsCol')
#pp.pprint(results)

job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')

#for job in job_elems:

    #print(job,end='\n'*2)
   

title_elems=[]
company_elems=[]
location_elems=[]
summary_elems=[]
links=[]
   
for job_elem in job_elems:
    
    # Each job_elem is a new BeautifulSoup object.
    
    title_elem = job_elem.find('h2', class_='title')
    
    company_elem = job_elem.find('span', class_='company')
    
    location_elem = job_elem.find('span', class_='location')
    
    summary_elem = job_elem.find('div',class_='summary')
    
    link = job_elem.find("a")["href"]
    link="https://fr.indeed.com"+link
        
    
    if None in (title_elem, company_elem, location_elem):
        continue

    # print(title_elem.text.strip())
    # print(company_elem.text.strip())
    
    # print(location_elem.text.strip())
    # print(summary_elem.text.strip())
    # #print(link.text.strip())
    # print(f"Apply here: {link}\n")
    
    
    
    #print()
    
    title_elems.append(title_elem.text.strip())
    
    company_elems.append(company_elem.text.strip())
    
    location_elems.append(location_elem.text.strip())
    
    summary_elems.append(summary_elem.text.strip())
    
    links.append(link)
    
jobs=pd.DataFrame(
    { 'title': title_elems,
      'company': company_elems,
      'location': location_elems,
      'link to apply': links
     }
    )

#some basic data cleaning before sending the file 
jobs['title']=jobs["title"].apply(lambda x: x.replace('\nnouveau',''))

#transform data to excel file 
jobs_xls=jobs.to_excel("jobs.xlsx")


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email
import smtplib

# create message object instance
msg = MIMEMultipart()
password = "job123456a"
msg['From'] = "jobnotifier49@gmail.com"
msg['To'] = "ismailbenlemsieh@gmail.com"
msg['Subject'] = "Today scrapped job offers"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Login Credentials for sending the mail
try:
    server.login(msg['From'], password)
except Exception as e:
    print("Connection Error: {}".format(e))

#attach file to email
Applyfilename = "jobs.xlsx"
attachment = open("jobs.xlsx","rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
email.encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename=%s" % "jobs.xlsx")

msg.attach(part)
text = msg.as_string()
server.sendmail(msg['From'], msg['To'], text)