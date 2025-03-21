const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('../models/User');

// Create a /signup route that uses the POST http method to create a new user 
router.post('/signup', async (req, res) => {

  // SECTION 1
  // EXTRACT DATA : Write code to extract data(username, email, password, role) from the request body. 
  // ---------------YOUR CODE GOES HERE---------------
  const { username, email, password, role } = req.body;
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  // SECTION 2
  // VALIDATE INPUT : The validation is based on the below given criteria
  // Check if non of the fields are empty. Else return a JSON 400 response with the message "All fields are required."
  // Check if the user has one of the following roles : admin or user. If not return a JSON 400 with the message "Role must be either admin or user." 
  // ---------------YOUR CODE GOES HERE---------------
  if (!username || !email || !password || !role) {
    return res.status(400).json({ message: 'All fields are required.' });
  }

  if (!['admin', 'user'].includes(role)) {
    return res.status(400).json({ message: 'Role must be either admin or user.' });
  }
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  try {
  // SECTION 3
  // CHECK FOR DUPLICATES
  // Write code to check whether the username or email is already present in the Database, if yes return a JSON 409 response with the message "Username or email already registered." 
  // ---------------YOUR CODE GOES HERE---------------
  const existingUser = await User.findOne({ $or: [{ email }, { username }] });
  if (existingUser) {
    return res.status(409).json({ message: 'Username or email already registered.' });
  }
  // ---------------YOUR CODE ENDS HERE---------------
  
  // **************************************************
  
  // SECTION 4
  // PASSWORD HASHING
  // Write code to hash the password received from the frontend, with salt rounds = 10 
  // ---------------YOUR CODE GOES HERE---------------
  const hashedPassword = await bcrypt.hash(password, 10);
  // ---------------YOUR CODE ENDS HERE---------------

  // **************************************************

  // SECTION 5
  // CREATING AND SAVING A NEW USER
  // Write code to create a new User object with the following details. {username, email, hashed_password, role}
  // Write code to save the newly created user to the MongoDB
  // Return appropriate JSON response based on user creation success or failure.  
  // ---------------YOUR CODE GOES HERE---------------
  const newUser = new User({ username, email, password: hashedPassword, role });
  await newUser.save();
  return res.status(201).json({ message: 'User registered successfully!' });
  // ---------------YOUR CODE ENDS HERE---------------

  // ---------------REMOVE THE DEMO RESPONSE BELOW---------------
  // return res.status(201).json({ message: 'This is a demo response' });
  
} catch (err) {
    console.error(err);
    return res.status(500).json({ message: 'Server error.' });
  }
});

module.exports = router;
