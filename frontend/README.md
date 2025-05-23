# AI Learning Assistant Frontend

This is the React frontend for the AI Learning Assistant application.

## Overview

The frontend provides a user interface for interacting with the AI Learning Assistant. It includes:

- Dashboard with learning statistics
- Learning materials browser
- User profile management
- Responsive design

## Getting Started

### Prerequisites

- Node.js 14+ (installed to C:\Program Files\nodejs)
- npm or yarn

### Installation & Running

For the best experience, use one of the provided startup scripts:

#### Using PowerShell (Recommended)

```powershell
.\start-app.ps1
```

#### Using Command Prompt

```cmd
start-app.cmd
```

These scripts will:
- Install required dependencies
- Skip problematic postinstall scripts
- Verify react-scripts installation
- Start the development server

### Manual Installation

```bash
npm config set ignore-scripts true
npm install
node node_modules\react-scripts\bin\react-scripts.js start
```

The frontend will be available at http://localhost:3000

## Project Structure

- `public/` - Static assets and index.html
- `src/` - Source code
  - `components/` - Reusable UI components
  - `pages/` - Application pages
  - `App.js` - Main application component
  - `index.js` - Application entry point

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `npm test`

Launches the test runner in interactive watch mode.

### `npm run build`

Builds the app for production to the `build` folder.

## Connecting to the Backend

The application is configured to proxy API requests to http://localhost:8000 where the FastAPI backend should be running.
