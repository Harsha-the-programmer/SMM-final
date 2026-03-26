import re
import gender_guesser.detector as gender

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

    return {
        "estimated_gender": gender,
        "estimated_age_group": "unknown"
    }