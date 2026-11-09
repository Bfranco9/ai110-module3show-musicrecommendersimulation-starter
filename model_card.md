# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender works like a judge scoring every song in the catalog against one listener's taste, then handing back the songs with the highest scores.

**What the listener tells us.** A taste profile lists a favorite genre, a favorite mood, a favorite artist, and target levels for energy, tempo, positivity (valence), danceability, and acousticness (how acoustic versus electronic a song sounds).

**How a song earns points.** Each song can earn up to 10 points, plus a half-point bonus if it is by the listener's favorite artist. The points are split across features by importance:

| Feature | Max points | Why it gets this much |
|---|---|---|
| Genre | 2.8 | Genre is a steady, long-term taste, so it counts most |
| Energy | 2.0 | The best single number for a song's overall "vibe" |
| Mood | 1.8 | Matters, but moods change by the hour and overlap with energy |
| Acousticness | 1.0 | Separates mellow acoustic tracks from electronic ones |
| Valence | 1.0 | Separates upbeat songs from darker ones at similar energy |
| Danceability | 0.7 | Useful but tends to move together with energy |
| Tempo | 0.7 | Useful but tends to move together with energy |

- **Genre and mood** are all-or-nothing, with one exception: a close neighbor (for example "indie pop" for a pop fan, or "focused" for someone who likes "chill") earns half the points, so near-misses are not treated as total misses.
- **The number-based features** reward being *close* to the listener's target, not being high or low. A song that matches the target exactly gets full points, and the further away it is, the fewer points it gets. This way, someone who wants calm music is not pushed toward loud songs.

**Choosing the winners.** Once every song has a total, the songs are sorted from highest to lowest and the top five are shown. Each result comes with a plain list of reasons (for example, "genre match: lofi (+2.80)") so the listener can see exactly why a song was picked.

**Why genre outweighs mood.** The two are weighted close to each other, but genre is a more reliable sign of taste. Mood is also partly captured by energy, valence, and acousticness, so giving it a large weight would count the same signal twice.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
