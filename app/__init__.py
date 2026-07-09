import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from peewee import CharField, DateTimeField, Model, MySQLDatabase, TextField
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

member = {
    "name": "Adora",
    "image": "img/Adora/profile.png",
    "about": (
        "I'm Adora, an incoming junior at the University of Florida pursuing a B.S. in "
        "Computer Science with a minor in Digital Arts & Sciences (graduating "
        "May 2028). I'm interested in UX/UI design, web development, and "
        "software engineering! I also love cats!"
    ),
    "work_experiences": [
        {
            "title": "Full-stack Developer",
            "company": "The Agency at UF",
            "dates": "Aug 2025 - Present · Gainesville, Florida",
            "description": (
                "Developed interactive, user-friendly web applications using "
                "React, ensuring functionality and intuitive user experiences."
            ),
        },
        {
            "title": "Research Assistant",
            "company": "University of Florida",
            "dates": "Jan 2026 - Present · Gainesville, Florida · Hybrid",
            "description": (
                "Contributing to an Afrodance research project exploring motion "
                "capture and data visualization within Unity."
            ),
        },
    ],
    "education": [
        {
            "school": "University of Florida",
            "degree": "Bachelor of Science - BS, Computer Science",
            "dates": "2024 – 2028",
        },
        {
            "school": "Osceola County School for The Arts",
            "degree": "High School",
            "dates": "2017 - 2020",
        },
    ],
    "hobbies": [
        {"name": "Violin", "image": "img/Adora/violin.png"},
        {"name": "Gaming", "image": "img/Adora/gaming.png"},
    ],
    "visited_places": [
        {"lat": 29.6516, "lng": -82.3248, "name": "Gainesville, FL"},
        {"lat": 28.2920, "lng": -81.4076, "name": "Kissimmee, FL"},
    ],
}

pages = [
    {"endpoint": "index", "name": "Home", "url": "/"},
    {"endpoint": "hobbies", "name": "Hobbies", "url": "/hobbies"},
]

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in 
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)

    if post is None:
        return {"error": "Timeline post not found"}, 404

    post.delete_instance()
    return {"message": "Timeline post deleted"}

@app.route('/timeline')
def timeline():
    logger.info("Serving timeline page")
    return render_template("timeline.html", title="Timeline")

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        member=member,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="My Hobbies",
        url=os.getenv("URL"),
        member=member,
        pages=pages,
    )
