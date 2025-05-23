/**
 * Mock Data Service for Active Recall Testing
 * Provides sample data for testing the active recall functionality
 */

export const SAMPLE_LEARNING_MATERIALS = [
  {
    id: 'material_1',
    title: 'Introduction to JavaScript',
    description: 'Fundamental concepts of JavaScript programming',
    content: `
      JavaScript is a versatile programming language primarily used for web development.
      It supports object-oriented, functional, and procedural programming paradigms.
      Key concepts include variables, functions, objects, arrays, and closures.
      JavaScript runs in browsers and also on servers using Node.js.
    `,
    difficulty: 'BEGINNER',
    estimatedDuration: 45,
    tags: ['javascript', 'programming', 'web-development']
  },
  {
    id: 'material_2',
    title: 'React Hooks Fundamentals',
    description: 'Understanding React Hooks and their usage',
    content: `
      React Hooks are functions that let you use state and other React features in functional components.
      Common hooks include useState for state management, useEffect for side effects,
      useCallback for memoizing functions, and useMemo for memoizing values.
      Custom hooks allow you to extract component logic into reusable functions.
    `,
    difficulty: 'INTERMEDIATE',
    estimatedDuration: 60,
    tags: ['react', 'hooks', 'frontend']
  },
  {
    id: 'material_3',
    title: 'Database Design Principles',
    description: 'Core principles of relational database design',
    content: `
      Database design involves organizing data efficiently and ensuring data integrity.
      Normalization reduces redundancy by dividing data into related tables.
      Primary keys uniquely identify records, while foreign keys establish relationships.
      ACID properties ensure database transactions are reliable and consistent.
    `,
    difficulty: 'ADVANCED',
    estimatedDuration: 90,
    tags: ['database', 'sql', 'design']
  }
];

export const SAMPLE_QUESTIONS = [
  {
    id: 'q1',
    materialId: 'material_1',
    type: 'MULTIPLE_CHOICE',
    difficulty: 'BEGINNER',
    text: 'Which of the following is NOT a programming paradigm supported by JavaScript?',
    options: [
      { text: 'Object-oriented', isCorrect: false },
      { text: 'Functional', isCorrect: false },
      { text: 'Procedural', isCorrect: false },
      { text: 'Assembly-based', isCorrect: true }
    ],
    correctAnswer: 'Assembly-based',
    explanation: 'JavaScript supports object-oriented, functional, and procedural programming paradigms, but not assembly-based programming.',
    context: 'JavaScript programming paradigms'
  },
  {
    id: 'q2',
    materialId: 'material_1',
    type: 'TRUE_FALSE',
    difficulty: 'BEGINNER',
    text: 'JavaScript can only run in web browsers.',
    correctAnswer: 'false',
    explanation: 'JavaScript can run in browsers and also on servers using Node.js, making it a versatile language for both frontend and backend development.',
    context: 'JavaScript runtime environments'
  },
  {
    id: 'q3',
    materialId: 'material_1',
    type: 'FILL_IN_BLANK',
    difficulty: 'BEGINNER',
    text: 'JavaScript supports ________, functional, and procedural programming paradigms.',
    correctAnswer: 'object-oriented',
    explanation: 'JavaScript is a multi-paradigm language that supports object-oriented programming along with functional and procedural approaches.',
    context: 'JavaScript programming paradigms'
  },
  {
    id: 'q4',
    materialId: 'material_2',
    type: 'MULTIPLE_CHOICE',
    difficulty: 'INTERMEDIATE',
    text: 'Which hook is used for memoizing functions in React?',
    options: [
      { text: 'useState', isCorrect: false },
      { text: 'useEffect', isCorrect: false },
      { text: 'useCallback', isCorrect: true },
      { text: 'useMemo', isCorrect: false }
    ],
    correctAnswer: 'useCallback',
    explanation: 'useCallback is used to memoize functions, while useMemo is used to memoize values. This helps optimize performance by preventing unnecessary re-renders.',
    context: 'React Hooks optimization'
  },
  {
    id: 'q5',
    materialId: 'material_2',
    type: 'SHORT_ANSWER',
    difficulty: 'INTERMEDIATE',
    text: 'Explain the purpose of custom hooks in React and provide an example use case.',
    correctAnswer: 'Custom hooks allow you to extract component logic into reusable functions that can be shared across multiple components.',
    explanation: 'Custom hooks enable code reuse and separation of concerns. For example, a useLocalStorage hook could manage localStorage operations across different components.',
    context: 'React custom hooks'
  },
  {
    id: 'q6',
    materialId: 'material_3',
    type: 'MULTIPLE_CHOICE',
    difficulty: 'ADVANCED',
    text: 'Which ACID property ensures that database transactions are processed reliably?',
    options: [
      { text: 'Atomicity', isCorrect: false },
      { text: 'Consistency', isCorrect: false },
      { text: 'Isolation', isCorrect: false },
      { text: 'All of the above', isCorrect: true }
    ],
    correctAnswer: 'All of the above',
    explanation: 'All ACID properties work together to ensure reliable transaction processing: Atomicity (all-or-nothing), Consistency (valid state), Isolation (concurrent transactions), and Durability (permanent changes).',
    context: 'Database ACID properties'
  }
];

