import { useEffect, useState } from "react";
import { getProjects } from "../requests/requests";
import ProjectCard from "../components/ProjectCard";

const Home = () => {
  const [projects, setProjects] = useState<Projects>([]);

  useEffect(() => {
    getProjects().then((res) => setProjects(res as Projects));
  }, []);

  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {projects.slice(0, 100).map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>
    </div>
  );
};

export default Home;
