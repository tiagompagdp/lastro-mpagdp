import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Player from "@vimeo/player";
import { getRandomProjects } from "../requests/requests";
import { useChat } from "../composables/useChat";
import logoSvg from "../assets/logo.svg";
import { SlArrowDown } from "react-icons/sl";

interface ProjectHomeProps {
  currentProjectId?: string;
  onVideoReady?: () => void;
}

export default function ProjectHome({
  currentProjectId,
  onVideoReady,
}: ProjectHomeProps) {
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

  // Init Vimeo player ASAP
  useEffect(() => {
    if (!iframeRef.current || !videoId) return;

    playerRef.current?.destroy();

    const player = new Player(iframeRef.current, {
      autoplay: true,
      muted: true,
      loop: true,
      background: true,
      autopause: false,
      quality: "240p", // fastest initial load
    });

    playerRef.current = player;

    player.on("playing", () => {
      setVideoReady(true);
      onVideoReady?.();
    });

    return () => {
      player.destroy();
    };
  }, [videoId, onVideoReady]);

  if (!videoId) return null;

  return (
    <div className="relative h-[100dvh] w-screen overflow-hidden left-1/2 -translate-x-1/2 mb-24 mt-[calc(var(--menu-height)*-1)]">
      {/* Preconnect for faster Vimeo load */}
      <link rel="preconnect" href="https://player.vimeo.com" />
      <link rel="dns-prefetch" href="https://player.vimeo.com" />

      {/* Video */}
      <div
        className={`absolute inset-0 transition-opacity duration-700 ease-out ${
          videoReady ? "opacity-50" : "opacity-0"
        }`}
        style={{ zIndex: 0 }}
      >
        <iframe
          ref={iframeRef}
          title="vimeo-background"
          src={`https://player.vimeo.com/video/${videoId}?autoplay=1&loop=1&muted=1&background=1&quality=240p&autopause=0`}
          allow="autoplay; fullscreen; picture-in-picture"
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
      <div className="absolute top-0 w-screen h-[100vh] bg-gradient-to-b from-transparent to-color-bg z-0" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-between h-full text-color-1 text-center px-8 pt-[var(--menu-height)]">
        <a
          href="https://amusicaportuguesaagostardelapropria.org/"
          target="_blank"
        >
          <img
            src={logoSvg}
            className="relative z-10 w-15 h-15 mx-auto mt-12"
          />
        </a>

        <div className="flex flex-col items-center">
          <h1 className="text-title-1 font-bold mb-2">LASTRO</h1>
          <h2 className="text-body-1 mb-12 opacity-50 whitespace-pre-line">
            {
              "O motor de busca inteligente da\n Música Portuguesa a Gostar Dela Própria."
            }
          </h2>

          <div className="flex gap-4 flex-wrap justify-center text-body-1">
            <button
              onClick={() => navigate(`/projetos/${videoId}`)}
              className="px-5 py-3 bg-color-1 text-color-bg font-bold rounded-lg hover:bg-color-1/80 transition"
            >
              Ver {projectTitle}
            </button>

            <button
              onClick={() => {
                clearMessages();
                navigate("/explorar");
              }}
              className="px-5 py-3 rounded-lg border border-color-2/40 text-color-2 hover:text-color-1 hover:border-color-1 bg-color-bg/20 hover:bg-color-bg/50 backdrop-blur-sm transition"
            >
              Nova Exploração
            </button>
          </div>
        </div>

        <button
          onClick={() =>
            document.getElementById("projects")?.scrollIntoView({
              behavior: "smooth",
              block: "start",
            })
          }
          aria-label="Scroll down"
          className="mb-[calc(var(--menu-height)*1.6)] inline-block cursor-pointer"
        >
          <SlArrowDown
            className="text-white h-10 w-10 p-2"
            style={{
              opacity: 0,
              animation: `fadeIn 2s ease forwards 2s,
                bounce 2s ease-out infinite`,
            }}
          />
        </button>
      </div>
    </div>
  );
}
