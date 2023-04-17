#!usr/bin/python3
"""Class to communicate with GitHub API V3"""

# Imported Libraries
import requests
from datetime import date
import datetime

from utils import ApplicationMessages, Constants


class GithubApi(object):
    """Github Api Class definition

    Args:
        object (_type_): _description_
    """

    def __init__(self, user_or_org, repository):
        """Method for Class Instantiation - Creates Class object

        Args:
            user_or_org (string): user or organization name
            repository (string): repository name
        """
        self.user_or_org = user_or_org
        self.repository = repository
        self.headers = {'User-Agent': 'request'}
        self.api_url = Constants.GIT_API_URL.value
        self.repo = "repo:" + str(user_or_org) + "/" +\
            str(repository) + "+" + "type:issue" + "+" + "state:open"
        # Calculating date of present day 
        self.date_today = date.today() 
        # Calculating date of previous day
        self.date_last_day = self.date_today - datetime.timedelta(days=1)
        # Calculating date of a day week ago 
        self.date_week_ago = self.date_today - datetime.timedelta(days=7)

    def total_issue_count(self):
        """Method for Returning Total Open Issue posted in Repository

        Returns:
            _type_: _description_
        """
        request_url = self.api_url + self.repo
        try:
            # Calling to GitHub API
            response = requests.get(request_url, headers=self.headers)
        except Exception as ex:
            return ex
        # Processing only if Response Status Code is 200-Ok
        if response.status_code == 200:
            response_json = response.json()
            return response_json["total_count"]
        else:
            return ApplicationMessages.SOMETHING_WENT_WRONG.value

    def total_issue_last_one_day(self):
        """Method for Returning Total Open Issue posted in Last 24 hours

        Returns:
            _type_: _description_
        """
        request_url = self.api_url + self.repo + "+created:>" + str(self.date_last_day)
        try:
            # Calling to GitHub API
            response = requests.get(request_url, headers=self.headers)
        except Exception as ex:
            return ex
        # Processing only if Response Status Code is 200-Ok
        if response.status_code == 200:
            response_json = response.json()
            return response_json["total_count"]
        else:
            return ApplicationMessages.SOMETHING_WENT_WRONG.value

    def total_issue_last_week(self):
        """Method for Returning Total Open Issue posted before Last 24 hours and not older than 7 days

        Returns:
            _type_: _description_
        """
        request_url = self.api_url + self.repo + "+created:" + str(self.date_week_ago) + ".." + str(self.date_last_day)
        try:
            # Calling to GitHub API
            response = requests.get(request_url, headers=self.headers) 
        except Exception as ex:
            return ex
        # Processing only if Response Status Code is 200-Ok
        if response.status_code == 200: 
            response_json = response.json()
            return response_json["total_count"]
        else:
            return ApplicationMessages.SOMETHING_WENT_WRONG.value

    def total_issue_before_last_week(self):
        """Method for returning Total Open Issue posted before 7 days

        Returns:
            _type_: _description_
        """
        request_url = self.api_url + self.repo + "+created:<" + str(self.date_week_ago)
        try:
            # Calling to GitHub API
            response = requests.get(request_url, headers=self.headers)
        except Exception as ex:
            return ex
        # Processing only if Response Status Code is 200-Ok
        if response.status_code == 200:
            response_json = response.json()
            return response_json["total_count"]
        else:
            return ApplicationMessages.SOMETHING_WENT_WRONG.value

    def results_issue_stats(self):
        """Method for returning all data to Route

        Returns:
            _type_: _description_
        """
        return self.total_issue_count(),\
            self.total_issue_last_one_day(),\
            self.total_issue_last_week(),\
            self.total_issue_before_last_week()
