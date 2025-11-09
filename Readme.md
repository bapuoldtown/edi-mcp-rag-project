# EDI MCP RAG Agent 🚀

An intelligent EDI (Electronic Data Interchange) processing system using Model Context Protocol (MCP), Retrieval Augmented Generation (RAG), and Agentic AI.

## About

This project combines modern AI technologies to create an intelligent EDI document processing system:

- **MCP (Model Context Protocol)**: Enables AI agents to communicate with tools and data sources
- **RAG (Retrieval Augmented Generation)**: Provides context-aware intelligent decision making
- **Document Parsing**: Extracts knowledge from PDFs, websites, Word docs, and Excel files
- **EDI Processing**: Parses and validates X12/EDIFACT EDI documents
- **Agentic AI**: Autonomous workflows powered by LLMs (Ollama/OpenAI)

## Features

- Parse EDI documents (X12, EDIFACT)
- Extract information from multiple document formats (PDF, web, Word, Excel)
- Build intelligent knowledge base with RAG
- Autonomous agent-based processing
- Extensible MCP server architecture

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)

### Installation

#### Step 1: Install Poetry

**Linux / macOS / WSL:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Windows PowerShell:**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Verify installation:**
```bash
poetry --version
```

#### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/edi-mcp-rag-project.git
cd edi-mcp-rag-project

# Install dependencies
poetry install

# Activate virtual environment
poetry shell



## 📚 Documentation

For detailed guides, see the `docs/` directory:
- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Poetry Guide](docs/POETRY_GUIDE.md)
- [Document Parsing](docs/DOCUMENT_PARSING.md)



---

**Built with for intelligent EDI processing**