import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <Link to="/">
          <h1>AI Learning Assistant</h1>
        </Link>
      </div>
      <nav className="nav-links">
        <Link to="/">Dashboard</Link>
        <Link to="/materials">Learning Materials</Link>
        <Link to="/sessions">Study Sessions</Link>
      </nav>
      <div className="user-actions">
        <Link to="/profile" className="profile-link">
          <div className="avatar">
            <span>JS</span>
          </div>
          <span className="username">John Smith</span>
        </Link>
      </div>
    </header>
  );
};

export default Header;