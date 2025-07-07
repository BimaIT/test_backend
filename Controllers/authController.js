// controllers/authController.js
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../models');

exports.login = async (req, res) => {
  const { username, password } = req.body;
  const user = await db.User.findOne({ where: { username }, include: db.Role });
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }

  const roles = user.Roles;
  if (roles.length > 1) {
    return res.json({ message: 'Multiple roles found', roles, userId: user.id });
  }

  const token = jwt.sign({ userId: user.id, roleId: roles[0].id }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
};

exports.chooseRole = async (req, res) => {
  const { userId, roleId } = req.body;
  const token = jwt.sign({ userId, roleId }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
};