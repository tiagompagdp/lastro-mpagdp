import React, { useState, useEffect } from "react";
import { createPortal } from "react-dom";

interface ClearHistoryPopupProps {
  visible: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

const ClearHistoryPopup: React.FC<ClearHistoryPopupProps> = ({
  visible,
  onConfirm,
  onCancel,
}) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [shouldRender, setShouldRender] = useState(false);

  useEffect(() => {
    if (visible) {
      setShouldRender(true);
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          setIsAnimating(true);
        });
      });
    } else {
      setIsAnimating(false);
      const timer = setTimeout(() => {
        setShouldRender(false);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [visible]);

  if (!shouldRender) return null;

  return createPortal(
    <>
      <div
        className={`fixed inset-0 bg-black/40 z-50 transition-opacity duration-300 ${
          isAnimating ? "opacity-100" : "opacity-0"
        }`}
        onClick={onCancel}
      ></div>

      <div
        className={`fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-color-bg border border-color-1/50 rounded-xl p-8 max-w-md w-[calc(100%-2rem)] shadow-2xl transition-all duration-300 ${
          isAnimating ? "opacity-100 scale-100" : "opacity-0 scale-95"
        }`}
      >
        <h2 className="text-title-2 font-bold text-color-1 mb-4">
          Nova Pesquisa
        </h2>
        <p className="text-body-1 text-color-2 mb-6">
          Tem a certeza que deseja limpar todo o histórico de pesquisa?
        </p>
        <div className="flex gap-3 justify-end text-body-1">
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded-lg border border-color-2/40 text-color-2 hover:text-color-1 hover:border-color-1 transition-all duration-250 cursor-pointer"
          >
            Cancelar
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 rounded-lg bg-color-1 text-color-bg font-bold hover:opacity-80 transition-opacity duration-250 cursor-pointer"
          >
            Limpar
          </button>
        </div>
      </div>
    </>,
    document.body
  );
};

export default ClearHistoryPopup;
