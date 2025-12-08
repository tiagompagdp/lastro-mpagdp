import { useState, useEffect } from "react";

export function usePublicIP(cookie: boolean) {
  const [ip, setIp] = useState<string | null>("");

  useEffect(() => {
    const fetchIP = async () => {
      try {
        const response = await fetch("https://api.ipify.org?format=json");
        if (!response.ok) throw new Error("Failed to fetch IP");
        const data = await response.json();
        setIp(data.ip);
      } catch (err: any) {
        console.log(err.message);
      }
    };

    if (cookie) fetchIP();
  }, [cookie]);

  return ip;
}
