import ProjectCard from "./ProjectCard";
import { MdArrowBackIosNew } from "react-icons/md";
import { useState, useRef } from "react";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
  topOffset?: number; // for sticky positioning
}

const ProjectBlock: React.FC<ProjectBlockProps> = ({
  title,
  projects,
  topOffset = 0,
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const blockRef = useRef<HTMLDivElement>(null);

  const handleToggle = () => {
    setIsCollapsed((prev) => !prev);
  };

  return (
    <div ref={blockRef} className="relative">
      <div
        className="sticky bg-color-bg z-1 pt-px pb-3"
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {projects.slice(0, 10).map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectBlock;
