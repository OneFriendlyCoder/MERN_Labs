const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');

router.get('/dashboard', authMiddleware, (req, res) => {
  if (!req.user) {
    return res.status(401).send('<h1>You are unauthorized</h1>');
  }

  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Dashboard</title>
      <style>
        body {
          font-family: 'Segoe UI', Arial, sans-serif;
          background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
          margin: 0;
          padding: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }
        .container {
          background: #fff;
          padding: 2rem 3rem;
          border-radius: 10px;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
          text-align: center;
          max-width: 90%;
        }
        h1 {
          color: #333;
          margin-bottom: 1rem;
          font-size: 2rem;
        }
        p {
          color: #555;
          font-size: 1.2rem;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Welcome ${req.user.username}!</h1>
      </div>
    </body>
    </html>
  `;

  res.status(200).send(html);
});

module.exports = router;
