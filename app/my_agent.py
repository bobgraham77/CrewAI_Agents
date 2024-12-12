import streamlit as st
import os
import uuid

# Remplacer l'import de utils par des fonctions locales
def rnd_id():
    """Générer un identifiant unique"""
    return str(uuid.uuid4())

def fix_columns_width(df):
    """Placeholder pour fix_columns_width si nécessaire"""
    return df

from crewai import Agent
from streamlit import session_state as ss
from datetime import datetime
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool

# Fonctions de sauvegarde et suppression d'agent factices
def save_agent(agent):
    """Placeholder pour sauvegarder un agent"""
    pass

def delete_agent(agent_id):
    """Placeholder pour supprimer un agent"""
    pass

# Fonction de création de LLM factice
def create_llm(provider, model):
    """Placeholder pour créer un modèle de langage"""
    return ChatOpenAI(temperature=0.7)

# Dictionnaire des fournisseurs et modèles de LLM
llm_providers_and_models = {
    "OpenAI": ["gpt-3.5-turbo", "gpt-4"]
}

class ResearcherAgent(Agent):
    def __init__(self, topic=None):
        # Vérifier et gérer l'absence de clé API OpenAI
        if 'OPENAI_API_KEY' not in os.environ or not os.environ['OPENAI_API_KEY']:
            st.warning("⚠️ Clé API OpenAI non configurée. Certaines fonctionnalités seront limitées.")
            
            # Demander la clé API à l'utilisateur si elle n'est pas définie
            openai_api_key = st.text_input(
                "🔑 Veuillez entrer votre clé API OpenAI", 
                type="password",
                help="Vous pouvez obtenir une clé API sur https://platform.openai.com/account/api-keys"
            )
            
            if openai_api_key:
                os.environ['OPENAI_API_KEY'] = openai_api_key
            else:
                # Utiliser un agent simulé sans LLM si pas de clé API
                st.warning("Fonctionnement en mode démo limité sans clé API OpenAI")
        
        # Initialiser le LLM avec gestion d'erreur
        try:
            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo", 
                temperature=0.7,
                api_key=os.environ.get('OPENAI_API_KEY')
            )
        except Exception as e:
            st.error(f"Erreur d'initialisation du modèle LLM : {e}")
            llm = None
        
        # Initialisation de l'agent avec gestion des outils
        super().__init__(
            role='Intelligent Research Agent',
            goal='Perform comprehensive and intelligent research on a given topic',
            backstory='An advanced AI agent specialized in gathering, filtering, and synthesizing information from diverse sources',
            verbose=True,
            allow_delegation=True,
            llm=llm  # Passer le LLM initialisé
        )
        
        # Utiliser un attribut personnalisé pour le topic
        self._topic = topic
        
        # Initialiser les outils avec gestion d'erreur
        self.tools = []
        try:
            self.tools.append(SerperDevTool())
        except Exception as e:
            st.warning(f"Impossible d'initialiser SerperDevTool : {e}")
        
        try:
            self.tools.append(WebsiteSearchTool())
        except Exception as e:
            st.warning(f"Impossible d'initialiser WebsiteSearchTool : {e}")
        
        try:
            self.tools.append(YoutubeVideoSearchTool())
        except Exception as e:
            st.warning(f"Impossible d'initialiser YoutubeVideoSearchTool : {e}")
    
    @property
    def topic(self):
        return self._topic
    
    @topic.setter
    def topic(self, value):
        self._topic = value

    def preliminary_research(self, topic, max_total_sources=15, research_rounds=1):
        """
        Effectue une recherche préliminaire sur un sujet donné
        
        Args:
            topic (str): Le sujet de recherche
            max_total_sources (int): Nombre maximum de sources
            research_rounds (int): Nombre de rounds de recherche
        
        Returns:
            dict: Résultats de la recherche préliminaire
        """
        # Simulation de la recherche de sources
        return {
            'total_sources': 10,
            'sources': {
                'web': [
                    'Article scientifique sur l\'IA',
                    'Blog technologique sur les tendances émergentes',
                    'Rapport de recherche académique'
                ],
                'youtube': [
                    'Vidéo de conférence sur l\'intelligence artificielle',
                    'Tutoriel technique sur les dernières avancées'
                ],
                'academic': [
                    'Publication de recherche de Stanford',
                    'Étude comparative des modèles de machine learning'
                ]
            }
        }
    
    def research_topic(self, topic):
        """
        Effectue une recherche approfondie sur un sujet
        
        Args:
            topic (str): Le sujet de recherche
        
        Returns:
            str: Résumé de la recherche détaillé et nuancé
        """
        # Liste de perspectives différentes pour un même sujet
        perspectives = {
            "Intelligence Artificielle": [
                "Avancées technologiques et éthiques",
                "Impact économique et social",
                "Développements récents en apprentissage profond",
                "Défis et limites actuels de l'IA"
            ],
            "Changement Climatique": [
                "Solutions technologiques innovantes",
                "Impacts géopolitiques et économiques",
                "Stratégies de réduction des émissions",
                "Adaptation et résilience des écosystèmes"
            ],
            "Santé Numérique": [
                "Technologies émergentes de diagnostic",
                "Intelligence artificielle en médecine personnalisée", 
                "Éthique et confidentialité des données de santé",
                "Télémédecine et accessibilité des soins"
            ]
        }
        
        # Sélectionner une perspective aléatoire si le sujet est prédéfini
        import random
        
        if topic in perspectives:
            perspective = random.choice(perspectives[topic])
            return f"Recherche approfondie sur {topic} : {perspective}"
        else:
            # Pour les sujets non prédéfinis, générer une description générique
            return f"Analyse multidimensionnelle du sujet : {topic}"

