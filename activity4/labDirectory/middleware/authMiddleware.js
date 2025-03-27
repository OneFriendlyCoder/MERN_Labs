const jwt = require('jsonwebtoken');
const User = require('../models/User');
const JWT_SECRET="ThisIsASecretKey";
const JWT_EXPIRES_IN="1h";


const authMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ message: 'Unauthorized: No token provided' });
    }
    
    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token,JWT_SECRET);
    const user = await User.findById(decoded.id).select('-password');
    if (!user) {
      return res.status(403).json({ message: 'Forbidden: Invalid token' });
    }
    req.user = user;
    next();
  } catch (error) {
    console.error('Auth Middleware Error:', error.message);
    return res.status(403).json({ message: 'Forbidden: Invalid or expired token' });
  }
};

module.exports = authMiddleware;
