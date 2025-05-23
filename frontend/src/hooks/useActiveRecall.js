/**
 * React Hook for Active Recall Functionality
 * Provides state management and actions for active recall features
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import activeRecallService, { QUESTION_TYPES, DIFFICULTY_LEVELS } from '../services/activeRecallService';

/**
 * Custom hook for managing active recall state
 * @param {string} userId - Current user ID
 * @param {Object} options - Hook configuration options
 * @returns {Object} Active recall state and actions
 */
export const useActiveRecall = (userId, options = {}) => {
  // State management
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [schedule, setSchedule] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionStats, setSessionStats] = useState({
    correct: 0,
    incorrect: 0,
    total: 0,
    timeSpent: 0,
    averageConfidence: 0
  });

  // Timer for tracking question time
  const startTimeRef = useRef(null);
  const [timeSpent, setTimeSpent] = useState(0);

  // Configuration
  const config = {
    autoAdvance: options.autoAdvance || false,
    showFeedback: options.showFeedback !== false,
    timeLimit: options.timeLimit || null,
    ...options
  };

  /**
   * Generate questions from learning material
   */
  const generateQuestions = useCallback(async (materialId, questionOptions = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await activeRecallService.generateQuestions(materialId, questionOptions);
      
      if (result.success) {
        setQuestions(result.questions);
        setCurrentQuestionIndex(0);
        setCurrentQuestion(result.questions[0] || null);
        setSessionStats({
          correct: 0,
          incorrect: 0,
          total: result.questions.length,
          timeSpent: 0,
          averageConfidence: 0
        });
        
        // Start timer for first question
        startTimeRef.current = Date.now();
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to generate questions');
      console.error('Error generating questions:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Load a specific question
   */
  const loadQuestion = useCallback(async (questionId) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await activeRecallService.getQuestion(questionId);
      
      if (result.success) {
        setCurrentQuestion(result.question);
        startTimeRef.current = Date.now();
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to load question');
      console.error('Error loading question:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Submit answer for current question
   */
  const submitAnswer = useCallback(async (answer, confidence = 3) => {
    if (!currentQuestion) return;

    setLoading(true);
    setError(null);

    const endTime = Date.now();
    const questionTimeSpent = startTimeRef.current ? 
      Math.round((endTime - startTimeRef.current) / 1000) : 0;

    try {
      const result = await activeRecallService.submitQuestionResponse(
        currentQuestion.id,
        {
          answer,
          timeSpent: questionTimeSpent,
          confidence,
          metadata: {
            questionIndex: currentQuestionIndex,
            sessionId: Date.now() // Simple session tracking
          }
        }
      );

      if (result.success) {
        setFeedback(result);
          // Update session stats
        setSessionStats(prev => ({
          ...prev,
          correct: prev.correct + (result.isCorrect ? 1 : 0),
          incorrect: prev.incorrect + (result.isCorrect ? 0 : 1),
          timeSpent: prev.timeSpent + questionTimeSpent,
          averageConfidence: (prev.averageConfidence * currentQuestionIndex + confidence) / (currentQuestionIndex + 1)
        }));
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to submit answer');
      console.error('Error submitting answer:', err);
    } finally {
      setLoading(false);
    }
  }, [currentQuestion, currentQuestionIndex]);

  /**
   * Move to next question
   */
  const nextQuestion = useCallback(() => {
    const nextIndex = currentQuestionIndex + 1;
    
    if (nextIndex < questions.length) {
      setCurrentQuestionIndex(nextIndex);
      setCurrentQuestion(questions[nextIndex]);
      setUserAnswer('');
      setFeedback(null);
      startTimeRef.current = Date.now();
    } else {
      // Session completed
      setCurrentQuestion(null);
      setFeedback(null);
    }
  }, [currentQuestionIndex, questions]);

  /**
   * Move to previous question
   */
  const previousQuestion = useCallback(() => {
    const prevIndex = currentQuestionIndex - 1;
    
    if (prevIndex >= 0) {
      setCurrentQuestionIndex(prevIndex);
      setCurrentQuestion(questions[prevIndex]);
      setUserAnswer('');
      setFeedback(null);
      startTimeRef.current = Date.now();
    }
  }, [currentQuestionIndex, questions]);

  /**
   * Load user's active recall schedule
   */
  const loadSchedule = useCallback(async (date = null) => {
    if (!userId) return;

    setLoading(true);
    setError(null);

    try {
      const result = await activeRecallService.getActiveRecallSchedule(userId, {
        date: date || new Date().toISOString().split('T')[0]
      });

      if (result.success) {
        setSchedule(result.schedule);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to load schedule');
      console.error('Error loading schedule:', err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  /**
   * Load learning analytics
   */
  const loadAnalytics = useCallback(async (timeRange = '30d') => {
    if (!userId) return;

    try {
      const result = await activeRecallService.getLearningAnalytics(userId, {
        timeRange,
        includeDetails: true
      });

      if (result.success) {
        setAnalytics(result);
      } else {
        console.warn('Failed to load analytics:', result.error);
      }
    } catch (err) {
      console.error('Error loading analytics:', err);
    }
  }, [userId]);

  /**
   * Reset current session
   */
  const resetSession = useCallback(() => {
    setQuestions([]);
    setCurrentQuestion(null);
    setCurrentQuestionIndex(0);
    setUserAnswer('');
    setFeedback(null);
    setError(null);
    setSessionStats({
      correct: 0,
      incorrect: 0,
      total: 0,
      timeSpent: 0,
      averageConfidence: 0
    });
    startTimeRef.current = null;
  }, []);

  /**
   * Timer effect for tracking time spent on current question
   */
  useEffect(() => {
    let interval;
    
    if (currentQuestion && startTimeRef.current) {
      interval = setInterval(() => {
        const elapsed = Math.round((Date.now() - startTimeRef.current) / 1000);
        setTimeSpent(elapsed);
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [currentQuestion]);

  /**
   * Load initial data when userId changes
   */
  useEffect(() => {
    if (userId) {
      loadSchedule();
      loadAnalytics();
    }
  }, [userId, loadSchedule, loadAnalytics]);

  // Computed values
  const isSessionComplete = questions.length > 0 && currentQuestionIndex >= questions.length;
  const hasNextQuestion = currentQuestionIndex < questions.length - 1;
  const hasPreviousQuestion = currentQuestionIndex > 0;
  const progress = questions.length > 0 ? (currentQuestionIndex / questions.length) * 100 : 0;
  const completedProgress = questions.length > 0 ? ((currentQuestionIndex + (feedback ? 1 : 0)) / questions.length) * 100 : 0;

  return {
    // State
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

    // Computed values
    isSessionComplete,
    hasNextQuestion,
    hasPreviousQuestion,
    progress,
    completedProgress,

    // Actions
    generateQuestions,
    loadQuestion,
    submitAnswer,
    nextQuestion,
    previousQuestion,
    loadSchedule,
    loadAnalytics,
    resetSession,
    setUserAnswer,
    setError: (err) => setError(err),
    clearError: () => setError(null),

    // Configuration
    config,
    
    // Constants
    QUESTION_TYPES,
    DIFFICULTY_LEVELS
  };
};

export default useActiveRecall;
