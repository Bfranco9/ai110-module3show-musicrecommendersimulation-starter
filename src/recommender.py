import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Points per feature (sum to 10.0). Genre outweighs mood: genre is a stable taste,
# mood is situational and partly captured by energy/valence/acousticness.
WEIGHTS = {
    "genre": 2.8,
    "mood": 1.8,
    "energy": 2.0,
    "acousticness": 1.0,
    "valence": 1.0,
    "danceability": 0.7,
    "tempo_bpm": 0.7,
}
ARTIST_BONUS = 0.5  # small extra on top of the 10 points

# Range used to normalize numeric differences to 0-1 (tempo spans ~60-168 BPM).
NUMERIC_RANGES = {"tempo_bpm": 108.0}

# Half-credit pairs, so near-misses (e.g. "indie pop" for a pop fan) don't score 0.
SIMILAR_GENRES = {frozenset(p) for p in (("pop", "indie pop"), ("lofi", "ambient"), ("rock", "metal"))}
SIMILAR_MOODS = {
    frozenset(p)
    for p in (("chill", "relaxed"), ("chill", "focused"), ("relaxed", "focused"),
              ("intense", "aggressive"), ("happy", "euphoric"), ("happy", "energetic"))
}


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    print(f"Loading songs from {csv_path}... ({len(songs)} songs)")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a taste profile; return (points, list of reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Categorical features: exact match earns full points, a close neighbor earns half.
    for field, weight, neighbors in (
        ("genre", WEIGHTS["genre"], SIMILAR_GENRES),
        ("mood", WEIGHTS["mood"], SIMILAR_MOODS),
    ):
        if field not in user_prefs:
            continue
        wanted, actual = user_prefs[field], song[field]
        if actual == wanted:
            points = weight
            reasons.append(f"{field} match: {actual} (+{points:.2f})")
        elif frozenset((actual, wanted)) in neighbors:
            points = weight * 0.5
            reasons.append(f"{field} close to {wanted}: {actual} (+{points:.2f})")
        else:
            continue
        score += points

    # Numeric features: reward closeness to the target, not a bigger value.
    for field, weight in WEIGHTS.items():
        if field in ("genre", "mood") or field not in user_prefs:
            continue
        span = NUMERIC_RANGES.get(field, 1.0)
        closeness = max(0.0, 1.0 - abs(song[field] - user_prefs[field]) / span)
        points = weight * closeness
        score += points
        reasons.append(
            f"{field} {song[field]:g} vs target {user_prefs[field]:g} (+{points:.2f})"
        )

    if user_prefs.get("artist") and song["artist"] == user_prefs["artist"]:
        score += ARTIST_BONUS
        reasons.append(f"favorite artist: {song['artist']} (+{ARTIST_BONUS:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    scored = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
