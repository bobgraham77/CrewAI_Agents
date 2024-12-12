import streamlit as st
import sys
import os
from pathlib import Path

# Get the absolute path of the current file
current_path = Path(__file__).parent.absolute()
agents_path = current_path.parent / 'agents'

# Add the project paths
sys.path.append(str(current_path))
sys.path.append(str(agents_path))

# Import the research agent
try:
    from agents.researcher import ResearcherAgent
except ImportError as e:
    st.error(f"Error importing ResearcherAgent: {str(e)}")
    st.error("Please check that the agents/researcher.py file exists.")
    st.stop()

def demonstrate_research_capabilities():
    # Initialize the session state if necessary
    if 'research_results' not in st.session_state:
        st.session_state.research_results = None
    if 'topic' not in st.session_state:
        st.session_state.topic = None
    if 'expand_sources' not in st.session_state:
        st.session_state.expand_sources = False
    if 'research_stage' not in st.session_state:
        st.session_state.research_stage = 'initial'

    st.title("🕵️ AI Research Agent - Advanced Demo")
    
    # Check for the presence of the OpenAI API key
    if 'OPENAI_API_KEY' not in os.environ or not os.environ['OPENAI_API_KEY']:
        st.warning("⚠️ OpenAI API key not configured. Some features will be limited.")
        st.info("🔑 You can obtain an API key at https://platform.openai.com/account/api-keys")
        
        # Ask the user for the API key
        openai_api_key = st.text_input(
            "Please enter your OpenAI API key", 
            type="password",
            help="The API key is required to use advanced research features"
        )
        
        if openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
        else:
            st.warning("Demo mode limited without OpenAI API key")
    
    # Section explaining the capabilities
    st.markdown("""
    ## 🔍 Capabilities of the Research Agent
    
    This agent uses advanced research and source selection techniques:
    
    1. 🌐 **Intelligent Source Selection**
       - Automatically filters out low-quality sources
       - Avoids unreliable sources (Wikipedia, personal blogs)
       - Prioritizes academic and professional sources
    
    2. 🔢 **Limited Source Management**
       - Maximum 15 sources per round of research
       - Controls source expansion
       - Prevents information overload
    
    3. 🧠 **Advanced Selection Criteria**
       - Description length
       - Content relevance
       - Source diversity
    """)
    
    # Select the research topic
    topic = st.text_input("🔬 Enter a research topic", 
                          value=st.session_state.topic or "",
                          placeholder="Ex: Artificial Intelligence, Climate Change, ...")
    
    # Update the topic in the session
    st.session_state.topic = topic
    
    if topic:
        # Create the research agent
        researcher = ResearcherAgent()
        
        # Demo button
        if st.session_state.research_stage == 'initial':
            if st.button("🚀 Launch Demo Research"):
                st.session_state.research_stage = 'preliminary_search'
                st.rerun()
        
        # Preliminary research step
        if st.session_state.research_stage == 'preliminary_search':
            st.subheader("🔍 Detailed Research Process")
            
            # Step 1: Preliminary Source Discovery
            st.markdown("#### 📋 Step 1: Preliminary Source Discovery")
            preliminary_results = researcher.preliminary_research(topic)
            
            # Store the results in the session
            st.session_state.research_results = preliminary_results
            
            # Display the source discovery details
            st.write(f"**Total Sources:** {preliminary_results['total_sources']}")
            
            # Demonstrate the selection criteria
            st.markdown("#### 🕵️ Source Selection Criteria")
            
            # Web sources
            st.markdown("**Selected Web Sources:**")
            for source in preliminary_results['sources']['web']:
                st.markdown(f"- 🌐 {source}")
                
            # YouTube sources
            st.markdown("**Selected YouTube Sources:**")
            for source in preliminary_results['sources']['youtube']:
                st.markdown(f"- 📺 {source}")
            
            # Academic sources
            st.markdown("**Selected Academic Sources:**")
            for source in preliminary_results['sources']['academic']:
                st.markdown(f"- 📚 {source}")
            
            # Demonstrate source expansion
            st.markdown("#### 🔄 Source Expansion Demonstration")
            
            # Checkbox for source expansion
            expand_sources = st.checkbox("Do you want more sources?")
            
            if expand_sources:
                st.session_state.expand_sources = True
                st.session_state.research_stage = 'expand_sources'
                st.rerun()
            
            # Button for final research
            if st.button("🔬 Launch In-Depth Research"):
                st.session_state.research_stage = 'deep_research'
                st.rerun()
        
        # Source expansion step
        if st.session_state.research_stage == 'expand_sources':
            st.warning("⚠️ Expanding sources (2nd round)")
            
            # Initialize research_results if not exists
            if not hasattr(st.session_state, 'research_results'):
                st.session_state.research_results = {
                    'sources': {'web': [], 'youtube': [], 'academic': []},
                    'total_sources': 0
                }
            
            # Simulate source expansion
            additional_results = researcher.preliminary_research(
                topic, 
                max_total_sources=15,  # 15 additional sources
                research_rounds=2
            )
            
            # Ensure additional_results has the expected structure
            if additional_results is None:
                additional_results = {
                    'sources': {'web': [], 'youtube': [], 'academic': []},
                    'total_sources': 0
                }
            
            # Merge results
            if (isinstance(additional_results, dict) and 'sources' in additional_results and 
                isinstance(st.session_state.research_results, dict) and 'sources' in st.session_state.research_results):
                for source_type in ['web', 'youtube', 'academic']:
                    if (source_type in additional_results['sources'] and 
                        source_type in st.session_state.research_results['sources']):
                        st.session_state.research_results['sources'][source_type].extend(
                            [src for src in additional_results['sources'][source_type] 
                             if src not in st.session_state.research_results['sources'][source_type]]
                        )
            
            # Update total sources count
            if (isinstance(additional_results, dict) and 'total_sources' in additional_results and 
                isinstance(st.session_state.research_results, dict) and 'total_sources' in st.session_state.research_results):
                st.session_state.research_results['total_sources'] += additional_results['total_sources']
            
            # Display updated total sources
            if isinstance(st.session_state.research_results, dict) and 'total_sources' in st.session_state.research_results:
                st.write(f"**Total Sources:** {st.session_state.research_results['total_sources']}")
            
            # Display sources
            if isinstance(st.session_state.research_results, dict) and 'sources' in st.session_state.research_results:
                st.markdown("#### 🔄 Updated Sources")
                for source_type in ['web', 'youtube', 'academic']:
                    if source_type in st.session_state.research_results['sources']:
                        st.markdown(f"**{source_type.capitalize()} Sources:**")
                        for source in st.session_state.research_results['sources'][source_type]:
                            st.write(f"- {source}")

            # Button to return to preliminary research
            if st.button("🔙 Return to Preliminary Research"):
                st.session_state.research_stage = 'preliminary_search'
                st.rerun()
            
            # Button for final research
            if st.button("🔬 Launch In-Depth Research"):
                st.session_state.research_stage = 'deep_research'
                st.rerun()
        
        # In-depth research step
        if st.session_state.research_stage == 'deep_research':
            # Perform the in-depth research
            with st.spinner("In-depth analysis in progress..."):
                research_result = researcher.research_topic(topic)
            
            # Display the results
            st.subheader("📄 Research Results")
            st.write(research_result)
            
            # Button to reset
            if st.button("🔁 New Research"):
                st.session_state.research_stage = 'initial'
                st.session_state.research_results = None
                st.session_state.topic = None
                st.rerun()

if __name__ == "__main__":
    demonstrate_research_capabilities()
