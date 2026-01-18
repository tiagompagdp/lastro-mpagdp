import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Cookies from "js-cookie";

import { useChat } from "../composables/useChat";
import { usePublicIP } from "../composables/usePublicIP";
import { sendQuery } from "../requests/requests";
import { BiSearch } from "react-icons/bi";
import { AiOutlinePlus } from "react-icons/ai";
import ClearHistoryPopup from "./ClearHistoryPopup";

const generalPlaceholders = [
  "Procure qualquer coisa...",
  "Descubra projetos de investigação...",
  "Explore temas científicos...",
  "Encontre publicações recentes...",
  "Pesquise por área de estudo...",
  "Procure investigadores...",
];

const projectPlaceholders = [
  "Pergunte sobre este projeto...",
  "Descubra mais detalhes...",
  "Explore os resultados...",
  "Pesquise informações específicas...",
  "Encontre publicações relacionadas...",
];

const getRandomPlaceholder = (placeholders: string[], currentIndex: number): number => {
  if (placeholders.length <= 1) return 0;
  let newIndex: number;
  do {
    newIndex = Math.floor(Math.random() * placeholders.length);
  } while (newIndex === currentIndex);
  return newIndex;
};

const PromptBar = () => {
  const [input, setInput] = useState("");
  const [cookieAccepted, setCookieAccepted] = useState(false);
  const [showClearPopup, setShowClearPopup] = useState(false);
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const [isFading, setIsFading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { messages, addMessage, clearMessages, isLoading, setIsLoading } = useChat();
  const ip = usePublicIP(cookieAccepted);

  const isProjectPage = /^\/projetos\/\d+$/.test(location.pathname);
  const [activeArray, setActiveArray] = useState<"general" | "project">(
    isProjectPage ? "project" : "general"
  );
  const placeholders = activeArray === "project" ? projectPlaceholders : generalPlaceholders;
  const currentPlaceholder = placeholders[placeholderIndex % placeholders.length];

  const historySize = 1;

  useEffect(() => {
    setCookieAccepted(Cookies.get("lastro-userDataConsent") === "true");
  }, []);

  // Immediately switch arrays when page type changes (with fade)
  useEffect(() => {
    const targetArray = isProjectPage ? "project" : "general";
    if (activeArray !== targetArray) {
      setIsFading(true);
      const timeout = setTimeout(() => {
        setActiveArray(targetArray);
        const newPlaceholders = targetArray === "project" ? projectPlaceholders : generalPlaceholders;
        setPlaceholderIndex(Math.floor(Math.random() * newPlaceholders.length));
        setIsFading(false);
      }, 300);
      return () => clearTimeout(timeout);
    }
  }, [isProjectPage, activeArray]);

  // Rotate placeholders every 5 seconds with fade animation
  useEffect(() => {
    const interval = setInterval(() => {
      setIsFading(true);
      setTimeout(() => {
        setPlaceholderIndex((prev) => getRandomPlaceholder(placeholders, prev));
        setIsFading(false);
      }, 300);
    }, 5000);

    return () => clearInterval(interval);
  }, [placeholders]);

  useEffect(() => {
    // Close popup when navigating away from explorar page
    if (location.pathname !== "/explorar") {
      setShowClearPopup(false);
    }
  }, [location.pathname]);

  const handleSend = async () => {
    if (!input.trim() || !ip) return;

    const prompt = input.trim();

    // Extract project ID from path like /projetos/1434903174
    const projectMatch = location.pathname.match(/^\/projetos\/(\d+)$/);
    const currentProjectId = projectMatch ? projectMatch[1] : undefined;

    if (location.pathname !== "/explorar") navigate("/explorar");

    setIsLoading(true);

    try {
      const response = await sendQuery({
        cookieConsent: cookieAccepted,
        userIp: ip,
        previousQueries: messages
          .slice(-historySize)
          .map((msg) => msg.queries?.[0] || ""),
        currentPrompt: prompt,
        currentProjectId,
      });

      addMessage({
        prompt,
        queries: response.queries,
        descriptions: response.descriptions,
        results: response.results,
        contextProject: response.contextProject,
      });
      setInput("");
    } catch (err) {
      console.error(err);
      addMessage({ prompt });
      setInput("");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    navigate("/explorar");
    // Only show popup if there's history to clear
    if (messages.length >= 1) {
      setShowClearPopup(true);
    }
  };

  const handleConfirmClear = () => {
    clearMessages();
    setShowClearPopup(false);
  };

  const handleCancelClear = () => {
    setShowClearPopup(false);
  };

  return (
    <>
      <ClearHistoryPopup
        visible={showClearPopup}
        onConfirm={handleConfirmClear}
        onCancel={handleCancelClear}
      />
      <div className="fixed bottom-0 left-0 w-full bg-color-bg border-t border-color-2/25 z-50">
        <div className="flex items-center h-full menu-footer-setup gap-2">
        <div className="flex gap-2 w-full bg-color-2/5 rounded-full transition-all focus-within:ring-1 focus-within:ring-color-2/25">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={currentPlaceholder}
            disabled={!ip || isLoading}
            className={`flex-1 bg-transparent pl-6 text-color-1 text-body-1 focus:outline-none transition-all ${
              isLoading ? "opacity-40" : "opacity-100"
            }`}
            style={{
              ["--tw-placeholder-opacity" as string]: isFading ? "0" : "0.4",
            }}
          />
          <style>{`
            input::placeholder {
              transition: opacity 0.3s ease-in-out;
              opacity: var(--tw-placeholder-opacity, 0.4);
            }
          `}</style>
          <button
            onClick={handleSend}
            disabled={!ip || isLoading || !input.trim()}
            className="text-color-1 pr-8 pl-4 rounded-lg hover:opacity-80 disabled:opacity-40 disabled:cursor-not-allowed transition-opacity flex items-center justify-center w-12 h-12 relative cursor-pointer"
          >
            <svg
              className={`animate-spin h-5 w-5 absolute transition-opacity duration-300 ${
                isLoading ? "opacity-100 delay-150" : "opacity-0 delay-0"
              }`}
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="3"
              ></circle>
              <path
                className="opacity-75"
                stroke="currentColor"
                strokeWidth="3"
                strokeLinecap="round"
                d="M12 2a10 10 0 0 1 10 10"
              ></path>
            </svg>
            <BiSearch
              className={`h-6 w-6 absolute transition-opacity duration-300 ${
                isLoading ? "opacity-0 delay-0" : "opacity-100 delay-150"
              }`}
            />
          </button>
        </div>
        <button onClick={handleNewChat} disabled={isLoading} className="text-white cursor-pointer flex items-center justify-center w-12 h-12 rounded-full bg-color-2/5 group disabled:cursor-not-allowed">
          <AiOutlinePlus className="h-6 w-6 opacity-50 group-hover:opacity-100 group-disabled:opacity-40 group-disabled:hover:opacity-40 transition-opacity duration-300" />
        </button>
      </div>
    </div>
    </>
  );
};

export default PromptBar;
