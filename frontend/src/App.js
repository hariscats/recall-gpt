import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';

// Pages
import Dashboard from './pages/Dashboard';
import LearningMaterials from './pages/LearningMaterials';
import Sessions from './pages/Sessions';
import Profile from './pages/Profile';
import ActiveRecall from './pages/ActiveRecall';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <div className="main-container">
          <Sidebar />
          <main className="content">            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/materials" element={<LearningMaterials />} />
              <Route path="/sessions" element={<Sessions />} />
              <Route path="/active-recall" element={<ActiveRecall />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;