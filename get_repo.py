from github import Github

user = input("Username: ")
password = input("Password: ")

g = Github(user, password, per_page=100)

# for repo in g.get_user('apache').get_repos():
#     print(repo.name)

owner = 'apache'
repo_list = []
repos = g.get_user(owner).get_repos()

with open('repo_list.txt', 'w') as f:
    f.write('Name,Stars,Language,Created \n')
    for repo in repos:
        f.write(repo.name + ',' +
                str('0' if repo.stargazers_count is None else repo.stargazers_count) + ',' +
                str('None' if repo.language is None else repo.language) + ',' +
                repo.created_at.isoformat() +
                '\n')
