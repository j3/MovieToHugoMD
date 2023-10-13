from bs4 import BeautifulSoup
from mechanize import Browser
import re, json
import math
from datetime import datetime
import requests

def main():
        movie = str(input('Movie Name: '))
        movie_search = '+'.join(movie.split())
        
        base_url = 'http://www.imdb.com/find?q='
        url = base_url+movie_search+'&s=all'
        
        title_search = re.compile('/title/tt\d+')
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open(url)

        link = br.find_link(url_regex = re.compile(r'/title/tt.*'))
        res = br.follow_link(link)
        
        soup = BeautifulSoup(res.read(), features="lxml")
        
        jsonFile = json.loads(soup.find('script', type='application/ld+json').text.replace("'", '"').replace("&apos;", "'"))
                
        movie_title = jsonFile["name"]
        cover = jsonFile["image"]
        
        actors=[]
        for person in jsonFile["actor"]:
            actors.append(person["name"])
        
        des = jsonFile["description"]

        genre = jsonFile["genre"]
        
        release_date = jsonFile["datePublished"]

        print ('\nDescription:')
        print (des)

        ecrire_film(movie_title, release_date, ', '.join(genre), ', '.join(actors), des, cover)


def ecrire_film(title, release_date, genres, actors, synopsis, cover):
    notes = ""

    txt = input("Do you want to add a note ? (y or n)")
    
    if txt == "y" or txt == "Y":
        notes = input("Write any notes you have about the movie here: ")

    rating = ""
    frac = 0

    rate = float(input("Please enter the rating you would like to assign to the movie here: "))
    frac, whole = math.modf(rate)
    
    for i in range(int(whole)):
        rating = rating+("★")
    if frac != 0:
        rating = rating + "½"
    
    title_clean = ''.join(e for e in title if e.isalnum())

    print('../content/en/movies/'+title_clean+release_date+'.md')
    file1 = open(r'../content/en/movies/'+title_clean+release_date+'.md', "w+", encoding='utf-8')


    myfile = requests.get(cover)
    open('../static/img/movies/'+title_clean+release_date+'.jpg', 'wb').write(myfile.content)


    if notes == "":
        file1.writelines(["---\n",
        'title: "'+ title +'"\n',
        'date: "'+ datetime.today().strftime('%Y-%m-%dT%H:%M:%S') +'+01:00"\n'
        "draft: false\n",
        "author: Leet\n",
        'tags: ["review"]\n',
        'categories: ["English"]\n',
        'layout: "moviesview"\n',
        'myrating: "'+ rating +'"\n',
        'synopsis: "'+ synopsis +'"\n',
        'year: "'+ release_date +'"\n',
        'genre: "'+ genres +'"\n',
        'poster: "/img/movies/'+title_clean+release_date+'.jpg"\n',
        'posterTiny: "/img/movies/'+title_clean+release_date+'.jpg-230x330.jpg"\n',
        'actors: "' + actors +'"\n',
        '---'])
    else:
        file1.writelines(["---\n",
        'title: "'+ title +'"\n',
        'date: "'+ datetime.today().strftime('%Y-%m-%dT%H:%M:%S') +'+01:00"\n'
        "draft: false\n",
        "author: Leet\n",
        'tags: ["review"]\n',
        'categories: ["English"]\n',
        'layout: "moviesview"\n',
        'myrating: "'+ rating +'"\n',
        'synopsis: "'+ synopsis +'"\n',
        'year: "'+ release_date +'"\n',
        'genre: "'+ genres +'"\n',
        'poster: "/img/movies/'+title_clean+release_date+'.jpg"\n',
        'posterTiny: "/img/movies/'+title_clean+release_date+'.jpg-230x330.jpg"\n',
        'actors: "' + actors +'"\n',
        'notes: "' + notes +'"\n',
        '---'])

    file1.close()
    
if __name__ == '__main__':
    '''
    How to change where the files are saved ?

    For the .md :
        - [L.72] : Replace /content/en/movies/
    For the .jpg :
        - [L.76] : Replace /static/img/movies/
    '''
    main()
