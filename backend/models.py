"""SQLAlchemy ORM models for all site content.

Each model maps to a content section found in the React frontend's ``src/data``
directory (courses, bootcamp, events, jobs, blog, quizzes, etc.). List/array
fields from the TypeScript interfaces are stored as JSON columns, while nested
objects that are naturally relational (course schedules and FAQs) use proper
foreign-key relationships.
"""

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


class SerializerMixin:
    """Adds a simple ``to_dict`` helper used by the API endpoints."""

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# ---------------------------------------------------------------------------
# Courses
# ---------------------------------------------------------------------------
class Course(Base, SerializerMixin):
    __tablename__ = "courses"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    short_title = Column(String, nullable=True)
    category = Column(String, nullable=False, index=True)
    badge = Column(String, nullable=True)
    # integer field to control display ordering of courses; lower values appear first
    display_order = Column(Integer, default=0, index=True)
    description = Column(Text, nullable=True)
    overview = Column(Text, nullable=True)
    key_features = Column(JSON, default=list)
    course_content = Column(JSON, default=list)
    who_should_attend = Column(JSON, default=list)

    schedules = relationship(
        "CourseSchedule", back_populates="course", cascade="all, delete-orphan"
    )
    faqs = relationship(
        "CourseFAQ", back_populates="course", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["schedules"] = [schedule.to_dict() for schedule in self.schedules]
        data["faqs"] = [faq.to_dict() for faq in self.faqs]
        return data

    def __str__(self) -> str:
        return self.title or self.id


class CourseSchedule(Base, SerializerMixin):
    __tablename__ = "course_schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    price = Column(String, nullable=True)
    original_price = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    instructor = Column(String, nullable=True)

    course = relationship("Course", back_populates="schedules")

    def __str__(self) -> str:
        return f"{self.date} ({self.mode})"


class CourseFAQ(Base, SerializerMixin):
    __tablename__ = "course_faqs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=True)

    course = relationship("Course", back_populates="faqs")

    def __str__(self) -> str:
        return self.question


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
class Event(Base, SerializerMixin):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    location = Column(String, nullable=True)
    type = Column(String, nullable=False, index=True)  # "upcoming" | "past"
    image = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    registration_link = Column(String, nullable=True)
    recording_link = Column(String, nullable=True)

    def __str__(self) -> str:
        return self.title


# ---------------------------------------------------------------------------
# Job openings
# ---------------------------------------------------------------------------
class Job(Base, SerializerMixin):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    location = Column(String, nullable=True)
    type = Column(String, nullable=True)  # Full-Time | Contract ...
    department = Column(String, nullable=True, index=True)
    description = Column(Text, nullable=True)
    link = Column(String, nullable=True)

    def __str__(self) -> str:
        return self.title


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------
class BlogPost(Base, SerializerMixin):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    author = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    category = Column(String, nullable=True, index=True)
    read_time = Column(String, nullable=True)

    def __str__(self) -> str:
        return self.title


class BlogHighlight(Base, SerializerMixin):
    """Short blog teaser cards shown on the home page (blogData.ts)."""

    __tablename__ = "blog_highlights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    excerpt = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    link = Column(String, nullable=True)

    def __str__(self) -> str:
        return self.title


# ---------------------------------------------------------------------------
# Quizzes
# ---------------------------------------------------------------------------
class Quiz(Base, SerializerMixin):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    short_title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    question_count = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)
    icon = Column(String, nullable=True)  # lucide icon name
    link = Column(String, nullable=True)

    def __str__(self) -> str:
        return self.title


# ---------------------------------------------------------------------------
# Interview guides
# ---------------------------------------------------------------------------
class InterviewGuide(Base, SerializerMixin):
    __tablename__ = "interview_guides"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False, index=True)
    coming_soon = Column(Boolean, default=False)

    def __str__(self) -> str:
        return self.title


# ---------------------------------------------------------------------------
# Testimonials
# ---------------------------------------------------------------------------
class Testimonial(Base, SerializerMixin):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    text = Column(Text, nullable=True)

    def __str__(self) -> str:
        return self.name


# ---------------------------------------------------------------------------
# Bootcamp sections
# ---------------------------------------------------------------------------
class PricingPlan(Base, SerializerMixin):
    __tablename__ = "pricing_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(String, nullable=True)
    original_price = Column(String, nullable=True)
    type = Column(String, nullable=True)
    features = Column(JSON, default=list)  # list of {text, included}
    highlighted = Column(Boolean, default=False)

    def __str__(self) -> str:
        return self.name


class WeeklyModule(Base, SerializerMixin):
    __tablename__ = "weekly_modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    week = Column(String, nullable=True)
    title = Column(String, nullable=False)
    topics = Column(JSON, default=list)

    def __str__(self) -> str:
        return f"{self.week}: {self.title}"


class AlumniStory(Base, SerializerMixin):
    __tablename__ = "alumni_stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    company = Column(String, nullable=True)
    headline = Column(String, nullable=True)
    quote = Column(Text, nullable=True)

    def __str__(self) -> str:
        return self.name


class BootcampFAQ(Base, SerializerMixin):
    __tablename__ = "bootcamp_faqs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=True)

    def __str__(self) -> str:
        return self.question


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class Stat(Base, SerializerMixin):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=True)
    suffix = Column(String, nullable=True)
    label = Column(String, nullable=False)

    def __str__(self) -> str:
        return self.label
