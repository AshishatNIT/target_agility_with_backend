"""FastAPI application exposing site content and a SQLAdmin dashboard.

Run locally with:
    uvicorn main:app --reload

- Public JSON API:   http://127.0.0.1:8000/api/...
- Interactive docs:  http://127.0.0.1:8000/docs
- Admin dashboard:   http://127.0.0.1:8000/admin
"""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session

import os

if os.getenv("RUN_SEED") == "true":
    import seed
    seed.seed()

from database import Base, engine, get_db
from security import BasicAuthMiddleware
from models import (
    AlumniStory,
    BlogHighlight,
    BlogPost,
    BootcampFAQ,
    Course,
    CourseFAQ,
    CourseSchedule,
    Event,
    InterviewGuide,
    Job,
    PricingPlan,
    Quiz,
    Stat,
    Testimonial,
    WeeklyModule,
)

# Create all tables on startup (safe to call repeatedly).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DigitalDimna Content API",
    description="Backend API and admin dashboard for the DigitalDimna React site.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS – allowed origins come from the ALLOWED_ORIGINS env var (comma-separated),
# falling back to the local Vite dev server origins for development.
# ---------------------------------------------------------------------------
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

env_origins = os.getenv("ALLOWED_ORIGINS", "")
origins = [origin.strip() for origin in env_origins.split(",") if origin.strip()] or default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protect /admin and /docs with HTTP Basic auth (credentials from env vars).
app.add_middleware(BasicAuthMiddleware)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs", "admin": "/admin"}


# ---------------------------------------------------------------------------
# Public GET API endpoints
# ---------------------------------------------------------------------------
@app.get("/api/courses")
def get_courses(db: Session = Depends(get_db)):
    # Return courses in a deterministic order controlled by the `display_order` field
    return [course.to_dict() for course in db.query(Course).order_by(Course.display_order.asc(), Course.title.asc()).all()]


@app.get("/api/events")
def get_events(db: Session = Depends(get_db)):
    return [event.to_dict() for event in db.query(Event).all()]


