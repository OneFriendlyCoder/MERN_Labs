const express = require('express');
const mongoose = require('mongoose');
const authRoutes = require('./routes/auth');
const path = require('path'); // Required to manage file paths

const app = express();
const MONGO_URI = "mongodb://127.0.0.1:27017/UserDB";

// Middleware to parse JSON bodies
app.use(express.json());

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.use('/', authRoutes);

// MongoDB Connection
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
.then(() => console.log('MongoDB Connected'))
.catch(err => console.log(err));

// Start Server
const PORT = 30002;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
