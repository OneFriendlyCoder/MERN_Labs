const jwt = require('jsonwebtoken');
const User = require('../models/User');
const JWT_SECRET="ThisIsASecretKey";
const JWT_EXPIRES_IN="1h";

const authMiddleware = async (req, res, next) => {
  try {

  // SECTION 1
  // EXTRACT AUTHORIZATION HEADERS : Write code to extract the authorization headers 
  // Also check if the authorization header is missing or do not starts with 'Bearer ', if any of the error is found return a 401 status with message "Unauthorized: No token provided" 
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************
  
  // SECTION 2
  // EXTRACT AND VERIFY THE TOKEN
  // Extract the token from the authorization header 
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  // **************************************************
  
  // SECTION 3
  // FIND THE USER IN THE DATABASE
  // Search the user in the database using the id extracted from the decoded JWT token
  // If the user is not found in the DB, return a 403 status with the message "Forbidden: Invalid token"
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  // **************************************************
  
  // SECTION 4
  // ATTACH THE USER TO REQUEST AND CALL NEXT MIDDLEWARE
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

} catch (error) {
    console.error('Auth Middleware Error:', error.message);
    return res.status(403).json({ message: 'Forbidden: Invalid or expired token' });
  }
};

module.exports = authMiddleware;
