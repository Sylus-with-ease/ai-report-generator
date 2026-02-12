# 📝 AI 报告生成助手

一个基于 Streamlit + 阿里云通义千问的智能报告生成系统，支持多种报告类型、自定义风格和模板管理。

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 核心特性

### 🎯 功能模块
- **多类型报告生成** - 日报、周报、月报、季度总结、项目复盘等
- **智能风格定制** - 支持 5 种语气和 4 种风格组合
- **📋 报告模板自定义** ⭐ - 预设 4 个模板，支持保存自定义模板
- **多格式导出** - Markdown、TXT、HTML 格式任选
- **历史记录管理** - 自动保存生成历史，支持查看和清空
- **响应式设计** - 支持桌面端和移动端

### 🔒 技术亮点
- ✅ **环境变量安全管理** - 使用 python-dotenv 管理 API Key，避免硬编码
- ✅ **自定义加载状态** - 实时进度提示（30% → 70% → 100%）
- ✅ **友好的用户指导** - 空内容智能提示
- ✅ **数据持久化** - 使用 pickle 存储历史记录和模板
- ✅ **完善的错误处理** - 详细的异常捕获和提示

## 🚀 快速开始

### 前置要求
- Python 3.8+
- pip 包管理工具

### 环境搭建

#### 1️⃣ 克隆项目（或下载文件）
```bash
cd 你的项目目录
```

#### 2️⃣ 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

#### 4️⃣ 配置 API Key

**方式一：使用 .env 文件（推荐）** ⭐

1. 复制 `.env.example` 为 `.env`：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 API Key：
```env
DASHSCOPE_API_KEY=sk-your-actual-api-key-here
```

**方式二：系统环境变量**

Windows (PowerShell):
```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-your-api-key", "User")
```

Linux/Mac:
```bash
export DASHSCOPE_API_KEY="sk-your-api-key"
```

#### 5️⃣ 运行应用
```bash
streamlit run app.py
```

应用将在浏览器中打开：
- 📱 本地访问：http://localhost:8502
- 🌐 网络访问：http://your-ip:8502

### 🔑 如何获取 API Key？

