# 基础镜像
FROM ubuntu:latest

# 设置工作目录
WORKDIR /app

# 复制文件到工作目录
COPY . .

# 安装依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# 安装Python依赖
RUN pip3 install -r requirements.txt

# 暴露端口
EXPOSE 3000

# 运行命令
CMD ["python3", "main.py"]
