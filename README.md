## Music Megahits

In this project, I analyze audio features of hit pop songs in order to answer the question of what makes certain hit pop songs stay on the charts week after week while others drop off. I also explored whether it is advantageous for a song to be right on trend with what is popular, or to be distinctive and differentiate itself with a different sound.


### Data Collection
<br>
<!--
![Image Not Found](https://github.com/nruedy/music-megahits/blob/master/images/Billboard.png "Billboard Logo")
-->
<img src="images/Billboard.png" alt="Image Not Found" width=200>
<br>
1. I built a scraper for the Billboard Top 100 Pop singles chart.

2. I cleaned the data extensively. This was important because songs and artists were often listed in two different ways (e.g., "Living on a Prayer" vs. "Livin' on a Prayer".)

3. I aggregated the data based on a combination of artist and song to get a count of how many weeks each song was in the charts.

4. I defined a hit as a song that was on the charts for more than 20 weeks, and a flop as one that was on for five weeks or fewer. I also restricted the data set to the years 1980-2005, because this was a period where the ratio of hits to flops was fairly stable.

<!--
![Image Not Found](https://github.com/nruedy/music-megahits/blob/master/images/EchoNest.png "Echo Nest Logo")
-->
<img src="images/EchoNest.png" alt="Image Not Found" width=220>
<br>
1. For the audio features, I used Echo Nest’s API, which provides an extensive list of features available by song. For a search on Echo Nest's API to produce a result, both the song and artist names must match. Unfortunately, Echo Nest and Billboard often list songs and artists differently, and if either does not match, the search will be unsuccessful. To address this, the module I wrote to call Echo Nest's API tries a number of transformations on the song and artist name from Billboard. For instance, if searching for a song/artist combination does not produce any results, the module will try variations on the song and artist name, for instance, removing 'the' or 'a' if they are present. In other words, if the artist "Eminem" and the song "*The* Real Slim Shady" does not produce any results, the program will also search for "Eminem" and "Real Slim Shady." By trying a number of different transformations, of the approximately 34,000 tracks I searched, I was able to find Echo Nest data for 84%.

2. Echo Nest features are produced using machine learning algorithms. They cover both straightforward aspects of the song, such as the key and time signature, as well as assessments of a song’s more subjective qualities such as danceability and positivity. Echo Nest data comes in JSON format. I parsed these files to extract audio features for each song.

### Feature Engineering
To supplement the Echo Nest features, I calculated two sets of additional features:

* **Change:** I calculated the degree of change within a song, for instance in tempo and volume. I did this by calculating the standard deviation of measures that were taken repeatedly. For instance, the change in tempo is measured by calculating the standard deviation of the length in seconds of each bar in the song.

* **Distinctiveness:** I calculated how different the song was on each of the features from other songs that were popular during the same time. First, I identified a “cohort” for each song, i.e., a list of other songs that were on the charts during the same weeks. Then I normalized the song's features using the mean and standard deviation of these features.

### Modelling

My final data set contained just over 2500 songs. I compared the results of several machine learning algorithms. Gradient Boosting fit the best, with an ROC-AUC score of .70. Looking at the top five predictors, it’s interesting to note that four out of the five are relative features. These are the features I engineered to measure *distinctiveness*.

##### Top Predictors

<img src="images/FeatureImportances.png" alt="Image Not Found" width=300>
<br>


##### Partial Dependence Plots
Note: The curve is above zero for the values of the feature for which the model would predict that a song is a hit.

<img src="images/PartDep_Rel_Instrum.png" alt="Image Not Found" width=300>
<br>
<br>
<img src="images/PartDep_Rel_TempoChg.png" alt="Image Not Found" width=300>
<br>
<br>
<img src="images/PartDep_Rel_RhythmicSimp.png" alt="Image Not Found" width=300>
<br>
<br>
<img src="images/PartDep_Rel_Liveness.png" alt="Image Not Found" width=300>
<br>
<br>
<img src="images/PartDep_Positivity.png" alt="Image Not Found" width=300>
<br>

### Libraries Used
* Pandas
* Numpy
* Scipy
* Scikit-learn
* Statsmodels
* Beautiful Soup
* Matplotlib
