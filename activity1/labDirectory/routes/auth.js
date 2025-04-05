// const express = require('express');
// const router = express.Router();
// const bcrypt = require('bcrypt');
// const User = require('../models/User');

// // Create a /signup route that uses the POST http method to create a new user 
// router.post('/signup', async (req, res) => {

//   // SECTION 1
//   // EXTRACT DATA : Write code to extract data(username, email, password) from the request body. 
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // SECTION 2
//   // VALIDATE INPUT : The validation is based on the below given criteria
//   // Check for empty username, password or email fields
//   // If any of the fields are empty send a 400 status code, with an error message "All fields are required"
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   try {
//   // SECTION 3
//   // CHECK FOR DUPLICATES
//   // Write code to check for duplicate entries for the same username or email
//   // If the Username is already present, send a 409 status code, with an error message "Username is already present"
//   // If the email is already present, send a 409 status code, with an error message "Email is already present" 
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------
  
//   // **************************************************
  
//   // SECTION 4
//   // PASSWORD HASHING
//   // Write code to hash the password received from the frontend, with salt rounds = 10 
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // **************************************************

//   // SECTION 5
//   // CREATING AND SAVING A NEW USER
//   // Write code to create a new User object with the following details. {username, email, hashed_password}
//   // Write code to save the newly created user to the MongoDB
//   // On success return a 201 status code, with a response "User successfully created"
//   // On failure return a 409 status code, with a response "Failed to create user"  
//   // ---------------YOUR CODE GOES HERE---------------
  
//   // ---------------YOUR CODE ENDS HERE---------------

//   // ---------------REMOVE THE DEMO RESPONSE BELOW---------------
//   return res.status(201).json({ message: 'This is a demo response' });
  
// } catch (err) {
//     console.error(err);
//     return res.status(500).json({ message: 'Server error.' });
//   }
// });

// module.exports = router;


const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('../models/User');

// Create a /signup route that uses the POST http method to create a new user 
router.post('/signup', async (req, res) => {

  // SECTION 1
  // EXTRACT DATA: Extract username, email, password,
  const { username, email, password } = req.body;
  
  // **************************************************

  // SECTION 2
  // VALIDATE INPUT: Check for empty username, password, or email fields.
  if (!username || !email || !password) {
    return res.status(400).json({ message: 'All fields are required' });
  }
  
  // **************************************************

  try {
    // SECTION 3
    // CHECK FOR DUPLICATES: Verify if the username or email already exists.
    const existingUserByUsername = await User.findOne({ username });
    if (existingUserByUsername) {
      return res.status(409).json({ message: 'Username is already present' });
    }

    const existingUserByEmail = await User.findOne({ email });
    if (existingUserByEmail) {
      return res.status(409).json({ message: 'Email is already present' });
    }
    
    // **************************************************
    
    // SECTION 4
    // PASSWORD HASHING: Hash the password with salt rounds = 10.
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // **************************************************

    // SECTION 5
    // CREATING AND SAVING A NEW USER:
    // Create a new User object with the username, email, hashed password.
    const newUser = new User({
      username,
      email,
      password: hashedPassword,
    });

    // Save the newly created user to MongoDB.
    const savedUser = await newUser.save();
    if (savedUser) {
      return res.status(201).json({ message: 'User successfully created' });
    } else {
      return res.status(409).json({ message: 'Failed to create user' });
    }
    
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: 'Server error.' });
  }
});

module.exports = router;
