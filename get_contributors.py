from github import Github
import os
from time import sleep

user = input("Username: ")
password = input("Password: ")


g = Github(user, password, per_page=100)

with open('repo_list.txt', 'r') as f:
    repos = f.read()

repo_list = [s.strip() for s in repos.splitlines()]

folder = 'Repo_Contributors'
if not os.path.exists(os.path.join(os.getcwd(), folder)):
    os.makedirs(os.path.join(os.getcwd(), folder))
os.chdir(os.path.join(os.getcwd(), folder))


for repo in repo_list:
    repo_name = repo.split(',')[0]
    print(repo_name)
    if os.path.isfile(repo_name + '.txt'):
        pass
    else:
        with open(repo_name + '.txt', 'w+') as f2:
            if repo_name is None:
                pass
            else:
                try:
                    contributors = g.get_user('apache').get_repo(repo_name).get_contributors()
                    for contributor in contributors:
                        try:
                            f2.write(str(repo_name) + ',' +
                                     contributor.login + ',' +
                                     str('None' if contributor.email is None else contributor.email) +
                                     '\n')
                        except:
                            f2.write(str(repo_name) + ',' +
                                     contributor.login + ',' +
                                     'None' +
                                     '\n')
                except Exception as e:
                    if e.status == 403:
                        print('Warning: ' + str(e.data))
                        print('Waiting 1 hour')
                        for i in range(1, 61):
                            sleep(60)
                            print(60 - i, ' minutes remaining')
                        f2.write(str(repo_name) + ',' +
                                 contributor.login + ',' +
                                 str('None' if contributor.email is None else contributor.email) +
                                 '\n')
                    else:
                        print("New Error!")
