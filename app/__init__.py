import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

team = [
    {
        "name": "Member One",
        "image": "img/logo.jpg",
        "about": "Write a short bio about yourself here.",
        "work_experiences": [
            {
                "title": "Software Intern",
                "company": "Example Corp",
                "dates": "Summer 2024",
                "description": "Built internal tools with Python and Flask.",
            },
        ],
        "education": [
            {
                "school": "My University",
                "degree": "B.S. Computer Science",
                "dates": "2022 - Present",
            },
        ],
        "hobbies": [
            {"name": "Photography"},
            {"name": "Hiking"},
        ],
    },
    {
        "name": "Member Two",
        "image": "img/logo.jpg",
        "about": "Write a short bio about yourself here.",
        "work_experiences": [
            {
                "title": "Teaching Assistant",
                "company": "My University",
                "dates": "2023 - Present",
                "description": "Helped students with computer science coursework.",
            },
        ],
        "education": [
            {
                "school": "My University",
                "degree": "B.S. Computer Science",
                "dates": "2022 - Present",
            },
        ],
        "hobbies": [
            {"name": "Reading"},
        ],
    },
    {
        "name": "Member Three",
        "image": "img/logo.jpg",
        "about": "Write a short bio about yourself here.",
        "work_experiences": [],
        "education": [],
        "hobbies": [],
    },
]

pages = [
    {"endpoint": "index", "name": "Home", "url": "/"},
    {"endpoint": "hobbies", "name": "Hobbies", "url": "/hobbies"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        team=team,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="My Hobbies",
        url=os.getenv("URL"),
        team=team,
        pages=pages,
    )
