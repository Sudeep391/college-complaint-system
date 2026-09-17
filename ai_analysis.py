import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing.")

client = Groq(api_key=GROQ_API_KEY)


def analyze_complaint(description):

    prompt = f"""
You are an AI assistant for a college complaint management system.

Analyze the following student complaint.

Complaint:
{description}

Return the result in exactly this format:

Summary: <short summary>
Department: <department>
Priority: <Low, Medium, High, or Critical>

Possible departments:
- Electrical
- Plumbing
- Classroom
- Hostel
- Laboratory
- Cleanliness
- Internet
- Furniture
- Security
- Water Supply
- Other

Choose the most appropriate department and priority.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content