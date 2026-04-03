import re
import gender_guesser.detector as gender
from parsers.ai_gender import guess_gender_ai

# Initialize detector once
detector = gender.Detector()

FEMALE_SIGNALS = [
    "she","her","girl","woman","female","lady","mrs","miss","ms",
    "queen","mom","mother","wife"
]

MALE_SIGNALS = [
    "he","him","boy","man","male","mr","sir","guy",
    "king","dad","father","husband"
]


def should_use_ai(name):

    if not name:
        return False

    name = name.strip()

    # too long → likely not a real name
    if len(name.split()) > 3:
        return False

    # must contain alphabets
    if not any(c.isalpha() for c in name):
        return False

    # avoid usernames / noisy strings
    if any(sym in name for sym in ["_", "@", "#", "123"]):
        return False

    return True


def estimate_demographics(username, display_name, bio=""):

    text = f"{username} {display_name} {bio}".lower()
    tokens = re.findall(r'\b\w+\b', text)

    gender = "unknown"

    # Step 1: keyword / pronoun detection
    if any(t in FEMALE_SIGNALS for t in tokens):
        gender = "female"
    elif any(t in MALE_SIGNALS for t in tokens):
        gender = "male"

    # Step 2: name-based fallback
    if gender == "unknown" and display_name:
        first_name = display_name.split()[0]
        guess = detector.get_gender(first_name)

        if guess in ["female", "mostly_female"]:
            gender = "female"
        elif guess in ["male", "mostly_male"]:
            gender = "male"

    # Step 3: AI fallback (only if safe)
    if gender == "unknown" and should_use_ai(display_name):
        ai_gender = guess_gender_ai(display_name)

        if ai_gender in ["male", "female"]:
            gender = ai_gender

    return {
        "estimated_gender": gender,
        "estimated_age_group": "unknown"
    }