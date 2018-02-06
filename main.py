#!/usr/bin/env python3
__version__ = "1.0.0"
__author__ = "Ersin Akyuz"
__email__ = "eakyuz@gmx.net"
__description__ = "Python Github REST API Browser"
import json
import jsonify
import requests
from flask import Flask, request, jsonify

GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_REPOS_URL = 'https://api.github.com/repos/'
GITLAB_API_URL = 'https://gitlab.com/api/v4'
GITLAB_API_REPOS_URL = 'https://gitlab.com/api/v4/projects'
BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'
BITBUCKET_REPOS_URL = 'https://api.bitbucket.org/2.0/repositories/'
API_TOKEN = 'd0f25ec096b7a2c5fa15008a9245270b7fcaf3f8'
MYHEADERS = {'Authorization': 'token %s' % API_TOKEN}

"""
I used my predefined GitHub Token in MYHEADERS for unlimited calls.
requests and flask library needed for run the code.


My Thoughts
1. Below control can be added for checking empty repos
    if repo_data['message'] != "This repository is empty.":
2. Bitbucket and Gitlab code needs to improve
3. 


"""
app = Flask(__name__)
@app.route("/index/<search_term>/<number_of_hits>/<page_number>/<sorting>", methods=['GET'])
def index(search_term, number_of_hits, page_number, sorting):
    """
    Access to Github API and retrieve the latest commits
    """
    if len(number_of_hits) < 0:
        number_of_hits = 24
    repodict = {}
    print(search_term)
    if len(search_term) > 0:
        url = GITHUB_API_URL + "/search/repositories?q=" + search_term + "&page=" + str(page_number) + "&per_page=" + str(number_of_hits) + "&sort=stars&order=desc"
        print(url)
        try:
            my_request = requests.get(url, headers=MYHEADERS)
            dataj = json.loads(my_request.text)
            for idx, items in enumerate(dataj['items']):
                repodict[idx] = {}
                repodict[idx]['name'] = items['name']
                repodict[idx]['owner'] = items['owner']['login']
                print(idx+1)
                print(repodict[idx]['name'])
                repo_url = GITHUB_API_REPOS_URL + items['owner']['login'] + "/" + items['name'] + "/contents/"
                print(repo_url)
                try:
                    repo_request = requests.get(repo_url, headers=MYHEADERS)
                    repo_data = json.loads(repo_request.text)
                    filez={}
                    for files_index, files in enumerate(repo_data):
                        if files['name']:
                            filez[files_index]=(files['name'])
                    repodict[idx]['files']=filez
                except:
                    return "Error getting files info"
        except:
            return "Error accessing Github API"
    else:
        return "Missing search_term<br/> " \
               "Usage: <a href='http://localhost:9876/navigator?search_term=arrow'>http://localhost:9876/navigator?search_term=arrow</a>"
    js = json.dumps(repodict)
    return jsonify(repodict)
if __name__ == "__main__":
    app.run(port=80)
