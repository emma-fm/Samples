from requests_html import HTMLSession
import numpy.core._dtype_ctypes #this import is necessary only because of a current bug in pyinstaller
import matplotlib.pyplot as plt

# URL format: https://www.imdb.com/title/tt0235918/
series = input("Type the series ID, or full url to main page: ")
if "http" not in series:
    series = "https://www.imdb.com/title/" + series
#Remove reference
if "?" in series:
    series = series.split("?")[0]
if not series.endswith("/"):
    series = series + "/"

session = HTMLSession()
numberOfSeasons = 0
seriesName = ""
seasonMarkers = []
web = session.get(series)
episodeRating = []

# Gets the series name. If no originalTItle, get it from page title
try:
    seriesName = web.html.find('.originalTitle')[0].text[:-17]
except IndexError:
    seriesName = web.html.find('title')[0].text.split('(')[0]

# Gets the number of seasons
web = session.get(series + "episodes")
numberOfSeasons = web.html.find('[selected=selected]')[0].text
if "Unknown" in numberOfSeasons:
    bySeasonOptions = web.html.find('#bySeason')[0].find('option')
    seasons = []
    for i in range(0, len(bySeasonOptions)):
        try:
            seasons.append(int(bySeasonOptions[i].text))
        except ValueError:
            continue
    numberOfSeasons = max(seasons)
numberOfSeasons = int(numberOfSeasons)

# Loops trough seasons, adding the value of each episode:
for i in range(0, numberOfSeasons):
    if numberOfSeasons == 1:
        web = session.get(series + "episodes?season=1")
    else:
        web = session.get(series + "episodes?season=" + str(i + 1))
    # The problem of getting the rates with the class .ipl-rating-star__rating is that many
    # elements use that class. We have to remove non-numeric values first and then those who
    # don't belong (numbers 1 to 10 between scores)
    ratings = web.html.find('.ipl-rating-star__rating')
    new_ratings = []
    # Removes non-numeric values (I think all of them are "Rate")
    for k in range(0, len(ratings)):
        try:
            n = float(ratings[k].text)
            new_ratings.append(n)
        except ValueError:
            continue
    
    ratings = new_ratings
    new_ratings = []
    # There's the numbers 1-10 between each score, we count to 10 and then add the following value
    n = 0
    for k in range(0, len(ratings)):
        # Unrated episodes get the following value of zero.
        # All the following episodes will be unrated, so we break here.
        if n == 0:
            if ratings[k] == 0:
                break
            new_ratings.append(ratings[k])
            n += 1
        elif n == 11:
            n = 0
        else:
            n += 1
    
    ratings = new_ratings
    for r in ratings:
        episodeRating.append(r)
    if ratings: # Empty list: season not released yet
        seasonMarkers.append(len(episodeRating))

# Makes the array start at index 1, for representation purpose:
new_rating = []
new_rating.append(None)
for e in episodeRating:
    new_rating.append(e)
episodeRating = new_rating

# Find median score
sumOfRates = 0
for e in range(1, len(episodeRating)):
    sumOfRates += episodeRating[e]
median = sumOfRates / (len(episodeRating) - 1)

# We have the data, now we only need to make the plot
plt.plot(episodeRating, 'co:')
plt.suptitle(seriesName)
plt.ylabel("Rating")
plt.xticks([])
plt.axis([0, len(episodeRating), 0, 10])
plt.tight_layout()
# Season markers
for m in range(0, len(seasonMarkers) - 1):
    plt.axvline(x=(seasonMarkers[m] + 0.5), color='r', linestyle='--', alpha=0.4)
# Median score
plt.axhline(y=median, color='b', linestyle='--', alpha=0.4)
plt.text(1.5, median, str(median)[0:3], color='b')
plt.show()