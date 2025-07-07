// routes/authRoutes.js
const express = require('express');
const router = express.Router();
const { login, chooseRole } = require('../Controllers/authController');
const db = require('../models');

// Login & role choosing
router.post('/login', login);
router.post('/choose-role', chooseRole);

// routes/authRoutes.js
router.get('/roles', async (req, res) => {
  try {
    const roles = await db.Role.findAll({ order: [['name', 'ASC']] });
    res.json(roles);
  } catch (err) {
    console.error('❌ Gagal ambil role:', err);  // ⬅️ Tambahkan ini
    res.status(500).json({ message: 'Gagal ambil role' });
  }
});


module.exports = router;

