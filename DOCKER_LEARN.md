# 🐳 Docker 学习

## 什么是 Docker
容器化平台，让应用在任何地方运行

## 基本命令

```bash
# 列出容器
docker ps

# 列出镜像
docker images

# 运行容器
docker run -p 5000:5000 openclaw-api

# 构建镜像
docker build -t openclaw-api .

# 停止容器
docker stop <container_id>
```

## 用于贾维斯
- 将 API 服务容器化
- 部署到云服务器
- 自动化部署
