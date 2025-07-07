const { RoleMenu, Menu } = require('../models'); // ✅ WAJIB ADA

// 🔧 Helper untuk membentuk menu tree
function buildMenuTree(menus, parentId = null) {
  const tree = [];
  for (const menu of menus) {
    if (menu.parent_id === parentId) {
      const children = buildMenuTree(menus, menu.id);
      tree.push({
        id: menu.id,
        name: menu.name,
        path: menu.path,
        parent_id: menu.parent_id,
        children: children.length ? children : []
      });
    }
  }
  return tree;
}

exports.getMenuByRole = async (req, res) => {
  try {
    const role_id = req.user.roleId;
    if (!role_id) return res.status(403).json({ message: 'Role tidak ditemukan' });

    // Ambil menu berdasarkan role
    const data = await RoleMenu.findAll({
      where: { role_id },
      include: [{
        model: Menu,
        attributes: ['id', 'name', 'path', 'parent_id']
      }]
    });

    // Ambil array Menu dari RoleMenu
    const menus = data.map(item => item.Menu).filter(Boolean);

    // Buat struktur bertingkat
    const tree = buildMenuTree(menus);

    // Kirim response ke frontend
    res.json({
      success: true,
      data: tree
    });
  } catch (err) {
    console.error('❌ Gagal ambil menu:', err);
    res.status(500).json({
      success: false,
      message: 'Gagal mengambil menu',
      error: err.message
    });
  }
};
