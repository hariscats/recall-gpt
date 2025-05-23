/**
 * Active Recall Page Component
 * Main page for active recall learning sessions
 */

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import useActiveRecall from '../hooks/useActiveRecall';
import ActiveRecallQuestion from '../components/ActiveRecallQuestion';
import { SAMPLE_LEARNING_MATERIALS } from '../services/mockData';
import './ActiveRecall.css';

const ActiveRecall = () => {
  const [searchParams] = useSearchParams();
  const urlMaterialId = searchParams.get('materialId');
  const userId = 'user_1'; // In a real app, get this from auth context
  
  // Use a default material for testing if none provided
  const materialId = urlMaterialId || 'material_1';
  
  // State for question generation settings
  const [generationSettings, setGenerationSettings] = useState({
    questionType: 'MULTIPLE_CHOICE',
    difficulty: 'BEGINNER',
    numQuestions: 5,
    focusAreas: []
  });
  
  const [showSettings, setShowSettings] = useState(false);
  const [showSessionComplete, setShowSessionComplete] = useState(false);

  // Use the active recall hook
  const {
    questions,
    currentQuestion,
    currentQuestionIndex,
    userAnswer,
    feedback,
    schedule,
    analytics,
    loading,
    error,
    sessionStats,
    timeSpent,
    isSessionComplete,
    hasNextQuestion,
    hasPreviousQuestion,
    progress,
    generateQuestions,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    loadSchedule,
    resetSession,
    setUserAnswer,
    clearError,
    QUESTION_TYPES,
    DIFFICULTY_LEVELS
  } = useActiveRecall(userId);

  // Generate questions on component mount if materialId is provided
  useEffect(() => {
    if (materialId && questions.length === 0) {
      handleGenerateQuestions();
    }
  }, [materialId]);

  // Show session complete when all questions are answered
  useEffect(() => {
    if (isSessionComplete && !showSessionComplete) {
      setShowSessionComplete(true);
    }
  }, [isSessionComplete, showSessionComplete]);

  const handleGenerateQuestions = async () => {
    if (!materialId) {
      alert('Please select a learning material first.');
      return;
    }

    clearError();
    await generateQuestions(materialId, generationSettings);
    setShowSettings(false);
    setShowSessionComplete(false);
  };

  const handleAnswerSubmit = async (answer, confidence) => {
    await submitAnswer(answer, confidence);
  };

  const handleNextQuestion = () => {
    if (hasNextQuestion) {
      nextQuestion();
    } else if (isSessionComplete) {
      setShowSessionComplete(true);
    }
  };

  const handleStartNewSession = () => {
    resetSession();
    setShowSessionComplete(false);
    setShowSettings(true);
  };
  const renderGenerationSettings = () => (
    <div className="generation-settings">
      <h3>Question Generation Settings</h3>
      
      <div className="setting-group">
        <label>Learning Material:</label>
        <select
          value={materialId}
          onChange={(e) => {
            // In a real app, you'd update the URL or material selection
            console.log('Material changed to:', e.target.value);
          }}
        >
          {SAMPLE_LEARNING_MATERIALS.map((material) => (
            <option key={material.id} value={material.id}>
              {material.title}
            </option>
          ))}
        </select>
      </div>

      <div className="setting-group">
        <label>Question Type:</label>
        <select
          value={generationSettings.questionType}
          onChange={(e) => setGenerationSettings(prev => ({
            ...prev,
            questionType: e.target.value
          }))}
        >
          {Object.entries(QUESTION_TYPES).map(([key, value]) => (
            <option key={key} value={value}>
              {key.replace('_', ' ')}
            </option>
          ))}
        </select>
      </div>

      <div className="setting-group">
        <label>Difficulty Level:</label>
        <select
          value={generationSettings.difficulty}
          onChange={(e) => setGenerationSettings(prev => ({
            ...prev,
            difficulty: e.target.value
          }))}
        >
          {Object.entries(DIFFICULTY_LEVELS).map(([key, value]) => (
            <option key={key} value={value}>
              {key}
            </option>
          ))}
        </select>
      </div>

      <div className="setting-group">
        <label>Number of Questions:</label>
        <input
          type="number"
          min="1"
          max="20"
          value={generationSettings.numQuestions}
          onChange={(e) => setGenerationSettings(prev => ({
            ...prev,
            numQuestions: parseInt(e.target.value) || 5
          }))}
        />
      </div>

      <div className="settings-actions">
        <button
          className="generate-button"
          onClick={handleGenerateQuestions}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Questions'}
        </button>
        
        <button
          className="cancel-button"
          onClick={() => setShowSettings(false)}
        >
          Cancel
        </button>
      </div>
    </div>
  );

  const renderSessionComplete = () => (
    <div className="session-complete">
      <div className="completion-header">
        <h2>🎉 Session Complete!</h2>
        <p>Great work! You've completed this active recall session.</p>
      </div>

      <div className="session-stats">
        <div className="stat-item">
          <span className="stat-value">{sessionStats.correct}</span>
          <span className="stat-label">Correct</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{sessionStats.incorrect}</span>
          <span className="stat-label">Incorrect</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">
            {Math.round((sessionStats.correct / sessionStats.total) * 100)}%
          </span>
          <span className="stat-label">Accuracy</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">
            {Math.floor(sessionStats.timeSpent / 60)}:{(sessionStats.timeSpent % 60).toString().padStart(2, '0')}
          </span>
          <span className="stat-label">Time</span>
        </div>
      </div>

      <div className="completion-actions">
        <button
          className="new-session-button"
          onClick={handleStartNewSession}
        >
          Start New Session
        </button>
        
        <button
          className="view-schedule-button"
          onClick={() => loadSchedule()}
        >
          View Schedule
        </button>
      </div>
    </div>
  );

  const renderScheduleItems = () => {
    if (!schedule.length) return null;

    return (
      <div className="schedule-section">
        <h3>Today's Active Recall Schedule</h3>
        <div className="schedule-items">
          {schedule.slice(0, 5).map((item, index) => (
            <div key={index} className="schedule-item">
              <div className="schedule-content">
                <h4>{item.title || 'Learning Material'}</h4>
                <p>{item.description || 'Ready for review'}</p>
              </div>
              <div className="schedule-meta">
                <span className="due-time">
                  Due: {new Date(item.due_date).toLocaleTimeString()}
                </span>
                <span className={`priority ${item.priority || 'medium'}`}>
                  {item.priority || 'medium'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="active-recall-page">
      <div className="page-header">
        <h1>Active Recall Learning</h1>
        <p>Challenge yourself with AI-generated questions to reinforce your learning.</p>
        
        {!currentQuestion && !showSessionComplete && (
          <button
            className="settings-button"
            onClick={() => setShowSettings(true)}
          >
            Generate Questions
          </button>
        )}
      </div>

      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={clearError}>×</button>
        </div>
      )}

      <div className="page-content">
        {showSettings && renderGenerationSettings()}
        
        {showSessionComplete && renderSessionComplete()}
        
        {currentQuestion && !showSessionComplete && (
          <ActiveRecallQuestion
            question={currentQuestion}
            userAnswer={userAnswer}
            onAnswerChange={setUserAnswer}
            onSubmit={handleAnswerSubmit}
            feedback={feedback}
            loading={loading}
            timeSpent={timeSpent}
            currentIndex={currentQuestionIndex}
            totalQuestions={questions.length}
            onNext={handleNextQuestion}
            onPrevious={previousQuestion}
            hasNext={hasNextQuestion || isSessionComplete}
            hasPrevious={hasPreviousQuestion}
          />
        )}

        {!currentQuestion && !showSettings && !showSessionComplete && (
          <div className="welcome-section">
            <div className="welcome-content">
              <h2>Welcome to Active Recall</h2>
              <p>
                Active recall is a powerful learning technique that challenges your memory
                and strengthens neural pathways through targeted questioning.
              </p>
              
              <div className="features">
                <div className="feature">
                  <span className="feature-icon">🧠</span>
                  <h3>AI-Generated Questions</h3>
                  <p>Personalized questions based on your learning materials</p>
                </div>
                
                <div className="feature">
                  <span className="feature-icon">📅</span>
                  <h3>Spaced Repetition</h3>
                  <p>Optimized review schedule for long-term retention</p>
                </div>
                
                <div className="feature">
                  <span className="feature-icon">📊</span>
                  <h3>Progress Tracking</h3>
                  <p>Monitor your performance and learning analytics</p>
                </div>
              </div>

              {materialId ? (
                <button
                  className="start-button"
                  onClick={() => setShowSettings(true)}
                >
                  Start Learning Session
                </button>
              ) : (
                <div className="no-material">
                  <p>Select a learning material to begin your active recall session.</p>
                  <a href="/materials" className="select-material-link">
                    Browse Learning Materials →
                  </a>
                </div>
              )}
            </div>

            {renderScheduleItems()}
          </div>
        )}
      </div>
    </div>
  );
};

export default ActiveRecall;
