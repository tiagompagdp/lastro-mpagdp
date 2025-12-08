import ProjectCard from "./ProjectCard";

interface ProjectBlockProps {
  title: string;
  projects: Projects;
}

const ProjectBlock: React.FC<ProjectBlockProps> = ({ title, projects }) => {
  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {projects.slice(0, 10).map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>
    </div>
  );
};

export default ProjectBlock;
