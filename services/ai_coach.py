import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

# Initialize Groq client
client = Groq(api_key=api_key)

# Current supported Groq model
MODEL_NAME = "openai/gpt-oss-20b"


def generate_ai_coach(
    total,
    breakdown,
    vehicle=None,
    distance=None
):
    """
    Generate personalized carbon reduction advice.

    Important:
    - Carbon emissions are calculated by EcoTrack's deterministic calculator.
    - The LLM only analyzes the provided numbers and gives recommendations.
    """

    prompt = f"""
You are EcoTrack AI, a personal carbon reduction coach.

USER'S CARBON FOOTPRINT
Total: {total:.2f} kg CO2e

CATEGORY BREAKDOWN:
{breakdown}

TRANSPORT DETAILS:
Vehicle: {vehicle}
Distance: {distance} km

Your task is to analyze the provided footprint and give practical,
personalized recommendations.

IMPORTANT RULES:
1. Do NOT calculate or modify emission factors.
2. Do NOT invent carbon emission numbers.
3. Use only the provided footprint data.
4. Identify the largest contributing category.
5. Give exactly 3 practical actions.
6. Recommendations should be realistic for a normal student/user.
7. Keep the response concise and easy to understand.
8. Do not give generic climate advice unrelated to the user's data.

Return exactly this format:

INSIGHT:
<one short personalized insight>

ACTIONS:
1. <first actionable recommendation>
2. <second actionable recommendation>
3. <third actionable recommendation>
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise, practical and personalized "
                    "sustainability coach."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=400,
        include_reasoning=False
    )

    return response.choices[0].message.content
