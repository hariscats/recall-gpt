import React from 'react';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="stats-overview">
        <div className="card stat-card">
          <h3>Learning Streak</h3>
          <div className="stat-value">7 Days</div>
          <p>Keep up the great work!</p>
        </div>
        
        <div className="card stat-card">
          <h3>Topics Studied</h3>
          <div className="stat-value">4</div>
          <p>Explore more topics to expand your knowledge.</p>
        </div>
        
        <div className="card stat-card">
          <h3>Time Studied</h3>
          <div className="stat-value">3.5 Hours</div>
          <p>This week</p>
        </div>
      </div>
      
      <div className="dashboard-section">
        <div className="card">
          <div className="card-header">
            <h2>Today's Schedule</h2>
            <button className="btn btn-primary">Start Session</button>
          </div>
          
          <div className="schedule-items">
            <div className="schedule-item">
              <div className="schedule-item-time">9:00 AM</div>
              <div className="schedule-item-content">
                <h4>Python Basics Review</h4>
                <p>Variables, Data Types and Functions</p>
              </div>
              <div className="schedule-item-duration">15 min</div>
            </div>
            
            <div className="schedule-item">
              <div className="schedule-item-time">2:30 PM</div>
              <div className="schedule-item-content">
                <h4>Machine Learning Concepts</h4>
                <p>Introduction to Neural Networks</p>
              </div>
              <div className="schedule-item-duration">20 min</div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="dashboard-section">
        <div className="card">
          <div className="card-header">
            <h2>Recent Activity</h2>
            <a href="/analytics">View All</a>
          </div>
          
          <div className="activity-timeline">
            <div className="activity-item">
              <div className="activity-icon">✅</div>
              <div className="activity-content">
                <h4>Completed "Introduction to Data Structures"</h4>
                <p>2 hours ago</p>
              </div>
            </div>
            
            <div className="activity-item">
              <div className="activity-icon">📝</div>
              <div className="activity-content">
                <h4>Scored 85% on "Python Fundamentals" quiz</h4>
                <p>Yesterday</p>
              </div>
            </div>
            
            <div className="activity-item">
              <div className="activity-icon">🏆</div>
              <div className="activity-content">
                <h4>Earned "Consistent Learner" badge</h4>
                <p>3 days ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="dashboard-section">
        <div className="card">
          <div className="card-header">
            <h2>Recommended Materials</h2>
            <a href="/materials">View All</a>
          </div>
          
          <div className="material-recommendations">
            <div className="material-card">
              <div className="material-card-header">
                <span className="material-type">Article</span>
                <span className="material-difficulty">Beginner</span>
              </div>
              <h4>Understanding Big O Notation</h4>
              <p>Learn about time complexity and algorithm efficiency</p>
              <div className="material-footer">
                <span>10 min read</span>
                <button className="btn btn-primary btn-sm">Study Now</button>
              </div>
            </div>
            
            <div className="material-card">
              <div className="material-card-header">
                <span className="material-type">Interactive</span>
                <span className="material-difficulty">Intermediate</span>
              </div>
              <h4>Recursion Practice</h4>
              <p>Hands-on exercises to master recursive algorithms</p>
              <div className="material-footer">
                <span>15 min practice</span>
                <button className="btn btn-primary btn-sm">Start</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;