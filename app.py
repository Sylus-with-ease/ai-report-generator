import streamlit as st
import requests
import os
import pickle
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ==================== 环境配置 ====================
"""
环境变量加载模块
使用 python-dotenv 从 .env 文件加载敏感信息
避免在代码中硬编码 API Key，提升安全性
"""
# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量读取 API Key，如不存在则显示警告并停止应用
API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not API_KEY:
    st.warning("⚠️ 未检测到 DASHSCOPE_API_KEY！")
    st.info("""
    **设置方法**：
    1. **最简单方式**：创建 `.env` 文件，添加：
       ```
       DASHSCOPE_API_KEY=sk-your-api-key-here
       ```
    2. **环境变量方式**：
       - Windows：在系统环境变量中添加 DASHSCOPE_API_KEY
       - Linux/Mac：`export DASHSCOPE_API_KEY="your_key"`
    
    **获取 API Key**：访问 [阿里云通义千问](https://dashscope.aliyuncs.com)
    """)
    st.stop()

# 设置页面配置（必须是第一个 st 命令）
st.set_page_config(
    page_title="📝 AI 周报生成器",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# 自定义样式
st.markdown("""
    <style>
    :root {
        --primary-color: #3498db;
        --success-color: #2ecc71;
        --warning-color: #f39c12;
        --danger-color: #e74c3c;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    /* 优化按钮样式 */
    .stButton>button[kind="primary"] {
        background-color: #3498db !important;
        color: white !important;
    }
    /* 优化输入框 */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .report-box {
        border-left: 4px solid #3498db;
        padding: 15px;
        border-radius: 8px;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    .history-item {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        background-color: white;
        transition: all 0.3s ease;
    }
    /* 优化历史记录 hover 效果 */
    .history-item:hover {
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    @media (max-width: 768px) {
        .stColumn { width: 100% !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 定义函数 ====================
"""
核心业务函数模块
包含历史记录管理和报告模板管理功能
"""

def load_history_from_disk():
    """
    从本地 pickle 文件加载历史记录
    
    功能：
        - 检查历史记录文件是否存在
        - 如果存在，加载到 session_state
        - 异常处理：若加载失败，显示警告信息
    
    返回值：无（直接更新 st.session_state）
    """
    history_file = Path("reports_history.pkl")
    if history_file.exists():
        try:
            with open(history_file, "rb") as f:
                st.session_state.reports_history = pickle.load(f)
        except Exception as e:
            st.warning(f"加载历史记录失败: {e}")

def save_history_to_disk():
    """
    将历史记录保存到本地 pickle 文件
    
    功能：
        - 将 session_state 中的历史记录序列化为 pickle 格式
        - 存储到 reports_history.pkl 文件
        - 异常处理：若保存失败，显示错误信息
    
    返回值：无（直接写入文件）
    """
    try:
        with open("reports_history.pkl", "wb") as f:
            pickle.dump(st.session_state.reports_history, f)
    except Exception as e:
        st.error(f"保存历史记录失败: {e}")

def load_templates():
    """
    加载所有可用的报告模板（预设 + 自定义）
    
    功能：
        - 初始化 4 个预设模板
        - 尝试加载自定义模板 (custom_templates.json)
        - 合并预设和自定义模板
    
    返回值：
        dict: {模板名: {prefix: 前缀, suffix: 后缀}}
        
    示例：
        {
            "专业正式": {
                "prefix": "## 报告摘要\\n...",
                "suffix": "\\n## 下周计划\\n..."
            }
        }
    """
    default_templates = {
        "专业正式": {
            "prefix": "## 报告摘要\n本报告总结了本周工作的主要进展和成果。\n\n## 核心成就\n",
            "suffix": "\n\n## 下周计划\n继续推进相关工作，确保项目按时交付。"
        },
        "简洁扼要": {
            "prefix": "### 本周工作\n",
            "suffix": "\n\n### 下步行动\n持续推进中。"
        },
        "数据驱动": {
            "prefix": "**关键指标**\n- 完成率：待补充\n- 效率提升：待补充\n\n**详细成果**\n",
            "suffix": "\n\n**数据对比**\n周环比提升中，持续优化迭代。"
        },
        "创意活泼": {
            "prefix": "🎯 **本周亮点回顾**\n",
            "suffix": "\n\n✨ 更多精彩下周继续！"
        }
    }
    
    # 尝试从本地加载自定义模板
    template_file = Path("custom_templates.json")
    if template_file.exists():
        try:
            with open(template_file, "r", encoding="utf-8") as f:
                custom_templates = json.load(f)
                # 将自定义模板合并到预设模板中
                default_templates.update(custom_templates)
        except Exception as e:
            st.warning(f"加载自定义模板失败: {e}")
    
    return default_templates

def save_template(name, prefix, suffix):
    """
    保存用户自定义的报告模板
    
    参数：
        name (str): 模板名称
        prefix (str): 报告模板前缀（开头部分）
        suffix (str): 报告模板后缀（结尾部分）
    
    功能：
        - 加载现有的自定义模板 JSON 文件
        - 添加或更新指定的模板
        - 保存到 custom_templates.json
        - 支持 UTF-8 编码（中文字符）
    
    返回值：
        bool: True 表示保存成功，False 表示失败
    """
    try:
        template_file = Path("custom_templates.json")
        templates = {}
        # 如果文件存在，先加载现有模板
        if template_file.exists():
            with open(template_file, "r", encoding="utf-8") as f:
                templates = json.load(f)
        
        # 添加或更新模板
        templates[name] = {"prefix": prefix, "suffix": suffix}
        # 保存到文件（ensure_ascii=False 保证中文不转义）
        with open(template_file, "w", encoding="utf-8") as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"保存模板失败: {e}")
        return False

# ==================== 初始化状态 ====================
"""
Streamlit Session State 初始化
session_state 在页面重新运行时保持状态，类似于全局变量
"""

# 初始化历史记录列表，并从磁盘加载已保存的记录
if "reports_history" not in st.session_state:
    st.session_state.reports_history = []
    load_history_from_disk()

# 初始化模板字典（预设 + 自定义）
if "templates" not in st.session_state:
    st.session_state.templates = load_templates()

# ==================== 页面标题 ====================
col1, col2 = st.columns([5, 1])
with col1:
    st.title("📝 AI 报告生成助手")
    st.caption("✨ 智能生成日报、周报、月报及更多文档")
with col2:
    if st.button("🔄 刷新", use_container_width=True):
        st.rerun()

st.divider()

# ==================== 侧边栏 - 报告类型和风格 ====================
with st.sidebar:
    st.header("⚙️ 配置选项")
    
    # 报告类型
    st.subheader("📋 报告类型")
    report_category = st.radio(
        "选择报告大类",
        ["日常报告", "专项报告", "分析报告"]
    )
    
    report_type_map = {
        "日常报告": ["日报", "周报", "月报"],
        "专项报告": ["季度总结", "项目复盘", "技术周报", "产品周报", "运营周报"],
        "分析报告": ["数据分析", "竞品分析", "市场调研"]
    }
    
    report_type = st.selectbox(
        "具体类型",
        report_type_map.get(report_category, [])
    )
    
    # 语气和风格
    st.subheader("🎨 语气和风格")
    tone = st.selectbox(
        "选择语气",
        ["正式商务", "轻松活泼", "技术严谨", "领导汇报", "简洁扼要"]
    )
    
    style = st.selectbox(
        "选择风格",
        ["结构化列表", "段落叙述", "要点总结", "数据驱动"]
    )
    
    # 输出格式
    st.subheader("📤 输出格式")
    output_format = st.radio(
        "选择格式",
        ["Markdown", "纯文本", "HTML"]
    )
    
    st.divider()
    
    # 历史记录管理
    st.subheader("📚 历史记录")
    if st.button("🗑️ 清空所有历史", use_container_width=True):
        st.session_state.reports_history = []
        save_history_to_disk()
        st.success("已清空历史记录")
        st.rerun()
    
    # 模板管理
    st.divider()
    st.subheader("🎨 报告模板")
    with st.expander("自定义模板"):
        template_name = st.text_input("模板名称", placeholder="例如：我的模板")
        template_prefix = st.text_area("模板前缀（开头）", placeholder="报告开头内容...", height=100)
        template_suffix = st.text_area("模板后缀（结尾）", placeholder="报告结尾内容...", height=100)
        
        if st.button("💾 保存模板", use_container_width=True):
            if template_name and (template_prefix or template_suffix):
                if save_template(template_name, template_prefix, template_suffix):
                    st.success(f"✅ 模板 '{template_name}' 已保存")
                    st.session_state.templates = load_templates()
            else:
                st.warning("请填写模板名称和内容")

# ==================== 主要区域 - 分栏布局 ====================
input_col, preview_col = st.columns([1, 1], gap="medium")

with input_col:
    st.subheader("📌 输入内容")
    
    work_content = st.text_area(
        "输入你的工作内容、成就或数据",
        height=200,
        placeholder="例如：\n- 完成了API接口开发\n- 修复了3个bug\n- 代码覆盖率提升到85%\n- 参加了团队讨论会议"
    )
    
    st.info("💡 **提示**: 内容越具体详细，生成的报告越专业")
    
    # 高级选项（可折叠）
    with st.expander("⚙️ 高级选项"):
        include_metrics = st.checkbox("包含指标和数据", value=True)
        include_next_plan = st.checkbox("包含下周计划", value=True)
        focus_area = st.text_input(
            "重点强调的领域（可选）",
            placeholder="例如：团队协作、创新、客户满意度"
        )
        
        st.divider()
        st.write("**模板选择**")
        template_names = list(st.session_state.templates.keys())
        selected_template = st.selectbox(
            "选择报告模板",
            template_names,
            help="选择预设模板或自定义模板来快速生成报告"
        )

with preview_col:
    st.subheader("👁️ 预览和历史")
    
    # 历史记录显示
    if st.session_state.reports_history:
        st.write(f"📖 **最近生成** ({len(st.session_state.reports_history)} 条)")
        
        for i, report_item in enumerate(reversed(st.session_state.reports_history[-5:])):
            with st.container(border=True):
                col_time, col_copy = st.columns([3, 1])
                with col_time:
                    st.caption(f"⏰ {report_item['timestamp']}")
                    st.caption(f"类型: {report_item['type']} | 语气: {report_item['tone']}")
                
                if st.button("📋 查看", key=f"view_{i}", use_container_width=True):
                    st.session_state.preview_report = report_item['content']
                    st.rerun()
    else:
        st.info("💡 **如何开始**：\n1. 在左侧输入你的工作内容\n2. 点击【生成报告】按钮\n3. 系统将自动生成专业报告\n\n✨ 支持多种报告类型和风格定制")

st.divider()

# ==================== 生成按钮和结果区域 ====================
col1, col2, col3 = st.columns([1.5, 1, 1], gap="small")

with col1:
    generate_btn = st.button(
        "✨ 生成报告",
        use_container_width=True,
        type="primary"
    )

with col2:
    clear_btn = st.button("🗑️ 清空", use_container_width=True)

with col3:
    if "preview_report" in st.session_state and st.session_state.preview_report:
        export_btn = st.button("📥 导出", use_container_width=True)
    else:
        st.button("📥 导出", use_container_width=True, disabled=True)

if clear_btn:
    if "preview_report" in st.session_state:
        del st.session_state.preview_report
    st.rerun()

# ==================== 生成报告逻辑 ====================
if generate_btn:
    if not work_content.strip():
        st.info("💡 **请输入工作内容**：描述你的工作成就、完成的任务或重要数据，这样生成的报告会更专业、更具体。\n\n✨ 示例内容：\n- 完成了用户认证模块开发\n- 修复了3个严重bug\n- 代码覆盖率提升到92%\n- 与产品团队进行了2次需求讨论")
    else:
        # 进度提示 - 使用自定义加载状态
        progress_container = st.container()
        with progress_container:
            col1, col2 = st.columns([3, 1])
            with col1:
                progress_bar = st.progress(0, text="")
            with col2:
                status_text = st.empty()
            
            # 构建完整的提示词
            prompt = f"""
            你是一个专业的办公助手和文案专家。请根据以下信息生成一份专业的{report_type}。

            【基本信息】
            - 报告类型：{report_type}
            - 语气风格：{tone}
            - 内容风格：{style}
            - 工作内容：{work_content}
            
            【可选增强】
            - 包含指标数据：{include_metrics}
            - 包含下周计划：{include_next_plan}
            {f'- 重点强调：{focus_area}' if focus_area else ''}
            
            【要求】
            1. 内容必须专业、有条理、逻辑清晰
            2. 如果是"{style}"风格，请使用对应的组织方式
            3. 语气应该是"{tone}"
            4. 避免冗余，直击要点
            5. 如果包含数据，请突出数据对比和趋势
            6. 长度控制在500-1000字
            
            请直接生成报告内容，不需要额外说明。
            """
            
            status_text.text("📤")
            progress_bar.progress(30, text="正在调用 AI 服务...")
            
            try:
                # ============ API 请求阶段 ============
                # 调用阿里云通义千问 API 生成报告内容
                headers = {
                    "Authorization": f"Bearer {API_KEY}",  # 认证头
                    "Content-Type": "application/json"      # 请求格式
                }
                data = {
                    "model": "qwen-turbo",  # 使用 turbo 模型（速度快，成本低）
                    "input": {"messages": [{"role": "user", "content": prompt}]},
                    "parameters": {"result_format": "message"}
                }
                
                # 发送 POST 请求到阿里云 API，设置 60 秒超时
                response = requests.post(
                    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
                    headers=headers,
                    json=data,
                    timeout=60
                )
                
                # 更新进度条
                progress_bar.progress(70, text="报告生成中...")
                status_text.text("✨")
                
                # ============ 响应处理阶段 ============
                if response.status_code == 200:
                    # API 返回成功，解析 JSON 响应
                    result = response.json()
                    ai_report = result["output"]["choices"][0]["message"]["content"]
                    
                    # ============ 模板应用阶段 ============
                    # 获取用户选择的模板
                    template = st.session_state.templates.get(selected_template, {})
                    template_prefix = template.get("prefix", "")
                    template_suffix = template.get("suffix", "")
                    
                    # 组合：模板前缀 + AI 生成内容 + 模板后缀
                    final_report = f"{template_prefix}\n{ai_report}\n{template_suffix}"
                    
                    # 进度完成
                    progress_bar.progress(100, text="完成！")
                    status_text.text("✅")
                    
                    # ============ 数据保存阶段 ============
                    # 创建历史记录对象，包含所有元数据
                    report_item = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": report_type,
                        "tone": tone,
                        "template": selected_template,
                        "content": final_report,
                        "input": work_content
                    }
                    # 添加到历史记录并持久化保存
                    st.session_state.reports_history.append(report_item)
                    save_history_to_disk()
                    # 更新预览区域
                    st.session_state.preview_report = final_report
                    
                    # 清空进度提示后重新运行页面
                    import time
                    time.sleep(0.5)
                    progress_container.empty()
                    st.rerun()
                else:
                    # API 返回错误状态码
                    st.error(f"❌ API 请求失败 (状态码: {response.status_code})")
                    st.text(f"错误信息: {response.text}")
            
            except requests.exceptions.Timeout:
                # 网络超时异常处理
                st.error("❌ 请求超时，请检查网络连接")
            except Exception as e:
                # 其他异常处理
                st.error(f"❌ 发生错误: {str(e)}")
            finally:
                # 无论成功失败都清空进度提示
                progress_container.empty()

# ==================== 显示生成的报告 ====================
if "preview_report" in st.session_state and st.session_state.preview_report:
    st.success("✅ 报告已生成！")
    
    # 显示报告内容
    st.markdown("---")
    st.markdown("""
        <div class="report-box">
    """, unsafe_allow_html=True)
    
    st.markdown(st.session_state.preview_report)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 导出选项
    st.divider()
    st.subheader("📥 导出选项")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Markdown 导出
        st.download_button(
            "📄 下载 Markdown",
            st.session_state.preview_report,
            file_name=f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        # 纯文本导出
        st.download_button(
            "📋 下载 TXT",
            st.session_state.preview_report,
            file_name=f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        # HTML 导出
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{report_type}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; max-width: 800px; }}
                h1 {{ color: #333; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                p {{ color: #555; }}
            </style>
        </head>
        <body>
            <h1>{report_type}</h1>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            {st.session_state.preview_report.replace(chr(10), '<br>')}
        </body>
        </html>
        """
        st.download_button(
            "🌐 下载 HTML",
            html_content,
            file_name=f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )

# ==================== 页脚 ====================
st.divider()
with st.expander("📖 项目说明（面试可讲）"):
    st.markdown("""
    ### 技术栈
    - **前端**：Streamlit（响应式布局、自定义 CSS）
    - **后端**：Python（文件操作、数据持久化）
    - **AI 集成**：调用阿里云通义千问 API（qwen-turbo 模型）
    - **配置管理**：python-dotenv（环保管理 API Key）

    ### 核心功能
    1. **多类型报告生成** - 支持日报/周报/月报/季度总结等
    2. **自定义语气/风格/输出格式** - 满足不同场景需求
    3. **本地历史记录持久化** - 使用 pickle 存储
    4. **多格式导出** - 支持 Markdown/TXT/HTML

    ### ⭐ 创新亮点：报告模板自定义
    - **预设 4 个专业模板**：专业正式、简洁扼要、数据驱动、创意活泼
    - **自定义模板功能**：在侧边栏定义模板前缀和后缀，一键保存
    - **模板持久化**：自定义模板存储为 JSON，支持跨会话使用
    - **实时切换**：在高级选项中选择模板，生成时自动应用

    ### 技术亮点
    - ✅ 安全提示（python-dotenv 管理 API Key，避免硬编码泄露）
    - ✅ 自定义加载状态（实时进度提示 30% → 70% → 100%）
    - ✅ 空内容引导提示（友好的用户指导）
    - ✅ 响应式设计（支持移动端适配）
    - ✅ 错误处理（完善的异常捕获）
    - ✅ 历史记录管理（查看/清空功能）

    ### 应用场景
    - 📝 职场日常报告生成
    - 📊 项目进度总结
    - 📈 数据分析报告
    - 🎯 工作成果展示

    ### 部署说明
    详见项目 `README.md` 文件，包含：
    - 环境搭建步骤
    - API Key 配置方法（.env 文件或环境变量）
    - 功能使用指南
    - 常见问题解答
    """)

st.caption("🚀 AI 报告生成助手 | 模板自定义 | 安全的 API 管理 | 多格式导出 | 自动保存历史")