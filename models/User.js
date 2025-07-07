module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    username: DataTypes.STRING,
    password: DataTypes.STRING,
    nama: DataTypes.STRING
  }, {
    tableName: 'users',   // Pastikan ini sesuai nama tabel
    timestamps: true
  });

  // 🔗 Association
  User.associate = (models) => {
    User.belongsToMany(models.Role, {
      through: 'UserRoles',
      foreignKey: 'UserId',
      otherKey: 'RoleId'
    });
  };

  return User;
};
