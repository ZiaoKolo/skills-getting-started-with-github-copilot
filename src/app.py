from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities"
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static"
)

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },

    # 🏀 Sports activities
    "Basketball Team": {
        "description": "Team basketball training and competitions",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Soccer practice and friendly matches",
        "schedule": "Mondays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": []
    },

    # 🎨 Artistic activities
    "Painting Workshop": {
        "description": "Explore painting techniques and creativity",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    },
    "Drama Club": {
        "description": "Acting, theater, and stage performance",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": []
    },

    # 🧠 Intellectual activities
    "Math Olympiad": {
        "description": "Advanced math problem solving and competitions",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 8,
        "participants": []
    },
    "Debate Club": {
        "description": "Improve public speaking and critical thinking",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""

    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # ✅ Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up for this activity"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
