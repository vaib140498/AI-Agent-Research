# AI Research Agent 🚀

This project is an **AI Agent-Based Research System** built using **Tavily Web Search API**, **LangGraph**, and **ChatOllama (Llama2 LLM)** to automate deep research tasks and generate comprehensive research reports on any topic.

## 🔑 Key Features

- Automated Web Research using Tavily API
- Multi-Agent Research Workflow using LangGraph
- Report Drafting with ChatOllama LLM
- Advanced Research Refinement with LLMChain
- Comprehensive Report Generation in Text Files

## 🛠️ Tech Stack

| Technology | Description                     |
| ---------- | ------------------------------- |
| Python     | Programming Language            |
| Tavily API | Web Search API                  |
| LangGraph  | Agent Workflow Manager          |
| ChatOllama | Local LLM for Report Generation |
| LangChain  | LLM Pipeline Chain              |

## 📄 Folder Structure

```
.
├── main.py                   # Main project file
├── requirements.txt          # Python dependencies
├── reports/                  # Generated Reports
├── README.md                 # Project Documentation
└── .gitignore                # Ignore unnecessary files
```

## 🔌 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VaibhavGoyal17/AI-Research-Agent.git
cd AI-Research-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Tavily API

Sign up on [Tavily](https://www.tavily.com) and get your **API Key**.

Replace the API key in the code:

```python
apiKey = 'your_tavily_api_key_here'
```

### 4. Start ChatOllama LLM Server

Run the following command:

```bash
ollama serve
```

### 5. Run the Project

```bash
python main.py
```

## 📌 Future Scope

- Add support for multiple LLM models (Gemini, GPT-4, Claude)
- Automatic PDF Report Generation
- GUI-based Dashboard
- Web App Integration

## 🎯 Author

**Vaibhav**

Let's build the future of AI Research 🔥🚀

