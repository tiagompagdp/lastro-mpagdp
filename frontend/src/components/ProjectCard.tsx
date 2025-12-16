import { useVimeoThumb } from "../composables/useVimeoThumb";
import { Link } from "react-router-dom";
import { useState } from "react";
import logoSvg from "../assets/logo.svg";

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  const [imageLoaded, setImageLoaded] = useState(false);

  return (
    <Link
      to={`/projetos/${project.id}`}
      className="group w-full flex flex-row gap-4"
    >
      <div className="aspect-square relative h-16 overflow-hidden flex-shrink-0 bg-color-bg flex items-center justify-center">
        <img
          src={logoSvg}
          alt="Loading"
          className={`w-10 h-10 transition-opacity duration-500 ${
            imageLoaded ? "opacity-0" : "opacity-50"
          }`}
        />
        <img
          src={useVimeoThumb(project.id)}
          alt={project.title}
          className={`absolute top-0 left-0 w-full h-full rounded-[5%] object-cover grayscale group-hover:grayscale-0 transition-all duration-250 ${
            imageLoaded ? "opacity-100" : "opacity-0"
          }`}
          loading="lazy"
          onLoad={() => setImageLoaded(true)}
        />
      </div>

      <div>
        <h3 className="text-body-1">
          {project.title == "" ? "Sem título registado" : project.title}
        </h3>

        <p className="text-note-2 pt-1 opacity-50">
          {project.author == "" ? "Sem autor registado" : project.author}
        </p>

        <p className="text-note-3 pt-3">
          {project.category == ""
            ? "Sem categoria registada"
            : project.category}
        </p>
      </div>
    </Link>
  );
};

export default ProjectCard;
