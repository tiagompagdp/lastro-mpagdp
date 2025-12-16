import { useEffect, useState, useRef } from "react";
import { useLocation, useOutlet } from "react-router-dom";

export default function PageTransition() {
  const location = useLocation();
  const [displayLocation, setDisplayLocation] = useState(location);
  const [transitionStage, setTransitionStage] = useState("fadeIn");

  const currentOutlet = useOutlet();
  const displayOutletRef = useRef(currentOutlet);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (location.pathname !== displayLocation.pathname)
      setTransitionStage("fadeOut");
    else displayOutletRef.current = currentOutlet;
  }, [location.pathname, displayLocation.pathname, currentOutlet]);

  const handleAnimationEnd = () => {
    if (transitionStage === "fadeOut") {
      setDisplayLocation(location);
      displayOutletRef.current = currentOutlet;
      if (containerRef.current) containerRef.current.scrollTop = 0;
      setTransitionStage("fadeIn");
    }
  };

  return (
    <div
      ref={containerRef}
      className={`page-transition ${transitionStage}`}
      onAnimationEnd={handleAnimationEnd}
    >
      {displayOutletRef.current}
    </div>
  );
}
