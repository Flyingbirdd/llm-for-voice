# LM-Studio-Voice-Conversation
本项目是一个结合本地大型语言模型（LLMs）和 Whisper 语音转文本技术的 Python 应用程序，旨在提供一个高效、安全、易于互动的语音对话平台。通过集成 Whisper 的语音识别功能，项目能够精准地将语音转换为文本，并结合本地运行的 LLMs，进行自然流畅的对话生成。所有数据处理完全在本地完成，保障了用户的隐私和数据安全，避免了外部服务器的依赖与潜在的隐私泄露风险。

该应用程序不仅支持高质量的语音识别和生成，还能够适应不同环境和噪音条件下的语音输入，确保在各种使用场景中都能提供流畅、清晰的对话体验。用户通过一个简洁直观的界面与 AI 进行互动，适合各类用户群体，包括普通用户和技术开发者。它的开源性质使得开发者可以根据具体需求对系统进行定制和优化，实现个性化的功能扩展或界面调整。

此外，项目的架构具有高度的灵活性，支持本地部署，减少了对外部服务的依赖，提升了响应速度和系统稳定性。作为一个开放源代码的项目，它不仅为开发者提供了丰富的学习和实验机会，也为实际应用中的语音交互系统的优化和创新提供了基础。无论是在学术研究、产品开发，还是个人兴趣项目中，都可以发挥重要作用。

### 准备工作

在开始之前，请确保已安装以下内容:

- **Anaconda**:  [Anaconda's official site](https://www.anaconda.com/).
- **LM Studio**: [LM Studio's website](https://lmstudio.ai/).

### 环境配置

1. Anaconda：从 Anaconda 官方网站 下载并安装

2. **创建一个新的 Conda 环境**:
   ```bash
   conda create -n myenv python=3.9.18

   Replace `myenv` with a name of your choice for the environment.

3. **激活环境**:
   ```bash
   conda activate myenv
   ```

4.**通过克隆仓库获取项目代码**:
```bash
git clone https://ghttps://github.com/Flyingbirdd/llm-for-voice
```

5. **安装所需的包**:
   Navigate to the cloned directory and install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

### 运行项目
- **LLM Python Script (`speak.py`)**: 语言模型的主脚本.
```bash
python speak.py
```

