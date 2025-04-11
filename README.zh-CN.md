# Restaurant Deep Research 餐厅深度研究

[English](README.md) | 简体中文

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/get-started)

Restaurant Deep Research（餐厅深度研究）是一个复杂的多智能体系统，用于查找和分析餐厅推荐。它利用CAMEL-AI框架和Google Maps MCP服务器集成，基于自然语言查询提供详细的、上下文感知的餐厅建议。

## 快速开始

1. **前提条件**：
   - 安装Docker
   - Google Maps API密钥（[在此获取](https://console.cloud.google.com/google/maps-apis/credentials)）
   - Gemini API密钥（[在此获取](https://makersuite.google.com/app/apikey)）

2. **克隆与构建**：
   ```bash
   git clone https://github.com/YangLi-leo/restaurant-deepresearch
   cd restaurant_deep_research
   docker build -t restaurant-research .
   ```

3. **运行**：
   ```bash
   docker run -e GEMINI_API_KEY=your_key -e GOOGLE_MAPS_API_KEY=your_key restaurant-research
   ```

## 功能特点

- **多智能体架构**：利用协作的AI智能体社区来理解和处理餐厅查询
- **自然语言理解**：以自然语言处理关于餐厅偏好的查询
- **上下文感知推荐**：考虑位置、菜系类型、预算、氛围和其他偏好
- **Google Maps MCP服务器集成**：通过Google Maps MCP服务器访问真实餐厅数据
- **详细分析**：提供关于推荐餐厅的结构化信息
- **异步处理**：使用现代异步Python构建，实现高效处理

## 使用方法（需要Docker）

本项目设计为使用Docker运行，它处理所有依赖项和设置。

### 前提条件

- 在您的系统上安装[Docker](https://www.docker.com/get-started)
- Docker镜像包含Node.js、npm和npx，这些是Google Maps MCP服务器所需的

### API密钥设置

#### Google Maps API密钥
1. 前往[Google Cloud控制台](https://console.cloud.google.com/google/maps-apis/credentials)
2. 创建新项目或选择现有项目
3. 启用以下API：
   - Geocoding API
   - Places API
   - Maps JavaScript API
4. 创建API密钥并复制它
5. 如有需要，设置使用限制（生产环境推荐）

#### Gemini API密钥
1. 前往[Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新API密钥或使用现有密钥
3. 注意Gemini API有使用配额：
   - 免费层级：每天有限请求
   - 如果遇到速率限制错误（HTTP 429），可以考虑：
     - 等待配额重置
     - 升级到付费层级
     - 切换到Gemini 2.5 Pro Preview模型（见故障排除部分）

### 步骤

1. **克隆仓库：**
   ```bash
   git clone https://github.com/YangLi-leo/restaurant-deepresearch
   cd restaurant_deep_research
   ```
2. **构建Docker镜像：**
   ```bash
   docker build -t restaurant-research .
   ```
3. **运行默认示例：**
   用您的实际API密钥替换`your_gemini_key`和`your_maps_key`。
   ```bash
   docker run \
     -e GEMINI_API_KEY=your_gemini_key \
     -e GOOGLE_MAPS_API_KEY=your_maps_key \
     restaurant-research
   ```
   
   注意：应用程序将自动使用GOOGLE_MAPS_API_KEY环境变量为Python应用程序和MCP服务器提供密钥。您不再需要手动编辑config/mcp_servers_config.json文件。

### 自定义查询

您可以使用自己的自定义餐厅查询运行应用程序：

```bash
docker run \
  -e GEMINI_API_KEY=your_gemini_key \
  -e GOOGLE_MAPS_API_KEY=your_maps_key \
  restaurant-research \
  python -c "import asyncio; from restaurant_deep_research import process_restaurant_query; asyncio.run(process_restaurant_query('您的自定义查询'))"
```

#### 示例自定义查询：

1. **简单查询**：
   ```
   我想在纽约找一家有户外座位的素食餐厅
   ```

2. **详细查询**：
   ```
   寻找芝加哥市中心附近适合家庭的意大利餐厅，人均预算30-50美元，最好有儿童菜单
   ```

3. **复杂查询**：
   ```
   我们是一个来自中国的三口之家，首次访问东京，计划在10月初享受温和的秋季天气和季节性日本特色美食。我们家庭包括两位成人和一位充满活力的6岁孩子。我们正在寻找一次非凡的晚餐体验，体现日本料理和文化的真正精髓，特别是寿司omakase或怀石料理，在浅草地区人均预算为8,000至15,000日元。
   ```

### 示例输出

当您运行应用程序时，您将收到结构化的餐厅推荐。以下是示例输出：

```
=== 餐厅推荐 ===

基于您对今晚在涩谷站附近寻找日本餐厅（寿司、拉面或居酒屋）的请求，人均预算为2,000-4,000日元，偏好休闲、正宗、愉快且不太奢华的氛围，并有良好评价，以下是两个最佳推荐：

1.  **Gochi Shibuya**
    *   **菜系：** 烤串 / 居酒屋
    *   **地址：** 日本，〒150-0042 东京都涩谷区宇田川町13−９ Kn Shibuya Bldg. I, B1F
    *   **推荐理由：** 这家高评分（4.5星）的餐厅非常符合您对休闲和正宗氛围的期望。评论者将其描述为一家专营美味烤串的小型本地居酒屋。它提供"充满灵魂的诚实本地场所"氛围，完美符合"不太奢华"的要求。在这里用餐应该舒适地符合2,000-4,000日元的预算。如果您正在寻找正宗的居酒屋体验，这里是理想选择。

2.  **Oreryu Shio-ramen Shibuya-main store**
    *   **菜系：** 拉面（专营盐味汤底）
    *   **地址：** 日本，〒150-0043 东京都涩谷区道玄坂1丁目22-8
    *   **推荐理由：** 如果您偏好拉面，这是一个符合您标准的极佳选择。它提供经典、休闲和正宗的本地拉面店体验，配有自动售货机点餐系统。它非常经济实惠（可能每人不到2,000日元），远低于您的最高预算。评价很好（4.3星），赞扬其风味丰富的拉面，特别是盐味和海鲜选项。它完美符合休闲和正宗氛围的偏好。

这两家餐厅都位于涩谷站附近，适合晚餐，有良好评价，并符合所需的休闲和正宗氛围。Gochi Shibuya提供居酒屋体验，价格可能在您预算的中等范围，而Oreryu Shio-ramen提供正宗的拉面体验，价格在您预算的较低范围。
```

## 项目结构

- `src/restaurant_deep_research/`：主要包
  - `agents/`：多智能体系统实现
  - `config/`：配置和提示
  - `main.py`：核心功能
- `examples/`：示例脚本
- `config/`：配置文件
- `docs/`：文档

## 高级用法

对于高级用法和自定义，您可以直接使用底层组件：

```python
from restaurant_deep_research import construct_society, arun_society
from restaurant_deep_research.agents import OwlRolePlaying

# 使用底层API的自定义实现
# 详见示例
```

## 未来博客文章和思考

我的主页目前正在建设中，但我很快会更新它，分享关于这个项目的思考、有趣细节、与其他深度研究工具（如Manus、OpenAI、Google和Perplexity）的比较，以及这个项目、多智能体系统和相关主题的未来方向。这些文章还将记录我的学习过程、挑战和对多智能体系统的更深入见解，这些内容未包含在本README中。一旦可用，我将在这里链接到它们：https://yangli-leo.github.io/。

## 致谢

本项目使用[CAMEL-AI](https://github.com/camel-ai)框架（Apache License 2.0）。

## 故障排除

### API密钥问题
- 确保两个API密钥都有效并具有必要的权限
- 对于Google Maps API密钥，确保在您的Google Cloud项目中启用了以下API：
  - Geocoding API
  - Places API
  - Maps JavaScript API
- 应用程序会自动使用环境变量中的Google Maps API密钥配置MCP服务器

### Gemini API速率限制
如果您遇到此错误：`Error code: 429 - You exceeded your current quota`，您有以下选择：
1. **等待配额重置**：配额通常每天重置
2. **切换到Gemini 2.5 Pro Preview**：修改`src/restaurant_deep_research/main.py`中的代码以使用预览模型：
   ```python
   # 将此处：
   model_type=ModelType.GEMINI_2_5_PRO_EXP
   
   # 改为：
   model_type=ModelType.GEMINI_2_5_PRO_PREVIEW
   ```
3. **升级到付费层级**：对于生产用途，考虑使用付费Google AI API计划

### Docker环境
- 应用程序使用入口点脚本确保环境变量正确传递给所有进程
- Docker容器包含Node.js、npm和npx，用于运行Google Maps MCP服务器
- 如果您修改代码，请使用`docker build -t restaurant-research .`重建Docker镜像

### 常见问题
- **空结果**：检查您的Google Maps API密钥是否具有正确的权限和启用的API
- **性能缓慢**：多智能体对话可能需要时间，特别是对于复杂查询
- **连接错误**：确保您有互联网访问权限，并且防火墙未阻止连接

## 许可证

本项目根据Apache License 2.0许可。详见[LICENSE](LICENSE)文件。
