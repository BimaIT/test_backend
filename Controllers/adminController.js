const { User, Role, UserRole, Menu, RoleMenu } = require('../models');
const bcrypt = require('bcrypt');

// ✅ REGISTER USER
exports.registerUser = async (req, res) => {
  const { username, password, nama, roleIds } = req.body;

  try {
    const existingUser = await User.findOne({ where: { username } });
    if (existingUser) {
      return res.status(400).json({ message: 'Username sudah terdaftar' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await User.create({
      username,
      password: hashedPassword,
      nama
    });

    // ⬇️ INSERT ke tabel user_roles
    if (Array.isArray(roleIds)) {
      await Promise.all(
        roleIds.map(roleId =>
          UserRole.create({
            user_id: user.id,  // ⬅️ Cocokkan nama kolom di DB
            role_id: roleId
          })
        )
      );
    }

    res.status(201).json({ message: 'User berhasil dibuat' });
  } catch (error) {
    console.error('❌ Error saat register user:', error);
    res.status(500).json({ message: 'Error saat membuat user' });
  }
};

// ✅ GET ROLES (untuk form daftar)
exports.getRoles = async (req, res) => {
  try {
    const roles = await Role.findAll({
      order: [['name', 'ASC']],
    });
    res.json(roles);
  } catch (err) {
    console.error('❌ Gagal ambil role:', err);
    res.status(500).json({ message: 'Gagal ambil role' });
  }
};

// ✅ GET MENUS (khusus authenticated user)
exports.getMenus = async (req, res) => {
  try {
    const menus = await Menu.findAll({
      order: [['name', 'ASC']]
    });
    res.json(menus);
  } catch (err) {
    res.status(500).json({ message: 'Gagal ambil menu' });
  }
};

// ✅ CREATE MENU
exports.createMenu = async (req, res) => {
  const { name, path, icon } = req.body;
  try {
    const menu = await Menu.create({ name, path, icon });
    res.status(201).json(menu);
  } catch (err) {
    res.status(500).json({ message: 'Gagal tambah menu' });
  }
};

// ✅ UPDATE MENU
exports.updateMenu = async (req, res) => {
  const { name, path, icon } = req.body;
  const { id } = req.params;
  try {
    await Menu.update({ name, path, icon }, { where: { id } });
    res.json({ message: 'Berhasil update menu' });
  } catch (err) {
    res.status(500).json({ message: 'Gagal update menu' });
  }
};

// ✅ DELETE MENU
exports.deleteMenu = async (req, res) => {
  const { id } = req.params;
  try {
    await Menu.destroy({ where: { id } });
    res.json({ message: 'Berhasil hapus menu' });
  } catch (err) {
    res.status(500).json({ message: 'Gagal hapus menu' });
  }
};

// ✅ ASSIGN MENU TO ROLE
exports.assignMenusToRole = async (req, res) => {
  const { roleId, menuIds } = req.body;
  try {
    await RoleMenu.destroy({ where: { role_id: roleId } }); // Clear old

    await Promise.all(
      menuIds.map(menuId =>
        RoleMenu.create({ role_id: roleId, menu_id: menuId })
      )
    );

    res.json({ message: 'Menu berhasil di-assign ke role' });
  } catch (err) {
    res.status(500).json({ message: 'Gagal assign menu ke role' });
  }
};

// ✅ ASSIGN ROLE TO USER
exports.assignRolesToUser = async (req, res) => {
  const { userId, roleIds } = req.body;
  try {
    await UserRole.destroy({ where: { user_id: userId } }); // Clear old

    await Promise.all(
      roleIds.map(roleId =>
        UserRole.create({ user_id: userId, role_id: roleId })
      )
    );

    res.json({ message: 'Role berhasil di-assign ke user' });
  } catch (err) {
    res.status(500).json({ message: 'Gagal assign role ke user' });
  }
};
