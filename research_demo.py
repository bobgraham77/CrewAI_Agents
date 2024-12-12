import streamlit as st
import sys
import os

# Ajouter le chemin du projet au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'CrewAI-Studio'))

# Importer l'agent de recherche
from app.my_agent import ResearcherAgent

def demonstrate_research_capabilities():
    # Initialiser l'état de la session si nécessaire
    if 'research_results' not in st.session_state:
        st.session_state.research_results = None
    if 'topic' not in st.session_state:
        st.session_state.topic = None
    if 'expand_sources' not in st.session_state:
        st.session_state.expand_sources = False
    if 'research_stage' not in st.session_state:
        st.session_state.research_stage = 'initial'

    st.title("🕵️ Agent de Recherche AI - Démonstration Avancée")
    
    # Vérifier la présence de la clé API OpenAI
    if 'OPENAI_API_KEY' not in os.environ or not os.environ['OPENAI_API_KEY']:
        st.warning("⚠️ Clé API OpenAI non configurée. Certaines fonctionnalités seront limitées.")
        st.info("🔑 Vous pouvez obtenir une clé API sur https://platform.openai.com/account/api-keys")
        
        # Demander la clé API à l'utilisateur
        openai_api_key = st.text_input(
            "Veuillez entrer votre clé API OpenAI", 
            type="password",
            help="La clé API est nécessaire pour utiliser les fonctionnalités avancées de recherche"
        )
        
        if openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
        else:
            st.warning("Mode démo limité sans clé API OpenAI")
    
    # Section d'explication des capacités
    st.markdown("""
    ## 🔍 Capacités de l'Agent de Recherche
    
    Cet agent utilise des techniques avancées de recherche et de sélection de sources :
    
    1. 🌐 **Sélection Intelligente des Sources**
       - Filtre automatiquement les sources de qualité
       - Évite les sources peu fiables (Wikipedia, blogs personnels)
       - Priorise les sources académiques et professionnelles
    
    2. 🔢 **Gestion Limitée des Sources**
       - Maximum 15 sources par round de recherche
       - Contrôle de l'expansion des sources
       - Prévention de la surcharge d'informations
    
    3. 🧠 **Critères de Sélection Avancés**
       - Longueur de la description
       - Pertinence du contenu
       - Diversité des sources
    """)
    
    # Sélection du sujet de recherche
    topic = st.text_input("🔬 Entrez un sujet de recherche", 
                          value=st.session_state.topic or "",
                          placeholder="Ex: Intelligence Artificielle, Changement Climatique, ...")
    
    # Mettre à jour le topic dans la session
    st.session_state.topic = topic
    
    if topic:
        # Créer l'agent de recherche
        researcher = ResearcherAgent()
        
        # Bouton de démonstration
        if st.session_state.research_stage == 'initial':
            if st.button("🚀 Lancer la Recherche Démonstrative"):
                st.session_state.research_stage = 'preliminary_search'
                st.rerun()
        
        # Étape de recherche préliminaire
        if st.session_state.research_stage == 'preliminary_search':
            st.subheader("🔍 Processus de Recherche Détaillé")
            
            # Étape 1 : Recherche Préliminaire
            st.markdown("#### 📋 Étape 1 : Découverte Préliminaire des Sources")
            preliminary_results = researcher.preliminary_research(topic)
            
            # Stocker les résultats dans la session
            st.session_state.research_results = preliminary_results
            
            # Afficher les détails de la découverte des sources
            st.write(f"**Nombre Total de Sources :** {preliminary_results['total_sources']}")
            
            # Démonstration des critères de sélection
            st.markdown("#### 🕵️ Critères de Sélection des Sources")
            
            # Sources Web
            st.markdown("**Sources Web Sélectionnées :**")
            for source in preliminary_results['sources']['web']:
                st.markdown(f"- 🌐 {source}")
                
            # Sources YouTube
            st.markdown("**Sources YouTube Sélectionnées :**")
            for source in preliminary_results['sources']['youtube']:
                st.markdown(f"- 📺 {source}")
            
            # Sources Académiques
            st.markdown("**Sources Académiques Sélectionnées :**")
            for source in preliminary_results['sources']['academic']:
                st.markdown(f"- 📚 {source}")
            
            # Démonstration de l'expansion des sources
            st.markdown("#### 🔄 Démonstration de l'Expansion des Sources")
            
            # Checkbox pour l'expansion
            expand_sources = st.checkbox("Voulez-vous plus de sources ?")
            
            if expand_sources:
                st.session_state.expand_sources = True
                st.session_state.research_stage = 'expand_sources'
                st.rerun()
            
            # Bouton de recherche finale
            if st.button("🔬 Lancer la Recherche Approfondie"):
                st.session_state.research_stage = 'deep_research'
                st.rerun()
        
        # Étape d'expansion des sources
        if st.session_state.research_stage == 'expand_sources':
            st.warning("⚠️ Expansion des sources (2ème round)")
            
            # Initialize research_results if not exists
            if not hasattr(st.session_state, 'research_results'):
                st.session_state.research_results = {
                    'sources': {'web': [], 'youtube': [], 'academic': []},
                    'total_sources': 0
                }
            
            # Simuler l'expansion des sources
            additional_results = researcher.preliminary_research(
                topic, 
                max_total_sources=15,  # 15 sources supplémentaires
                research_rounds=2
            )
            
            # Ensure additional_results has the expected structure
            if additional_results is None:
                additional_results = {
                    'sources': {'web': [], 'youtube': [], 'academic': []},
                    'total_sources': 0
                }
            
            # Fusionner les résultats
            if (isinstance(additional_results, dict) and 'sources' in additional_results and 
                isinstance(st.session_state.research_results, dict) and 'sources' in st.session_state.research_results):
                for source_type in ['web', 'youtube', 'academic']:
                    if (source_type in additional_results['sources'] and 
                        source_type in st.session_state.research_results['sources']):
                        st.session_state.research_results['sources'][source_type].extend(
                            [src for src in additional_results['sources'][source_type] 
                             if src not in st.session_state.research_results['sources'][source_type]]
                        )
            
            # Mettre à jour le nombre total de sources
            if (isinstance(additional_results, dict) and 'total_sources' in additional_results and 
                isinstance(st.session_state.research_results, dict) and 'total_sources' in st.session_state.research_results):
                st.session_state.research_results['total_sources'] += additional_results['total_sources']
            
            # Réafficher les sources mises à jour
            if isinstance(st.session_state.research_results, dict) and 'total_sources' in st.session_state.research_results:
                st.write(f"**Nombre Total de Sources :** {st.session_state.research_results['total_sources']}")
            
            # Réafficher les sources
            if isinstance(st.session_state.research_results, dict) and 'sources' in st.session_state.research_results:
                st.markdown("#### 🔄 Sources Mises à Jour")
                for source_type in ['web', 'youtube', 'academic']:
                    if source_type in st.session_state.research_results['sources']:
                        st.markdown(f"**{source_type.capitalize()} Sources :**")
                        for source in st.session_state.research_results['sources'][source_type]:
                            st.write(f"- {source}")

            # Bouton de retour à la recherche préliminaire
            if st.button("🔙 Retour à la Recherche Préliminaire"):
                st.session_state.research_stage = 'preliminary_search'
                st.rerun()
            
            # Bouton de recherche finale
            if st.button("🔬 Lancer la Recherche Approfondie"):
                st.session_state.research_stage = 'deep_research'
                st.rerun()
        
        # Étape de recherche approfondie
        if st.session_state.research_stage == 'deep_research':
            # Effectuer la recherche complète
            with st.spinner("Analyse approfondie en cours..."):
                research_result = researcher.research_topic(topic)
            
            # Afficher les résultats
            st.subheader("📄 Résultats de la Recherche")
            st.write(research_result)
            
            # Bouton de réinitialisation
            if st.button("🔁 Nouvelle Recherche"):
                st.session_state.research_stage = 'initial'
                st.session_state.research_results = None
                st.session_state.topic = None
                st.rerun()

if __name__ == "__main__":
    demonstrate_research_capabilities()
