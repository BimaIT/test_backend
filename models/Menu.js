// models/Menu.js
module.exports = (sequelize, DataTypes) => {
  const Menu = sequelize.define("Menu", {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    name: DataTypes.STRING,
    path: DataTypes.STRING,
    parent_id: DataTypes.INTEGER
  }, {
    tableName: "menus",
    timestamps: false // ⛔️ penting: tidak pakai createdAt/updatedAt
  });

  return Menu;
};
