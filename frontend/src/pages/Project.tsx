import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getProject,
  getSuggestions,
  getRandomProjects,
} from "../requests/requests";
import ProjectBlock from "../components/ProjectBlock";

const Project: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project>();
  const [suggestions, setSuggestions] = useState<Suggestions>([]);
  const [randomProjects, setRandomProjects] = useState<Projects>([]);
  const nRandom = 50;

  useEffect(() => {
    if (id) {
      getProject(id).then((res) => setProject(res as Project));
      getSuggestions(id).then((res) => setSuggestions(res as Suggestions));
      getRandomProjects(nRandom).then((res) =>
        setRandomProjects(res as Projects)
      );
    }
  }, [id]);

  if (!project) {
    return <div className="flex flex-col h-screen p-4">Loading...</div>;
  }

  return (
    <div className="flex flex-col h-screen p-4">
      <div className="mb-6">
        <div className="aspect-video w-full mb-4">
          <iframe
            src={`https://player.vimeo.com/video/${id}`}
            className="w-full h-full border-0"
            allow="autoplay; fullscreen; picture-in-picture"
            allowFullScreen
            title={project.title}
          ></iframe>
        </div>
        <h1 className="text-2xl font-bold mb-4">{project.title}</h1>
        <p className="text-gray-600">by {project.author}</p>
        <p className="text-sm text-gray-500">{project.category}</p>
      </div>

      {suggestions.map((suggestion, index) => (
        <ProjectBlock
          key={index}
          title={suggestion.description}
          projects={suggestion.projects}
        />
      ))}
    </div>
  );
};

export default Project;
