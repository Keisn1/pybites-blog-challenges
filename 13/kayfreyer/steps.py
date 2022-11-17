import csv
from operator import itemgetter
from collections import OrderedDict, Counter, defaultdict, namedtuple
from itertools import groupby


def check_empty_string(movie, keys):
    for key in keys:
        if not len(movie[key]):
            return False
    return True


with open("../movie_metadata.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    movies = []
    filter_keys = ["director_name", "movie_title", "title_year", "imdb_score"]
    for row in reader:
        movie = {key: value for key, value in row.items() if key in filter_keys}
        if check_empty_string(movie, filter_keys):
            movies.append(movie)


directors = [movie["director_name"] for movie in movies]
counter = Counter(directors)

movies_min_four = [movie for movie in movies if counter[movie["director_name"]] >= 4]
min_year = datetime(year=1960, month=1, day=1)
final_movies = [
    movie
    for movie in movies_min_four
    if datetime.strptime(movie["title_year"], "%Y") >= min_year
    and movie["director_name"] != ""
]


final_movies = sorted(
    final_movies, key=lambda item: item["director_name"]
)  # because changes each time a new value is encountered


directors = defaultdict(list)
for director, value in groupby(final_movies, key_func):
    directors[director] = sorted(
        list(value), key=itemgetter("imdb_score"), reverse=True
    )


def average_score(movies):
    sum_ = 0
    for movie in movies:
        sum_ += float(movie["imdb_score"])
    return round(sum_ / len(movies), 1)


director = namedtuple("Director", "Movies")
ds = sorted(
    directors.items(), key=lambda element: average_score(element[1]), reverse=True
)
