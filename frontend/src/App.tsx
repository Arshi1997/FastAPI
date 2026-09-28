import { useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Settings from "./pages/Settings";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="brand">
          <div className="brand-mark">F</div>
          <div>
            <strong>FastAPI UI</strong>
            <span>React Frontend</span>
          </div>
        </div>

        <nav>
          <NavLink to="/" end onClick={() => setSidebarOpen(false)}>Dashboard</NavLink>
          <NavLink to="/users" onClick={() => setSidebarOpen(false)}>Users</NavLink>
          <NavLink to="/settings" onClick={() => setSidebarOpen(false)}>Settings</NavLink>
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          Backend integration ready
        </div>
      </aside>

      {sidebarOpen && <div className="overlay" onClick={() => setSidebarOpen(false)} />}

      <main className="main-content">
        <header className="topbar">
          <button className="menu-button" onClick={() => setSidebarOpen(!sidebarOpen)}>☰</button>
          <div>
            <h1>Frontend Dashboard</h1>
            <p>React + Vite + TypeScript</p>
          </div>
          <div className="api-badge">FastAPI Ready</div>
        </header>

        <section className="page-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<Users />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </section>
      </main>
    </div>
  );
}

export default App;