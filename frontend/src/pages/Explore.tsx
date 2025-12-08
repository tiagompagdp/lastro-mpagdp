import { useState, useEffect } from "react";
import Cookies from "js-cookie";

import CookiePopup from "../components/CookiePopup";
import { usePublicIP } from "../composables/usePublicIP";
import { sendQuery } from "../requests/requests";

const Explore: React.FC = () => {
  const [cookieAccepted, setCookieAccepted] = useState(false);

  useEffect(() => {
    setCookieAccepted(Cookies.get("lastro-userDataConsent") === "true");
  }, []);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const ip = usePublicIP(cookieAccepted);

  const historySize = 2;

  // ==================================================
  // send queries
  // ==================================================

  const handleSend = async () => {
    if (!input.trim() || !ip) return;

    const prompt = input.trim();
    setLoading(true);

    try {
      const response = await sendQuery({
        cookieConsent: cookieAccepted,
        userIp: ip,
        previousPrompts: messages.slice(-historySize).map((msg) => msg.prompt),
        currentPrompt: prompt,
      });

      setMessages((prev) => [...prev, { prompt, response: response.queries }]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { prompt, response: "Error sending query" },
      ]);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSend();
  };

  // ==================================================
  // html
  // ==================================================

  return (
    <div className="flex flex-col h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Explore</h1>
      <p>Cookie Accepted: {cookieAccepted ? "Yes" : "No"}</p>
      <p>Your public IP: {ip ?? "Loading..."}</p>

      <CookiePopup onAccept={() => setCookieAccepted(true)} />

      {/* Messages list */}
      <div className="flex-1 overflow-y-auto my-4 space-y-2 border p-2 rounded bg-gray-50">
        {messages.length === 0 && (
          <p className="text-gray-400">No messages yet.</p>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className="p-2 rounded border bg-white">
            <p className="font-semibold">{msg.prompt}</p>
            <p className="font-semibold opacity-50">{msg.response}</p>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="flex space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your prompt..."
          className="flex-1 border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-400"
          disabled={!ip || loading}
        />
        <button
          onClick={handleSend}
          disabled={!ip || loading || !input.trim()}
          className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Explore;
