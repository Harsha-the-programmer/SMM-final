from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# simple cache to reduce API calls
gender_cache = {}

def guess_gender_ai(name):

    if not name or len(name.strip()) < 3:
        return "unknown"

    # caching
    if name in gender_cache:
        return gender_cache[name]

    prompt = f"""
Return ONLY one word: male, female, or unknown.

If the input is not a real human name → return unknown.
Do NOT guess.

Name: {name}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # FIXED MODEL
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=5
        )

        result = response.choices[0].message.content.strip().lower()

        if result not in ["male", "female"]:
            result = "unknown"

        gender_cache[name] = result
        return result

    except Exception as e:
        print("Groq error:", e)
        return "unknown"