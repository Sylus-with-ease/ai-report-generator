# 📝 GitHub 部署快速指南

## 🎯 上传前最后检查

### 1️⃣ 验证敏感文件未被追踪

```bash
# 确认 .env 不在 Git 中
git status    # 不应该出现 .env

# 验证方式
git ls-files .env    # 应该返回空
```

### 2️⃣ 验证 .gitignore 生效

```bash
# 如果 .env 被误追踪，移除它
git rm --cached .env
git commit -m "Remove .env from version control"
```

### 3️⃣ 最后提交

```bash
git add .
git commit -m "Initial commit: AI Report Generator

- Multi-type report generation
- Custom templates
- Export to Markdown/TXT/HTML
- Secure API key management with .env
- History and template persistence"

git push origin main
```

---

## 📂 GitHub 上传清单

### ✅ 需要上传
- `app.py` - 主应用
- `requirements.txt` - 依赖列表
- `README.md` - 项目说明
- `.env.example` - **环境变量模板（示例）**
- `.gitignore` - **Git 配置**
- `.editorconfig` - 代码风格
- `LICENSE` - 开源证书
- `run.sh` / `run.bat` - 运行脚本

### ❌ 不要上传（.gitignore已配置）
- `.env` - ⚠️ **包含你的API密钥！**
- `.env.local` - 本地测试密钥
- `reports_history.pkl` - 用户生成的历史记录
- `custom_templates.json` - 用户自定义模板
- `__pycache__/` - Python 缓存
- `venv/` - 虚拟环境
- `.streamlit/` - Streamlit 缓存

---

## 🔒 安全确认

| 项目 | 状态 | 说明 |
|------|------|------|
| API Key 硬编码 | ✅ 否 | 使用 python-dotenv 管理 |
| .env 在 .gitignore | ✅ 是 | 防止密钥泄露 |
| .env.example 存在 | ✅ 是 | 用户参考 |
| 代码注释清晰 | ✅ 是 | 便于他人理解 |
| 相对路径配置 | ✅ 是 | 跨平台兼容 |

---

## 📝 GitHub 仓库设置建议

1. **仓库描述** (About)
   ```
   📝 AI Report Generator - Streamlit + Aliyun Tongyi Qianwen
   多类型报告生成、自定义模板、多格式导出
   ```

2. **Topics** (标签)
   - streamlit
   - ai
   - report-generator
   - aliyun-qianwen
   - python

3. **README 首行添加演示 GIF**（可选）
   ```markdown
   ![Demo](./demo.gif)
   ```

---

## 🚀 部署后维护

### 用户如何使用

```bash
# 1. 克隆
git clone https://github.com/Sylus/ai-report-generator.git

# 2. 设置
cp .env.example .env
# 编辑 .env，填入 API Key

# 3. 运行
pip install -r requirements.txt
streamlit run app.py
```

### 未来更新

```bash
# 新增功能/修复时
git add .
git commit -m "chore: update description"
git push origin main
```

---

✅ **准备就绪，可以上传到 GitHub！** 🎉
