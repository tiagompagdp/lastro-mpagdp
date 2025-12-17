import { useEffect, useState } from "react";
import { getRandomProjects } from "../requests/requests";
import { useContentReady } from "../composables/usePageTransition";

const Home = () => {
  const [project, setProject] = useState<Project>();

  useContentReady(true);

  useEffect(() => {
    getRandomProjects(1).then((res) => setProject((res as Project[])[0]));
  }, []);

  if (!project) return <div />;

  return <div className="grid-setup">Home</div>;
};

export default Home;
