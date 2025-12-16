import { useEffect, useRef, useState } from "react";
import gsap from "gsap";

interface SearchLoadingProps {
  isVisible: boolean;
}

const SearchLoading: React.FC<SearchLoadingProps> = ({ isVisible }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const spinnerRef = useRef<SVGSVGElement>(null);
  const wordsRef = useRef<(HTMLSpanElement | null)[]>([]);
  const [shouldRender, setShouldRender] = useState(false);
  const [showSecondMessage, setShowSecondMessage] = useState(false);

  useEffect(() => {
    if (isVisible) {
      setShouldRender(true);
      setShowSecondMessage(false);

      // After 10 seconds, change to second message
      const timer = setTimeout(() => {
        setShowSecondMessage(true);
      }, 2000);

      return () => clearTimeout(timer);
    }
  }, [isVisible]);

  useEffect(() => {
    if (!shouldRender || !containerRef.current) return;

    if (!isVisible) {
      const ctx = gsap.context(() => {
        gsap.to(containerRef.current, {
          opacity: 0,
          duration: 0.3,
          ease: "power2.in",
          onComplete: () => {
            setShouldRender(false);
            setShowSecondMessage(false);
          },
        });
      }, containerRef);
      return () => ctx.revert();
    }
  }, [isVisible, shouldRender]);

  useEffect(() => {
    if (!shouldRender) return;

    const ctx = gsap.context(() => {
      // Fade in spinner
      if (spinnerRef.current) {
        gsap.fromTo(
          spinnerRef.current,
          { opacity: 0 },
          { opacity: 1, duration: 0.5, ease: "power4.out" }
        );
      }

      // Animate each word: opacity 0 to 1, y from -10% to 0%
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
  }, [showSecondMessage, shouldRender]);

  if (!shouldRender) return null;

  const firstMessage = ["A", "procurar..."];
  const secondMessage = ["Já", "não", "falta", "muito..."];
  const currentMessage = showSecondMessage ? secondMessage : firstMessage;

  return (
    <div ref={containerRef} className="pt-6 pb-6 min-h-[4rem]">
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
        <p className="text-body-1 text-color-2 whitespace-nowrap">
          {currentMessage.map((word, index) => (
            <span
              key={`${showSecondMessage ? "second" : "first"}-${index}`}
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

export default SearchLoading;
