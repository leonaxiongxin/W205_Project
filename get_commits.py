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
                commits = g.get_user('apache').get_repo(repo_name).get_commits()
                for commit in commits:
                    try:
                        additions = commit.stats.additions
                        deletions = commit.stats.deletions
                        total_lines_changed = additions + deletions
                        f2.write(('None' if commit.author is None else commit.author.login) + ',' +
                                 str(additions) + ',' +
                                 str(deletions) + ',' +
                                 str(total_lines_changed) + ',' +
                                 ('0' if commit.author is None else commit.commit.author.date.isoformat()) + '\n')
                    except Exception as e:
                        print("Exception, likely API rate limit")
                        if 403 == e.status:
                            print('Warning: ' + str(e.data))
                            print('Waiting 1 hour')
                            for i in range(1, 61):
                                sleep(60)
                                print(60-i, ' minutes remaining')
                            additions = commit.stats.additions
                            deletions = commit.stats.deletions
                            total_lines_changed = additions + deletions
                            f2.write(('None' if commit.author is None else commit.author.login) + ',' +
                                     str(additions) + ',' +
                                     str(deletions) + ',' +
                                     str(total_lines_changed) + ',' +
                                     ('0' if commit.author is None else commit.commit.author.date.isoformat()) + '\n')
                        else:
                            raise e
