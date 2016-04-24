from urllib.request import urlopen
import datetime
import requests
import json


def get_latest_commit(owner, repo):
    url = 'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1'.format(owner=owner, repo=repo)
    response = urlopen(url).read()
    data = json.loads(response.decode())
    return data[0]


def get_all_commits(owner, repo):
    url = 'https://api.github.com/repos/{owner}/{repo}/commits'.format(owner=owner, repo=repo)
    response = urlopen(url).read()
    data = json.loads(response.decode())
    return data[0]


def get_statistics(owner, repo):
    url = 'https://api.github.com/repos/{owner}/{repo}/stats/contributors'.format(owner=owner, repo=repo)
    response = urlopen(url).read()
    data = json.loads(response.decode())
    return data


def get_repos(owner):
    url = 'https://api.github.com/orgs/{owner}/repos'.format(owner=owner)
    response = urlopen(url).read()
    data = json.loads(response.decode())
    return data

if __name__ == '__main__':
    owner = 'apache'

    repos = get_repos(owner)

    for repo in repos:
        print(repo['name'])
        stats = get_statistics(owner, repo['name'])
        contributor_list = []
        for i in range(0, len(stats)):
            user = stats[i]['author']['login']
            commits = stats[i]['total']
            deletions = 0
            additions = 0
            first_commit = None
            last_commit = None
            for week in stats[i]['weeks']:
                deletions += week['d']
                additions += week['a']
                # assume that weeks are ordered
                if first_commit is None and week['c'] > 0:
                    first_commit = week['w']
                if week['c'] > 0:
                    last_commit = week['w']
            contributor_list.append([repo['name'],
                                     user,
                                     commits,
                                     additions,
                                     deletions,
                                     datetime.datetime.fromtimestamp(first_commit).strftime('%Y-%m-%d'),
                                     datetime.datetime.fromtimestamp(last_commit).strftime('%Y-%m-%d')
                                     ])

        for contributor in contributor_list:
            print(contributor)

