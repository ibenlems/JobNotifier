#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 22:45:07 2021

@author: ismail
"""

import smtplib
import email
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#prepare list where to store data 
title_elems=[]
company_elems=[]
location_elems=[]
summary_elems=[]
links=[]


def scrap_page(page_URL):

    page = requests.get(page_URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='resultsCol')

    job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')

    for job_elem in job_elems:

        # Each job_elem is a new BeautifulSoup object.

        title_elem = job_elem.find('h2', class_='title')

        company_elem = job_elem.find('span', class_='company')

        location_elem = job_elem.find('span', class_='location')

        summary_elem = job_elem.find('div', class_='summary')

        link = "https://fr.indeed.com"+job_elem.find("a")["href"]

        if None in (title_elem, company_elem, summary_elem, location_elem):
            continue

        title_elems.append(title_elem.text.strip())

        company_elems.append(company_elem.text.strip())

        location_elems.append(location_elem.text.strip())

        summary_elems.append(summary_elem.text.strip())

        links.append(link)


URL = 'https://fr.indeed.com/jobs?q=data+scientist+junior&fromage=1'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')


# prepare list where to store data
title_elems = []
company_elems = []
location_elems = []
summary_elems = []
links = []

# scrap data from the first page
scrap_page(URL)

# a try excpet bloc because first page could not include the pagination-list if there is only one page
try:
    # get the number of pages
    list_pages = soup.find('ul', class_='pagination-list')
    pages = list_pages.findAll('li')
    number_pages = len(list)-1

    # iterate to scrap other pages of the same website
    for num in range(1, number_pages-2):
        page_url = 'https://fr.indeed.com/jobs?q=data+scientist+junior&fromage=1&start='+str(num*10)
        scrap_page(page_url)

except:
    pass


# store data in a pandas dataframe
jobs = pd.DataFrame(
    {'title': title_elems,
     'company': company_elems,
     'location': location_elems,
     'link to apply': links
     }
)

# some basic data cleaning before sending the file
jobs['title'] = jobs["title"].apply(lambda x: x.replace('\nnouveau', ''))

# transform data to excel file
jobs_xls = jobs.to_excel("jobs.xlsx")


# create message object instance
msg = MIMEMultipart()

# use environment variables to hide password
password = str(os.environ.get('key'))
msg['From'] = "jobnotifier49@gmail.com"
msg['To'] = str(os.environ.get('send_to'))
msg['Subject'] = "Today scrapped job offers"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Login Credentials for sending the mail
try:
    server.login(msg['From'], password)
except Exception as e:
    print("Connection Error: {}".format(e))

# attach file to email
Applyfilename = "jobs.xlsx"
attachment = open("jobs.xlsx", "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
email.encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename=%s" % "jobs.xlsx")

# send the email
msg.attach(part)
text = msg.as_string()
server.sendmail(msg['From'], msg['To'], text)