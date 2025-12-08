import { useVimeoThumb } from "../composables/useVimeoThumb";
import { Link } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  const [isVisible, setIsVisible] = useState(false);
  const cardRef = useRef<HTMLAnchorElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true);
        observer.disconnect();
      }
    });

    if (cardRef.current) {
      observer.observe(cardRef.current);
    }

    return () => {
      observer.disconnect();
    };
  }, []);

  return (
    <Link
      ref={cardRef}
      to={`/projetos/${project.id}`}
      className="group block"
      onClick={() => window.scrollTo(0, 0)}
    >
      <div className="relative w-full overflow-hidden rounded-lg mb-3 bg-gray-200" style={{ paddingBottom: '56.25%' }}>
        {isVisible && (
          <img
            src={useVimeoThumb(project.id)}
            alt={project.title}
            className="absolute top-0 left-0 w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-300"
            loading="lazy"
          />
        )}
      </div>
      <div className={isVisible ? "" : "invisible"}>
        <h3 className="font-medium text-lg mb-1 line-clamp-2">{project.title}</h3>
        <p className="text-sm text-gray-600">{project.author}</p>
        <p className="text-xs text-gray-500">{project.category}</p>
      </div>
    </Link>
  );
};

export default ProjectCard;
