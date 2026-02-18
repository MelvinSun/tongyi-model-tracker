# 通义大模型追踪器 (Tongyi Model Tracker)

每日自动抓取阿里巴巴通义实验室新发大模型，梳理模型名称、尺寸、介绍、魔搭及 HuggingFace 地址等信息。

## 📊 最新模型列表

<!-- MODEL_TABLE_START -->
| 模型名称 | 尺寸 | 简介 | 魔搭地址 | HuggingFace |
|---------|------|------|---------|-------------|
| Qwen/QwQ-32B-Preview | 32B | QwQ 推理模型预览版，擅长复杂推理任务 | [魔搭](https://www.modelscope.cn/models/qwen/QwQ-32B-Preview) | [HF](https://huggingface.co/Qwen/QwQ-32B-Preview) |
| Qwen/Qwen2.5-14B-Instruct | 14B | Qwen2.5 系列中等模型，适合本地部署 | [魔搭](https://www.modelscope.cn/models/qwen/Qwen2.5-14B-Instruct) | [HF](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct) |
| Qwen/Qwen2.5-32B-Instruct | 32B | Qwen2.5 系列大模型，平衡性能与效率 | [魔搭](https://www.modelscope.cn/models/qwen/Qwen2.5-32B-Instruct) | [HF](https://huggingface.co/Qwen/Qwen2.5-32B-Instruct) |
| Qwen/Qwen2.5-72B-Instruct | 72B | Qwen2.5 系列最大模型，支持 128K 上下文，多语言能力强 | [魔搭](https://www.modelscope.cn/models/qwen/Qwen2.5-72B-Instruct) | [HF](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) |
| Qwen/Qwen2.5-7B-Instruct | 7B | Qwen2.5 系列小模型，消费级 GPU 可运行 | [魔搭](https://www.modelscope.cn/models/qwen/Qwen2.5-7B-Instruct) | [HF](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) |
| Qwen/Qwen2.5-Coder-32B-Instruct | 32B | 专为代码生成优化的 Qwen2.5 模型 | [魔搭](https://www.modelscope.cn/models/qwen/Qwen2.5-Coder-32B-Instruct) | [HF](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct) |
| Qwen/Qwen2.5-Math-72B-Instruct | 72B | 专为数学推理优化的 Qwen2.5 模型 | [魔搭](https://www.modelscope.cn/models/qwen/Qwen2.5-Math-72B-Instruct) | [HF](https://huggingface.co/Qwen/Qwen2.5-Math-72B-Instruct) |
<!-- MODEL_TABLE_END -->

*数据每日自动更新，最后更新：2026-02-18 09:30*

## 🔧 技术栈

- Python 3.10+
- BeautifulSoup / Requests - 网页抓取
- GitHub Actions - 定时任务

## 📁 项目结构

```
.
├── scraper.py              # 主爬虫脚本
├── models.json             # 抓取的原始数据
├── .github/
│   └── workflows/
│       └── daily-scraper.yml  # 每日定时任务
├── requirements.txt        # Python 依赖
└── README.md              # 项目说明
```

## 🚀 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行爬虫
python scraper.py
```

## ⏰ 自动更新

项目配置了 GitHub Actions，每天北京时间早上 8:00 自动运行爬虫并更新 README。

## 📌 数据来源

- [通义实验室](https://tongyi.aliyun.com/)
- [魔搭社区](https://modelscope.cn/)
- [HuggingFace](https://huggingface.co/)

## 📝 License

MIT
