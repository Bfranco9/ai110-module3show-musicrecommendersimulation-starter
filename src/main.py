"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from recommender import ARTIST_BONUS, WEIGHTS, load_songs, recommend_songs
except ModuleNotFoundError:  # run as `python -m src.main` from the project root
    from src.recommender import ARTIST_BONUS, WEIGHTS, load_songs, recommend_songs

SONGS_CSV = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

MAX_SCORE = sum(WEIGHTS.values()) + ARTIST_BONUS


# Taste profile: keys match the songs.csv headers so each preference
# can be compared directly against the same field on a song.
TASTE_PROFILE = {
    "genre": "lofi",         # favorite genre
    "mood": "chill",         # favorite mood
    "artist": "LoRoom",      # favorite artist
    "energy": 0.40,          # target energy (0.0 calm - 1.0 intense)
    "tempo_bpm": 80,         # target tempo
    "valence": 0.60,         # target positivity (0.0 dark - 1.0 upbeat)
    "danceability": 0.60,    # target danceability
    "acousticness": 0.80,    # target acousticness (0.0 electric - 1.0 acoustic)
}


# Adversarial / edge-case profiles: each one probes a specific weakness in score_song.
ADVERSARIAL_PROFILES = {
    # Categorical labels say "loud", numeric targets say "quiet". Does the 4.6
    # points of genre+mood outrank a song that actually fits the numbers?
    "Conflicted Metalhead": {
        "genre": "metal",
        "mood": "aggressive",
        "energy": 0.10,
        "tempo_bpm": 60,
        "valence": 0.60,
        "danceability": 0.30,
        "acousticness": 0.95,
    },
    # Genre/mood not in the catalog and numbers outside 0-1 / the BPM range:
    # no categorical points are possible and closeness clamps to 0.
    "Out-of-Vocabulary Fan": {
        "genre": "k-pop",
        "mood": "bittersweet",
        "artist": "Nobody Known",
        "energy": 1.50,
        "tempo_bpm": 300,
        "valence": -0.20,
        "danceability": 1.00,
        "acousticness": 0.50,
    },
    # Sparse, dead-center profile: no genre, mood or artist, only middling
    # targets. Does everything tie, and is the /10.5 max score still fair?
    "Perfectly Average Listener": {
        "energy": 0.50,
        "valence": 0.50,
    },
}


def main() -> None:
    songs = load_songs(str(SONGS_CSV))

    profiles = {"Taste Profile (lofi/chill)": TASTE_PROFILE, **ADVERSARIAL_PROFILES}

    for name, user_prefs in profiles.items():
        print(f"\n### {name}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(recommendations)


def print_recommendations(recommendations, max_score: float = MAX_SCORE) -> None:
    """Print each recommendation as a ranked card: title, score, then one reason per line."""
    width = 60
    print("\n" + "=" * width)
    print("TOP RECOMMENDATIONS".center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        header = f"{rank}. {song['title']} - {song['artist']}"
        score_text = f"{score:.2f} / {max_score:.1f}"
        print(f"\n{header:<{width - len(score_text)}}{score_text}")
        print("-" * width)
        for reason in explanation.split("; "):
            print(f"  * {reason}")

    print("\n" + "=" * width)


if __name__ == "__main__":
    main()
