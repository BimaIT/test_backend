const express = require('express');
const router = express.Router();
const menuController = require('../Controllers/menuController');
const auth = require('../middleware/authMiddleware');

// Route ini WAJIB ADA:
router.get('/menu', auth, menuController.getMenuByRole);

module.exports = router;
