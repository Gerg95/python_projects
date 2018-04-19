import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus, quote
from urllib.error import HTTPError, URLError
from random import randint
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import ssl
import tablib

import time
from datetime import datetime
import re
import os

import sys, traceback


def call_url(url):
  response = requests.get(url)
  return response

def get_soup(url):
  response = call_url(url)
  soup = BeautifulSoup(response.content, 'lxml')
  return soup

def get_job(url):
  soup = get_soup(url)
  # EX :


  company = soup.find('span' ,{'itemprop' : 'name'}).text.strip()

  title = soup.find('h1').text.strip()

  location = soup.find('div', {'class' : 'location col-xs-12 col-sm-6 col-md-6 col-lg-6'})
  location = location.text.strip()

  salary = soup.find('div', {'class' : 'salary col-xs-12 col-sm-6 col-md-6 col-lg-6'})
  salary = salary.text.strip()

  employment_type = soup.find('div', {'class' : 'time col-xs-12 col-sm-6 col-md-6 col-lg-6'})
  employment_type = employment_type.text.strip()

  desc = soup.find('div', {'class' : 'description'}) 
  desc = desc.text.strip()

  job = {
  "company" : company,
  "title" : title,
  "location" : location,
  "salary" : salary,
  "employment_type" : employment_type,
  "job_description" : desc,
  }

 

  return job

def export_data(jobs):
  jobs = []
  jobs.append(job)
  data = tablib.Dataset()
  data.json = json.dumps(jobs)

  filename = 'reed_data.csv'

  csv_file = open(filename, 'w')

  csv_file.write(data.csv)

  return

def get_search(url):
  soup = get_soup(url)

  urls = soup.find_all('a', {'class': 'gtmJobTitleClickResponsive'})
  for url in urls:
    url = 'https://www.reed.co.uk'+url['href']
    get_job(url)

  return

def get_website(url):
  # loop to 1 ,,, 10 
  for x in range(1):
    print('#### Page: '+str(x))
    get_search(url + '&cached=True&pageno=' + str(x))
  return

def main(url):
  get_website(url)
  export_data(jobs)

  return

if __name__ == '__main__':
  #main('https://www.reed.co.uk/jobs/sales-representative/34848957?source=searchResults#/jobs/howdens-joinery-31154/p31154')
  # main(sys.argv[1])
  main('https://www.reed.co.uk/jobs/jobs-in-london?keywords=Sales')

