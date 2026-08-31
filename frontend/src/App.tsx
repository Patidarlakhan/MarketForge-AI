import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { CampaignList } from './pages/CampaignList';
import { CampaignCreate } from './pages/CampaignCreate';
import { CampaignDetail } from './pages/CampaignDetail';
import './App.css';

function Sidebar() {
  const location = useLocation();
  const isHome = location.pathname === '/';

  return (
    <aside className="app-sidebar">
      <div className="sidebar-logo">CE</div>
      <Link to="/" className={`sidebar-btn ${isHome ? 'active' : ''}`} title="Campaigns">🏠</Link>
      <Link to="/campaigns/new" className="sidebar-btn" title="New Campaign">➕</Link>
      <div className="sidebar-spacer"></div>
      <button className="sidebar-btn" title="Settings">⚙️</button>
    </aside>
  );
}

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-brand">Content Engine AI</div>
      <div className="navbar-search">
        <input type="text" placeholder="Search campaigns..." />
      </div>
      <div className="navbar-actions">
        <div className="navbar-avatar">L</div>
        <button className="navbar-menu-btn">Menu ▾</button>
        <Link to="/campaigns/new" className="btn btn-primary">+ New Campaign</Link>
      </div>
    </header>
  );
}

function App() {
  return (
    <Router>
      <div className="app-shell">
        <Sidebar />
        <div className="app-content">
          <Navbar />
          <Routes>
            <Route path="/" element={<CampaignList />} />
            <Route path="/campaigns/new" element={<CampaignCreate />} />
            <Route path="/campaigns/:id" element={<CampaignDetail />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
