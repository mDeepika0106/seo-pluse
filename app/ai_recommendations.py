
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_recommendations(audit_data):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "AI API key is missing. Please configure your .env file."

    client = Groq(api_key=api_key)

    prompt = f"""
    You are an SEO marketing intelligence assistant.

    Analyze the following website SEO audit data.

    The SEO score and metrics have already been calculated
    by our Python program. Do not change or recalculate them.

    Your job is to:
    1. Explain the main SEO problems.
    2. Prioritize issues as High, Medium or Low.
    3. Give practical solutions.
    4. Suggest actionable tasks for the marketing team.
    5. Use simple language.

    Audit data:
    {json.dumps(audit_data, indent=2)}

    Format your answer using:
    - Overall summary
    - High priority tasks
    - Medium priority tasks
    - Low priority tasks
    - Marketing action plan
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI recommendation failed: {error}"
