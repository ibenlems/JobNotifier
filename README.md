# JobNotifier
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
* requests
* email and smtplib libraries 
* pandas to process and store the data
* github actions to automate the script to run on shedule
	
