#!/usr/bin/env python3
"""
🔐 GitHub部署安全检查脚本
验证项目是否安全可部署（特别是敏感文件）
"""

import os
import sys
from pathlib import Path

def check_gitignore():
    """检查 .gitignore 是否正确配置"""
    print("\n📋 检查 .gitignore 配置...")
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        print("❌ .gitignore 文件不存在")
        return False
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_entries = [
        '.env',
        'reports_history.pkl',
        'custom_templates.json',
        '__pycache__',
        'venv'
    ]
    
    missing = [entry for entry in required_entries if entry not in content]
    
    if missing:
        print(f"❌ .gitignore 缺少以下条目：{missing}")
        return False
    
    print("✅ .gitignore 配置正确")
    return True

def check_env_file():
    """检查是否存在未被忽略的 .env 文件"""
    print("\n🔐 检查 .env 文件...")
    
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  发现 .env 文件（应该在 .gitignore 中）")
        print("   提示：这个文件通常不应上传到GitHub")
        return True  # 警告但不失败
    
    print("✅ 未发现 .env 文件（正确）")
    return True

def check_env_example():
    """检查 .env.example 是否存在"""
    print("\n📝 检查 .env.example...")
    
    env_example = Path(".env.example")
    if not env_example.exists():
        print("❌ .env.example 不存在（用户需要这个作为参考）")
        return False
    
    with open(env_example, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'sk-' in content.lower() or 'real' in content.lower():
        print("⚠️  .env.example 看起来包含真实数据，应该只有示例值")
        return False
    
    print("✅ .env.example 正确（包含示例值）")
    return True

def check_api_key_in_code():
    """检查代码中是否硬编码了API密钥"""
    print("\n🔍 检查代码中的硬编码密钥...")
    
    dangerous_patterns = [
        'DASHSCOPE_API_KEY=',
        'sk-',
        'api_key=',
        'apikey=',
    ]
    
    py_files = Path(".").glob("**/*.py")
    found_issues = False
    
    for py_file in py_files:
        # 跳过虚拟环境和隐藏目录
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # 跳过注释和示例
                if line.strip().startswith('#'):
                    continue
                
                for pattern in dangerous_patterns:
                    if pattern in line.lower() and 'sk-' in line.lower():
                        print(f"❌ {py_file}:{line_num} - 发现可能的API密钥")
                        found_issues = True
    
    if found_issues:
        return False
    
    print("✅ 代码中无硬编码密钥")
    return True

def check_requirements():
    """检查 requirements.txt 是否存在"""
    print("\n📦 检查 requirements.txt...")
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("❌ requirements.txt 不存在")
        return False
    
    with open(req_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_packages = ['streamlit', 'requests', 'python-dotenv']
    missing = [pkg for pkg in required_packages if pkg not in content]
    
    if missing:
        print(f"⚠️  requirements.txt 缺少：{missing}")
        return False
    
    print("✅ requirements.txt 配置正确")
    return True

def check_readme():
    """检查 README.md 是否存在"""
    print("\n📖 检查 README.md...")
    
    readme = Path("README.md")
    if not readme.exists():
        print("❌ README.md 不存在")
        return False
    
    print("✅ README.md 存在")
    return True

def main():
    print("=" * 50)
    print("🔐 GitHub 部署安全检查")
    print("=" * 50)
    
    checks = [
        ("✓ .gitignore", check_gitignore),
        ("✓ .env 文件", check_env_file),
        ("✓ .env.example", check_env_example),
        ("✓ 代码检查", check_api_key_in_code),
        ("✓ requirements.txt", check_requirements),
        ("✓ README.md", check_readme),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"❌ {name} 检查时出错：{e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print(f"检查结果：{sum(results)}/{len(results)} 通过")
    print("=" * 50)
    
    if all(results):
        print("\n✅ 所有检查通过！项目安全可部署到 GitHub")
        print("\n建议的后续步骤：")
        print("  1. git add .")
        print("  2. git commit -m 'Initial commit: AI Report Generator'")
        print("  3. git push origin main")
        return 0
    else:
        print("\n❌ 存在未通过的检查，请修复后再部署")
        return 1

if __name__ == "__main__":
    sys.exit(main())
