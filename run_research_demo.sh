#!/bin/bash

# Activer l'environnement Conda
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base

# Aller dans le répertoire du projet
cd "/Users/bob-ordi/Desktop/Manual Library/Programmation/CascadeProjects/Ai Agents/ai_agents_project/CrewAI-Studio"

# Lancer Streamlit
streamlit run research_demo.py
