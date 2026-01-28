import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Player from "@vimeo/player";
import { getRandomProjects } from "../requests/requests";
import { useChat } from "../composables/useChat";

interface ProjectFooterProps {
  currentProjectId?: string;
}

export default function ProjectFooter({
  currentProjectId,
}: ProjectFooterProps) {
  const navigate = useNavigate();
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const playerRef = useRef<Player | null>(null);

  const [videoReady, setVideoReady] = useState(false);
  const [videoId, setVideoId] = useState<string | null>(null);
  const [projectTitle, setProjectTitle] = useState<string>("");

  const { clearMessages } = useChat();

  // Fetch project
  useEffect(() => {
    setVideoReady(false);

    getRandomProjects(1).then((res) => {
      const project = (res as Project[])[0];
      if (project?.id) {
        setVideoId(project.id);
        setProjectTitle(project.title || "este projeto");
      }
    });
  }, [currentProjectId]);

  // Init Vimeo player
  useEffect(() => {
    if (!iframeRef.current || !videoId) return;

    playerRef.current?.destroy();

    const player = new Player(iframeRef.current, {
      autoplay: true,
      muted: true,
      loop: true,
      background: true,
      autopause: false,
      quality: "240p", // faster first frame
    });

    playerRef.current = player;

    // Fire only when first frame is rendered
    player.on("playing", () => {
      setVideoReady(true);
    });

    return () => {
      player.destroy();
    };
  }, [videoId]);

  if (!videoId) return null;

  return (
    <div className="relative h-[100vh] w-screen overflow-hidden bg-black left-1/2 -translate-x-1/2">
      {/* Preconnect for faster Vimeo startup */}
      <link rel="preconnect" href="https://player.vimeo.com" />
      <link rel="dns-prefetch" href="https://player.vimeo.com" />

      {/* Video */}
      <div
        className={`absolute inset-0 transition-opacity duration-[1000ms] ease-in-out ${
          videoReady ? "opacity-50" : "opacity-0"
        }`}
        style={{ zIndex: 0 }}
      >
        <iframe
          ref={iframeRef}
          title="vimeo-background"
          src={`https://player.vimeo.com/video/${videoId}?autoplay=1&loop=1&muted=1&background=1&quality=240p&autopause=0`}
          allow="autoplay; fullscreen"
          className="absolute top-0 left-1/2 -translate-x-1/2 pointer-events-none"
          style={{
            height: "100vh",
            width: "177.78vh",
            minWidth: "100vw",
            minHeight: "56.25vw",
          }}
        />
      </div>

      {/* Gradient overlay */}
      <div className="absolute top-0 w-screen h-[100vh] bg-gradient-to-b from-color-bg to-transparent z-0" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-color-1 text-center px-8 pt-[var(--menu-height)]">
        <h2 className="text-title-1 font-bold mb-12 whitespace-pre-line">
          {"Não encontrou o que procurava?\nMude de direção."}
        </h2>

        <div className="flex gap-4 flex-wrap justify-center text-body-1">
          <button
            onClick={() => navigate(`/projetos/${videoId}`)}
            className="px-5 py-3 bg-color-1 text-color-bg font-bold rounded-lg hover:bg-color-1/80 transition-all duration-250 cursor-pointer"
          >
            Ver {projectTitle}
          </button>

          <button
            onClick={() => {
              clearMessages();
              navigate("/explorar");
            }}
            className="px-5 py-3 rounded-lg border border-color-2/40 text-color-2 hover:text-color-1 hover:border-color-1 bg-color-bg/20 hover:bg-color-bg/50 transition-all duration-250 backdrop-blur-sm cursor-pointer"
          >
            Nova Exploração
          </button>
        </div>
      </div>
    </div>
  );
}
