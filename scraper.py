import json
import re
import os
from datetime import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# 配置
MODELSCOPE_API = "https://www.modelscope.cn/api/v1/models"
HUGGINGFACE_API = "https://huggingface.co/api/models"
KEYWORDS = ["qwen", "tongyi", "通义", "千问"]
OUTPUT_FILE = "models.json"
README_FILE = "README.md"

def fetch_modelscope_models():
    """从魔搭社区抓取通义相关模型"""
    models = []
    try:
        # 搜索通义相关模型
        search_url = f"{MODELSCOPE_API}?Name=qwen&PageSize=100"
        response = requests.get(search_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if "Data" in data:
                for item in data["Data"]:
                    model_info = {
                        "name": item.get("Name", ""),
                        "size": extract_size(item.get("Introduction", "")),
                        "description": item.get("Introduction", "")[:200] + "..." if len(item.get("Introduction", "")) > 200 else item.get("Introduction", ""),
                        "modelscope_url": f"https://www.modelscope.cn/models/{item.get('Name', '')}",
                        "huggingface_url": "",
                        "source": "modelscope",
                        "updated_at": datetime.now().isoformat()
                    }
                    models.append(model_info)
    except Exception as e:
        print(f"Error fetching from ModelScope: {e}")
    return models

def fetch_huggingface_models():
    """从 HuggingFace 抓取 Qwen 相关模型"""
    models = []
    try:
        search_url = f"{HUGGINGFACE_API}?search=qwen&limit=100"
        response = requests.get(search_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                model_id = item.get("id", "")
                if any(keyword in model_id.lower() for keyword in ["qwen", "tongyi"]):
                    model_info = {
                        "name": model_id,
                        "size": extract_size_from_tags(item.get("tags", [])),
                        "description": item.get("description", "") or "",
                        "modelscope_url": "",
                        "huggingface_url": f"https://huggingface.co/{model_id}",
                        "source": "huggingface",
                        "updated_at": datetime.now().isoformat()
                    }
                    models.append(model_info)
    except Exception as e:
        print(f"Error fetching from HuggingFace: {e}")
    return models

def extract_size(text):
    """从描述中提取模型尺寸"""
    if not text:
        return "-"
    # 匹配常见尺寸格式
    patterns = [
        r'(\d+(\.\d+)?[BMK])',  # 7B, 13B, 70B, 1.8B
        r'(\d+)[\s-]?billion',
        r'(\d+)[\s-]?亿参数',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return "-"

def extract_size_from_tags(tags):
    """从 HuggingFace tags 中提取尺寸"""
    size_keywords = ["7b", "13b", "70b", "110b", "1.8b", "3b", "14b", "32b", "72b"]
    for tag in tags:
        if tag.lower() in size_keywords:
            return tag.upper()
    return "-"

def merge_models(modelscope_models, hf_models):
    """合并并去重模型列表"""
    merged = {}
    
    # 先添加魔搭的模型
    for m in modelscope_models:
        name = m["name"].lower().replace("-", "_")
        merged[name] = m
    
    # 合并 HuggingFace 的模型
    for m in hf_models:
        name = m["name"].lower().replace("-", "_")
        if name in merged:
            # 合并 URL
            if m["huggingface_url"] and not merged[name]["huggingface_url"]:
                merged[name]["huggingface_url"] = m["huggingface_url"]
            if m["size"] != "-":
                merged[name]["size"] = m["size"]
        else:
            merged[name] = m
    
    return list(merged.values())

def generate_markdown_table(models):
    """生成 Markdown 表格"""
    # 按名称排序
    models_sorted = sorted(models, key=lambda x: x.get("name", ""))
    
    lines = ["| 模型名称 | 尺寸 | 简介 | 魔搭地址 | HuggingFace |", "|---------|------|------|---------|-------------|"]
    
    for m in models_sorted[:50]:  # 只显示前50个
        name = m.get("name", "-")
        size = m.get("size", "-")
        desc = m.get("description", "-")[:80] + "..." if len(m.get("description", "")) > 80 else m.get("description", "-")
        # 转义 Markdown 特殊字符
        desc = desc.replace("|", "\\|").replace("\n", " ")
        
        ms_url = m.get("modelscope_url", "")
        hf_url = m.get("huggingface_url", "")
        
        ms_link = f"[魔搭]({ms_url})" if ms_url else "-"
        hf_link = f"[HF]({hf_url})" if hf_url else "-"
        
        lines.append(f"| {name} | {size} | {desc} | {ms_link} | {hf_link} |")
    
    return "\n".join(lines)

def update_readme(table_content):
    """更新 README.md 中的表格"""
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 替换表格部分
        start_marker = "<!-- MODEL_TABLE_START -->"
        end_marker = "<!-- MODEL_TABLE_END -->"
        
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n{table_content}\n{end_marker}"
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("README.md updated successfully!")
    except Exception as e:
        print(f"Error updating README: {e}")

def main():
    print("开始抓取通义模型数据...")
    print("-" * 50)
    
    # 抓取数据
    print("1. 正在从魔搭社区抓取...")
    ms_models = fetch_modelscope_models()
    print(f"   找到 {len(ms_models)} 个模型")
    
    print("2. 正在从 HuggingFace 抓取...")
    hf_models = fetch_huggingface_models()
    print(f"   找到 {len(hf_models)} 个模型")
    
    # 合并数据
    print("3. 合并数据...")
    all_models = merge_models(ms_models, hf_models)
    print(f"   去重后共 {len(all_models)} 个模型")
    
    # 保存原始数据
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "total": len(all_models),
            "models": all_models
        }, f, ensure_ascii=False, indent=2)
    print(f"4. 数据已保存到 {OUTPUT_FILE}")
    
    # 更新 README
    print("5. 正在更新 README.md...")
    table = generate_markdown_table(all_models)
    update_readme(table)
    
    print("-" * 50)
    print("✅ 完成！")

if __name__ == "__main__":
    main()
