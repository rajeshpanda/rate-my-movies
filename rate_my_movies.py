import os
import re
import string
import urllib.request
import json
import csv
import sys

class Movie:
    def __init__(self, name, year):
        self.name = name
        self.year = year

class MovieResponse:
    def __init__(self, name, original_title, vote_average, vote_count, release_date):
        self.name = name
        self.original_title = original_title
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.release_date = release_date

def formatMovieRequest(movieName):
    try:
        year = re.findall('(\d{4})',movieName)[0]
        if year.isdigit():
            movieName = movieName.split(year)[0]
            chars = re.escape(string.punctuation)
            name = re.sub(r'['+chars+']', ' ',movieName)
            arr = name.split('com')
            if(len(arr) > 1):
                name = arr[1]
            else:
                name = arr[0]
            return Movie(name.strip(),year)
        return None;
    except:
        pass

def main():
    path = ""
    if(len(sys.argv[1:]) !=  1):
        raise Exception('Just the path to the folder containing movies!')  
    for arg in sys.argv[1:]:
        path = arg
    list_movies = []
    outputList = []
    print("Searching files at " + path)
    for index, file in  enumerate(os.listdir(path)):
        list_movies.append(file)
        movie = formatMovieRequest(list_movies[index])
        if(movie != None):
            print("Getting "+ movie.name+ "...")
            response = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key=3fab9acf7fe989b92072a0753182bd09&language=en-US&query="+ movie.name.replace(' ', '+') +"&page=1&include_adult=false&year="+ movie.year).read().decode('utf-8')
            json_obj = json.loads(response)
            if(len(json_obj['results']) > 0):
                movieResp = json_obj['results'][0]
                outputList.append(MovieResponse(movie.name,movieResp['original_title'],movieResp['vote_average'],movieResp['vote_count'],movieResp['release_date']))
            else:
                response = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key=3fab9acf7fe989b92072a0753182bd09&language=en-US&query="+ movie.name.replace(' ', '+') +"&page=1&include_adult=false").read().decode('utf-8')
                json_obj = json.loads(response)
                if(len(json_obj['results']) > 0):
                    movieResp = json_obj['results'][0]
                    outputList.append(MovieResponse(movie.name,movieResp['original_title'],movieResp['vote_average'],movieResp['vote_count'],movieResp['release_date']))
    wtr = csv.writer(open ('Output\MovieRatings.csv', 'w'), lineterminator='\n')
    name_header = "Name";
    vote_average_header = "Vote Average"
    vote_count_header = "Vote Count"
    release_date_header = "Release Date"
    print("\n\nWriting output...")
    wtr.writerow ([name_header,vote_average_header, vote_count_header, release_date_header])
    for x in outputList : wtr.writerow ([x.name,x.vote_average,x.vote_count,x.release_date])
    print("\nComplete --> Output\MovieRatings.csv")            
      
if __name__ == "__main__": main()
