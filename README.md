## Music Megahits

In this project, I analyze audio features of hit pop songs in order to answer the question of what makes certain hit pop songs stay on the charts week after week while others drop off. I also wondered if it is advantageous for a song to be right on trend with what is popular, or to be distinctive and differentiate itself with a different sound.

To begin to answer these questions, I used the following packages for my data collection and analysis:

1. I scraped data from the Billboard Top 100 Pop singles chart.
2. I cleaned the data. This was important because songs and artists were sometimes listed in two different ways (e.g., "Living on a Prayer" vs. "Livin' on a Prayer".) I then aggregated the data based on a combination of Artist and Song to get a count of how many weeks each song was in the charts.
3. I defined a hit as a song that was on the charts for more than 20 weeks, and a flop as one that was on for five weeks or fewer. I also restricted the data set to the years 1980-2005, because this was a period where the ratio of hits to flops was fairly stable. In all, I had just over 2500 songs for my analysis.
4. For the audio features, I used Echo Nest’s API, which provides an extensive list of features available by song. EN data comes in JSON format. I parsed these files to pull out audio features for each song, such as the key and time signature. EN also provides ML assessments on a song’s qualities such as danceability and positivity. I also engineered two additional sets of features:
    - I calculated the degree of change within a song, for instance in tempo and volume.
    - I calculated how different the song was on each of the features from other songs on the chart in the same weeks.
5. I compared the results of several machine learning algorithms. Gradient Boosting fit the best, with an ROC-AUC score of .70. Looking at the top five predictors, it’s interesting to note that four out of the five are relative features. These are the ‘black sheep’ features I engineered to measure how similar or different a song is on that feature, so it appears putting them into context might be helpful.

To examine these features in a little more depth, we can look at the partial dependence plots. Basically, the curve is above zero for the values of the feature for which the model would predict that a song is a hit.

Looking at the first one, being low on “instrumentalness” (that is, having singing) appears to be favorable. Singing is good – no surprises there.

Low values of rhythmic simplicity are good, which means having some syncopations or other rhythmic variations is probably a good thing.

And lastly, sad songs appear to be doing well.