1. 访问 [阿里云通义千问官网](https://dashscope.aliyuncs.com)
2. 注册/登录账户
3. 在控制台 → API 密钥管理中创建新密钥
4. 复制完整的密钥值到 `.env` 文件

## 📖 使用指南

### 基础流程
1. **输入内容** - 在左侧文本框输入你的工作成就
2. **配置选项** - 在侧边栏选择报告类型、语气和风格
3. **选择模板** - 在高级选项中选择预设模板或自定义模板
4. **生成报告** - 点击"✨ 生成报告"按钮
5. **导出结果** - 选择格式（Markdown/TXT/HTML）下载

### 内容输入建议
```
✅ 推荐示例：
- 完成了用户认证模块开发（3 天）
- 修复了 3 个严重 bug，代码覆盖率提升至 92%
- 参加了 2 次产品需求讨论会
- 代码审查 5 次 PR，反馈优化建议

❌ 避免：
- 内容过于简短
- 使用模糊词汇（"做了一些工作"）
- 没有具体数字或成果
```

### 🎨 报告模板说明

#### 预设模板
| 模板名 | 适用场景 | 特点 |
|--------|--------|------|
| **专业正式** | 领导汇报、工作总结 | 结构化、正式、易理解 |
| **简洁扼要** | 日常沟通、快速总结 | 简短、精炼、直达要点 |
| **数据驱动** | 业务分析、成果展示 | 强调数据、对比、趋势 |
| **创意活泼** | 团队分享、创新展示 | 活泼、亮点突出、有趣 |

#### 自定义模板
1. 在侧边栏展开"🎨 报告模板"
2. 输入模板名称、前缀和后缀
3. 点击"💾 保存模板"
4. 下次使用时在高级选项中选择自定义模板

## 📊 功能截图

### 1. 主界面
```
┌─────────────────────────────────────────┐
│ 📝 AI 报告生成助手                      │
│ ✨ 智能生成日报、周报、月报及更多文档    │
└─────────────────────────────────────────┘
┌──────────────────┬──────────────────────┐
│  📌 输入内容      │  👁️ 预览和历史      │
│ ┌──────────────┐ │ ┌────────────────┐  │
│ │输入工作内容  │ │ │最近生成 (3 条) │  │
│ │...           │ │ │├─ 周报 13:20   │  │
│ │              │ │ │├─ 日报 11:45   │  │
│ └──────────────┘ │ │├─ 月报 09:30   │  │
│                  │ │└────────────────┘  │
└──────────────────┴──────────────────────┘
```

### 2. 侧边栏配置
```
⚙️ 配置选项
────────────
📋 报告类型
  ✓ 日常报告
    └─ 日报/周报/月报

🎨 语气和风格
  语气：正式商务 ▼
  风格：结构化列表 ▼

📤 输出格式
  ✓ Markdown

📚 历史记录
  🗑️ 清空所有历史

🎨 报告模板
  └─ 自定义模板 ▼
```

### 3. 生成效果
```
✅ 报告已生成！

━━━━━━━━━━━━━━━━━━━━━━━━
## 本周工作总结

### 核心成就
- 完成了用户认证模块开发
- 修复了 3 个严重 bug
- 代码覆盖率提升至 92%
...

📥 导出选项
┌─────────────┬─────────────┬─────────────┐
│ 📄 Markdown │ 📋 TXT      │ 🌐 HTML     │
└─────────────┴─────────────┴─────────────┘
```

## 🛠️ 技术架构

### 技术栈
- **前端**：Streamlit 1.28+ (响应式布局、自定义 CSS)
- **后端**：Python 3.8+ (文件操作、数据持久化)
- **AI 集成**：阿里云通义千问 API (qwen-turbo 模型)
- **配置管理**：python-dotenv (环境变量加载)
- **数据存储**：pickle (历史记录)、JSON (自定义模板)

### 项目结构
```
AI报告生成助手/
├── app.py                 # 主应用程序
├── requirements.txt       # 依赖列表
├── .env.example          # 环境变量示例
├── .env                  # 环境变量配置（本地使用）
├── .gitignore            # Git 忽略文件
├── reports_history.pkl   # 历史记录（自动生成）
├── custom_templates.json # 自定义模板（自动生成）
└── README.md             # 本文件
```

## 📦 依赖说明

| 包名 | 版本 | 用途 |
|-----|------|------|
| streamlit | ≥1.28.0 | Web 框架 |
| requests | ≥2.31.0 | HTTP 请求 |
| python-dotenv | ≥1.0.0 | 环境变量加载 |

### 安装所有依赖
```bash
pip install streamlit>=1.28.0 requests>=2.31.0 python-dotenv>=1.0.0
```

## 🔐 安全建议

### 生产环境部署
1. **不要在代码中硬编码 API Key**
   ```python
   # ❌ 错误
   API_KEY = "sk-xxxxx"
   
   # ✅ 正确
   API_KEY = os.getenv("DASHSCOPE_API_KEY")
   ```

2. **使用 .env 文件管理敏感信息**
   ```env
   # .env
   DASHSCOPE_API_KEY=sk-your-actual-key
   ```

3. **将 .env 添加到 .gitignore**
   ```bash
   echo ".env" >> .gitignore
   ```

4. **定期轮换 API Key**
   - 每月或每季度更换一次
   - 立即删除泄露的 Key

## 🐛 常见问题

### Q1: 报错 "ModuleNotFoundError: No module named 'dotenv'"
**A**: 未安装 python-dotenv，运行：
```bash
pip install python-dotenv
```

### Q2: "未检测到 DASHSCOPE_API_KEY"
**A**: 检查以下几点：
1. `.env` 文件是否存在且格式正确
2. 环境变量是否已设置
3. 应用是否已重启（重启后才能读取环境变量）

### Q3: API 请求超时
**A**: 可能原因：
1. 网络连接不稳定
2. API 配额已用完
3. 服务器响应慢

解决办法：
- 检查网络连接
- 登录 DashScope 控制台检查配额
- 稍后重试

### Q4: 如何修改应用端口？
**A**: 运行时指定端口：
```bash
streamlit run app.py --server.port 8888
```

## 🚀 进阶功能

### 模板自定义
```python
# 在 "🎨 报告模板" 中自定义：
模板名称: "我的企业风格"
模板前缀: """
## 企业周报
生成时间：2024年2月
"""
模板后缀: """
---
声明：本报告自动生成，仅供参考
"""
```

### 批量生成
可在高级选项中设置多个参数组合，系统会逐个生成。

## 📈 性能优化建议

1. **历史记录定期清理**
   - 使用"清空所有历史"保持应用流畅
   - 或定期删除 `reports_history.pkl`

2. **缓存优化**
   ```bash
   # 清理 Streamlit 缓存
   streamlit cache clear
   ```

3. **并发处理**
   - 不建议同时发起多个 API 请求
   - 建议分别生成后再进行操作

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

### 提交流程
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT License，详见 [LICENSE](LICENSE) 文件。

## 👤 作者

- GitHub: [Sylus-with-ease]
- 邮箱: [1368412172@qq.com]

## 🙏 致谢

- 感谢 [Streamlit](https://streamlit.io) 提供优秀的 Web 框架
- 感谢 [阿里云](https://www.aliyun.com) 提供通义千问 API
- 感谢所有贡献者和用户的支持

## 📞 支持

有问题或建议？
- 📧 Email: [1368412172@qq.com]
- 🐛 提交 Issue: [GitHub Issues]
- 💬 讨论区: [GitHub Discussions]

---

**Made with ❤️ by [Sylus]**

**最后更新**: 2026 年 2 月 12 日

