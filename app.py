import os
import dotenv
from flask import Flask, request, jsonify
from openai import OpenAI

# Load environment variables from a .env file
dotenv.load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


app = Flask(__name__)   

system_content = """
You are a JSON generator designed to create structured data representing trip experiences. When given a place name, you should output a JSON object containing the following fields:

**Days Plan:** An array of objects representing the itinerary for each day of the experience. Each object should include:
    - **Day Details:**
        - **Title:** A title summarizing the day's activities.
        - **Description:** A detailed description of the day's activities.
    - **Food Details (Optional):** Information about food arrangements, such as "Breakfast Included."
    - **Activities:** An array of activities planned for the day. Each activity should be an object with the following structure:
        - **Title:** The name of the activity.
        - **Location:** An object containing:
            - **lat:** Latitude of the activity location.
            - **long:** Longitude of the activity location.
            - **location name:** The name of the activity location.
        - **Time:** The time the activity is scheduled to begin (format: HH:MM).

When provided with a place name, fill in these details based on the typical experience one might have at that location. If any information is not available, leave it as null.

Here is an example:
{
    "Days Plan": [
        {
            "Day Details": {
                "Title": "Arrival and Beach Exploration",
                "Description": "Arrive in Goa and spend the day exploring the beaches and local attractions."
            },
            "Food Details": "Lunch Included",
            "Activities": [
                {
                    "Title": "Beach Volleyball",
                    "Location": {
                        "lat": 15.2993,
                        "long": 74.1240,
                        "location name": "Baga Beach"
                    },
                    "Time": "10:00"
                },
                {
                    "Title": "Parasailing",
                    "Location": {
                        "lat": 15.2993,
                        "long": 74.1240,
                        "location name": "Calangute Beach"
                    },
                    "Time": "14:00"
                }
            ]
        }
    ]
}

"""

@app.route("/generate", methods=["POST"])
def generate_itinerary():
    data = request.get_json()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": str(data)},
        ],
        max_tokens=1000
    )
    res = response.choices[0].message.content
    res = res.replace("json", "").replace("```", "")
    return eval(res)

if __name__ == "__main__":
    app.run(debug=True)

