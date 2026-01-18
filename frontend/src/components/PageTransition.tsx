import { useEffect, useState, useRef, useCallback, useMemo } from "react";
import { useLocation, useOutlet } from "react-router-dom";
import { PageTransitionContext } from "../composables/usePageTransition";

export default function PageTransition() {
  const location = useLocation();
  const [displayLocation, setDisplayLocation] = useState(location);
  const [transitionStage, setTransitionStage] = useState("fadeIn");
  const [isContentReady, setIsContentReady] = useState(false);

  const currentOutlet = useOutlet();
  const displayOutletRef = useRef(currentOutlet);

  useEffect(() => {
    if (location.pathname !== displayLocation.pathname) {
      setTransitionStage("fadeOut");
      setIsContentReady(false);
    } else {
      displayOutletRef.current = currentOutlet;
    }
  }, [location.pathname, displayLocation.pathname, currentOutlet]);

  useEffect(() => {
    if (isContentReady && transitionStage === "waiting") {
      setTransitionStage("fadeIn");
    }
  }, [isContentReady, transitionStage]);

  const handleAnimationEnd = () => {
    if (transitionStage === "fadeOut") {
      // Scroll to top for all pages except explorar (happens while page is faded out)
      if (location.pathname !== "/explorar") {
        window.scrollTo({
          top: 0,
          behavior: "instant",
        });
      }

      setDisplayLocation(location);
      displayOutletRef.current = currentOutlet;
      setTransitionStage("waiting");
    } else if (transitionStage === "fadeIn") {
      // Scroll to bottom when navigating to explorar page (after fade in completes)
      if (location.pathname === "/explorar") {
        window.scrollTo({
          top: document.documentElement.scrollHeight,
          behavior: "smooth",
        });
      }
    }
  };

  const notifyContentReady = useCallback(() => {
    setIsContentReady(true);
  }, []);

  const contextValue = useMemo(
    () => ({ notifyContentReady }),
    [notifyContentReady]
  );

  return (
    <PageTransitionContext.Provider value={contextValue}>
      <div
        className={`page-transition ${
          transitionStage === "waiting" ? "" : transitionStage
        }`}
        onAnimationEnd={handleAnimationEnd}
        style={transitionStage === "waiting" ? { opacity: 0 } : undefined}
      >
        {displayOutletRef.current}
      </div>
    </PageTransitionContext.Provider>
  );
}
