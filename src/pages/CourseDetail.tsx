import { useParams, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  CheckCircle,
  Calendar,
  Clock,
  MapPin,
  User,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useState } from "react";
import { useFetch } from "@/hooks/useFetch";
import { LoadingState, ErrorState } from "@/components/FetchState";

interface CourseSchedule {
  date: string;
  time: string;
  price: string;
  originalPrice: string;
  mode: string;
  instructor: string;
}

interface CourseFAQ {
  question: string;
  answer: string;
}

interface ApiCourse {
  id: string;
  title: string;
  shortTitle: string;
  category: string;
  badge: string;
  description: string;
  overview: string;
  keyFeatures: string[];
  courseContent: string[];
  whoShouldAttend: string[];
  schedules: CourseSchedule[];
  faqs: CourseFAQ[];
}

const tabs = [
  "Overview",
  "Course Content",
  "Who Should Attend",
  "FAQ",
] as const;

const CourseDetail = () => {
  const { id } = useParams<{ id: string }>();
  const { data: courses, loading, error } = useFetch<ApiCourse[]>("courses");
  const sortedCourses = [...(courses ?? [])].sort((a, b) =>
    ((a as any).display_order ?? (a as any).displayOrder ?? 0) -
    ((b as any).display_order ?? (b as any).displayOrder ?? 0) ||
    a.title.localeCompare(b.title),
  );
  const course = sortedCourses.find((c) => c.id === id);
  const [activeTab, setActiveTab] = useState<(typeof tabs)[number]>("Overview");
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  if (loading) {
    return (
      <div className="py-32">
        <LoadingState label="Loading course…" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-32">
        <ErrorState message="We couldn't load this course right now. Please try again later." />
      </div>
    );
  }

  if (!course) {
    return (
      <div className="py-32 text-center">
        <h1 className="font-heading text-3xl font-bold text-foreground mb-4">
          Course Not Found
        </h1>
        <Link to="/" className="text-secondary hover:underline font-heading">
          ← Back to Home
        </Link>
      </div>
    );
  }

  const related = sortedCourses
    .filter((c) => c.category === course.category && c.id !== course.id)
    .slice(0, 3);

  return (
    <>
      {/* Hero */}
      <section className="bg-primary py-16 md:py-24">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl">
            <Badge className="bg-secondary text-secondary-foreground font-heading mb-4">
              {course.badge}
            </Badge>
            <h1 className="font-heading font-bold text-3xl md:text-5xl text-primary-foreground mb-6">
              {course.title}
            </h1>
            <p className="text-primary-foreground/80 text-lg mb-8 font-body leading-relaxed">
              {course.description}
            </p>
            <ul className="space-y-3 mb-8">
              {course.keyFeatures.slice(0, 5).map((f) => (
                <li
                  key={f}
                  className="flex items-start gap-3 text-primary-foreground/90"
                >
                  <CheckCircle className="h-5 w-5 text-secondary shrink-0 mt-0.5" />
                  <span className="font-body">{f}</span>
                </li>
              ))}
            </ul>
            <div className="flex flex-wrap gap-4">
              <Button
                size="lg"
                variant="secondary"
                className="font-heading font-semibold"
              >
                Enroll Now
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="font-heading font-semibold !bg-transparent !text-white !border-white hover:!bg-white/10"
              >
                Download Brochure
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Upcoming Schedules */}
      <section className="py-16 bg-background">
        <div className="container mx-auto px-4">
          <h2 className="font-heading font-bold text-2xl md:text-3xl text-foreground mb-8">
            Upcoming Schedules
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {course.schedules.map((s, i) => (
              <div
                key={i}
                className="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex flex-wrap gap-4 mb-4">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Calendar className="h-4 w-4" />
                    <span className="font-body text-sm">{s.date}</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Clock className="h-4 w-4" />
                    <span className="font-body text-sm">{s.time}</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <MapPin className="h-4 w-4" />
                    <span className="font-body text-sm">{s.mode}</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <User className="h-4 w-4" />
                    <span className="font-body text-sm">{s.instructor}</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-muted-foreground line-through text-sm font-body mr-2">
                      {s.originalPrice}
                    </span>
                    <span className="font-heading font-bold text-xl text-foreground">
                      {s.price}
                    </span>
                  </div>
                  <Button
                    variant="secondary"
                    className="font-heading font-semibold"
                  >
                    Enroll Now
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tabs */}
      <section className="py-16 bg-muted">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap gap-2 mb-8 border-b border-border">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 font-heading font-semibold text-sm transition-colors border-b-2 -mb-px ${
                  activeTab === tab
                    ? "border-secondary text-secondary"
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="bg-card rounded-xl p-8 shadow-sm border border-border">
            {activeTab === "Overview" && (
              <div>
                <div className="prose max-w-none font-body text-muted-foreground leading-relaxed whitespace-pre-line mb-8">
                  {course.overview}
                </div>
                <h3 className="font-heading font-bold text-xl text-foreground mb-4">
                  Key Features
                </h3>
                <div className="grid sm:grid-cols-2 gap-3">
                  {course.keyFeatures.map((f) => (
                    <div key={f} className="flex items-start gap-3">
                      <CheckCircle className="h-5 w-5 text-secondary shrink-0 mt-0.5" />
                      <span className="font-body text-muted-foreground">
                        {f}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "Course Content" && (
              <ul className="space-y-3">
                {course.courseContent.map((item) => (
                  <li key={item} className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-secondary shrink-0 mt-0.5" />
                    <span className="font-body text-muted-foreground">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            )}

            {activeTab === "Who Should Attend" && (
              <ul className="space-y-3">
                {course.whoShouldAttend.map((item) => (
                  <li key={item} className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-secondary shrink-0 mt-0.5" />
                    <span className="font-body text-muted-foreground">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            )}

            {activeTab === "FAQ" && (
              <div className="space-y-4">
                {course.faqs.map((item, i) => (
                  <div key={i} className="border border-border rounded-lg">
                    <button
                      onClick={() => setOpenFaq(openFaq === i ? null : i)}
                      className="w-full flex items-center justify-between p-4 font-heading font-semibold text-foreground text-left"
                    >
                      {item.question}
                      {openFaq === i ? (
                        <ChevronUp className="h-5 w-5 text-secondary" />
                      ) : (
                        <ChevronDown className="h-5 w-5 text-muted-foreground" />
                      )}
                    </button>
                    {openFaq === i && (
                      <div className="px-4 pb-4 font-body text-muted-foreground">
                        {item.answer}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Related Courses */}
      {related.length > 0 && (
        <section className="py-16 bg-background">
          <div className="container mx-auto px-4">
            <h2 className="font-heading font-bold text-2xl md:text-3xl text-foreground mb-8">
              Explore Other Courses
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {related.map((c) => (
                <Link
                  key={c.id}
                  to={`/courses/${c.id}`}
                  className="bg-card rounded-xl p-6 border border-border shadow-sm hover:shadow-lg transition-shadow group"
                >
                  <Badge className="bg-secondary text-secondary-foreground font-heading text-xs mb-3">
                    {c.badge}
                  </Badge>
                  <h3 className="font-heading font-semibold text-foreground group-hover:text-secondary transition-colors">
                    {c.title}
                  </h3>
                  <p className="text-sm text-muted-foreground mt-2 font-body line-clamp-2">
                    {c.description}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}
    </>
  );
};

export default CourseDetail;
