import requests
from pprint import pprint
import base64
from github import Github
from pprint import pprint
import pygal 
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# github username
#username = "alantrivandrum"
# url to request
#url = f"https://api.github.com/users/{username}"
# make the request and return the json
#
# pretty print JSON data
#pprint(user_data)
# 


username = input("Please input a valid GitHub username here: ")




#token = "80fd7422d2994e5262b2d93b435121616a8de47d"
repos = {} 
languages = {}

f = open("authorisation.txt", "r") 
c_id = f.readline(1)
c_secret = f.readline(2)
# pygithub object
g = Github(client_id=c_id, client_secret=c_secret)  
# get that user by username
user = g.get_user(username)
#print(user.get_repos)



def print_repo(repo):
    # repository full name
    print("Full name:", repo.full_name)
    # repository description
    #print("Description:", repo.description)
    # the date of when the repo was created
    print("Date created:", repo.created_at)
    print("")
    # the date of the last git push
    #print("Date of last push:", repo.pushed_at)
    # home website (if available)
    #print("Home Page:", repo.homepage)
    # programming language
    print("Language:", repo.language)
    # number of forks
    #print("Number of forks:", repo.forks)
    # number of stars
    print("Number of stars:", repo.stargazers_count)
    #print("-"*50)
    # repository content (files & directories)
    #print("Contents:")
    #for content in repo.get_contents(""):
    #    print(content)
    #try:
        # repo license
    #    print("License:", base64.b64decode(repo.get_license().content.encode()).decode())
    #except:
    #    pass

def printRepoCommits(repo):
    try:
        if repo.get_commits() is not None:
            commits = repo.get_commits().totalCount
            print(f"Number of commits: {commits}")
    except:
        print("Number of commits: 0")

def addRepoToDict(repo):
    try:
        if repo.get_commits() is not None:
            commits = repo.get_commits().totalCount
            repos[f"{repo.name}"] = commits
    except:
        repos[f"{repo.name}"] = 0

def addRepoLanguages(repo):
    if repo is not None:
        language = repo.language
        if language is None:
            language = "No Language"
        if language in languages:
            languages[language] = languages[language] + 1
        else:
            languages[language] = 1
    
       

    


count = 0
for repo in user.get_repos():
    addRepoToDict(repo)
    addRepoLanguages(repo)

#print(repos)
#print(languages)
names = []
commits = []
languageNames = []
languageCount = []
for value in repos:
    names.append(value)
    commits.append(repos[value])

for language in languages:
    languageNames.append(language)
    languageCount.append(languages[language])

#print(names)
#print(commits)

#Make Visualisation
my_style = LS("#39FF14", base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
my_config.height = 500



if __name__ == '__main__':
    chart = pygal.Bar(my_config,style = my_style)
    chart.title = f"{user.login}'s Github repositories and their corresponding commits"
    chart.x_labels = names
    chart.add("", commits)
    chart.render_in_browser()
    chart.render_to_file("barchart.html")


    #chart2 = pygal.CHARTS(my_config,style = my_style)
    #chart2.title = f"{user.login}'s Github repositorys and their corresponding commits"
    #chart2.x_labels = names
    #chart2.add("", commits)
    #chart.render_to_file("repos.svg")
    chart2 = pygal.Pie()
    chart2.title = f"Number of repositories owned by {user.login} using different languages"
    count = 0
    for language in languages:
        chart2.add(language, languages[language])
        count = count + 1
    chart2.width = 1500
    chart2.render_in_browser()
    chart2.render_to_file("piechart.html")

