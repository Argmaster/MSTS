import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./components/app";

(async () => {
    const root = ReactDOM.createRoot(
        document.getElementById("app-root-element")
    );
    root.render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );
})();
