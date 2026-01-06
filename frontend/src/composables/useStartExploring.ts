import { getRandomProjects } from "../requests/requests";
import { useChat } from "./useChat";

export const useStartExploring = () => {
  const { addMessage } = useChat();

  const startExploring = async () => {
    try {
      const randomProjects = await getRandomProjects(100);
      const descriptions = [
        "Um ponto de partida",
        "Apenas o começo",
        "Vai um empurrão?",
      ];

      const randomDescription =
        descriptions[Math.floor(Math.random() * descriptions.length)];

      addMessage({
        prompt: "começar a explorar",
        descriptions: [randomDescription],
        results: [randomProjects as Projects],
      });
    } catch (error) {
      console.error("Error fetching random projects:", error);
    }
  };

  return { startExploring };
};