export const SAMPLE_USER_SCHEDULE = [
  {
    id: 'schedule_1',
    userId: 'user_1',
    materialId: 'material_1',
    questionId: 'q1',
    scheduledDate: new Date().toISOString(),
    reviewCount: 0,
    difficulty: 2.5,
    lastReviewed: null,
    nextReview: new Date().toISOString(),
    status: 'DUE'
  },
  {
    id: 'schedule_2',
    userId: 'user_1',
    materialId: 'material_1',
    questionId: 'q2',
    scheduledDate: new Date(Date.now() + 86400000).toISOString(), // Tomorrow
    reviewCount: 1,
    difficulty: 2.0,
    lastReviewed: new Date(Date.now() - 86400000).toISOString(), // Yesterday
    nextReview: new Date(Date.now() + 86400000).toISOString(),
    status: 'SCHEDULED'
  },
  {
    id: 'schedule_3',
    userId: 'user_1',
    materialId: 'material_2',
    questionId: 'q4',
    scheduledDate: new Date().toISOString(),
    reviewCount: 0,
    difficulty: 3.0,
    lastReviewed: null,
    nextReview: new Date().toISOString(),
    status: 'DUE'
  }
];

export const SAMPLE_ANALYTICS = {
  success: true,
  timeRange: '30d',
  totalQuestions: 25,
  correctAnswers: 18,
  incorrectAnswers: 7,
  averageConfidence: 3.2,
  averageResponseTime: 12.5,
  streakCurrent: 5,
  streakLongest: 12,
  difficultyBreakdown: {
    BEGINNER: { total: 10, correct: 9, incorrect: 1 },
    INTERMEDIATE: { total: 10, correct: 7, incorrect: 3 },
    ADVANCED: { total: 5, correct: 2, incorrect: 3 }
  },
  typeBreakdown: {
    MULTIPLE_CHOICE: { total: 12, correct: 10, incorrect: 2 },
    TRUE_FALSE: { total: 8, correct: 6, incorrect: 2 },
    FILL_IN_BLANK: { total: 3, correct: 1, incorrect: 2 },
    SHORT_ANSWER: { total: 2, correct: 1, incorrect: 1 }
  },
  dailyStats: [
    { date: '2025-05-17', questions: 3, correct: 2, timeSpent: 45 },
    { date: '2025-05-18', questions: 5, correct: 4, timeSpent: 67 },
    { date: '2025-05-19', questions: 2, correct: 2, timeSpent: 23 },
    { date: '2025-05-20', questions: 4, correct: 3, timeSpent: 52 },
    { date: '2025-05-21', questions: 6, correct: 4, timeSpent: 78 },
    { date: '2025-05-22', questions: 3, correct: 2, timeSpent: 41 },
    { date: '2025-05-23', questions: 2, correct: 1, timeSpent: 28 }
  ]
};

/**
 * Mock API responses for testing
 */
export class MockActiveRecallAPI {
  constructor() {
    this.questions = [...SAMPLE_QUESTIONS];
    this.materials = [...SAMPLE_LEARNING_MATERIALS];
    this.schedules = [...SAMPLE_USER_SCHEDULE];
    this.analytics = { ...SAMPLE_ANALYTICS };
  }

