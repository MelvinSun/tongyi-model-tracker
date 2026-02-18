import json
from datetime import datetime

# 模拟一些示例数据来测试流程
SAMPLE_MODELS = [
    {
        "name": "Qwen/Qwen2.5-72B-Instruct",
        "size": "72B",
        "description": "Qwen2.5 系列最大模型，支持 128K 上下文，多语言能力强",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/Qwen2.5-72B-Instruct",
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-72B-Instruct",
        "updated_at": datetime.now().isoformat()
    },
    {
        "name": "Qwen/Qwen2.5-32B-Instruct",
        "size": "32B",
        "description": "Qwen2.5 系列大模型，平衡性能与效率",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/Qwen2.5-32B-Instruct",
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-32B-Instruct",
        "updated_at": datetime.now().isoformat()
    },
    {
        "name": "Qwen/Qwen2.5-14B-Instruct",
        "size": "14B",
        "description": "Qwen2.5 系列中等模型，适合本地部署",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/Qwen2.5-14B-Instruct",
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-14B-Instruct",
        "updated_at": datetime.now().isoformat()
    },
    {
        "name": "Qwen/Qwen2.5-7B-Instruct",
        "size": "7B",
        "description": "Qwen2.5 系列小模型，消费级 GPU 可运行",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/Qwen2.5-7B-Instruct",
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct",
        "updated_at": datetime.now().isoformat()
    },
    {
        "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "size": "32B",
        "description": "专为代码生成优化的 Qwen2.5 模型",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/Qwen2.5-Coder-32B-Instruct",
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct",
        "updated_at": datetime.now().isoformat()
    },
    {
        "name": "Qwen/Qwen2.5-Math-72B-Instruct",
        "size": "72B",
        "description": "专为数学推理优化的 Qwen2.5 模型",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/Qwen2.5-Math-72B-Instruct",
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-Math-72B-Instruct",
        "updated_at": datetime.now().isoformat()
    },
    {
        "name": "Qwen/QwQ-32B-Preview",
        "size": "32B",
        "description": "QwQ 推理模型预览版，擅长复杂推理任务",
        "modelscope_url": "https://www.modelscope.cn/models/qwen/QwQ-32B-Preview",
        "huggingface_url": "https://huggingface.co/Qwen/QwQ-32B-Preview",
        "updated_at": datetime.now().isoformat()
    }
]

def generate_markdown_table(models):
    """生成 Markdown 表格"""
    models_sorted = sorted(models, key=lambda x: x.get("name", ""))
    
    lines = ["| 模型名称 | 尺寸 | 简介 | 魔搭地址 | HuggingFace |", "|---------|------|------|---------|-------------|"]
    
    for m in models_sorted:
        name = m.get("name", "-")
        size = m.get("size", "-")
        desc = m.get("description", "-")[:80] + "..." if len(m.get("description", "")) > 80 else m.get("description", "-")
        desc = desc.replace("|", "\\|").replace("\n", " ")
        
        ms_url = m.get("modelscope_url", "")
        hf_url = m.get("huggingface_url", "")
        
        ms_link = f"[魔搭]({ms_url})" if ms_url else "-"
        hf_link = f"[HF]({hf_url})" if hf_url else "-"
        
        lines.append(f"| {name} | {size} | {desc} | {ms_link} | {hf_link} |")
    
    return "\n".join(lines)

def update_readme(table_content):
    """更新 README.md 中的表格"""
    import re
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        start_marker = "<!-- MODEL_TABLE_START -->"
        end_marker = "<!-- MODEL_TABLE_END -->"
        
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n{table_content}\n{end_marker}"
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # 更新最后更新时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_content = new_content.replace("待首次运行", now)
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("README.md 更新成功!")
    except Exception as e:
        print(f"更新 README 失败: {e}")

def main():
    print("开始生成示例数据...")
    print("-" * 50)
    
    # 保存示例数据
    with open("models.json", "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "total": len(SAMPLE_MODELS),
            "models": SAMPLE_MODELS
        }, f, ensure_ascii=False, indent=2)
    print(f"1. 数据已保存到 models.json (共 {len(SAMPLE_MODELS)} 个模型)")
    
    # 生成表格
    print("2. 正在生成 Markdown 表格...")
    table = generate_markdown_table(SAMPLE_MODELS)
    
    # 更新 README
    print("3. 正在更新 README.md...")
    update_readme(table)
    
    print("-" * 50)
    print("✅ 完成！")
    print("\n生成的表格预览:")
    print(table[:500] + "...")

if __name__ == "__main__":
    main()
