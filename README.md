# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

A recommendation system primarily uses stages in order to recomment a system: candidate generation, scoring and ranking, and re-ranking. These go to identify the relevance in large categories which are used to predict based on past user interactions with the different attributes from listened to songs, searches, and general interactions (i.e. likes or saves). Then there is a third stage where it can re-rank the evaluation to reintroduce recommendations outside of the designated scoring for "freshness"

We are going to implement some of those features found in popular recommendation systems by looking at categorical data like mood, genre, and artist and compare the numberical data like the energy, tempo, acousticness, and valence to provide a range and rank songs and lists. The categorical data will have more weight compared to the numerical data and the main points that have the most significance is the acousticness and tempo/bpm to measure the preference.
---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Generally speaking, the genre will outweigh the mood but not by  a large factor so it isn't  the only focus to creating the recommendations. The logic will take the user input/preferences, then rank by weight to sum up a weight of 1 for all available features and then compare that with the individual songs in the CSV file before recommending songs that have a close matching score to the user preference.
- Categorical (genre, mood): a binary match (1 or 0) works. Optionally add partial credit for near neighbors, such as pop ↔ indie pop at 0.5, or chill ↔ relaxed ↔ focused. That would stop "indie pop" from scoring 0 for a pop fan.
- Numeric (energy, valence, danceability, acousticness): score similarity, not magnitude, as 1 - |song - target|. Otherwise "high energy" always wins, even for users who want low energy.
- Tempo: normalize it first, as 1 |song_bpm - target_bpm| / (168 - 60). Raw BPM would dwarf the 0–1 features.

Potential pitfalls can be not enough weight given to minor features that are arbitrary for each song such as energy, dancability, or tempo. There is a huge emphasis currently on genre that can dwarf meaningful comparisons to the songs. The last pitfall is limited genres generated with a list of 20 songs, so a bigger pool to choose from can help variance of data.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
1. Rainy Day Tapes - LoRoom                     10.40 / 10.5
------------------------------------------------------------
  * genre match: lofi (+2.80)
  * mood match: chill (+1.80)
  * energy 0.38 vs target 0.4 (+1.96)
  * acousticness 0.8 vs target 0.8 (+1.00)
  * valence 0.57 vs target 0.6 (+0.97)
  * danceability 0.6 vs target 0.6 (+0.70)
  * tempo_bpm 75 vs target 80 (+0.67)
  * favorite artist: LoRoom (+0.50)

2. Midnight Coding - LoRoom                     10.30 / 10.5
------------------------------------------------------------
  * genre match: lofi (+2.80)
  * mood match: chill (+1.80)
  * energy 0.42 vs target 0.4 (+1.96)
  * acousticness 0.71 vs target 0.8 (+0.91)
  * valence 0.56 vs target 0.6 (+0.96)
  * danceability 0.62 vs target 0.6 (+0.69)
  * tempo_bpm 78 vs target 80 (+0.69)
  * favorite artist: LoRoom (+0.50)

3. Library Rain - Paper Lanterns                 9.77 / 10.5
------------------------------------------------------------
  * genre match: lofi (+2.80)
  * mood match: chill (+1.80)
  * energy 0.35 vs target 0.4 (+1.90)
  * acousticness 0.86 vs target 0.8 (+0.94)
  * valence 0.6 vs target 0.6 (+1.00)
  * danceability 0.58 vs target 0.6 (+0.69)
  * tempo_bpm 72 vs target 80 (+0.65)

4. Focus Flow - LoRoom                           9.57 / 10.5
------------------------------------------------------------
  * genre match: lofi (+2.80)
  * mood close to chill: focused (+0.90)
  * energy 0.4 vs target 0.4 (+2.00)
  * acousticness 0.78 vs target 0.8 (+0.98)
  * valence 0.59 vs target 0.6 (+0.99)
  * danceability 0.6 vs target 0.6 (+0.70)
  * tempo_bpm 80 vs target 80 (+0.70)
  * favorite artist: LoRoom (+0.50)

5. Spacewalk Thoughts - Orbit Bloom              7.93 / 10.5
------------------------------------------------------------
  * genre close to lofi: ambient (+1.40)
  * mood match: chill (+1.80)
  * energy 0.28 vs target 0.4 (+1.76)
  * acousticness 0.92 vs target 0.8 (+0.88)
  * valence 0.65 vs target 0.6 (+0.95)
  * danceability 0.41 vs target 0.6 (+0.57)
  * tempo_bpm 60 vs target 80 (+0.57)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



