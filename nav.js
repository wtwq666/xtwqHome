// AI-NAV 助手生成的导航模块

const navItems = [
  { name: "Home", path: "/" },
  { name: "Guide", path: "/guide" },
  { name: "About", path: "/about" }
];

function renderNav() {
  return navItems.map(item => `<a href="${item.path}">${item.name}</a>`).join(" | ");
}

module.exports = { renderNav };
