"""Seed the database with initial content mirrored from the React frontend's ``src/data``.

Run once (or any time) with:
    python seed.py

Each section is only populated when its table is empty, so re-running the
script will not create duplicates.
"""

from datetime import date

from database import Base, SessionLocal, engine
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

# Ensure tables exist before we try to write to them.
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
COURSES = [
    {
        "id": "psm-1",
        "title": "Professional Scrum Master I",
        "short_title": "PSM I",
        "category": "scrum-master",
        "badge": "Best Seller",
        "description": "Experience 100% confidence in exceeding your expectations, supported by a remarkable 5/5 rating for our online Agile & Scrum training.",
        "overview": "The Professional Scrum Master (PSM I) course is a dynamic and engaging learning experience designed to provide students with a comprehensive understanding of Professional Scrum and the crucial role of the Scrum Master within Agile teams.",
        "key_features": [
            "2-day virtual classroom training",
            "Trained by an experienced PST",
            "PSM-I exam fees included",
            "14 SEUs and PDUs included",
            "Certification Body: Scrum.org",
        ],
        "course_content": [
            "Help Scrum Teams deliver value to their organization",
            "Understand the theory and principles behind Scrum and empiricism",
            "Understand uncertainty and complexity in product delivery",
            "Learn what Done means and why it is crucial to transparency",
        ],
        "who_should_attend": [
            "Practitioners interested in starting a career as a Scrum Master",
            "Scrum Masters, Agile/Scrum Coaches and consultants looking to improve their use of Scrum",
            "Anyone involved in product delivery using Scrum",
        ],
        "schedules": [
            {"date": "Mar 14th - 15th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹18,000", "original_price": "₹21,000", "mode": "Online", "instructor": "Expert Trainer"},
            {"date": "Mar 28th - 29th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹18,000", "original_price": "₹21,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "How many attempts do I get for the exam?", "answer": "Two attempts. Participants who score below 85% within 14 days are granted a 2nd attempt at no additional cost."},
            {"question": "Does my PSM certificate expire?", "answer": "Your certificate is lifelong and does not require any additional payments or renewals."},
        ],
    },
    {
        "id": "SC-AI",
        "title": "Scrum Master with AI",
        "short_title": "SC -AI",
        "category": "scrum-master",
        "badge": "Advanced",
        "description": "Future ready scrum master by combining Agile expertise with the power of Artificial Intelligence",
        "overview": "The Professional Scrum Master II (PSM II) course is designed for Scrum Masters who want to deepen their knowledge and skills, focusing on the Scrum Master as a servant-leader.",
        "key_features": ["100% Live Interactive Sessions", "Advanced facilitation techniques", "Real-Time Projects", "Lifetime Learning Resources", "Personalized Mentorship"],
        "course_content": ["Advanced Scrum Master stances", "Facilitating complex team dynamics", "Organizational change management", "Scaling Scrum", "Advanced coaching techniques"],
        "who_should_attend": ["Experienced Scrum Masters", "Agile Coaches", "Team leads transitioning to Scrum"],
        "schedules": [
            {"date": "Apr 11th - 12th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹30,000", "original_price": "₹40,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Do I need PSM I to take this course?", "answer": "While not required, having PSM I certification or equivalent experience is strongly recommended."},
        ],
    },
    {
        "id": "psm-ai",
        "title": "Professional Scrum Master™ - AI Essentials",
        "short_title": "PSM-AI",
        "category": "scrum-master",
        "badge": "New",
        "description": "Learn how to leverage AI tools and techniques within the Scrum framework to enhance team productivity.",
        "overview": "This cutting-edge course combines Professional Scrum with AI essentials, teaching Scrum Masters how to integrate AI tools into their workflows for enhanced team performance.",
        "key_features": ["AI tools for Scrum Masters", "AI-Integrated Agile Learning", "Hands-on workshops"],
        "course_content": ["AI fundamentals for Agile teams", "Using AI in Sprint Planning", "AI-powered retrospectives", "Data-driven decision making"],
        "who_should_attend": ["Scrum Masters wanting to leverage AI", "Tech leads", "Product teams"],
        "schedules": [
            {"date": "Apr 25th - 26th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹22,000", "original_price": "₹26,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Do I need AI experience?", "answer": "No prior AI experience is needed. The course covers fundamentals."},
        ],
    },
    {
        "id": "pspo-1",
        "title": "Professional Scrum Product Owner I",
        "short_title": "PSPO I",
        "category": "product-owner",
        "badge": "Best Seller",
        "description": "Master the Product Owner role and learn to maximize the value delivered by Scrum Teams.",
        "overview": "The Professional Scrum Product Owner (PSPO I) course focuses on the critical role of the Product Owner in the Scrum framework.",
        "key_features": ["2-day virtual classroom training", "PSPO-I exam fees included", "Product backlog management", "Stakeholder engagement techniques", "1:1 coaching"],
        "course_content": ["Agile Product Management", "Product Backlog Management", "Stakeholder Management", "Release Planning", "Value-driven development"],
        "who_should_attend": ["Aspiring Product Owners", "Business Analysts", "Product Managers", "Entrepreneurs"],
        "schedules": [
            {"date": "Mar 21st - 22nd, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹18,000", "original_price": "₹21,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Is this course suitable for beginners?", "answer": "Yes, this course is designed for anyone looking to understand and excel in the Product Owner role."},
        ],
    },
    {
        "id": "pspo-2",
        "title": "Advanced Professional Scrum Product Owner II",
        "short_title": "PSPO II",
        "category": "product-owner",
        "badge": "Advanced",
        "description": "Advance your Product Owner skills with deeper product management and stakeholder strategies.",
        "overview": "PSPO II is an advanced course for experienced Product Owners who want to grow their skills in product management, stakeholder engagement, and value delivery.",
        "key_features": ["Advanced product strategies", "PSPO-II exam included", "Complex stakeholder management", "Scaling product ownership"],
        "course_content": ["Advanced product vision", "Product strategy & roadmapping", "Evidence-based management", "Complex stakeholder landscapes"],
        "who_should_attend": ["Experienced Product Owners", "Senior Product Managers", "Product leaders"],
        "schedules": [
            {"date": "May 2nd - 3rd, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹25,000", "original_price": "₹30,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Prerequisites?", "answer": "PSPO I or equivalent experience recommended."},
        ],
    },
    {
        "id": "pspo-ai",
        "title": "Professional Scrum Product Owner™ - AI Essentials",
        "short_title": "PSPO-AI",
        "category": "product-owner",
        "badge": "New",
        "description": "Integrate AI into product ownership for smarter backlog management and data-driven decisions.",
        "overview": "This course teaches Product Owners how to leverage AI for better product decisions, backlog prioritization, and stakeholder communication.",
        "key_features": ["AI for product decisions", "Data-driven prioritization", "Exam included", "Practical workshops"],
        "course_content": ["AI in product management", "AI-powered analytics", "Smart backlog management", "Predictive planning"],
        "who_should_attend": ["Product Owners", "Product Managers", "Business leaders"],
        "schedules": [
            {"date": "May 16th - 17th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹22,000", "original_price": "₹26,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "AI background needed?", "answer": "No, the course starts from fundamentals."},
        ],
    },
    {
        "id": "icp-acc",
        "title": "ICAgile Certified Professional - Agile Coaching (ICP-ACC)",
        "short_title": "ICP-ACC",
        "category": "agile-coaching",
        "badge": "Popular",
        "description": "Become a certified Agile Coach with ICAgile's comprehensive coaching certification program.",
        "overview": "The ICP-ACC certification course provides a deep understanding of the Agile coaching competencies, including professional coaching skills, mentoring, and facilitation techniques.",
        "key_features": ["ICAgile certification included", "Professional coaching skills", "Mentoring frameworks", "Team facilitation techniques", "Organizational change"],
        "course_content": ["Agile coaching mindset", "Professional coaching skills", "Mentoring vs Coaching", "Team dynamics", "Conflict resolution", "Organizational coaching"],
        "who_should_attend": ["Aspiring Agile Coaches", "Scrum Masters wanting coaching skills", "Leaders driving Agile transformation"],
        "schedules": [
            {"date": "Apr 4th - 5th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹35,000", "original_price": "₹40,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Is this recognized globally?", "answer": "Yes, ICAgile certifications are recognized worldwide."},
        ],
    },
    {
        "id": "leading-safe",
        "title": "Leading SAFe Course",
        "short_title": "SA",
        "category": "safe",
        "badge": "Trending",
        "description": "Learn to lead a Lean-Agile enterprise by leveraging the Scaled Agile Framework® (SAFe®).",
        "overview": "Leading SAFe provides the principles and practices of the Scaled Agile Framework to drive Lean-Agile transformation at enterprise scale.",
        "key_features": ["SAFe Agilist certification exam", "Enterprise Agile transformation", "Lean-Agile leadership", "PI Planning facilitation", "Value stream mapping"],
        "course_content": ["SAFe principles", "Lean-Agile mindset", "PI Planning", "Agile Release Trains", "Value Streams", "Lean Portfolio Management"],
        "who_should_attend": ["Executives and leaders", "Managers", "Consultants", "Agile coaches scaling Agile"],
        "schedules": [
            {"date": "Mar 28th - 29th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹30,000", "original_price": "₹35,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "What certification do I receive?", "answer": "You'll be eligible for the SAFe® Agilist (SA) certification."},
        ],
    },
    {
        "id": "ssm",
        "title": "SAFe® Scrum Master Certification (SSM)",
        "short_title": "SSM",
        "category": "safe",
        "badge": "Popular",
        "description": "Become a certified SAFe® Scrum Master and learn to facilitate Agile team events at scale.",
        "overview": "The SAFe® Scrum Master course equips attendees with the skills to facilitate Scrum events within a SAFe® environment, coaching teams, and enabling value delivery at the program level.",
        "key_features": ["Live virtual training by Certified SPCs", "Case studies, simulations & practical exercises", "SAFe® Exam + 1-Year Community Access", "Earn 16 PDUs & SEUs"],
        "course_content": ["SAFe Scrum Master role", "Facilitating iteration execution", "Coaching the Agile team", "Supporting PI Planning"],
        "who_should_attend": ["Scrum Masters in SAFe environments", "Team leads", "Agile practitioners scaling"],
        "schedules": [
            {"date": "Apr 18th - 19th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹24,999", "original_price": "₹33,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Difference from PSM?", "answer": "SSM focuses on Scrum within the SAFe® enterprise framework, while PSM is framework-agnostic."},
        ],
    },
    {
        "id": "safe-popm",
        "title": "SAFe Product Owner Product Manager (POPM)",
        "short_title": "POPM",
        "category": "safe",
        "badge": "Trending",
        "description": "Master the dual role of Product Owner and Product Manager within the SAFe® framework.",
        "overview": "Learn how to effectively perform the Product Owner and Product Manager roles within a SAFe® Lean-Agile enterprise.",
        "key_features": ["POPM certification exam", "Dual role mastery", "SAFe product management", "Backlog management at scale"],
        "course_content": ["SAFe PO/PM roles", "Writing epics and features", "PI Planning from PO perspective", "Customer centricity"],
        "who_should_attend": ["Product Owners", "Product Managers", "Business Analysts in SAFe"],
        "schedules": [
            {"date": "May 9th - 10th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹28,000", "original_price": "₹33,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "Is SAFe experience required?", "answer": "Basic understanding of Agile is recommended but not mandatory."},
        ],
    },
    {
        "id": "prince2",
        "title": "Prince2 Foundation Practitioner Certification",
        "short_title": "PRINCE2",
        "category": "project-management",
        "badge": "Classic",
        "description": "Master the PRINCE2 methodology for structured project management excellence.",
        "overview": "PRINCE2 (Projects IN Controlled Environments) is a structured project management method widely used globally. This course covers both Foundation and Practitioner levels.",
        "key_features": ["Foundation & Practitioner exams", "Globally recognized certification", "Structured project management", "Real-world case studies"],
        "course_content": ["PRINCE2 principles", "PRINCE2 themes", "PRINCE2 processes", "Tailoring PRINCE2", "Business case development"],
        "who_should_attend": ["Project Managers", "Team leads", "Anyone managing projects"],
        "schedules": [
            {"date": "Apr 25th - 27th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹32,000", "original_price": "₹38,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "How many days is this course?", "answer": "This is a 3-day intensive course covering both Foundation and Practitioner levels."},
        ],
    },
    {
        "id": "pmp",
        "title": "Project Management Professional (PMP)",
        "short_title": "PMP",
        "category": "project-management",
        "badge": "Best Seller",
        "description": "Earn the globally recognized PMP® certification and advance your project management career.",
        "overview": "The PMP® certification is the gold standard in project management. This comprehensive course prepares you for the PMP exam while equipping you with practical project management skills.",
        "key_features": ["35 contact hours (PDUs)", "PMP exam preparation", "Practice exams included", "Real-world scenarios", "Study materials provided"],
        "course_content": ["Project initiation & planning", "Project execution", "Monitoring & controlling", "Agile & hybrid approaches", "Stakeholder management", "Risk management"],
        "who_should_attend": ["Experienced project managers", "Program managers", "Team leads seeking PMP"],
        "schedules": [
            {"date": "May 2nd - 4th, 2026", "time": "9:30 AM - 4:30 PM IST", "price": "₹35,000", "original_price": "₹42,000", "mode": "Online", "instructor": "Expert Trainer"},
        ],
        "faqs": [
            {"question": "What are the PMP prerequisites?", "answer": "A 4-year degree with 3 years of project management experience, or a high school diploma with 5 years of experience."},
        ],
    },
]

EVENTS = [
    {"id": "navigating-pm-careers", "title": "Navigating Careers in Product Management", "description": "Join us for a LIVE session with industry leaders as we deep-dive into the career journey of a PM — the challenges, the skills, and the roadmap to success.", "date": "April 12, 2026", "time": "08:00 PM – 09:00 PM IST", "location": "Online (Zoom)", "type": "upcoming", "image": "/placeholder.svg", "tags": ["Webinar", "Product Management"], "registration_link": "#"},
    {"id": "scrum-master-workshop", "title": "Scrum Master Certification Prep Workshop", "description": "A hands-on workshop to prepare for the PSM-I certification. Practice with real exam questions, learn key Scrum concepts, and get tips from certified trainers.", "date": "April 26, 2026", "time": "10:00 AM – 12:00 PM IST", "location": "Online (Zoom)", "type": "upcoming", "image": "/placeholder.svg", "tags": ["Workshop", "Scrum"], "registration_link": "#"},
    {"id": "agile-transformation", "title": "Agile Transformation: Leadership Perspectives", "description": "Hear from senior leaders who have driven enterprise-level agile transformations. Learn strategies, pitfalls to avoid, and how to build an agile culture.", "date": "May 10, 2026", "time": "07:00 PM – 08:30 PM IST", "location": "Online (Zoom)", "type": "upcoming", "image": "/placeholder.svg", "tags": ["Webinar", "Leadership"], "registration_link": "#"},
    {"id": "safe-deep-dive", "title": "SAFe Framework Deep Dive", "description": "An in-depth session covering the Scaled Agile Framework (SAFe) — roles, events, artifacts, and how to implement SAFe in large organisations.", "date": "February 15, 2026", "time": "06:00 PM – 07:30 PM IST", "location": "Online (Zoom)", "type": "past", "image": "/placeholder.svg", "tags": ["Webinar", "SAFe"], "registration_link": "#", "recording_link": "#"},
    {"id": "kanban-best-practices", "title": "Kanban Methodology: Best Practices", "description": "Explore how Kanban can streamline your team's workflow. Covers WIP limits, flow metrics, and real-world case studies from successful Kanban adoptions.", "date": "January 22, 2026", "time": "08:00 PM – 09:00 PM IST", "location": "Online (Zoom)", "type": "past", "image": "/placeholder.svg", "tags": ["Webinar", "Kanban"], "registration_link": "#", "recording_link": "#"},
    {"id": "sprint-planning-retro", "title": "Sprint Planning & Retrospective Workshop", "description": "Master the art of sprint planning and running effective retrospectives. Interactive exercises and templates included for your team to use immediately.", "date": "December 10, 2025", "time": "10:00 AM – 11:30 AM IST", "location": "Online (Zoom)", "type": "past", "image": "/placeholder.svg", "tags": ["Workshop", "Scrum"], "registration_link": "#", "recording_link": "#"},
]

JOBS = [
    {"title": "Agile Coach Remote master", "location": "Remote", "type": "Full-Time", "department": "Consulting", "description": "Guide enterprise teams through Agile transformations and coach leadership on best practices.", "link": "#"},
    {"title": "Scrum Master", "location": "Bangalore, India", "type": "Full-Time", "department": "Delivery", "description": "Facilitate Scrum ceremonies, remove impediments, and drive continuous improvement across squads.", "link": "#"},
    {"title": "Product Owner", "location": "Hyderabad, India", "type": "Full-Time", "department": "Product", "description": "Own the product backlog, define user stories, and collaborate with stakeholders to maximize value.", "link": "#"},
    {"title": "DevOps Engineer", "location": "Remote", "type": "Contract", "department": "Engineering", "description": "Build and maintain CI/CD pipelines, automate infrastructure, and ensure high availability.", "link": "#"},
    {"title": "Corporate Trainer – Agile & SAFe", "location": "Mumbai, India", "type": "Full-Time", "department": "Training", "description": "Deliver instructor-led training sessions on Agile, Scrum, and SAFe frameworks to corporate clients.", "link": "#"},
    {"title": "Business Development Manager", "location": "Remote", "type": "Full-Time", "department": "Sales", "description": "Drive new client acquisition, manage partnerships, and grow the training business pipeline.", "link": "#"},
]

BLOG_HIGHLIGHTS = [
    {"title": "Why Agile Teams That Embrace AI Will Lead the Future???", "excerpt": "Organizations adopting AI-powered agile practices are seeing unprecedented improvements in delivery speed...", "image": "/placeholder.svg", "link": "#"},
    {"title": "The Role of AI in Modern Project Management", "excerpt": "Artificial intelligence is reshaping how teams plan, execute, and deliver projects at scale...", "image": "/placeholder.svg", "link": "#"},
    {"title": "5 Metrics Every Scrum Team Should Track in 2026", "excerpt": "Data-driven scrum teams outperform their peers. Here are the key metrics that matter most...", "image": "/placeholder.svg", "link": "#"},
]

BLOG_POSTS = [
    {"slug": "understanding-definition-of-done", "title": "Understanding the Definition of Done (DoD) in Scrum", "excerpt": "One of the most important concepts every Scrum Master should understand is the Definition of Done (DoD).", "content": "The Definition of Done is a shared agreement within the Scrum Team that determines when a Product Backlog Item or Increment is truly complete. It represents the team's quality standards and ensures every completed feature is ready for release.", "image": "/placeholder.svg", "author": "Chandan Kumar", "date": date(2026, 3, 1), "category": "Scrum Master", "read_time": "10 min read"},
    {"slug": "choosing-a-right-career-scrum-master", "title": "Choosing a right career - Scrum Master", "excerpt": "Choosing the right career path isn't always straightforward — and if you've been wondering whether Agile is worth exploring, you've landed in the right place.", "content": "At its core, Scrum is a lightweight framework designed to help teams tackle complex problems through small, adaptive steps rather than one big rigid plan. It's most commonly associated with software development, but its real strength lies in flexibility.", "image": "/placeholder.svg", "author": "Chandan Kumar", "date": date(2026, 2, 22), "category": "Scrum Practices", "read_time": "4 min read"},
]

QUIZZES = [
    {"id": "psm-1", "title": "PSM-I Practice Assessment", "short_title": "PSM I", "description": "Evaluate your knowledge and preparedness for the Professional Scrum Master (PSM-I) exam with 80 practice questions.", "question_count": 80, "duration": "60 minutes", "icon": "ClipboardCheck", "link": "#"},
    {"id": "psm-a", "title": "PSM-A Practice Assessment", "short_title": "PSM II", "description": "Evaluate your advanced Scrum Master knowledge and preparedness for the PSM-A exam with 30 in-depth questions.", "question_count": 30, "duration": "90 minutes", "icon": "Award", "link": "#"},
    {"id": "pspo-1", "title": "PSPO-I Practice Assessment", "short_title": "PSPO I", "description": "Test your Product Owner fundamentals and preparedness for the PSPO-I certification exam.", "question_count": 80, "duration": "60 minutes", "icon": "Target", "link": "#"},
    {"id": "pspo-2", "title": "PSPO-II Practice Assessment", "short_title": "PSPO II", "description": "Challenge your advanced Product Owner skills and readiness for the PSPO-II certification exam.", "question_count": 40, "duration": "60 minutes", "icon": "BarChart3", "link": "#"},
    {"id": "safe-sm", "title": "SAFe Scrum Master Practice Assessment", "short_title": "SAFe SM", "description": "Evaluate your knowledge and preparedness for the SAFe Scrum Master certification exam.", "question_count": 45, "duration": "90 minutes", "icon": "Shield", "link": "#"},
    {"id": "agile-fundamentals", "title": "Agile Fundamentals Assessment", "short_title": "Agile", "description": "Test your understanding of core Agile principles, the Agile Manifesto, and common frameworks used in modern teams.", "question_count": 50, "duration": "45 minutes", "icon": "Users", "link": "#"},
]

INTERVIEW_GUIDES = [
    {"id": "scrum-master-guide", "title": "Scrum Master Interview Guide", "description": "Complete preparation guide covering Scrum framework, facilitation techniques, team dynamics, and real-world scenarios.", "category": "scrum-master", "coming_soon": False},
    {"id": "estimation-guide", "title": "Estimation Interview Guide", "description": "A practical interview guide using storytelling answers to address common estimation challenges like team disagreements and building team alignment.", "category": "scrum-master", "coming_soon": False},
    {"id": "team-collaboration-guide", "title": "Team Collaboration Interview Guide", "description": "A practical interview guide addressing common team collaboration challenges like resistance to cross-training and building true team ownership.", "category": "scrum-master", "coming_soon": False},
    {"id": "hybrid-teams-guide", "title": "Collaboration in Hybrid Teams Guide", "description": "Turn hybrid chaos into connection. Master 10 real interview questions on hybrid collaboration with refined, storytelling answers.", "category": "scrum-master", "coming_soon": False},
    {"id": "saying-not-yet", "title": "How to Say 'Not Yet' Without Saying No", "description": "Practical questions that test how Scrum Masters and Agile Coaches handle leadership-set deadlines before estimation.", "category": "agile-coach", "coming_soon": False},
    {"id": "remote-scrum-master", "title": "Remote Scrum Master Visibility", "description": "This guide dives into real challenges faced by remote Scrum Masters and how to turn invisibility into influence.", "category": "scrum-master", "coming_soon": False},
    {"id": "enterprise-scale", "title": "Scrum Masters in Enterprise-Scale Agility", "description": "10 real-world scenarios where Scrum Masters navigate scaled agility — balancing autonomy with alignment and influencing without authority.", "category": "scrum-master", "coming_soon": False},
    {"id": "product-owner-guide", "title": "Product Owner Interview Guide", "description": "Comprehensive guide covering product vision, backlog management, stakeholder communication, and value delivery strategies.", "category": "product-owner", "coming_soon": True},
    {"id": "agile-coach-guide", "title": "Agile Coach Interview Guide", "description": "Advanced guide for coaching roles covering organisational transformation, mentoring teams, and driving cultural change.", "category": "agile-coach", "coming_soon": True},
]

TESTIMONIALS = [
    {"name": "Chakri Nutalapati", "role": "Scrum Master at TechCorp", "text": "Chandan Kumar's guidance as a Scrum Master coach has been instrumental in enhancing my understanding of Agile practices. I highly recommend his coaching for anyone looking to excel in Agile methodologies."},
    {"name": "Kapil Shah", "role": "Product Owner at FinServe", "text": "The training perfectly balances theory and practical application. If you want to go into a scrum master's job, I strongly suggest taking Chandan's mentorship."},
    {"name": "Swati Singh", "role": "Agile Coach at StartupHub", "text": "Chandan sir helped me to secure a job as Scrum Master. He not only coached me but also guided me on how to self-study, identify mistakes, and work on improving them. I am grateful for everything."},
    {"name": "Chetan Chavan", "role": "Engineering Lead at CloudBase", "text": "He has the ability to simplify Agile concepts with relatable examples that resonate with everyone. His sessions are not only informative but engaging and interactive."},
]

STATS = [
    {"value": 3500, "suffix": "+", "label": "Students Trained"},
    {"value": 4, "suffix": ".8", "label": "Average Rating"},
    {"value": 25, "suffix": "+", "label": "Companies Trained"},
    {"value": 270, "suffix": "+", "label": "Trainings Delivered"},
]

PRICING_PLANS = [
    {"name": "Self-Learning Pack", "price": "₹9,999", "original_price": None, "type": "Self-Paced", "highlighted": False, "features": [
        {"text": "PDF Interview Questions", "included": True},
        {"text": "PDF Course Notes & Templates", "included": True},
        {"text": "Certificate of Completion", "included": True},
        {"text": "Live Project Work", "included": False},
        {"text": "Personal Feedback", "included": False},
        {"text": "Community Access", "included": False},
        {"text": "Free Future Batch Access", "included": False},
    ]},
    {"name": "Core Bootcamp", "price": "₹34,999", "original_price": None, "type": "Guided Learning", "highlighted": False, "features": [
        {"text": "30-Hr Live Project Bootcamp", "included": True},
        {"text": "6 Group Interview Sessions", "included": True},
        {"text": "PDF Notes + Study Resources", "included": True},
        {"text": "Certificate of Completion", "included": True},
        {"text": "Group Feedback Only", "included": True},
        {"text": "Limited Community Access", "included": False},
        {"text": "Free Future Batch Access", "included": False},
    ]},
    {"name": "Premium Bootcamp", "price": "₹38,599", "original_price": "₹45,999", "type": "Full Mentorship & Support", "highlighted": True, "features": [
        {"text": "30-Hr Live Project + Jira Execution", "included": True},
        {"text": "Individual Review of Assignments", "included": True},
        {"text": "6 Group + 2 Personal Interview Sessions", "included": True},
        {"text": "Lifetime Community Access", "included": True},
        {"text": "PDF Notes + Bonus Templates + Career Resources", "included": True},
        {"text": "PSM-I, PSPO-I, PSM-II Prep + Cert", "included": True},
        {"text": "Join Future Batches for Free", "included": True},
    ]},
]

WEEKLY_MODULES = [
    {"week": "Week 1", "title": "Product Strategy & Foundation", "topics": [
        "Career Branding & Networking — Optimizing LinkedIn and profiles to stand out to recruiters.",
        "Design Thinking & Discovery — Applying Design Thinking principles alongside AI prompts for rapid personas.",
        "Resume Building — Create ATS-friendly, keyword-optimized resumes with live expert review.",
        "Process Optimization — Utilizing AI to analyze Value Stream Maps and identify waste patterns.",
    ]},
    {"week": "Week 2", "title": "Operational Excellence", "topics": [
        "Conflict & Flow Management — Navigating interpersonal friction while optimizing Kanban flow.",
        "Metrics & Governance — Implementing essential metrics and management dashboards using Jira.",
        "Financial & Release Planning — Aligning project budgeting with realistic release timelines.",
        "Agile Maturity — Assessing team growth through Agile Maturity Models with AI-generated coaching roadmaps.",
    ]},
    {"week": "Week 3", "title": "Scaled Planning & Backlog Readiness", "topics": [
        "SAFe PI Preparation — Prioritizing Epics and creating a healthy, high-readiness ART backlog.",
        "PI Planning Execution — Conducting PI Planning events, crafting PI Objectives and the Program Board.",
        "Backlog Refinement — Leveraging AI to draft User Stories and Acceptance Criteria meeting DoR and DoD.",
        "Strategic Alignment — Synchronizing team objectives with the broader Program Board.",
    ]},
    {"week": "Week 4", "title": "Mastery of Execution & Growth", "topics": [
        "Risk & Dependency Management — Using AI to identify hidden dependencies and predict project risks.",
        "Feedback & Retrospectives — Sprint Reviews, Inspect & Adapt sessions, and data-driven Retrospectives.",
        "The Execution Cycle — Facilitating Sprint Planning, Daily Scrums, ART Syncs, and PI System Demos.",
        "Continuous Improvement — Observing anti-patterns and coaching teams toward high performance.",
    ]},
]

ALUMNI_STORIES = [
    {"name": "Rachit", "role": "Associate Manager", "company": "Tredence", "headline": "Landed a Role at Tredence", "quote": "Huge thanks to my coach for an impactful Scrum Master Bootcamp. It went beyond frameworks—real-world insights, mindset shifts, and lessons I could apply instantly."},
    {"name": "Nelson", "role": "Scrum Master", "company": "New Role", "headline": "Secured Scrum Master Role", "quote": "Recently attended a Scrum Bootcamp that turned out to be a real game-changer. It gave me practical insights that helped me crack my new role."},
    {"name": "Biswajit Rajkumar", "role": "Scrum Master", "company": "Top MNC", "headline": "Got Hired by a Top MNC", "quote": "I'm thrilled to share that I've now secured a Scrum Master role at a top MNC — a milestone made possible by expert mentorship during the Bootcamp."},
    {"name": "Gaurav", "role": "Senior Scrum Master", "company": "Netlink Software", "headline": "Started Role at Netlink", "quote": "It wasn't just a Scrum Master refresher—it gave me practical insights and confidence for my new role. Truly grateful for the mentorship and support!"},
]

BOOTCAMP_FAQS = [
    {"question": "What if I miss a session? How do I catch up?", "answer": "We have a built-in catch-up structure. Weekday sessions include a 30-minute catch-up slot, and weekend sessions repeat the same weekday topics so you can re-attend and stay aligned with the cohort."},
    {"question": "How does this bootcamp help with job placement?", "answer": "Our program transforms learning into real career opportunities through hands-on Scrum practice, live mock interviews with feedback, resume optimization, LinkedIn profile guidance, and access to our alumni and hiring manager network."},
    {"question": "How is the payment done?", "answer": "We offer a weekly installment plan — the total fee is split into 4 manageable weekly payments. A secure payment link is shared after enrollment."},
    {"question": "Do I need prior experience in Agile or Scrum?", "answer": "No prior experience needed! This is a structured, beginner-friendly cohort that guides you step by step from fundamentals to job-ready expertise."},
]


# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------
def seed():
    db = SessionLocal()
    created = []
    try:
        if db.query(Course).count() == 0:
            # Preserve the explicit author-defined ordering by adding a display_order
            # field based on the list position. This makes ordering deterministic
            # and editable via the admin dashboard (Course.display_order).
            for idx, item in enumerate(COURSES):
                item["display_order"] = idx

            for item in COURSES:
                schedules = item.pop("schedules", [])
                faqs = item.pop("faqs", [])
                course = Course(**item)
                course.schedules = [CourseSchedule(**s) for s in schedules]
                course.faqs = [CourseFAQ(**f) for f in faqs]
                db.add(course)
            created.append(f"courses ({len(COURSES)})")

        if db.query(Event).count() == 0:
            db.add_all([Event(**item) for item in EVENTS])
            created.append(f"events ({len(EVENTS)})")

        if db.query(Job).count() == 0:
            db.add_all([Job(**item) for item in JOBS])
            created.append(f"jobs ({len(JOBS)})")

        if db.query(BlogHighlight).count() == 0:
            db.add_all([BlogHighlight(**item) for item in BLOG_HIGHLIGHTS])
            created.append(f"blog_highlights ({len(BLOG_HIGHLIGHTS)})")

        if db.query(BlogPost).count() == 0:
            db.add_all([BlogPost(**item) for item in BLOG_POSTS])
            created.append(f"blog_posts ({len(BLOG_POSTS)})")

        if db.query(Quiz).count() == 0:
            db.add_all([Quiz(**item) for item in QUIZZES])
            created.append(f"quizzes ({len(QUIZZES)})")

        if db.query(InterviewGuide).count() == 0:
            db.add_all([InterviewGuide(**item) for item in INTERVIEW_GUIDES])
            created.append(f"interview_guides ({len(INTERVIEW_GUIDES)})")

        if db.query(Testimonial).count() == 0:
            db.add_all([Testimonial(**item) for item in TESTIMONIALS])
            created.append(f"testimonials ({len(TESTIMONIALS)})")

        if db.query(Stat).count() == 0:
            db.add_all([Stat(**item) for item in STATS])
            created.append(f"stats ({len(STATS)})")

        if db.query(PricingPlan).count() == 0:
            db.add_all([PricingPlan(**item) for item in PRICING_PLANS])
            created.append(f"pricing_plans ({len(PRICING_PLANS)})")

        if db.query(WeeklyModule).count() == 0:
            db.add_all([WeeklyModule(**item) for item in WEEKLY_MODULES])
            created.append(f"weekly_modules ({len(WEEKLY_MODULES)})")

        if db.query(AlumniStory).count() == 0:
            db.add_all([AlumniStory(**item) for item in ALUMNI_STORIES])
            created.append(f"alumni_stories ({len(ALUMNI_STORIES)})")

        if db.query(BootcampFAQ).count() == 0:
            db.add_all([BootcampFAQ(**item) for item in BOOTCAMP_FAQS])
            created.append(f"bootcamp_faqs ({len(BOOTCAMP_FAQS)})")

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    if created:
        print("Seeded: " + ", ".join(created))
    else:
        print("Nothing to seed — all tables already contain data.")


if __name__ == "__main__":
    seed()
