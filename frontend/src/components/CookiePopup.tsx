import React, { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import Cookies from "js-cookie";

const COOKIE_NAME = "lastro-userDataConsent";

const CookiePopup: React.FC<CookiePopupProps> = ({ onAccept }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const consent = Cookies.get(COOKIE_NAME);
    if (!consent) setVisible(true);
  }, []);

  const handleAccept = () => {
    Cookies.set(COOKIE_NAME, "true", { expires: 365 });
    setVisible(false);
    if (onAccept) onAccept();
  };

  const handleReject = () => {
    Cookies.set(COOKIE_NAME, "false", { expires: 365 });
    setVisible(false);
  };

  if (!visible) return null;

  return createPortal(
    <>
      <div className="fixed inset-0 bg-black/40 z-50"></div>

      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-color-bg border border-color-1/50 rounded-xl p-8 max-w-md w-[calc(100%-2rem)] shadow-2xl">
        <h2 className="text-title-2 font-bold text-color-1 mb-4">
          Consentimento de Cookies
        </h2>
        <p className="text-body-1 text-color-2 mb-6">
          Ao aceitar, consente a recolha de dados de utilização, com o objetivo
          de melhorar a qualidade dos resultados de pesquisa.
        </p>
        <div className="flex gap-3 justify-end text-body-1">
          <button
            onClick={handleReject}
            className="px-4 py-2 rounded-lg border border-color-2/40 text-color-2 hover:text-color-1 hover:border-color-1 transition-all duration-250 cursor-pointer"
          >
            Rejeitar
          </button>
          <button
            onClick={handleAccept}
            className="px-4 py-2 rounded-lg bg-color-1 text-color-bg font-bold hover:opacity-80 transition-opacity duration-250 cursor-pointer"
          >
            Aceitar
          </button>
        </div>
      </div>
    </>,
    document.body
  );
};

export default CookiePopup;
