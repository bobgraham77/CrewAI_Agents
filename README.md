# AI Research Agent - Advanced Demo 🕵️‍♂️

## Description
A Streamlit application demonstrating the capabilities of an AI research agent using CrewAI. The agent can conduct in-depth research on various topics using multiple sources and providing detailed analyses.

## Features
- 🔍 Intelligent multi-source search
- 📊 Automatic source analysis and filtering
- 🤖 AI-powered information synthesis
- 📈 Dynamic research source expansion

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bobgraham77/CrewAI_Agents.git
cd CrewAI_Agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configuration:
- Create a `.env` file in the project root
- Add your API keys:
```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
```

## Usage
To run the application locally:
```bash
streamlit run research_demo.py
```

## Deployment
The application can be deployed on Streamlit Share:
1. Fork this repository
2. Visit https://share.streamlit.io/
3. Deploy using your forked repository
4. Add the required environment variables in the Streamlit Share settings

## Project Structure
```
CrewAI-Studio/
├── app/
│   ├── __init__.py
│   ├── my_tools.py
│   └── my_agent.py
├── research_demo.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