class MyAgent:
    def __init__(self, id=None, role=None, backstory=None, goal=None, temperature=None, allow_delegation=False, verbose=False, cache= None, llm_provider_model=None, max_iter=None, created_at=None, tools=None):
        self.id = id or "A_" + rnd_id()
        self.role = role or "Senior Researcher"
        self.backstory = backstory or "Driven by curiosity, you're at the forefront of innovation, eager to explore and share knowledge that could change the world."
        self.goal = goal or "Uncover groundbreaking technologies in AI"
        self.temperature = temperature or 0.1
        self.allow_delegation = allow_delegation if allow_delegation is not None else False
        self.verbose = verbose if verbose is not None else True
        self.llm_provider_model = llm_providers_and_models()[0] if llm_provider_model is None else llm_provider_model
        self.created_at = created_at or datetime.now().isoformat()
        self.tools = tools or []
        self.max_iter = max_iter or 25
        self.cache = cache if cache is not None else True
        self.edit_key = f'edit_{self.id}'
        if self.edit_key not in ss:
            ss[self.edit_key] = False

    @property
    def edit(self):
        return ss[self.edit_key]

    @edit.setter
    def edit(self, value):
        ss[self.edit_key] = value

    def get_crewai_agent(self) -> Agent:
            llm = create_llm(self.llm_provider_model, temperature=self.temperature)
            tools = [tool.create_tool() for tool in self.tools]
            return Agent(
                role=self.role,
                backstory=self.backstory,
                goal=self.goal,
                allow_delegation=self.allow_delegation,
                verbose=self.verbose,
                max_iter=self.max_iter,
                cache=self.cache,
                tools=tools,
                llm=llm
            )

    def delete(self):
        ss.agents = [agent for agent in ss.agents if agent.id != self.id]
        delete_agent(self.id)

    def get_tool_display_name(self, tool):
        first_param_name = tool.get_parameter_names()[0] if tool.get_parameter_names() else None
        first_param_value = tool.parameters.get(first_param_name, '') if first_param_name else ''
        return f"{tool.name} ({first_param_value if first_param_value else tool.tool_id})"

    def is_valid(self, show_warning=False):
        for tool in self.tools:
            if not tool.is_valid(show_warning=show_warning):
                if show_warning:
                    st.warning(f"Tool {tool.name} is not valid")
                return False
        return True

    def validate_llm_provider_model(self):
        available_models = llm_providers_and_models()
        if self.llm_provider_model not in available_models:
            self.llm_provider_model = available_models[0]

    def draw(self, key=None):
        self.validate_llm_provider_model()
        expander_title = f"{self.role[:60]} -{self.llm_provider_model.split(':')[1]}" if self.is_valid() else f"❗ {self.role[:20]} -{self.llm_provider_model.split(':')[1]}"
        if self.edit:
            with st.expander(f"Agent: {self.role}", expanded=True):
                with st.form(key=f'form_{self.id}' if key is None else key):
                    self.role = st.text_input("Role", value=self.role)
                    self.backstory = st.text_area("Backstory", value=self.backstory)
                    self.goal = st.text_area("Goal", value=self.goal)
                    self.allow_delegation = st.checkbox("Allow delegation", value=self.allow_delegation)
                    self.verbose = st.checkbox("Verbose", value=self.verbose)
                    self.cache = st.checkbox("Cache", value=self.cache)
                    self.llm_provider_model = st.selectbox("LLM Provider and Model", options=llm_providers_and_models(), index=llm_providers_and_models().index(self.llm_provider_model))
                    self.temperature = st.slider("Temperature", value=self.temperature, min_value=0.0, max_value=1.0)
                    self.max_iter = st.number_input("Max Iterations", value=self.max_iter, min_value=1, max_value=100)
                    enabled_tools = [tool for tool in ss.tools]
                    selected_tools = st.multiselect(
                        "Select Tools",
                        [self.get_tool_display_name(tool) for tool in enabled_tools],
                        default=[self.get_tool_display_name(tool) for tool in self.tools],
                        key=f"{self.id}_tools{key}"
                    )
                    submitted = st.form_submit_button("Save")
                    if submitted:
                        self.tools = [tool for tool in enabled_tools if self.get_tool_display_name(tool) in selected_tools]
                        self.set_editable(False)
        else:
            fix_columns_width(None)
            with st.expander(expander_title, expanded=False):
                st.markdown(f"**Role:** {self.role}")
                st.markdown(f"**Backstory:** {self.backstory}")
                st.markdown(f"**Goal:** {self.goal}")
                st.markdown(f"**Allow delegation:** {self.allow_delegation}")
                st.markdown(f"**Verbose:** {self.verbose}")
                st.markdown(f"**Cache:** {self.cache}")
                st.markdown(f"**LLM Provider and Model:** {self.llm_provider_model}")
                st.markdown(f"**Temperature:** {self.temperature}")
                st.markdown(f"**Max Iterations:** {self.max_iter}")
                st.markdown(f"**Tools:** {[self.get_tool_display_name(tool) for tool in self.tools]}")

                self.is_valid(show_warning=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.button("Edit", on_click=self.set_editable, args=(True,), key=rnd_id())
                with col2:
                    st.button("Delete", on_click=self.delete, key=rnd_id())

    def set_editable(self, edit):
        self.edit = edit
        save_agent(self)
        if not edit:
            st.rerun()