from github import Github
from time import sleep
import os

user = input("Username: ")
password = input("Password: ")

g = Github(user, password, per_page=100)

with open('repo_list.txt', 'r') as f:
    repos = f.read()

repo_list = [s.strip() for s in repos.splitlines()][1:]


folder = 'Repo_Commits'
if not os.path.exists(os.path.join(os.getcwd(), folder)):
    os.makedirs(os.path.join(os.getcwd(), folder))
os.chdir(os.path.join(os.getcwd(), folder))


for repo in repo_list:
    repo_name = repo.split(',')[0]
    if os.path.isfile(repo_name + '.txt'):
        pass
    else:
        with open(repo_name + '.txt', 'w+') as f2:
            print(repo_name)
            if repo_name is None:
                pass
            else:
                try:
                    commits = g.get_user('apache').get_repo(repo_name).get_commits()
                    for commit in commits:
                        try:
                            f2.write(repo_name + ',' +
                                     ('None' if commit.author is None else commit.author.login) + ',' +
                                     ('0' if commit.author is None else commit.commit.author.date.isoformat()) +
                                     '\n')
                        except Exception as e:
                            print(e)
                            if 'NoneType' not in str(e):
                                if 403 == e.status:
                                    print('Warning: ' + str(e.data))
                                    print('Waiting 1 hour')
                                    for i in range(1, 61):
                                        sleep(60)
                                        print(60-i, ' minutes remaining')
                                    f2.write(repo_name + ',' +
                                             ('None' if commit.author is None else commit.author.login) + ',' +
                                             ('0' if commit.author is None else commit.commit.author.date.isoformat()) +
                                             '\n')
                            else:
                                print("NoneType issue failed try/except prior")
                                pass
                except Exception as e:
                    if e.status == 409:
                        print("Skipping empty repository")
                    elif e.status == 403:
                        print('Warning: ' + str(e.data))
                        print('Waiting 1 hour')
                        for i in range(1, 61):
                            sleep(60)
                            print(60 - i, ' minutes remaining')
                        f2.write(repo_name + ',' +
                                 ('None' if commit.author is None else commit.author.login) + ',' +
                                 ('0' if commit.author is None else commit.commit.author.date.isoformat()) +
                                 '\n')
                    else:
                        print("No Idea")
                        print(e)
