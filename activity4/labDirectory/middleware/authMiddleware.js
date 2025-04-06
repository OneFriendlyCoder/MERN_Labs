// const jwt = require('jsonwebtoken');
// const User = require('../models/User');
// const JWT_SECRET="ThisIsASecretKey";
// const JWT_EXPIRES_IN="1h";

// const authMiddleware = async (req, res, next) => {
//   try {

//   // SECTION 1
//   // EXTRACT AUTHORIZATION HEADERS : Write code to extract the authorization headers 
//   // Also check if the authorization header is missing or do not starts with 'Bearer ', if any of the error is found return a 401 status with message "Unauthorized: No token provided" 
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************
  
//   // SECTION 2
//   // EXTRACT AND VERIFY THE TOKEN
//   // Extract the token from the authorization header 
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // **************************************************
  
//   // SECTION 3
//   // FIND THE USER IN THE DATABASE
//   // Search the user in the database using the id extracted from the decoded JWT token
//   // If the user is not found in the DB, return a 403 status with the message "Forbidden: Invalid token"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // **************************************************
  
//   // SECTION 4
//   // ATTACH THE USER TO REQUEST AND CALL NEXT MIDDLEWARE
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************
//   return res.status(200).json({ message: 'Success' });

// } catch (error) {
//     console.error('Auth Middleware Error:', error.message);
//     return res.status(403).json({ message: 'Forbidden: Invalid or expired token' });
//   }
// };

// module.exports = authMiddleware;


const jwt = require('jsonwebtoken');
const User = require('../models/User');
const JWT_SECRET = "ThisIsASecretKey";
const JWT_EXPIRES_IN = "1h";

const authMiddleware = async (req, res, next) => {
  try {
    // SECTION 1
    // EXTRACT AUTHORIZATION HEADERS
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ message: "Unauthorized: No token provided" });
    }

    // **************************************************

    // SECTION 2
    // EXTRACT AND VERIFY THE TOKEN
    const token = authHeader.split(" ")[1];
    const decoded = jwt.verify(token, JWT_SECRET);

    // **************************************************

    // SECTION 3
    // FIND THE USER IN THE DATABASE
    const user = await User.findById(decoded.id);
    if (!user) {
      return res.status(403).json({ message: "Forbidden: Invalid token" });
    }

    // **************************************************

    // SECTION 4
    // ATTACH THE USER TO REQUEST AND CALL NEXT MIDDLEWARE
    req.user = user;
    next();

    // **************************************************

  } catch (error) {
    console.error('Auth Middleware Error:', error.message);
    return res.status(403).json({ message: 'Forbidden: Invalid or expired token' });
  }
};

module.exports = authMiddleware;
