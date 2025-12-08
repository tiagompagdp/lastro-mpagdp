import { useEffect, useState } from "react";
import { getRandomProjects } from "../requests/requests";
import ProjectCard from "../components/ProjectCard";

const Home = () => {
  const [projects, setProjects] = useState<Projects>([]);
  const nProjects = 1;

  useEffect(() => {
    getRandomProjects(nProjects).then((res) => setProjects(res as Projects));
  }, []);

  return (
    <div className="container mx-auto p-4">
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
      <h1 className="text-5xl text-hl-color font-mono-bold uppercase">
        Lastro
      </h1>
    </div>
  );
};

export default Home;
