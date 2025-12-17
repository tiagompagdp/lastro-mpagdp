import { useContentReady } from "../composables/usePageTransition";

const About = () => {
  useContentReady(true);

  return <div className="grid-setup">Sobre</div>;
};

export default About;
