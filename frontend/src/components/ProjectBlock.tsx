import ProjectCard from "./ProjectCard";
import { MdArrowBackIosNew } from "react-icons/md";
import { useState, useRef } from "react";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
  topOffset?: number;
}

const CARDS_PER_CHUNK = 10;

const ProjectBlock: React.FC<ProjectBlockProps> = ({
  title,
  projects,
  topOffset = 0,
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [visibleCount, setVisibleCount] = useState(CARDS_PER_CHUNK);
  const blockRef = useRef<HTMLDivElement>(null);

  const handleToggle = () => {
    setIsCollapsed((prev) => !prev);
  };

  const handleShowMore = () => {
    const newVisible = Math.min(
      visibleCount + CARDS_PER_CHUNK,
      projects.length
    );
    setVisibleCount(newVisible);
  };

  const hasMore = visibleCount < projects.length;

  return (
    <div ref={blockRef} className="relative">
      <div
        className="sticky bg-color-bg z-0 pt-px pb-3"
        style={{ top: `calc(var(--menu-height) + ${topOffset}px)` }}
      >
        <div className="flex items-start gap-4 mb-3">
          <button
            onClick={handleToggle}
            className="text-xl hover:opacity-70 transition-opacity mt-[2px] cursor-pointer"
            aria-label={isCollapsed ? "Expand section" : "Collapse section"}
          >
            <MdArrowBackIosNew
              className={`transition-transform duration-250 ${
                isCollapsed ? "-rotate-180" : "-rotate-90"
              }`}
            />
          </button>

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
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-[-1]">
            <div className="hidden md:block" />

            {[0, 1].map((colIndex) => {
              const cardsInColumn = projects
                .slice(0, visibleCount)
                .filter((_, index) => index % 2 === colIndex);

              return (
                <div key={colIndex} className="flex flex-col gap-2">
                  {cardsInColumn.map((project) => (
                    <div key={project.id}>
                      <ProjectCard project={project} />
                    </div>
                  ))}
                </div>
              );
            })}

            {hasMore && (
              <>
                <div className="hidden md:block" />
                <div className="md:col-span-2">
                  <button
                    onClick={handleShowMore}
                    className="py-2 y-80 text-note-2 underline cursor-pointer text-color-2 hover:text-color-1 transition-all duration-300"
                  >
                    Mostrar mais ({projects.length - visibleCount} restantes)
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectBlock;
