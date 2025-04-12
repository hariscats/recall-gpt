import React, { useState } from 'react';

const Profile = () => {
  const [activeTab, setActiveTab] = useState('info');
  
  // Dummy user data
  const userData = {
    id: "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
    username: "learner42",
    email: "user@example.com",
    fullName: "Jane Doe",
    joinDate: "September 15, 2023",
    preferences: {
      preferredTopics: ["python", "machine learning", "data structures"],
      learningPace: "medium",
      notificationEnabled: true,
      dailySessionGoal: 30,
      difficultyPreference: "adaptive"
    },
    proficiency: {
      python: 0.75,
      "machine learning": 0.45,
      "data structures": 0.6,
      algorithms: 0.55
    }
  };
  
  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-avatar">
          <span>{userData.fullName.split(' ').map(n => n[0]).join('')}</span>
        </div>
        <div className="profile-info">
          <h1>{userData.fullName}</h1>
          <p className="username">@{userData.username}</p>
          <p className="join-date">Member since {userData.joinDate}</p>
        </div>
      </div>
      
      <div className="profile-nav">
        <button 
          className={`profile-nav-btn ${activeTab === 'info' ? 'active' : ''}`}
          onClick={() => setActiveTab('info')}
        >
          Personal Info
        </button>
        <button 
          className={`profile-nav-btn ${activeTab === 'preferences' ? 'active' : ''}`}
          onClick={() => setActiveTab('preferences')}
        >
          Learning Preferences
        </button>
        <button 
          className={`profile-nav-btn ${activeTab === 'proficiency' ? 'active' : ''}`}
          onClick={() => setActiveTab('proficiency')}
        >
          Topic Proficiency
        </button>
      </div>
      
      <div className="profile-content">
        {activeTab === 'info' && (
          <div className="profile-section">
            <h2>Personal Information</h2>
            <div className="card">
              <form className="profile-form">
                <div className="form-group">
                  <label>Username</label>
                  <input type="text" className="form-control" defaultValue={userData.username} />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input type="email" className="form-control" defaultValue={userData.email} />
                </div>
                <div className="form-group">
                  <label>Full Name</label>
                  <input type="text" className="form-control" defaultValue={userData.fullName} />
                </div>
                <div className="form-group">
                  <label>Password</label>
                  <button className="btn btn-secondary">Change Password</button>
                </div>
                
                <button className="btn btn-primary">Save Changes</button>
              </form>
            </div>
          </div>
        )}
        
        {activeTab === 'preferences' && (
          <div className="profile-section">
            <h2>Learning Preferences</h2>
            <div className="card">
              <form className="profile-form">
                <div className="form-group">
                  <label>Preferred Topics</label>
                  <div className="topic-tags">
                    {userData.preferences.preferredTopics.map(topic => (
                      <span className="topic-tag" key={topic}>
                        {topic}
                        <button className="remove-topic-btn">×</button>
                      </span>
                    ))}
                    <button className="btn btn-sm btn-secondary">+ Add Topic</button>
                  </div>
                </div>
                
                <div className="form-group">
                  <label>Learning Pace</label>
                  <select className="form-control" defaultValue={userData.preferences.learningPace}>
                    <option value="slow">Slow</option>
                    <option value="medium">Medium</option>
                    <option value="fast">Fast</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Daily Session Goal (minutes)</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    defaultValue={userData.preferences.dailySessionGoal}
                    min="5"
                    max="120"
                    step="5"
                  />
                </div>
                
                <div className="form-group">
                  <label>Difficulty Preference</label>
                  <select className="form-control" defaultValue={userData.preferences.difficultyPreference}>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                    <option value="adaptive">Adaptive (AI-adjusted)</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label className="checkbox-label">
                    <input 
                      type="checkbox" 
                      defaultChecked={userData.preferences.notificationEnabled}
                    />
                    Enable Notifications
                  </label>
                </div>
                
                <button className="btn btn-primary">Save Preferences</button>
              </form>
            </div>
          </div>
        )}
        
        {activeTab === 'proficiency' && (
          <div className="profile-section">
            <h2>Topic Proficiency</h2>
            <div className="card">
              <div className="proficiency-stats">
                {Object.entries(userData.proficiency).map(([topic, level]) => (
                  <div className="proficiency-item" key={topic}>
                    <div className="proficiency-topic">
                      <h4>{topic}</h4>
                      <span className="proficiency-percentage">{Math.round(level * 100)}%</span>
                    </div>
                    <div className="proficiency-bar-container">
                      <div 
                        className="proficiency-bar" 
                        style={{ width: `${level * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;