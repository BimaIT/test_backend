const express = require('express');
const router = express.Router();
const adminController = require('../Controllers/adminController');
const auth = require('../middleware/authMiddleware'); // Middleware JWT

// =========================
// ✅ Public Routes (No JWT)
// =========================
router.post('/register-user', adminController.registerUser);
router.get('/roles', adminController.getRoles);

// ===========================
// ✅ Protected Routes (JWT)
// ===========================
router.use(auth); // Mulai dari sini butuh token akses

router.get('/menus', adminController.getMenus);
router.post('/menus', adminController.createMenu);
router.put('/menus/:id', adminController.updateMenu);
router.delete('/menus/:id', adminController.deleteMenu);

// Assign Menu ke Role
router.post('/assign-menu', adminController.assignMenusToRole);

// Assign Role ke User
router.post('/assign-role', adminController.assignRolesToUser);

module.exports = router;
