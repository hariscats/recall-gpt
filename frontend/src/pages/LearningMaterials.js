import React, { useState } from 'react';

const LearningMaterials = () => {
  const [activeTab, setActiveTab] = useState('all');
  
  // Dummy data
  const materials = [
    {
      id: 1,
      title: 'Introduction to Python Variables',
      description: 'Learn about variables and data types in Python',
      topics: ['python', 'programming basics'],
      difficulty: 0.2,
      type: 'article',
      estimatedTime: 10
    },
    {
      id: 2,
      title: 'Understanding Big O Notation',
      description: 'Learn about time complexity and algorithm efficiency',
      topics: ['algorithms', 'computer science'],
      difficulty: 0.4,
      type: 'article',
      estimatedTime: 15
    },
    {
      id: 3,
      title: 'Recursion Practice',
      description: 'Hands-on exercises to master recursive algorithms',
      topics: ['algorithms', 'problem solving'],
      difficulty: 0.6,
      type: 'interactive',
      estimatedTime: 20
    },
    {
      id: 4,
      title: 'Machine Learning Fundamentals',
      description: 'Introduction to core concepts in machine learning',
      topics: ['machine learning', 'data science'],
      difficulty: 0.7,
      type: 'video',
      estimatedTime: 30
    }
  ];
  
  const filterMaterials = () => {
    if (activeTab === 'all') return materials;
    return materials.filter(material => material.type === activeTab);
  };
  
  const getDifficultyLabel = (difficulty) => {
    if (difficulty < 0.3) return 'Beginner';
    if (difficulty < 0.6) return 'Intermediate';
    return 'Advanced';
  };
  
  return (
    <div className="learning-materials">
      <div className="page-header">
        <h1>Learning Materials</h1>
        <button className="btn btn-primary">Upload New Material</button>
      </div>
      
      <div className="filter-tabs">
        <button 
          className={`filter-tab ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          All
        </button>
        <button 
          className={`filter-tab ${activeTab === 'article' ? 'active' : ''}`}
          onClick={() => setActiveTab('article')}
        >
          Articles
        </button>
        <button 
          className={`filter-tab ${activeTab === 'video' ? 'active' : ''}`}
          onClick={() => setActiveTab('video')}
        >
          Videos
        </button>
        <button 
          className={`filter-tab ${activeTab === 'interactive' ? 'active' : ''}`}
          onClick={() => setActiveTab('interactive')}
        >
          Interactive
        </button>
      </div>
      
      <div className="search-bar">
        <input 
          type="text" 
          placeholder="Search materials..." 
          className="form-control"
        />
      </div>
      
      <div className="materials-grid">
        {filterMaterials().map(material => (
          <div className="material-card" key={material.id}>
            <div className="material-card-header">
              <span className="material-type">{material.type}</span>
              <span className="material-difficulty">{getDifficultyLabel(material.difficulty)}</span>
            </div>
            <h4>{material.title}</h4>
            <p>{material.description}</p>
            <div className="material-topics">
              {material.topics.map(topic => (
                <span className="topic-tag" key={topic}>{topic}</span>
              ))}
            </div>
            <div className="material-footer">
              <span>{material.estimatedTime} min</span>
              <button className="btn btn-primary btn-sm">Study Now</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LearningMaterials;