import { createContext, useContext, useEffect } from "react";

type PageTransitionContextType = {
  notifyContentReady: () => void;
};

export const PageTransitionContext = createContext<PageTransitionContextType>({
  notifyContentReady: () => {},
});

export const usePageTransition = () => {
  return useContext(PageTransitionContext);
};

export const useContentReady = (isReady: boolean) => {
  const { notifyContentReady } = usePageTransition();

  useEffect(() => {
    if (isReady) {
      notifyContentReady();
    }
  }, [isReady, notifyContentReady]);
};
