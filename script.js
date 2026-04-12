// 简单的点击计数器演示

const btn = document.getElementById('clickBtn');
const countSpan = document.getElementById('count');
let count = 0;

btn.addEventListener('click', () => {
  count++;
  countSpan.textContent = count;

  // 添加一点视觉反馈
  btn.style.transform = 'scale(0.96)';
  setTimeout(() => {
    btn.style.transform = 'scale(1)';
  }, 100);
});

console.log('xtwqHome 页面加载完成，Vercel 部署成功！');
