#!/bin/bash

# Start MongoDB
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

# Start Node.js server (in foreground)
echo "🚀 Starting Node server..."
node server.js