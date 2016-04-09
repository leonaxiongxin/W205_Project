from github import Github

g = Github()

for repo in g.get_user('jameswinegar').get_repos():
    print(repo.name)