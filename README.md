# JobNotifier
![Automated jobs web scrapping](https://github.com/ibenlems/JobNotifier/blob/main/1_4oYQrqyrLmLhPtPvFw7PKg.jpeg)

Ever felt too busy to go trough job search platforms everyday to find the right opportunity? It was my case when I had to find an internship while having so many exams and work to do,  I came up with a simple and very practical solution:  A web scrapper application that sends data daily to your email using github actions.   
 
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)

## General info
This project is a simple web scrapper that gets job offers data frow the web (for now it only scraps Indeed but could easily be generated to any other website that could be scrapped), and send results as an excel file to your email every day, using github actions. 
	
## Technologies
Project is created with:
* Python version 3.6
* beautifulsoup4
A python librarie to extract data from html and xml files. 
* requests
A python HTTP librarie that makes http requests to the web easier 
* email and smtplib 
libraries to send an email from python script
* pandas
 To process and store the data
* github actions 
To automate the script to run on schedule (every day around 8 pm)
	
