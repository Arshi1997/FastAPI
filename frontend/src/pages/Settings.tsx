import { useState } from "react";

export default function Settings() {
  const [saved, setSaved] = useState(false);

  return (
    <div className="settings-layout">
      <div className="panel">
        <h2>Settings</h2>
        <p>Frontend configuration you can customize before connecting FastAPI.</p>

        <label>
          API Base URL
          <input defaultValue={import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"} />
        </label>

        <label>
          Application Name
          <input defaultValue="FastAPI Frontend" />
        </label>

        <button className="primary-button" onClick={() => setSaved(true)}>
          Save Settings
        </button>

        {saved && <div className="save-message">Settings saved locally for this demo.</div>}
      </div>

      <div className="panel">
        <h3>Environment</h3>
        <div className="env-row"><span>Frontend</span><strong>Vite</strong></div>
        <div className="env-row"><span>Framework</span><strong>React 19</strong></div>
        <div className="env-row"><span>Language</span><strong>TypeScript</strong></div>
        <div className="env-row"><span>HTTP Client</span><strong>Axios</strong></div>
        <div className="env-row"><span>Backend</span><strong>FastAPI</strong></div>
      </div>
    </div>
  );
}