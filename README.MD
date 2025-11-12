# Summary Agent

This document provides instructions on how to set up and run the Summary Agent application.

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine using Git.

```bash
git clone https://github.com/vanessavasquez-r/adk-agent-structure.git
cd adk-agent-structure
```

### 2. Create and Activate Virtual Environment

Create a virtual environment using Python 3.12.

```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
```

### 3. Run the Application

Use `uv` to run the ADK web application. This command will also handle installing any necessary dependencies like `uvicorn`.

```bash
uv run adk web . --port 8501 --reload_agents
```