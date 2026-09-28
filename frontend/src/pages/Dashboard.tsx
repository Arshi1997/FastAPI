import { useEffect, useState } from "react";
import { api } from "../api/client";

const mockStats = {
  users: 1284,
  requests: 48291,
  successRate: 99.2,
  responseTime: 142,
};

export default function Dashboard() {
  const [stats, setStats] = useState(mockStats);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (import.meta.env.VITE_USE_MOCK_DATA === "true") return;

    setLoading(true);
    api.get("/api/stats")
      .then((response) => setStats(response.data))
      .catch((error) => console.error("Failed to load stats:", error))
      .finally(() => setLoading(false));
  }, []);

  const cards = [
    ["Total Users", stats.users.toLocaleString(), "↑ 12.4%"],
    ["API Requests", stats.requests.toLocaleString(), "↑ 8.7%"],
    ["Success Rate", `${stats.successRate}%`, "↑ 0.4%"],
    ["Avg Response", `${stats.responseTime} ms`, "↓ 16 ms"],
  ];

  return (
    <>
      <div className="welcome">
        <div>
          <h2>Welcome back 👋</h2>
          <p>Your frontend is ready. Connect your FastAPI endpoints when you're ready.</p>
        </div>
        <span className="mock-pill">
          {loading ? "Loading API..." : import.meta.env.VITE_USE_MOCK_DATA === "true" ? "Mock Data" : "Live API"}
        </span>
      </div>

      <div className="stats-grid">
        {cards.map(([label, value, change]) => (
          <div className="stat-card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{change} from last period</small>
          </div>
        ))}
      </div>

      <div className="content-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <h3>API Integration</h3>
              <p>Where your FastAPI connection starts</p>
            </div>
            <span className="badge success">Ready</span>
          </div>
          <div className="code-box">
            <div><span className="muted">GET</span> /api/stats</div>
            <div><span className="muted">GET</span> /api/users</div>
            <div><span className="muted">POST</span> /api/users</div>
            <div><span className="muted">DELETE</span> /api/users/:id</div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <h3>Quick Start</h3>
              <p>Three steps to connect your backend</p>
            </div>
          </div>
          <ol className="steps">
            <li>Copy <code>.env.example</code> to <code>.env</code></li>
            <li>Set <code>VITE_API_BASE_URL</code></li>
            <li>Replace mock API functions with Axios calls</li>
          </ol>
        </div>
      </div>
    </>
  );
}