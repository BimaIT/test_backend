// models/UserRole.js
module.exports = (sequelize, DataTypes) => {
  const UserRole = sequelize.define('UserRole', {
    user_id: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    role_id: {
      type: DataTypes.INTEGER,
      allowNull: false
    }
  }, {
    tableName: 'user_roles',       // 👈 nama tabel sesuai database
    createdAt: 'created_at',       // 👈 sesuaikan nama kolom
    updatedAt: 'updated_at',       // 👈 sesuaikan nama kolom
    timestamps: true
  });

  return UserRole;
};
