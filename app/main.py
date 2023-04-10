#!usr/bin/python3
from flask import Flask, render_template, request

from utils import validate_request, extract_user_org_and_repository

import github_api_issue

app = Flask(__name__) # Creating Flask Application Instance


@app.route('/')
@app.route('/index', methods=['GET', 'POST']) # App Route Decorator
def submit():
    """Method to be executed when above route/endpoint are hit

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':

        # Validate git url
        repository_url, valid_git_url = validate_request(request)
        if valid_git_url:
            user_or_org, repository = extract_user_org_and_repository(repository_url)
            class_object = github_api_issue.GithubApi(user_or_org, repository) # Calling the GitHub API class by providing the required arguments
            (total_issue_count, total_issue_last_one_day, total_issue_last_week, total_issue_before_last_week) = class_object.results_issue_stats()

            # Sending the above info to the Template
            return render_template('result.html',
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
