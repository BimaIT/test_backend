// models/RoleMenu.js
module.exports = (sequelize, DataTypes) => {
  const RoleMenu = sequelize.define("RoleMenu", {
    role_id: DataTypes.INTEGER,
    menu_id: DataTypes.INTEGER
  }, {
    tableName: "role_menus",
    timestamps: false // ⛔️ penting
  });

  return RoleMenu;
};
