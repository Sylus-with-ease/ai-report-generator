#!/bin/bash
# AI 报告生成助手 - Linux/Mac 启动脚本

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -q -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "创建 .env 文件..."
    cp .env.example .env
    echo ""
    echo "⚠️  请编辑 .env 文件，填入您的 DASHSCOPE_API_KEY"
    echo ""
    read -p "按 Enter 继续..."
fi

# 启动应用
echo ""
echo "🚀 正在启动 AI 报告生成助手..."
echo "📱 本地访问: http://localhost:8502"
echo ""
streamlit run app.py

