const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('../models/User');

// Create a /signup route that uses the POST http method to create a new user 
router.post('/signup', async (req, res) => {

  // SECTION 1
  // EXTRACT DATA : Write code to extract data(username, email, password, role) from the request body. 
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  // SECTION 2
  // VALIDATE INPUT : The validation is based on the below given criteria
  // Check for empty username, password or email fields
  // If any of the fields are empty send a 400 status code, with an error message "All fields are required"
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  try {
  // SECTION 3
  // CHECK FOR DUPLICATES
  // Write code to check for duplicate entries for the same username or email
  // If the Username is already present, send a 409 status code, with an error message "Username is already present"
  // If the email is already present, send a 409 status code, with an error message "Email is already present" 
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------
  
  // **************************************************
  
  // SECTION 4
  // PASSWORD HASHING
  // Write code to hash the password received from the frontend, with salt rounds = 10 
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  // SECTION 5
  // CREATING AND SAVING A NEW USER
  // Write code to create a new User object with the following details. {username, email, hashed_password}
  // Write code to save the newly created user to the MongoDB
  // On success return a 201 status code, with a response "User successfully created"
  // On failure return a 409 status code, with a response "Failed to create user"  
  // ---------------YOUR CODE GOES HERE---------------
  
  // ---------------YOUR CODE ENDS HERE---------------

  // ---------------REMOVE THE DEMO RESPONSE BELOW---------------
  return res.status(201).json({ message: 'This is a demo response' });
  
} catch (err) {
    console.error(err);
    return res.status(500).json({ message: 'Server error.' });
  }
});

module.exports = router;
