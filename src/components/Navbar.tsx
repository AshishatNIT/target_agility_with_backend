import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X, ChevronDown } from "lucide-react";
import { navItems, resourceItems } from "@/data/navbarData";
import { useFetch } from "@/hooks/useFetch";

interface NavCourse {
  id: string;
  title: string;
  shortTitle: string;
  displayOrder?: number;
}

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showCourses, setShowCourses] = useState(false);
  const [showResources, setShowResources] = useState(false);
  const [mobileCoursesOpen, setMobileCoursesOpen] = useState(false);
  const [mobileResourcesOpen, setMobileResourcesOpen] = useState(false);
  const { data } = useFetch<NavCourse[]>("courses");
  const courses = data ?? [];
  const sortedCourses = [...courses].sort((a, b) =>
    ((a as any).display_order ?? (a as any).displayOrder ?? 0) -
    ((b as any).display_order ?? (b as any).displayOrder ?? 0) ||
    a.title.localeCompare(b.title),
  );

  return (
    <nav className="bg-card shadow-sm sticky top-0 z-50">
      <div className="container mx-auto flex items-center justify-between px-4 py-4">
        <Link to="/" className="font-heading font-bold text-2xl text-primary">
          DigitalDimna
        </Link>

        <div className="hidden lg:flex items-center gap-8">
          {navItems.map((item) => {
            if (item.label === "Courses") {
              return (
                <div
                  key={item.label}
                  className="relative"
                  onMouseEnter={() => setShowCourses(true)}
                  onMouseLeave={() => setShowCourses(false)}
                >
                  <button className="flex items-center gap-1 font-heading font-medium text-sm text-foreground hover:text-secondary transition-colors">
                    {item.label}
                    <ChevronDown
                      className={`h-3.5 w-3.5 transition-transform ${showCourses ? "rotate-180" : ""}`}
                    />
                  </button>

                  {showCourses && (
                    <div className="absolute top-full left-1/2 -translate-x-1/2 pt-2 w-[800px]">
                      <div className="bg-card rounded-xl shadow-2xl border border-border p-6">
                        <h3 className="font-heading font-bold text-lg text-foreground mb-5 text-center">
                          Our Courses
                        </h3>
                        <div className="grid grid-cols-3 gap-x-6 gap-y-4">
                          {sortedCourses.map((course) => (
                            <Link
                              key={course.id}
                              to={`/courses/${course.id}`}
                              className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted transition-colors group"
                              onClick={() => setShowCourses(false)}
                            >
                              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                                <span className="font-heading font-bold text-xs text-primary leading-tight text-center">
                                  {course.shortTitle}
                                </span>
                              </div>
                              <span className="font-heading font-medium text-sm text-foreground group-hover:text-secondary transition-colors leading-snug">
                                {course.title}
                              </span>
                            </Link>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            }

            if (item.label === "Resources") {
              return (
                <div
                  key={item.label}
                  className="relative"
                  onMouseEnter={() => setShowResources(true)}
                  onMouseLeave={() => setShowResources(false)}
                >
                  <button className="flex items-center gap-1 font-heading font-medium text-sm text-foreground hover:text-secondary transition-colors">
                    {item.label}
                    <ChevronDown
                      className={`h-3.5 w-3.5 transition-transform ${showResources ? "rotate-180" : ""}`}
                    />
                  </button>

                  {showResources && (
                    <div className="absolute top-full left-1/2 -translate-x-1/2 pt-2 w-[500px]">
                      <div className="bg-card rounded-xl shadow-2xl border border-border p-6">
                        <h3 className="font-heading font-bold text-lg text-foreground mb-5 text-center">
                          Resources
                        </h3>
                        <div className="grid grid-cols-1 gap-3">
                          {resourceItems.map((res) => {
                            const Icon = res.icon;
                            const content = (
                              <>
                                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                                  <Icon className="h-5 w-5 text-primary" />
                                </div>
                                <div>
                                  <span className="font-heading font-medium text-sm text-foreground group-hover:text-secondary transition-colors block">
                                    {res.label}
                                  </span>
                                  <span className="text-xs text-muted-foreground leading-snug">
                                    {res.description}
                                  </span>
                                </div>
                              </>
                            );
                            const className =
                              "flex items-center gap-4 p-3 rounded-lg hover:bg-muted border border-transparent hover:border-border transition-all group";
                            return res.to.startsWith("/") ? (
                              <Link
                                key={res.label}
                                to={res.to}
                                className={className}
                                onClick={() => setShowResources(false)}
                              >
                                {content}
                              </Link>
                            ) : (
                              <a
                                key={res.label}
                                href={res.to}
                                className={className}
                                onClick={() => setShowResources(false)}
                              >
                                {content}
                              </a>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            }

            if (item.to.startsWith("/")) {
              return (
                <Link
                  key={item.label}
                  to={item.to}
                  className="flex items-center gap-1 font-heading font-medium text-sm text-foreground hover:text-secondary transition-colors"
                >
                  {item.label}
                </Link>
              );
            }

            return (
              <a
                key={item.label}
                href={item.to}
                className="flex items-center gap-1 font-heading font-medium text-sm text-foreground hover:text-secondary transition-colors"
              >
                {item.label}
                {item.hasDropdown && <ChevronDown className="h-3.5 w-3.5" />}
              </a>
            );
          })}
        </div>

        <button className="lg:hidden" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="lg:hidden border-t border-border px-4 pb-4">
          {navItems.map((item) => {
            if (item.label === "Courses") {
              return (
                <div key={item.label}>
                  <button
                    onClick={() => setMobileCoursesOpen(!mobileCoursesOpen)}
                    className="w-full flex items-center justify-between py-3 font-heading font-medium text-sm text-foreground border-b border-border"
                  >
                    Courses
                    <ChevronDown
                      className={`h-4 w-4 transition-transform ${mobileCoursesOpen ? "rotate-180" : ""}`}
                    />
                  </button>
                  {mobileCoursesOpen && (
                    <div className="pl-4 pb-2">
                      {sortedCourses.map((course) => (
                        <Link
                          key={course.id}
                          to={`/courses/${course.id}`}
                          onClick={() => {
                            setIsOpen(false);
                            setMobileCoursesOpen(false);
                          }}
                          className="block py-2 font-heading text-sm text-muted-foreground hover:text-secondary transition-colors"
                        >
                          {course.title}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              );
            }

            if (item.label === "Resources") {
              return (
                <div key={item.label}>
                  <button
                    onClick={() => setMobileResourcesOpen(!mobileResourcesOpen)}
                    className="w-full flex items-center justify-between py-3 font-heading font-medium text-sm text-foreground border-b border-border"
                  >
                    Resources
                    <ChevronDown
                      className={`h-4 w-4 transition-transform ${mobileResourcesOpen ? "rotate-180" : ""}`}
                    />
                  </button>
                  {mobileResourcesOpen && (
                    <div className="pl-4 pb-2">
                      {resourceItems.map((res) =>
                        res.to.startsWith("/") ? (
                          <Link
                            key={res.label}
                            to={res.to}
                            onClick={() => {
                              setIsOpen(false);
                              setMobileResourcesOpen(false);
                            }}
                            className="block py-2 font-heading text-sm text-muted-foreground hover:text-secondary transition-colors"
                          >
                            {res.label}
                          </Link>
                        ) : (
                          <a
                            key={res.label}
                            href={res.to}
                            onClick={() => {
                              setIsOpen(false);
                              setMobileResourcesOpen(false);
                            }}
                            className="block py-2 font-heading text-sm text-muted-foreground hover:text-secondary transition-colors"
                          >
                            {res.label}
                          </a>
                        ),
                      )}
                    </div>
                  )}
                </div>
              );
            }

            if (item.to.startsWith("/")) {
              return (
                <Link
                  key={item.label}
                  to={item.to}
                  onClick={() => setIsOpen(false)}
                  className="block py-3 font-heading font-medium text-sm text-foreground hover:text-secondary transition-colors border-b border-border last:border-0"
                >
                  {item.label}
                </Link>
              );
            }

            return (
              <a
                key={item.label}
                href={item.to}
                className="block py-3 font-heading font-medium text-sm text-foreground hover:text-secondary transition-colors border-b border-border last:border-0"
              >
                {item.label}
              </a>
            );
          })}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
