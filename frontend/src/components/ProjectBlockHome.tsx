import ProjectCard from "./ProjectCard";
import { useState, useRef, useLayoutEffect } from "react";
import gsap from "gsap";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
  topOffset?: number;
}

const CARDS_PER_CHUNK = 9;

const ProjectBlockHome: React.FC<ProjectBlockProps> = ({
  title,
  projects,
  topOffset = 0,
}) => {
  const [isCollapsed] = useState(false);
  const [visibleCount, setVisibleCount] = useState(CARDS_PER_CHUNK);

  const blockRef = useRef<HTMLDivElement>(null);
  const previousVisibleCount = useRef(CARDS_PER_CHUNK);

  const handleShowMore = () => {
    setVisibleCount((prev) =>
      Math.min(prev + CARDS_PER_CHUNK, projects.length)
    );
  };

  const hasMore = visibleCount < projects.length;

  useLayoutEffect(() => {
    if (!blockRef.current) return;
    if (visibleCount <= previousVisibleCount.current) return;

    const newCards = Array.from(
      blockRef.current.querySelectorAll<HTMLElement>(
        `[data-card-index]`
      )
    ).filter((el) => {
      const index = Number(el.dataset.cardIndex);
      return (
        index >= previousVisibleCount.current &&
        index < visibleCount
      );
    });

    if (newCards.length) {
      const ctx = gsap.context(() => {
        gsap.set(newCards, { opacity: 0, xPercent: 10 });
        gsap.to(newCards, {
          opacity: 1,
          xPercent: 0,
          duration: 1,
          stagger: 0.08,
          ease: "expo.out",
        });
      }, blockRef);

      previousVisibleCount.current = visibleCount;
      return () => ctx.revert();
    }

    previousVisibleCount.current = visibleCount;
  }, [visibleCount]);

  return (
    <div ref={blockRef} className="project-block relative z-0">
      <div
        className="sticky bg-color-bg z-20 py-3"
        style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}
      >
        <div className="flex gap-4 mb-3">
          <h2 className="text-title-2">{title}</h2>
        </div>

        <span className="block h-px w-full bg-color-1 opacity-50" />
      </div>

      <div
        className={`
          grid transition-[grid-template-rows,opacity,margin] duration-250 ease-in-out
          ${
            isCollapsed
              ? "grid-rows-[0fr] opacity-0 mb-0"
              : "grid-rows-[1fr] opacity-100 mb-24"
          }
        `}
      >
        <div className="overflow-hidden">
        <div className="flex flex-wrap gap-y-6 md:gap-y-8 -mx-0 md:-mx-3 lg:-mx-4">
            {projects.slice(0, visibleCount).map((project, index) => (
            <div
              key={project.id}
              data-card-index={index}
              className="
                w-full
                md:w-1/2
                lg:w-1/3
                px-0 md:px-3 lg:px-4
              "
            >
              <ProjectCard project={project} />
            </div>
          ))}
        </div>

        {hasMore && (
          <div className="pt-6">
            <button
              onClick={handleShowMore}
              className="
                h-8
                text-note-2
                underline
                cursor-pointer
                text-color-2
                hover:text-color-1
                transition-all
                duration-300
              "
            >
              Mostrar mais ({projects.length - visibleCount} restantes)
            </button>
          </div>
        )}
        </div>
      </div>
    </div>
  );
};

export default ProjectBlockHome;
