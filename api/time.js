// Vercel Serverless Function
// 访问路径: /api/time

export default function handler(req, res) {
  const now = new Date();
  res.status(200).json({
    utc: now.toISOString(),
    local: now.toLocaleString("zh-CN", { timeZone: "Asia/Shanghai" }),
    timezone: "Asia/Shanghai",
    tip: "这个接口运行在 Vercel 的服务器上，不是本地电脑"
  });
}
