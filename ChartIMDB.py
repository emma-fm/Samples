from requests_html import HTMLSession
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
    # If the season selected is "Unknown", get all values in the bySeason selector
    # and get the max value
    bySeasonOptions = web.html.find('#bySeason')[0].find('option')
    seasons = []
    for i in range(0, len(bySeasonOptions)):
        try:
            seasons.append(int(bySeasonOptions[i].text))
        except ValueError: # Is not a number: "Unknown"
            continue
    numberOfSeasons = max(seasons)
numberOfSeasons = int(numberOfSeasons)

# Loops trough seasons, adding the value of each episode:
warningShowed = False # Handles the season skipped warning
for i in range(0, numberOfSeasons):
    web = session.get(series + "episodes?season=" + str(i + 1))
    # The problem of getting the rates with the class .ipl-rating-star__rating is that many
    # elements use that class. We have to remove non-numeric values first and then those who
    # don't belong (numbers 0 to 10 between scores)
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
        if n == 0:
            # Unrated episodes get the following value of zero.
            # All the following episodes will be unrated, so we break here.
            # THIS IS NOT TRUE FOR NOT SO POPULAR SERIES, because they may have unrated episodes
            # The problem is that you can't make a reliable chart if some episodes are unrated
            # so I'm not going to change anything here.
            if ratings[k] == 0:
                if not warningShowed:
                    print("Season skipped! It might be an unreleased season, or there might be an unrated episode.")
                    print("If it's a single chapter, all the season has been skipped!")
                    print("Charts like this with unrated chapters might not be reliable, consider another series, program, or presentation.")
                    warningShowed = True
                else:
                    print("Season skipped!")
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