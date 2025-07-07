module.exports = (sequelize, DataTypes) => {
  const Role = sequelize.define('Role', {
    name: DataTypes.STRING,
  }, {
    tableName: 'roles',
    timestamps: true
  });

  // 🔗 Association
  Role.associate = (models) => {
    Role.belongsToMany(models.User, {
      through: 'UserRoles',
      foreignKey: 'RoleId',
      otherKey: 'UserId'
    });
  };

  return Role;
};
