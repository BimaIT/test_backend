// app.js

require('dotenv').config();
const express = require('express');
const app = express();
const path = require('path');


// Middleware untuk parsing JSON & form-urlencoded
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static file (misalnya login.html, register.html, dll)
app.use(express.static(path.join(__dirname, 'public')));


// Import routes
const authRoutes = require('./routes/authRoutes');
const adminRoutes = require('./routes/adminRoutes');
const menuRoutes = require('./routes/menuRoutes');

// Pasangkan routes
app.use('/api/auth', authRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api', menuRoutes);

// Jalankan server
const PORT = process.env.PORT || 5050;
app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
});

// Cek koneksi database Sequelize
const { sequelize } = require('./models');
sequelize.authenticate()
  .then(() => console.log('✅ Database connected'))
  .catch(err => console.error('❌ DB connection error:', err));
