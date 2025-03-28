#!/bin/bash

# Start the backend server
echo "Starting Django backend server..."
cd backend/edteti_project
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Wait a moment for the backend to initialize
sleep 2

# Start the frontend server
echo "Starting Vue.js frontend server..."
cd ../../frontend
npm run serve &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"

# Function to handle script termination
function cleanup {
  echo "Stopping servers..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Both servers are running. Press Ctrl+C to stop."
wait
