from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author must have a name")

        existing = db.session.query(Author).filter_by(name=name).first()

        if existing:
            raise ValueError("Author name must be unique")

        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError("Phone number is required")

        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")

        return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, title):
        if not title or title.strip() == "":
            raise ValueError("Title is required")

        clickbait_words = [
            "Won't Believe",
            "Secret",
            "Top",
            "Guess"
        ]

        if not any(word in title for word in clickbait_words):
            raise ValueError("Title is not clickbait enough")

        return title

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters")

        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary is not None and len(summary) > 250:
            raise ValueError("Summary cannot exceed 250 characters")

        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Invalid category")

        return category

    def __repr__(self):
        return (
            f"Post(id={self.id}, title={self.title}, "
            f"content={self.content}, summary={self.summary})"
        )