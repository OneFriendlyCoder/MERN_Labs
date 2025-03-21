#!/bin/bash

pip3 install bcrypt requests pymongo

# Start MongoDB (it will keep running)
mongod --bind_ip_all --dbpath /data/db --logpath /var/log/mongodb/mongod.log --logappend &

# Wait for MongoDB to fully start
sleep 5
echo "✅ MongoDB started."

cd /home/labDirectory

# Install Node dependencies if not installed
if [ ! -d "node_modules" ]; then
  echo "📦 Installing dependencies..."
  npm install
fi

# Infinite loop to run and restart Node server every 5 seconds
while true; do
  echo "🚀 Starting Node server..."
  node server.js &
  NODE_PID=$!
  
  # Let the Node server run for 5 seconds
  sleep 5
  
  echo "🛑 Stopping Node server..."
  kill $NODE_PID
  
  # Optional: Wait a moment to ensure the process is terminated
  sleep 1
done
