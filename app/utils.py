import re
from enum import Enum


class ApplicationMessages(Enum):
    """Add constant application message
    """
    
    SOMETHING_WENT_WRONG = "Something Wrong with the GitHub API!"
    INVALID_GIT_URL = "Please try again! Not a Valid Github URL"
    

class Constants(Enum):
    """Constant values

    Args:
        Enum (_type_): _description_
    """
    
    GIT_REGEX = "https://github.com(/.*?)*"
    GIT_URL = "https://github.com/"
    GIT_API_URL = "https://api.github.com/search/issues?q="
    

def validate_request(request):
    """Validate request and github url

    Args:
        request (_type_): _description_
    """
    
    # Getting repository_url from Submitted Form
    repository_url = request.form["repositoryUrl"]
    valid_git_url = re.match(Constants.GIT_REGEX.value, repository_url)
    return (repository_url, valid_git_url)
    

def extract_user_org_and_repository(repository_url):
    """Extract user/org and repository name from repository url

    Args:
        repository_url (string): Repository url
    """
    
    # Extracting the User/Org name from the URL
    user_or_org = repository_url.rsplit('https://github.com/')[1].rsplit('/')[0]
    # Extracting the repository name from the URL
    repository = repository_url.rsplit('https://github.com/')[1].rsplit('/')[1]

    return (user_or_org, repository)