  // Simulate API delay
  async delay(ms = 500) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async generateQuestions(materialId, options = {}) {
    await this.delay();
    
    const material = this.materials.find(m => m.id === materialId);
    if (!material) {
      return { success: false, error: 'Material not found' };
    }

    const materialQuestions = this.questions.filter(q => q.materialId === materialId);
    const filteredQuestions = materialQuestions.filter(q => {
      if (options.questionType && q.type !== options.questionType) return false;
      if (options.difficulty && q.difficulty !== options.difficulty) return false;
      return true;
    });

    const numQuestions = Math.min(
      options.numQuestions || 5,
      filteredQuestions.length
    );

    const selectedQuestions = filteredQuestions.slice(0, numQuestions);

    return {
      success: true,
      questions: selectedQuestions,
      material: material
    };
  }

  async getQuestion(questionId) {
    await this.delay(200);
    
    const question = this.questions.find(q => q.id === questionId);
    if (!question) {
      return { success: false, error: 'Question not found' };
    }

    return {
      success: true,
      question: question
    };
  }

  async submitQuestionResponse(questionId, response) {
    await this.delay(300);
    
    const question = this.questions.find(q => q.id === questionId);
    if (!question) {
      return { success: false, error: 'Question not found' };
    }

    const userAnswer = response.answer.toLowerCase().trim();
    const correctAnswer = question.correctAnswer.toLowerCase().trim();
    
    let isCorrect = false;
    let confidenceScore = response.confidence / 5; // Convert to 0-1 scale

    if (question.type === 'MULTIPLE_CHOICE') {
      isCorrect = userAnswer === correctAnswer;
    } else if (question.type === 'TRUE_FALSE') {
      isCorrect = userAnswer === correctAnswer;
    } else if (question.type === 'FILL_IN_BLANK') {
      isCorrect = userAnswer.includes(correctAnswer) || correctAnswer.includes(userAnswer);
    } else if (question.type === 'SHORT_ANSWER') {
      // Simple keyword matching for demo
      const keywords = correctAnswer.split(' ').filter(word => word.length > 3);
      const userWords = userAnswer.split(' ');
      const matchCount = keywords.filter(keyword => 
        userWords.some(word => word.includes(keyword) || keyword.includes(word))
      ).length;
      isCorrect = matchCount >= keywords.length * 0.6; // 60% keyword match
    }

    // Adjust confidence score based on correctness
    if (isCorrect) {
      confidenceScore = Math.min(1, confidenceScore + 0.1);
    } else {
      confidenceScore = Math.max(0, confidenceScore - 0.2);
    }

    // Calculate next review date (simplified spaced repetition)
    const now = new Date();
    const baseInterval = isCorrect ? 2 : 1; // Days
    const confidenceMultiplier = confidenceScore * 2;
    const nextReviewDays = Math.round(baseInterval * confidenceMultiplier);
    const nextReviewDate = new Date(now.getTime() + nextReviewDays * 24 * 60 * 60 * 1000);

    return {
      success: true,
      isCorrect,
      confidenceScore,
      explanation: question.explanation,
      correctAnswer: question.correctAnswer,
      nextReviewDate: nextReviewDate.toISOString(),
      timeSpent: response.timeSpent,
      userAnswer: response.answer
    };
  }

  async getActiveRecallSchedule(userId, options = {}) {
    await this.delay();
    
    const userSchedules = this.schedules.filter(s => s.userId === userId);
    
    if (options.date) {
      const targetDate = new Date(options.date);
      const filteredSchedules = userSchedules.filter(schedule => {
        const scheduleDate = new Date(schedule.nextReview);
        return scheduleDate.toDateString() === targetDate.toDateString();
      });
      
      return {
        success: true,
        schedule: filteredSchedules
      };
    }

    return {
      success: true,
      schedule: userSchedules
    };
  }

  async getLearningAnalytics(userId, options = {}) {
    await this.delay();
    
    return {
      success: true,
      ...this.analytics
    };
  }
}

export default MockActiveRecallAPI;
