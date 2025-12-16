import { useEffect, useState } from "react";
import { getRandomProjects } from "../requests/requests";
import { Link } from "react-router-dom";

const Home = () => {
  const [project, setProject] = useState<Project>();

  useEffect(() => {
    getRandomProjects(1).then((res) => setProject((res as Project[])[0]));
  }, []);

  if (!project) return <div />;

  return (
    <div className="grid-setup">
      <Link to={`/projetos/${project.id}`}>Home</Link>
    </div>
  );
};

export default Home;
