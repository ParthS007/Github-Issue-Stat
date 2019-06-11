#!usr/bin/python3
"""Class to communicate with GitHub API V3"""

# Imported Libraries
import requests
from datetime import date
import datetime


class GithubApi(object): # Github Api Class definition

    def __init__(self, user_or_org, repository): # Method for Class Instantiation - Creates Class object
        self.user_or_org = user_or_org
        self.repository = repository
        self.headers = {'User-Agent': 'request'}
        self.api_url = "https://api.github.com/search/issues?q="
        self.repo = "repo:" + str(user_or_org) + "/" +\
            str(repository) + "+" + "type:issue" + "+" + "state:open"
        self.date_today = date.today() # Calculating date of present day 
        self.date_last_day = self.date_today - datetime.timedelta(days=1) # Calculating date of previous day
        self.date_week_ago = self.date_today - datetime.timedelta(days=7) # Calculating date of a day week ago
        self.total_issue_count = self.total_issue_count() # Calling `total_issue_count`
        self.total_issue_last_one_day = self.total_issue_last_one_day() # Calling `total_issue_last_one_day`
        self.total_issue_last_week = self.total_issue_last_week() # Calling `total_issue_last_week`
        self.total_issue_before_last_week = self.total_issue_before_last_week() # Calling `total_issue_before_last_week`
        self.results_issue_stats() # Calling `results_issue_stats` which will return the data to route which will further send it to Template 

    def total_issue_count(self): # Method for Returning Total Issue posted in Repository
        request_url = self.api_url + self.repo
        try:
            response = requests.get(request_url, headers=self.headers) # Calling to GitHub API
        except Exception as e:
            return e
        if response.status_code == 200: # Proceesing only if Response Status Code is 200-Ok
            response_json = response.json()
            return response_json["total_count"]
        else:
            return "Something Wrong with the GitHub API!"

    def total_issue_last_one_day(self): # Method for Returning Total Issue posted in Last 24 hours
        request_url = self.api_url + self.repo + "+created:>" + str(self.date_last_day)
        try:
            response = requests.get(request_url, headers=self.headers) # Calling to GitHub API
        except Exception as e:
            return e
        if response.status_code == 200: # Proceesing only if Response Status Code is 200-Ok
            response_json = response.json()
            return response_json["total_count"]
        else:
            return "Something Wrong with the GitHub API!"

    def total_issue_last_week(self): # Method for Returning Total Issue posted before Last 24 hours and not older than 7 days
        request_url = self.api_url + self.repo + "+created:" + str(self.date_week_ago) + ".." + str(self.date_last_day)
        try:
            response = requests.get(request_url, headers=self.headers) # Calling to GitHub API
        except Exception as e:
            return e
        if response.status_code == 200: # Proceesing only if Response Status Code is 200-Ok
            response_json = response.json()
            return response_json["total_count"]
        else:
            return "Something Wrong with the GitHub API!"

    def total_issue_before_last_week(self): # Method for returning Total Issue posted before 7 days
        request_url = self.api_url + self.repo + "+created:<" + str(self.date_week_ago)
        try:
            response = requests.get(request_url, headers=self.headers) # Calling to GitHub API
        except Exception as e:
            return e
        if response.status_code == 200: # Proceesing only if Response Status Code is 200-Ok
            response_json = response.json()
            return response_json["total_count"]
        else:
            return "Something Wrong with the GitHub API!"

    def results_issue_stats(self): # Method for returning all data to Route
        return self.total_issue_count,\
            self.total_issue_last_one_day,\
            self.total_issue_last_week,\
            self.total_issue_before_last_week
