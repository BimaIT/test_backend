const Sequelize = require('sequelize');
const sequelize = require('../config/db');

// Import semua model
const User = require('./User')(sequelize, Sequelize.DataTypes);
const Role = require('./Role')(sequelize, Sequelize.DataTypes);
const UserRole = require('./UserRole')(sequelize, Sequelize.DataTypes);
const Menu = require('./menu')(sequelize, Sequelize.DataTypes);
const RoleMenu = require('./RoleMenu')(sequelize, Sequelize.DataTypes);

// Relasi User <-> Role melalui UserRole
User.belongsToMany(Role, {
  through: UserRole,
  foreignKey: 'user_id',
  otherKey: 'role_id',
});
Role.belongsToMany(User, {
  through: UserRole,
  foreignKey: 'role_id',
  otherKey: 'user_id',
});

// Relasi Role <-> Menu melalui RoleMenu
Role.belongsToMany(Menu, {
  through: RoleMenu,
  foreignKey: 'role_id',
  otherKey: 'menu_id',
});
Menu.belongsToMany(Role, {
  through: RoleMenu,
  foreignKey: 'menu_id',
  otherKey: 'role_id',
});

// ✅ Relasi tambahan untuk akses langsung
RoleMenu.belongsTo(Menu, { foreignKey: 'menu_id' });
RoleMenu.belongsTo(Role, { foreignKey: 'role_id' });

// ✅ Tambahan agar bisa include langsung dari Menu
Menu.hasMany(RoleMenu, { foreignKey: 'menu_id' });
Role.hasMany(RoleMenu, { foreignKey: 'role_id' });

module.exports = {
  sequelize,
  Sequelize,
  User,
  Role,
  UserRole,
  Menu,
  RoleMenu,
};
