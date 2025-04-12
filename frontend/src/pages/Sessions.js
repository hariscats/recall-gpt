import React, { useState } from 'react';

const Sessions = () => {
  const [sessionType, setSessionType] = useState('new');

  // Dummy data for sessions history
  const sessionsHistory = [
    {
      id: 's123',
      date: 'Oct 15, 2023',
      duration: '25 mins',
      type: 'mixed',
      topicsCovered: ['Python', 'Data Structures'],
      performance: 85
    },
    {
      id: 's124',
      date: 'Oct 14, 2023',
      duration: '40 mins',
      type: 'review',
      topicsCovered: ['Algorithms', 'Problem Solving'],
      performance: 92
    },
    {
      id: 's125',
      date: 'Oct 12, 2023',
      duration: '15 mins',
      type: 'new_content',
      topicsCovered: ['Machine Learning'],
      performance: 78
    }
  ];

  return (
    <div className="sessions-page">
      <h1>Study Sessions</h1>
      
      <div className="card">
        <div className="card-header">
          <h2>Start a New Session</h2>
        </div>
        <div className="session-options">
          <div className="form-group">
            <label>Session Type</label>
            <div className="session-type-selector">
              <button 
                className={`session-type-btn ${sessionType === 'new' ? 'active' : ''}`}
                onClick={() => setSessionType('new')}
              >
                Learn New Content
              </button>
              <button 
                className={`session-type-btn ${sessionType === 'review' ? 'active' : ''}`}
                onClick={() => setSessionType('review')}
              >
                Review Material
              </button>
              <button 
                className={`session-type-btn ${sessionType === 'mixed' ? 'active' : ''}`}
                onClick={() => setSessionType('mixed')}
              >
                Mixed Session
              </button>
            </div>
          </div>
          
          <div className="form-group">
            <label>Topics to Focus On (Optional)</label>
            <select className="form-control">
              <option value="">All Topics</option>
              <option value="python">Python</option>
              <option value="algorithms">Algorithms</option>
              <option value="data-structures">Data Structures</option>
              <option value="machine-learning">Machine Learning</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Session Duration</label>
            <select className="form-control">
              <option value="10">10 minutes</option>
              <option value="15">15 minutes</option>
              <option value="20" selected>20 minutes</option>
              <option value="30">30 minutes</option>
              <option value="45">45 minutes</option>
              <option value="60">1 hour</option>
            </select>
          </div>
          
          <button className="btn btn-primary start-session-btn">Start Session</button>
        </div>
      </div>
      
      <div className="card session-history-card">
        <div className="card-header">
          <h2>Previous Sessions</h2>
        </div>
        <div className="session-history">
          <table className="sessions-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Duration</th>
                <th>Type</th>
                <th>Topics</th>
                <th>Performance</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sessionsHistory.map(session => (
                <tr key={session.id}>
                  <td>{session.date}</td>
                  <td>{session.duration}</td>
                  <td>
                    <span className={`session-type ${session.type}`}>
                      {session.type === 'new_content' ? 'New Content' : 
                       session.type === 'review' ? 'Review' : 'Mixed'}
                    </span>
                  </td>
                  <td>
                    {session.topicsCovered.map(topic => (
                      <span className="session-topic" key={topic}>{topic}</span>
                    ))}
                  </td>
                  <td>
                    <div className="performance-bar-container">
                      <div 
                        className="performance-bar" 
                        style={{ width: `${session.performance}%`, backgroundColor: 
                          session.performance > 85 ? '#4CAF50' : 
                          session.performance > 70 ? '#FFC107' : '#F44336'
                        }}
                      ></div>
                      <span>{session.performance}%</span>
                    </div>
                  </td>
                  <td>
                    <button className="btn btn-sm btn-secondary">Details</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Sessions;