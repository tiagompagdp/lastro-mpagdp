import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { BiArrowBack } from "react-icons/bi";
import { getProject, getSuggestions } from "../requests/requests";
import ProjectBlock from "../components/ProjectBlock";
import VideoSection from "../components/VideoSection";
import ProjectFooter from "../components/ProjectFooter";

const Project: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project>();
  const [suggestions, setSuggestions] = useState<Suggestions>([]);
  const [headerHeight, setHeaderHeight] = useState<number>(0);
  const headerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (id) {
      getProject(id).then((res) => setProject(res as Project));
      getSuggestions(id).then((res) => setSuggestions(res as Suggestions));
    }
  }, [id]);

  useEffect(() => {
    const observer = new ResizeObserver((entries) => {
      entries.forEach((entry) => {
        setHeaderHeight(entry.target.clientHeight);
      });
    });

    if (headerRef.current) observer.observe(headerRef.current);

    return () => observer.disconnect();
  }, [project]);

  if (!project) return <div />;

  return (
    <div className="grid-setup !py-[var(--menu-height)]">
      <div>
        <div
          ref={headerRef}
          className="sticky top-[var(--menu-height)] bg-color-bg z-2 py-3"
        >
          <div className="flex items-start gap-3">
            <button
              onClick={() => navigate("/explorar")}
              className="text-2xl hover:opacity-70 transition-opacity mt-px cursor-pointer"
              aria-label="Go back"
            >
              <BiArrowBack />
            </button>
            <div>
              <h1 className="text-title-2">
                {project.title == "" ? "Sem título registado" : project.title}
              </h1>
              <p className="text-note-1 opacity-50 mt-1 mb-3">
                {project.author == "" ? "Sem autor registado" : project.author}
              </p>
            </div>
          </div>

          <span className="block h-px w-full bg-color-1 opacity-50" />
        </div>

        <VideoSection project={project} />

        {suggestions.map((suggestion, index) => (
          <ProjectBlock
            key={index}
            title={suggestion.description}
            projects={suggestion.projects}
            topOffset={headerHeight}
          />
        ))}
      </div>

      <ProjectFooter currentProjectId={id} />
    </div>
  );
};

export default Project;
