# AI Learning Assistant

An AI-powered learning assistant app that implements active recall and spaced repetition techniques to optimize learning and retention.

## Project Overview

This project provides a simplified starting point for building an AI-powered learning assistant. The app demonstrates:

- Backend API built with FastAPI
- Frontend UI built with React
- Basic data models for learning materials and user tracking
- Integration points for AI capabilities

## Project Structure

- `ai-learning-assistants/app/` - FastAPI backend application
- `frontend/` - React frontend application
- `config/` - Configuration settings

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the backend:
   ```
   python run_app.py
   ```

The API will be available at http://127.0.0.1:8000

- API documentation: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Using the startup script (recommended):
   
   For PowerShell:
   ```powershell
   .\start-app.ps1
   ```
   
   For Command Prompt:
   ```cmd
   start-app
   ```
   
   These scripts will automatically:
   - Install required dependencies
   - Skip problematic postinstall scripts
   - Verify react-scripts installation
   - Start the development server

   **Note:** The startup scripts handle Node.js path issues and ensure reliable execution.

3. Alternatively, for manual installation:
   ```
   npm config set ignore-scripts true
   npm install
   node node_modules\react-scripts\bin\react-scripts.js start
   ```

The frontend will be available at http://localhost:3000

## Features (Minimal Implementation)

### Backend API

- Simple user management
- Learning materials CRUD operations
- In-memory data store for demonstration purposes

### Frontend UI

- Dashboard with learning statistics
- Learning materials browser
- User profile management
- Responsive design

## Extending the Project

This minimal sample can be extended in the following ways:

### AI Integration

The project includes placeholder files for AI integration:

- `app/plugins/content_generation.py` - For generating learning materials
- `app/plugins/knowledge_assessment.py` - For assessing user knowledge
- `app/services/learning_agent.py` - For personalized learning recommendations

### Database Integration

Replace the in-memory data store with a database:

- Consider MongoDB for flexible document storage
- Use SQLAlchemy with PostgreSQL for relational data
- Implement proper data persistence and retrieval

### Authentication

Add user authentication:

- JWT-based authentication
- OAuth integration with providers like Google or Microsoft
- User session management

## Core Technologies and Concepts

### Active Recall

The app is designed to implement active recall by generating challenging questions that force users to retrieve information from memory, which strengthens neural pathways and improves long-term retention.

### Spaced Repetition

The architecture supports implementing the SM-2 algorithm to calculate optimal intervals between reviews, scheduling items just before they would be forgotten to maximize retention with minimal time investment.

### Personalization

The system is structured to track user performance to adapt question difficulty, learning pace, and review schedules to each individual's learning patterns.

## Development Notes

- This is a minimal sample implementation focused on demonstrating the architecture
- Error handling has been simplified for clarity
- Default values are used in place of environment variables for ease of setup
- The frontend uses dummy data for demonstration purposes

## License

This project is licensed under the MIT License.