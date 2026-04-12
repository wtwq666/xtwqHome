// Vercel Serverless Function
// 访问路径: /api/hello

export default function handler(req, res) {
  res.status(200).json({
    message: "Hello from Vercel Serverless API! 🎉",
    from: "xtwqHome 后端",
    method: req.method,
    timestamp: new Date().toISOString()
  });
}
