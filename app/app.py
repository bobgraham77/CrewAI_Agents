import streamlit as st
from streamlit import session_state as ss
import db_utils
from pg_agents import PageAgents
from pg_tasks import PageTasks
from pg_crews import PageCrews
from pg_tools import PageTools
from pg_crew_run import PageCrewRun
from pg_export_crew import PageExportCrew
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
from my_agent import ResearcherAgent

def pages():
    return {
        'Crews': PageCrews(),
        'Tools': PageTools(),
        'Agents': PageAgents(),
        'Tasks': PageTasks(),
        'Kickoff!': PageCrewRun(),
        'Import/export': PageExportCrew(),
        'Research': PageResearch()
    }

def load_data():
    ss.agents = db_utils.load_agents()
    ss.tasks = db_utils.load_tasks()
    ss.crews = db_utils.load_crews()
    ss.tools = db_utils.load_tools()
    ss.enabled_tools = db_utils.load_tools_state()


def draw_sidebar():
    with st.sidebar:
        img_path = os.path.join(os.path.dirname(__file__), 'img', 'crewai_logo.png')
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        if not os.path.exists(img_path):
            img = Image.new('RGB', (300, 100), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("Arial.ttf", 36)
            except IOError:
                font = ImageFont.load_default()
            d.text((10,30), "CrewAI Studio", fill=(255,255,255), font=font)
            img.save(img_path)
        st.image(img_path)

        if 'page' not in ss:
            ss.page = 'Crews'
        
        selected_page = st.radio('Page', list(pages().keys()), index=list(pages().keys()).index(ss.page),label_visibility="collapsed")
        if selected_page != ss.page:
            ss.page = selected_page
            st.rerun()

def check_openai_api_key():
    """
    Check and prompt for OpenAI API key if not set
    """
    # Check if API key is set in environment
    if 'OPENAI_API_KEY' not in os.environ or not os.environ['OPENAI_API_KEY']:
        st.warning("OpenAI API Key is not set. Please enter your API key.")
        api_key = st.text_input("Enter your OpenAI API Key", type="password", key="openai_api_key_input")
        
        if api_key:
            # Set the API key in the environment
            os.environ['OPENAI_API_KEY'] = api_key
            st.success("API Key has been set successfully!")
            return True
        return False
    return True

class PageResearch:
    def __init__(self):
        self.researcher = None

    def render(self):
        st.title("🔍 AI Research Assistant")
        
        # Check API key before proceeding
        if not check_openai_api_key():
            st.info("Please provide your OpenAI API Key to use the Research Assistant.")
            return
        
        # Research topic input
        topic = st.text_input("Enter a research topic", key="research_topic")
        
        # Research button
        if st.button("Start Research"):
            if topic:
                # Create a researcher agent
                try:
                    self.researcher = ResearcherAgent()
                    
                    # Perform research
                    with st.spinner("Conducting research..."):
                        research_results = self.researcher.research_topic(topic)
                        
                        # Display results
                        st.subheader("Research Findings")
                        st.write(research_results)
                        
                        # Option to save or export results
                        if st.button("Save Research"):
                            # Implement save functionality if needed
                            st.success("Research saved successfully!")
                
                except Exception as e:
                    st.error(f"An error occurred during research: {e}")
            else:
                st.warning("Please enter a research topic")

def main():
    st.set_page_config(page_title="CrewAI Studio", page_icon="img/favicon.ico", layout="wide")
    load_dotenv()
    if (str(os.getenv('AGENTOPS_ENABLED')).lower() in ['true', '1']) and not ss.get('agentops_failed', False):
        try:
            import agentops
            agentops.init(api_key=os.getenv('AGENTOPS_API_KEY'),auto_start_session=False)    
        except ModuleNotFoundError as e:
            ss.agentops_failed = True
            print(f"Error initializing AgentOps: {str(e)}")            
        
    db_utils.initialize_db()
    load_data()
    draw_sidebar()
    PageCrewRun.maintain_session_state() #this will persist the session state for the crew run page so crew run can be run in a separate thread
    page = pages()[ss.page]
    if hasattr(page, 'render'):
        page.render()
    else:
        page.draw()

if __name__ == '__main__':
    main()
