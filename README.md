# 通义大模型追踪器 (Tongyi Model Tracker)

每日自动抓取阿里巴巴通义实验室新发大模型，梳理模型名称、尺寸、介绍、魔搭及 HuggingFace 地址等信息。

## 📊 最新模型列表

<!-- MODEL_TABLE_START -->
| 模型名称 | 尺寸 | 简介 | 魔搭地址 | HuggingFace |
|---------|------|------|---------|-------------|
<!-- MODEL_TABLE_END -->

*数据每日自动更新，最后更新：待首次运行*

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
