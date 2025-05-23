import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <ul>
          <li>
            <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
              <i className="icon">📊</i>
              <span>Dashboard</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/materials" className={({ isActive }) => isActive ? 'active' : ''}>
              <i className="icon">📚</i>
              <span>Learning Materials</span>
            </NavLink>
          </li>          <li>
            <NavLink to="/sessions" className={({ isActive }) => isActive ? 'active' : ''}>
              <i className="icon">🧠</i>
              <span>Study Sessions</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/active-recall" className={({ isActive }) => isActive ? 'active' : ''}>
              <i className="icon">🎯</i>
              <span>Active Recall</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/schedule" className={({ isActive }) => isActive ? 'active' : ''}>
              <i className="icon">📆</i>
              <span>Schedule</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/analytics" className={({ isActive }) => isActive ? 'active' : ''}>
              <i className="icon">📈</i>
              <span>Analytics</span>
            </NavLink>
          </li>
        </ul>
      </nav>
      
      <div className="sidebar-footer">
        <div className="progress-widget">
          <h3>Today's Progress</h3>
          <div className="progress-bar">
            <div className="progress" style={{ width: '60%' }}></div>
          </div>
          <p>12/20 minutes studied</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;