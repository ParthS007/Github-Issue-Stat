#!usr/bin/python3
from flask import Flask, render_template, flash, redirect, request

import re

import github_api_issue

app = Flask(__name__) # Creating Flask Application Instance


@app.route('/')
@app.route('/index', methods=['GET', 'POST']) # App Route Decorator
def submit(): # Method to be executed when above route/endpoint are hit
    if request.method == 'POST':
        repository_url = request.form["repositoryUrl"] # Getting repository_url from Submitted Form
        valid_git_url = re.match("https://github.com(/.*?)*", repository_url) # Validating the URL with help of regexp
        if valid_git_url:
            user_or_org = repository_url.rsplit('https://github.com/')[1].rsplit('/')[0] # Extracting the User/Org name from the URL
            repository = repository_url.rsplit('https://github.com/')[1].rsplit('/')[1] # Extracting the repository name from the URL
            class_object = github_api_issue.GithubApi(user_or_org, repository) # Calling the GitHub API class by prviding the required arguments
            total_issue_count = class_object.total_issue_count # Extracting the `total_issue_count` from the class object
            total_issue_last_one_day = class_object.total_issue_last_one_day # Extracting the `total_issue_last_one_day` from the class object
            total_issue_last_week = class_object.total_issue_last_week # Extracting the `total_issue_last_week` from the class object
            total_issue_before_last_week = class_object.total_issue_before_last_week # Extracting the `total_issue_before_last_week` from the class object

            return render_template('result.html', # Sending the above info to the Template
                                total_issue_count=total_issue_count,
                                total_issue_last_one_day=total_issue_last_one_day,
                                total_issue_last_week=total_issue_last_week,
                                total_issue_before_last_week=total_issue_before_last_week)
        else:
            error = 'Please try again! Not a Valid Github URL'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
