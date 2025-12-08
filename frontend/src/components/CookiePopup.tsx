import React, { useState, useEffect } from "react";
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

  return (
    <div
      className={`
        fixed bottom-5 left-5 right-5
        bg-gray-800 text-white p-4 px-6 rounded-lg
        flex justify-between items-center gap-4

      `}
    >
      <p className="text-sm m-0">We use cookies to improve your experience.</p>
      <div className="flex gap-2">
        <button
          onClick={handleReject}
          className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md transition-colors"
        >
          Reject
        </button>
        <button
          onClick={handleAccept}
          className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md transition-colors"
        >
          Accept
        </button>
      </div>
    </div>
  );
};

export default CookiePopup;
