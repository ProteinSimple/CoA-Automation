import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import 'primereact/resources/themes/lara-dark-indigo/theme.css'; // or any other theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
