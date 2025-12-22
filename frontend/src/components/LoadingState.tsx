import { useEffect, useRef, useState } from "react";
import gsap from "gsap";

interface LoadingStateProps {
  messages: string[][];
  fullHeight?: boolean;
}

const LoadingState: React.FC<LoadingStateProps> = ({
  messages,
  fullHeight = false,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const spinnerRef = useRef<SVGSVGElement>(null);
  const wordsRef = useRef<(HTMLSpanElement | null)[]>([]);
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    // Reset to first message when component mounts
    setMessageIndex(0);

    // Cycle through messages
    if (messages.length > 1) {
      const timer = setInterval(() => {
        setMessageIndex((prev) => (prev + 1) % messages.length);
      }, 5000);

      return () => clearInterval(timer);
    }
  }, [messages.length]);

  useEffect(() => {
    if (!containerRef.current) return;

    const ctx = gsap.context(() => {
      // Fade in spinner
      if (spinnerRef.current) {
        gsap.fromTo(
          spinnerRef.current,
          { opacity: 0 },
          { opacity: 1, duration: 0.7, ease: "power4.out" }
        );
      }

      const validWords = wordsRef.current.filter((ref) => ref !== null);
      if (validWords.length > 0) {
        gsap.fromTo(
          validWords,
          { opacity: 0, y: "-10%" },
          {
            opacity: 1,
            y: "0%",
            duration: 1.5,
            stagger: 0.2,
            delay: 0.25,
            ease: "expo.out",
          }
        );
      }
    });

    return () => ctx.revert();
  }, [messageIndex]);

  const currentMessage = messages[messageIndex];

  return (
    <div
      ref={containerRef}
      className={
        fullHeight
          ? "flex items-center justify-center h-[50vh]"
          : "pt-6 pb-6 min-h-[4rem]"
      }
    >
      <div className="flex items-center gap-3">
        <svg
          ref={spinnerRef}
          className="animate-spin h-5 w-5 flex-shrink-0"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          style={{ opacity: 0 }}
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
        <p className="text-body-1 text-color-2">
          {currentMessage.map((word, index) => (
            <span
              key={`word-${index}`}
              ref={(el) => {
                wordsRef.current[index] = el;
              }}
              className="inline-block"
            >
              {word}
              {index < currentMessage.length - 1 && "\u00A0"}
            </span>
          ))}
        </p>
      </div>
    </div>
  );
};

export default LoadingState;
