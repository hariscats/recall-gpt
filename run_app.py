#!/usr/bin/env python3
"""
Simplified launcher script for the AI Learning Assistant application.
"""
import os
import sys
import uvicorn

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    print("Starting AI Learning Assistant (simplified version)...")
    
    # Run the application directly
    uvicorn.run(
        "ai-learning-assistants.app.main:app",
        host="127.0.0.1",  # Only listen on localhost for development
        port=8000,
        reload=True
    )