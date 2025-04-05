// const express = require('express');
// const router = express.Router();
// const bcrypt = require('bcrypt');
// const User = require('../models/User');

// // Create a /login route that uses the POST http method to login a user
// router.post('/login', async (req, res) => {
//   try {

//   // SECTION 1
//   // EXTRACT DATA : Write code to extract data(username, email, password) from the request body. 
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************
  
//   // SECTION 2
//   // INPUT VALIDATION : Check if both email and password fields are present 
//   // If any of the fields are empty return a 400 status code, with an error message "All fields are required"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // SECTION 3
//   // PROPER EMAIL FORMAT : Check for proper email format, you can use this regex to match email patterns "/^[^\s@]+@[^\s@]+\.[^\s@]+$/" 
//   // If not proper email format, return a 400 status code, with an error message "Invalid email format"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // SECTION 4
//   // USER CHECK : Check if the user details are in the DB or not 
//   // If user has not already registered return a 400 status code, with an error message "User not found"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // SECTION 5
//   // MATCH PASSWORD : Check for a valid password 
//   // If the entered password is incorrect, return a 401 status with an error message "Invalid password"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // SECTION 6
//   // ALL CHECKS PASSED 
//   // Return a success 200 status with a message "Login successful"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // ---------------REMOVE THE DEMO RESPONSE BELOW---------------
//   return res.status(201).json({ message: 'This is a demo response' });

//   } catch (error) {
//     res.status(500).json({ message: 'Server error', error });
//   }
// });

// module.exports = router;



const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('../models/User');

router.post('/login', async (req, res) => {
  try {
    // SECTION 1 - EXTRACT DATA
    const { username, email, password } = req.body;
    
    // **************************************************
    
    // SECTION 2 - INPUT VALIDATION
    if (!email || !password) {
      return res.status(400).json({ message: 'All fields are required' });
    }
    
    // **************************************************
    
    // SECTION 3 - PROPER EMAIL FORMAT
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ message: 'Invalid email format' });
    }
    
    // **************************************************
    
    // SECTION 4 - USER CHECK
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: 'User not found' });
    }
    
    // **************************************************
    
    // SECTION 5 - MATCH PASSWORD
    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) {
      return res.status(401).json({ message: 'Invalid password' });
    }
    
    // **************************************************
    
    // SECTION 6 - ALL CHECKS PASSED
    return res.status(200).json({ message: 'Login successful' });
    
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
});

module.exports = router;
