from django.shortcuts import render
import requests
from datetime import datetime, timedelta


def index(request):
    ten_days_ago = datetime.now() - timedelta(days=10) # get 10 days ago 
    ten_days_ago = ten_days_ago.strftime('%Y-%m-%d') # convert to YYYY-MM-DD

    # get the data from the API 
    repos = requests.get(f"https://api.github.com/search/repositories?q=created:>{ten_days_ago}&sort=stars&order=desc&per_page=3").json()
    

    # get languages for each repo
    for repo in repos['items']:
        languages = repo['languages_url']
        repo['languages_url'] = requests.get(languages).json()

        languages_dic = {}
        for lang in repo['languages_url']:
            # get count of repos using each language
            res = requests.get(f"https://api.github.com/search/repositories?q=language:{lang}&page=1&per_page=1").json()
            
            # print(lang, res['total_count'])  
            languages_dic[lang] = res['total_count']
        
        repo['languages_url'] = languages_dic
            

    return render(request, 'app/index.html', {
        'repos': repos['items'],
    })
