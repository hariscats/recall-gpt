/**
 * Active Recall Question Component
 * Interactive component for displaying and answering questions
 */

import React, { useState } from 'react';
import './ActiveRecallQuestion.css';

const ActiveRecallQuestion = ({
  question,
  userAnswer,
  onAnswerChange,
  onSubmit,
  feedback,
  loading,
  timeSpent,
  showTimer = true,
  showProgress = true,
  currentIndex = 0,
  totalQuestions = 0,
  onNext,
  onPrevious,
  hasNext = false,
  hasPrevious = false
}) => {
  const [confidence, setConfidence] = useState(3);
  const [showExplanation, setShowExplanation] = useState(false);

  if (!question) {
    return (
      <div className="active-recall-question empty">
        <div className="empty-state">
          <h3>No question available</h3>
          <p>Generate questions from your learning materials to get started.</p>
        </div>
      </div>
    );
  }

  const handleSubmit = () => {
    if (userAnswer.trim()) {
      onSubmit(userAnswer.trim(), confidence);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && userAnswer.trim()) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const renderQuestionContent = () => {
    switch (question.type) {
      case 'MULTIPLE_CHOICE':
        return (
          <div className="question-options">
            {question.options?.map((option, index) => (
              <label key={index} className="option-label">
                <input
                  type="radio"
                  name="question-option"
                  value={option.text || option}
                  checked={userAnswer === (option.text || option)}
                  onChange={(e) => onAnswerChange(e.target.value)}
                  disabled={feedback}
                />
                <span className="option-text">{option.text || option}</span>
              </label>
            ))}
          </div>
        );

      case 'TRUE_FALSE':
        return (
          <div className="question-options true-false">
            <label className="option-label">
              <input
                type="radio"
                name="question-option"
                value="true"
                checked={userAnswer === 'true'}
                onChange={(e) => onAnswerChange(e.target.value)}
                disabled={feedback}
              />
              <span className="option-text">True</span>
            </label>
            <label className="option-label">
              <input
                type="radio"
                name="question-option"
                value="false"
                checked={userAnswer === 'false'}
                onChange={(e) => onAnswerChange(e.target.value)}
                disabled={feedback}
              />
              <span className="option-text">False</span>
            </label>
          </div>
        );

      case 'FILL_IN_BLANK':
      case 'SHORT_ANSWER':
      default:
        return (
          <div className="question-input">
            <textarea
              value={userAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your answer here..."
              disabled={feedback}
              rows={question.type === 'SHORT_ANSWER' ? 4 : 2}
              className="answer-textarea"
            />
          </div>
        );
    }
  };

  const renderFeedback = () => {
    if (!feedback) return null;

    return (
      <div className={`feedback ${feedback.isCorrect ? 'correct' : 'incorrect'}`}>
        <div className="feedback-header">
          <span className={`feedback-icon ${feedback.isCorrect ? 'correct' : 'incorrect'}`}>
            {feedback.isCorrect ? '✓' : '✗'}
          </span>
          <span className="feedback-text">
            {feedback.isCorrect ? 'Correct!' : 'Incorrect'}
          </span>
          <span className="confidence-score">
            Confidence: {Math.round(feedback.confidenceScore * 100)}%
          </span>
        </div>
        
        {feedback.explanation && (
          <div className="feedback-explanation">
            <button
              className="explanation-toggle"
              onClick={() => setShowExplanation(!showExplanation)}
            >
              {showExplanation ? 'Hide' : 'Show'} Explanation
            </button>
            {showExplanation && (
              <div className="explanation-content">
                {feedback.explanation}
              </div>
            )}
          </div>
        )}

        {feedback.nextReviewDate && (
          <div className="next-review">
            <small>Next review: {new Date(feedback.nextReviewDate).toLocaleDateString()}</small>
          </div>
        )}
      </div>
    );
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="active-recall-question">
      {/* Progress and Timer */}
      <div className="question-header">
        {showProgress && totalQuestions > 0 && (
          <div className="progress-info">
            <span className="question-counter">
              Question {currentIndex + 1} of {totalQuestions}
            </span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }}
              />
            </div>
          </div>
        )}
        
        {showTimer && (
          <div className="timer">
            <span className="timer-icon">⏱️</span>
            <span className="timer-text">{formatTime(timeSpent)}</span>
          </div>
        )}
      </div>

      {/* Question Content */}
      <div className="question-content">
        <div className="question-metadata">
          <span className={`difficulty ${question.difficulty?.toLowerCase()}`}>
            {question.difficulty}
          </span>
          <span className={`type ${question.type?.toLowerCase()}`}>
            {question.type?.replace('_', ' ')}
          </span>
        </div>

        <div className="question-text">
          <h3>{question.text}</h3>
          {question.context && (
            <div className="question-context">
              <p>{question.context}</p>
            </div>
          )}
        </div>

        {renderQuestionContent()}
      </div>

      {/* Confidence Slider */}
      {!feedback && (
        <div className="confidence-section">
          <label className="confidence-label">
            How confident are you in your answer?
          </label>
          <div className="confidence-slider">
            <input
              type="range"
              min="1"
              max="5"
              value={confidence}
              onChange={(e) => setConfidence(Number(e.target.value))}
              className="confidence-input"
            />
            <div className="confidence-labels">
              <span>Not Sure</span>
              <span>Very Sure</span>
            </div>
          </div>
        </div>
      )}      {/* Feedback */}
      {renderFeedback()}

      {/* Action Buttons */}
      <div className="question-actions">
        <button
          className="nav-button previous"
          onClick={onPrevious}
          disabled={!hasPrevious}
        >
          ← Previous
        </button>

        {!feedback ? (
          <button
            className="submit-button"
            onClick={handleSubmit}
            disabled={!userAnswer.trim() || loading}
          >
            {loading ? 'Submitting...' : 'Submit Answer'}
          </button>
        ) : (
          <button
            className="next-button"
            onClick={onNext}
            disabled={!hasNext}
          >
            {hasNext ? 'Next Question →' : 'Complete Session'}
          </button>
        )}
      </div>
    </div>
  );
};

export default ActiveRecallQuestion;