@app.get("/api/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return [job.to_dict() for job in db.query(Job).all()]


@app.get("/api/blog-posts")
def get_blog_posts(db: Session = Depends(get_db)):
    return [post.to_dict() for post in db.query(BlogPost).all()]


@app.get("/api/blog-highlights")
def get_blog_highlights(db: Session = Depends(get_db)):
    return [item.to_dict() for item in db.query(BlogHighlight).all()]


@app.get("/api/quizzes")
def get_quizzes(db: Session = Depends(get_db)):
    return [quiz.to_dict() for quiz in db.query(Quiz).all()]


@app.get("/api/interview-guides")
def get_interview_guides(db: Session = Depends(get_db)):
    return [guide.to_dict() for guide in db.query(InterviewGuide).all()]


@app.get("/api/testimonials")
def get_testimonials(db: Session = Depends(get_db)):
    return [item.to_dict() for item in db.query(Testimonial).all()]


@app.get("/api/pricing-plans")
def get_pricing_plans(db: Session = Depends(get_db)):
    return [plan.to_dict() for plan in db.query(PricingPlan).all()]


@app.get("/api/weekly-modules")
def get_weekly_modules(db: Session = Depends(get_db)):
    return [module.to_dict() for module in db.query(WeeklyModule).all()]


@app.get("/api/alumni-stories")
def get_alumni_stories(db: Session = Depends(get_db)):
    return [story.to_dict() for story in db.query(AlumniStory).all()]


@app.get("/api/bootcamp-faqs")
def get_bootcamp_faqs(db: Session = Depends(get_db)):
    return [faq.to_dict() for faq in db.query(BootcampFAQ).all()]


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    return [stat.to_dict() for stat in db.query(Stat).all()]


# ---------------------------------------------------------------------------
# SQLAdmin dashboard
# ---------------------------------------------------------------------------
admin = Admin(app, engine, title="DigitalDimna Admin")


class CourseAdmin(ModelView, model=Course):
    name = "Course"
    name_plural = "Courses"
    icon = "fa-solid fa-graduation-cap"
    form_include_pk = True  # id is a user-supplied slug (e.g. "psm-1"), not autoincremented
    column_list = [Course.id, Course.title, Course.display_order, Course.category, Course.badge]
    column_searchable_list = [Course.title, Course.category]
    column_sortable_list = [Course.display_order, Course.title, Course.category]


class CourseScheduleAdmin(ModelView, model=CourseSchedule):
    name = "Course Schedule"
    name_plural = "Course Schedules"
    icon = "fa-solid fa-calendar-days"
    column_list = [
        CourseSchedule.id,
        CourseSchedule.course_id,
        CourseSchedule.date,
        CourseSchedule.mode,
        CourseSchedule.price,
    ]


class CourseFAQAdmin(ModelView, model=CourseFAQ):
    name = "Course FAQ"
    name_plural = "Course FAQs"
    icon = "fa-solid fa-circle-question"
    column_list = [CourseFAQ.id, CourseFAQ.course_id, CourseFAQ.question]


class EventAdmin(ModelView, model=Event):
    name = "Event"
    name_plural = "Events"
    icon = "fa-solid fa-calendar-check"
    form_include_pk = True  # id is a user-supplied slug, not autoincremented
    column_list = [Event.id, Event.title, Event.date, Event.type, Event.location]
    column_searchable_list = [Event.title]


class JobAdmin(ModelView, model=Job):
    name = "Job Opening"
    name_plural = "Job Openings"
    icon = "fa-solid fa-briefcase"
    column_list = [Job.id, Job.title, Job.department, Job.location, Job.type]
    column_searchable_list = [Job.title, Job.department]


class BlogPostAdmin(ModelView, model=BlogPost):
    name = "Blog Post"
    name_plural = "Blog Posts"
    icon = "fa-solid fa-newspaper"
    column_list = [BlogPost.id, BlogPost.title, BlogPost.author, BlogPost.category, BlogPost.date]
    column_searchable_list = [BlogPost.title, BlogPost.author]


class BlogHighlightAdmin(ModelView, model=BlogHighlight):
    name = "Blog Highlight"
    name_plural = "Blog Highlights"
    icon = "fa-solid fa-star"
    column_list = [BlogHighlight.id, BlogHighlight.title]


class QuizAdmin(ModelView, model=Quiz):
    name = "Quiz"
    name_plural = "Quizzes"
    icon = "fa-solid fa-clipboard-question"
    form_include_pk = True  # id is a user-supplied slug, not autoincremented
    column_list = [Quiz.id, Quiz.title, Quiz.question_count, Quiz.duration]


class InterviewGuideAdmin(ModelView, model=InterviewGuide):
    name = "Interview Guide"
    name_plural = "Interview Guides"
    icon = "fa-solid fa-book"
    form_include_pk = True  # id is a user-supplied slug, not autoincremented
    column_list = [
        InterviewGuide.id,
        InterviewGuide.title,
        InterviewGuide.category,
        InterviewGuide.coming_soon,
    ]


class TestimonialAdmin(ModelView, model=Testimonial):
    name = "Testimonial"
    name_plural = "Testimonials"
    icon = "fa-solid fa-quote-left"
    column_list = [Testimonial.id, Testimonial.name, Testimonial.role]


class PricingPlanAdmin(ModelView, model=PricingPlan):
    name = "Pricing Plan"
    name_plural = "Pricing Plans"
    icon = "fa-solid fa-tags"
    column_list = [PricingPlan.id, PricingPlan.name, PricingPlan.price, PricingPlan.highlighted]


class WeeklyModuleAdmin(ModelView, model=WeeklyModule):
    name = "Weekly Module"
    name_plural = "Weekly Modules"
    icon = "fa-solid fa-list-check"
    column_list = [WeeklyModule.id, WeeklyModule.week, WeeklyModule.title]


class AlumniStoryAdmin(ModelView, model=AlumniStory):
    name = "Alumni Story"
    name_plural = "Alumni Stories"
    icon = "fa-solid fa-user-graduate"
    column_list = [AlumniStory.id, AlumniStory.name, AlumniStory.company, AlumniStory.headline]


class BootcampFAQAdmin(ModelView, model=BootcampFAQ):
    name = "Bootcamp FAQ"
    name_plural = "Bootcamp FAQs"
    icon = "fa-solid fa-circle-question"
    column_list = [BootcampFAQ.id, BootcampFAQ.question]


class StatAdmin(ModelView, model=Stat):
    name = "Stat"
    name_plural = "Stats"
    icon = "fa-solid fa-chart-simple"
    column_list = [Stat.id, Stat.label, Stat.value, Stat.suffix]


for view in (
    CourseAdmin,
    CourseScheduleAdmin,
    CourseFAQAdmin,
    EventAdmin,
    JobAdmin,
    BlogPostAdmin,
    BlogHighlightAdmin,
    QuizAdmin,
    InterviewGuideAdmin,
    TestimonialAdmin,
    PricingPlanAdmin,
    WeeklyModuleAdmin,
    AlumniStoryAdmin,
    BootcampFAQAdmin,
    StatAdmin,
):
    admin.add_view(view)
