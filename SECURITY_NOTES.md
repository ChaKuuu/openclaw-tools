# 网络安全学习 - 恶意插件识别

## 今日学习要点

### 1. 恶意 Chrome 扩展特征

#### 危险权限
- `http://*/*` 或 `https://*/*` - 读取所有网页
- `cookies` - 窃取 cookie
- `webRequest` / `webRequestBlocking` - 拦截请求
- `debugger` - 调试接口
- `tabs` - 访问标签页
- `history` - 访问历史

#### 可疑行为
- 频繁请求权限
- 代码混淆
- 远程加载脚本
- 数据外发

### 2. 防范措施

#### 安装前检查
1. 查看权限列表
2. 检查开发者信息
3. 阅读用户评论
4. 验证来源

#### 安装后监控
1. 定期检查权限
2. 监控网络流量
3. 观察浏览器行为

### 3. 我们的安全状态

当前 Chrome 扩展：
- manifest.json: 无危险权限 ✅
- popup.html/js: 本地文件 ✅

### 4. 参考资源

- Chrome Web Store 政策
- Google 安全博客
- OWASP Top 10
