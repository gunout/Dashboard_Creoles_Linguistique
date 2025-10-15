# dashboard_creoles_francaises.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE COMPLÈTE DES CRÉOLES FRANÇAISES",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec fond noir et contraste amélioré
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #0a0a0a !important;
    }
    
    .stApp {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #00d4ff;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    
    .academic-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.3);
        border-color: #00d4ff;
    }
    
    .haiti-card { 
        border-left: 5px solid #ff4757; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .martinique-card { 
        border-left: 5px solid #3498db; 
        background: linear-gradient(135deg, #0a1a2a 0%, #1a2d3d 100%);
    }
    .guadeloupe-card { 
        border-left: 5px solid #2ecc71; 
        background: linear-gradient(135deg, #0a1a0a 0%, #1a2d1a 100%);
    }
    .reunion-card { 
        border-left: 5px solid #9b59b6; 
        background: linear-gradient(135deg, #1a0a1a 0%, #2d1a2d 100%);
    }
    .maurice-card { 
        border-left: 5px solid #f39c12; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .seychelles-card { 
        border-left: 5px solid #1abc9c; 
        background: linear-gradient(135deg, #0a1a1a 0%, #1a2d2d 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00d4ff !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #00d4ff;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #00d4ff;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2d2d2d;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3d3d3d;
        border-color: #00d4ff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #00d4ff;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: #000000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00e5ff 0%, #00b8d4 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
    }
    
    .stDataFrame {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #00d4ff;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(26, 26, 26, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
</style>
""", unsafe_allow_html=True)

class CreoleAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour fond noir
        self.color_palette = {
            'HAÏTIEN': '#ff4757',      # Rouge vif
            'MARTINIQUAIS': '#3498db',  # Bleu vif
            'GUADELOUPÉEN': '#2ecc71',  # Vert vif
            'RÉUNIONNAIS': '#9b59b6',   # Violet
            'MAURICIEN': '#f39c12',     # Orange
            'SEYCHELLOIS': '#1abc9c',   # Turquoise
            'Caraïbes': '#ff4757',      # Rouge pour la région
            'Océan Indien': '#3498db',  # Bleu pour la région
            'Toutes': '#2ecc71'         # Vert pour éléments communs
        }
        
        # Couleurs pour les types de données adaptées au fond noir
        self.data_colors = {
            'vocabulaire_francais': '#3498db',    # Bleu
            'influences_africaines': '#ff4757',   # Rouge
            'influences_autres': '#f39c12',       # Orange
            'Fondation': '#ff4757',               # Rouge
            'Développement': '#3498db',           # Bleu
            'Récession': '#95a5a6',               # Gris
            'Revitalisation': '#2ecc71',          # Vert
            'Institutionnalisation': '#9b59b6'    # Violet
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur les créoles françaises"""
        
        # Données principales sur chaque créole
        self.creoles_data = {
            'HAÏTIEN': {
                'locuteurs': 12000000,
                'pays': 'Haïti',
                'statut_officiel': 'Langue co-officielle avec le français',
                'annee_creation': '1650-1750',
                'region': 'Caraïbes',
                'influences': ['Français', 'Langues ouest-africaines', 'Taïno', 'Espagnol'],
                'ecriture': 'Orthographe officielle depuis 1979',
                'vitalite': 95,
                'media': 'Presse, radio, télévision, littérature',
                'education': 'Enseignement bilingue en développement',
                'variantes_dialectales': ['Nord', 'Sud', 'Centre', 'Ouest'],
                'texte_exemple': 'Bonjou, koman ou ye?',
                'traduction': 'Bonjour, comment allez-vous?',
                'caracteristiques_linguistiques': ['SVO', 'Pas de conjugaison verbale', 'Articles définis postposés'],
                'population': 11400000,
                'superficie_km2': 27750,
                'capital': 'Port-au-Prince',
                'independance': '1804',
                'economie': 'Agriculture, transferts, aide internationale',
                'systeme_politique': 'République semi-présidentielle',
                'contexte_historique': 'Première république noire indépendante, révolution haïtienne'
            },
            'MARTINIQUAIS': {
                'locuteurs': 400000,
                'pays': 'Martinique (France)',
                'statut_officiel': 'Langue régionale',
                'annee_creation': '1650-1750',
                'region': 'Caraïbes',
                'influences': ['Français', 'Langues ouest-africaines', 'Caribéen'],
                'ecriture': 'Plusieurs systèmes',
                'vitalite': 85,
                'media': 'Radio, musique, théâtre',
                'education': 'Enseignement optionnel',
                'variantes_dialectales': ['Nord-Atlantique', 'Sud-Caraïbe', 'Centre'],
                'texte_exemple': 'Sa ou fè?',
                'traduction': 'Qu\'est-ce que tu fais?',
                'caracteristiques_linguistiques': ['SVO', 'Reduplication', 'Particules aspectuelles'],
                'population': 376000,
                'superficie_km2': 1128,
                'capital': 'Fort-de-France',
                'statut_politique': 'Département et région d\'outre-mer',
                'economie': 'Tourisme, banane, rhum',
                'contexte_historique': 'Colonie française depuis 1635, département d\'outre-mer depuis 1946'
            },
            'GUADELOUPÉEN': {
                'locuteurs': 400000,
                'pays': 'Guadeloupe (France)',
                'statut_officiel': 'Langue régionale',
                'annee_creation': '1650-1750',
                'region': 'Caraïbes',
                'influences': ['Français', 'Langues ouest-africaines', 'Kali\'na'],
                'ecriture': 'Plusieurs systèmes',
                'vitalite': 85,
                'media': 'Radio, musique',
                'education': 'Enseignement optionnel',
                'variantes_dialectales': ['Basse-Terre', 'Grande-Terre', 'Marie-Galante'],
                'texte_exemple': 'Ka ou ni?',
                'traduction': 'Comment vas-tu?',
                'caracteristiques_linguistiques': ['SVO', 'Marqueurs préverbaux', 'Absence de genre grammatical'],
                'population': 395000,
                'superficie_km2': 1628,
                'capital': 'Basse-Terre',
                'statut_politique': 'Département et région d\'outre-mer',
                'economie': 'Tourisme, banane, canne à sucre',
                'contexte_historique': 'Colonie française, département d\'outre-mer depuis 1946'
            },
            'RÉUNIONNAIS': {
                'locuteurs': 600000,
                'pays': 'La Réunion (France)',
                'statut_officiel': 'Langue régionale',
                'annee_creation': '1650-1750',
                'region': 'Océan Indien',
                'influences': ['Français', 'Malagasy', 'Hindi', 'Tamoul', 'Chinois'],
                'ecriture': 'Graphie harmonisée',
                'vitalite': 90,
                'media': 'Radio, télévision locale',
                'education': 'Enseignement optionnel',
                'variantes_dialectales': ['Nord', 'Sud', 'Est', 'Ouest'],
                'texte_exemple': 'Koman i lé?',
                'traduction': 'Comment ça va?',
                'caracteristiques_linguistiques': ['SVO', 'Influence malgache forte', 'Pronoms spécifiques'],
                'population': 860000,
                'superficie_km2': 2512,
                'capital': 'Saint-Denis',
                'statut_politique': 'Département et région d\'outre-mer',
                'economie': 'Tourisme, sucre, services',
                'contexte_historique': 'Île déserte peuplée à partir de 1665, département d\'outre-mer depuis 1946'
            },
            'MAURICIEN': {
                'locuteurs': 1200000,
                'pays': 'Maurice',
                'statut_officiel': 'Langue nationale de facto',
                'annee_creation': '1720-1820',
                'region': 'Océan Indien',
                'influences': ['Français', 'Anglais', 'Hindi', 'Ourdou', 'Chinois'],
                'ecriture': 'Graphie LPT (Ledikasyon pu Travayer)',
                'vitalite': 92,
                'media': 'Presse, radio, télévision',
                'education': 'Utilisé informellement',
                'variantes_dialectales': ['Port-Louis', 'Plaines Wilhems', 'Nord'],
                'texte_exemple': 'Ki manyèr?',
                'traduction': 'Comment ça va?',
                'caracteristiques_linguistiques': ['SVO', 'Influence anglaise', 'Emprunts multiples'],
                'population': 1266000,
                'superficie_km2': 2040,
                'capital': 'Port-Louis',
                'independance': '1968',
                'economie': 'Textile, tourisme, services financiers',
                'systeme_politique': 'République parlementaire',
                'contexte_historique': 'Colonie française puis britannique, indépendante depuis 1968'
            },
            'SEYCHELLOIS': {
                'locuteurs': 95000,
                'pays': 'Seychelles',
                'statut_officiel': 'Langue officielle avec français et anglais',
                'annee_creation': '1770-1850',
                'region': 'Océan Indien',
                'influences': ['Français', 'Anglais', 'Malagasy', 'Swahili'],
                'ecriture': 'Orthographe standardisée',
                'vitalite': 88,
                'media': 'Presse, radio, télévision',
                'education': 'Langue d\'enseignement au primaire',
                'variantes_dialectales': ['Mahé', 'Praslin', 'La Digue'],
                'texte_exemple': 'Kouman ou i ye?',
                'traduction': 'Comment allez-vous?',
                'caracteristiques_linguistiques': ['SVO', 'Syllabique', 'Pronoms spécifiques'],
                'population': 98000,
                'superficie_km2': 459,
                'capital': 'Victoria',
                'independance': '1976',
                'economie': 'Tourisme, pêche',
                'systeme_politique': 'République présidentielle',
                'contexte_historique': 'Colonie française puis britannique, indépendante depuis 1976'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1635, 'evenement': 'Colonisation de la Martinique et Guadeloupe', 'region': 'Caraïbes', 'importance': 8},
            {'annee': 1659, 'evenement': 'Colonisation de Saint-Domingue (Haïti)', 'region': 'Caraïbes', 'importance': 9},
            {'annee': 1665, 'evenement': 'Peuplement de La Réunion', 'region': 'Océan Indien', 'importance': 7},
            {'annee': 1715, 'evenement': 'Colonisation de l\'Île de France (Maurice)', 'region': 'Océan Indien', 'importance': 8},
            {'annee': 1770, 'evenement': 'Colonisation des Seychelles', 'region': 'Océan Indien', 'importance': 7},
            {'annee': 1804, 'evenement': 'Indépendance d\'Haïti', 'region': 'Caraïbes', 'importance': 10},
            {'annee': 1810, 'evenement': 'Conquête britannique de Maurice', 'region': 'Océan Indien', 'importance': 8},
            {'annee': 1814, 'evenement': 'Conquête britannique des Seychelles', 'region': 'Océan Indien', 'importance': 7},
            {'annee': 1848, 'evenement': 'Abolition de l\'esclavage français', 'region': 'Toutes', 'importance': 9},
            {'annee': 1946, 'evenement': 'Départementalisation des Antilles et La Réunion', 'region': 'Caraïbes/Océan Indien', 'importance': 8},
            {'annee': 1968, 'evenement': 'Indépendance de Maurice', 'region': 'Océan Indien', 'importance': 8},
            {'annee': 1976, 'evenement': 'Indépendance des Seychelles', 'region': 'Océan Indien', 'importance': 7},
            {'annee': 1979, 'evenement': 'Standardisation de l\'orthographe haïtienne', 'region': 'Caraïbes', 'importance': 9},
            {'annee': 1982, 'evenement': 'Reconnaissance des langues régionales en France', 'region': 'Toutes', 'importance': 8},
            {'annee': 2000, 'evenement': 'Constitution haïtienne reconnaissant le créole', 'region': 'Caraïbes', 'importance': 9},
            {'annee': 2015, 'evenement': 'Loi pour la refondation de l\'école incluant les langues régionales', 'region': 'Toutes', 'importance': 7}
        ]

        # Données linguistiques comparatives
        self.linguistic_data = {
            'HAÏTIEN': {
                'vocabulaire_francais': 90,
                'influences_africaines': 8,
                'influences_autres': 2,
                'complexite_grammaticale': 6.5,
                'vitalite': 95,
                'standardisation': 85,
                'caracteristiques_uniques': ['Système aspectuel complexe', 'Pronoms spécifiques', 'Absence de conjugaison'],
                'phonetique': '7 voyelles, consonnes simples',
                'morphologie': 'Analytique, peu de flexions'
            },
            'MARTINIQUAIS': {
                'vocabulaire_francais': 88,
                'influences_africaines': 7,
                'influences_autres': 5,
                'complexite_grammaticale': 6.8,
                'vitalite': 85,
                'standardisation': 70,
                'caracteristiques_uniques': ['Reduplication expressive', 'Particules modales', 'Influence caribéenne'],
                'phonetique': '7 voyelles, nasalisation',
                'morphologie': 'Analytique, marqueurs préverbaux'
            },
            'GUADELOUPÉEN': {
                'vocabulaire_francais': 87,
                'influences_africaines': 8,
                'influences_autres': 5,
                'complexite_grammaticale': 6.7,
                'vitalite': 85,
                'standardisation': 70,
                'caracteristiques_uniques': ['Système aspectuel', 'Pronoms emphatiques', 'Influence kali\'na'],
                'phonetique': '7 voyelles, consonnes palatalisées',
                'morphologie': 'Analytique, ordre SVO strict'
            },
            'RÉUNIONNAIS': {
                'vocabulaire_francais': 85,
                'influences_africaines': 5,
                'influences_autres': 10,
                'complexite_grammaticale': 7.2,
                'vitalite': 90,
                'standardisation': 75,
                'caracteristiques_uniques': ['Influence malgache forte', 'Particules malgaches', 'Système numéral mixte'],
                'phonetique': '7 voyelles, influence malgache',
                'morphologie': 'Mixte, influences multiples'
            },
            'MAURICIEN': {
                'vocabulaire_francais': 80,
                'influences_africaines': 5,
                'influences_autres': 15,
                'complexite_grammaticale': 7.0,
                'vitalite': 92,
                'standardisation': 80,
                'caracteristiques_uniques': ['Influence anglaise importante', 'Emprunts indiens', 'Flexibilité syntaxique'],
                'phonetique': '7 voyelles, influence anglaise',
                'morphologie': 'Analytique, emprunts multiples'
            },
            'SEYCHELLOIS': {
                'vocabulaire_francais': 82,
                'influences_africaines': 8,
                'influences_autres': 10,
                'complexite_grammaticale': 6.9,
                'vitalite': 88,
                'standardisation': 85,
                'caracteristiques_uniques': ['Orthographe standardisée', 'Influence swahili', 'Système éducatif intégré'],
                'phonetique': '7 voyelles, syllabique',
                'morphologie': 'Analytique, régulier'
            }
        }

        # Données géopolitiques
        self.geopolitical_data = {
            'HAÏTIEN': {
                'statut_politique': 'Langue co-officielle',
                'reconnaissance_internationale': 'Oui',
                'usage_gouvernement': 'Limité',
                'usage_judiciaire': 'Oui',
                'usage_education': 'En développement',
                'presence_media': 'Forte',
                'mouvements_activistes': 'Très actifs',
                'financements': 'Limités',
                'politiques_linguistiques': 'Pro-créole depuis 1987'
            },
            'MARTINIQUAIS': {
                'statut_politique': 'Langue régionale',
                'reconnaissance_internationale': 'Non',
                'usage_gouvernement': 'Aucun',
                'usage_judiciaire': 'Non',
                'usage_education': 'Optionnel',
                'presence_media': 'Moyenne',
                'mouvements_activistes': 'Actifs',
                'financements': 'Publics limités',
                'politiques_linguistiques': 'Reconnaissance symbolique'
            },
            'GUADELOUPÉEN': {
                'statut_politique': 'Langue régionale',
                'reconnaissance_internationale': 'Non',
                'usage_gouvernement': 'Aucun',
                'usage_judiciaire': 'Non',
                'usage_education': 'Optionnel',
                'presence_media': 'Moyenne',
                'mouvements_activistes': 'Actifs',
                'financements': 'Publics limités',
                'politiques_linguistiques': 'Reconnaissance symbolique'
            },
            'RÉUNIONNAIS': {
                'statut_politique': 'Langue régionale',
                'reconnaissance_internationale': 'Non',
                'usage_gouvernement': 'Aucun',
                'usage_judiciaire': 'Non',
                'usage_education': 'Optionnel',
                'presence_media': 'Moyenne',
                'mouvements_activistes': 'Actifs',
                'financements': 'Publics limités',
                'politiques_linguistiques': 'Reconnaissance symbolique'
            },
            'MAURICIEN': {
                'statut_politique': 'Langue nationale de facto',
                'reconnaissance_internationale': 'Non',
                'usage_gouvernement': 'Informel',
                'usage_judiciaire': 'Non',
                'usage_education': 'Informel',
                'presence_media': 'Forte',
                'mouvements_activistes': 'Très actifs',
                'financements': 'Privés',
                'politiques_linguistiques': 'Tolérance active'
            },
            'SEYCHELLOIS': {
                'statut_politique': 'Langue officielle',
                'reconnaissance_internationale': 'Oui',
                'usage_gouvernement': 'Oui',
                'usage_judiciaire': 'Oui',
                'usage_education': 'Primaire',
                'presence_media': 'Forte',
                'mouvements_activistes': 'Actifs',
                'financements': 'Publics',
                'politiques_linguistiques': 'Proactive et intégrée'
            }
        }

        # Données démographiques et sociales
        self.demographic_data = {
            'HAÏTIEN': {
                'locuteurs_natifs': 12000000,
                'locuteurs_seconde_langue': 2000000,
                'tranches_age': {'0-14': 35, '15-64': 60, '65+': 5},
                'urbanisation': 55,
                'niveau_education': 65,
                'bilinguisme': 45,
                'transmission_familiale': 95,
                'attitude_locuteurs': 'Très positive'
            },
            'MARTINIQUAIS': {
                'locuteurs_natifs': 380000,
                'locuteurs_seconde_langue': 20000,
                'tranches_age': {'0-14': 20, '15-64': 65, '65+': 15},
                'urbanisation': 90,
                'niveau_education': 85,
                'bilinguisme': 95,
                'transmission_familiale': 80,
                'attitude_locuteurs': 'Positive'
            },
            'GUADELOUPÉEN': {
                'locuteurs_natifs': 380000,
                'locuteurs_seconde_langue': 20000,
                'tranches_age': {'0-14': 22, '15-64': 63, '65+': 15},
                'urbanisation': 88,
                'niveau_education': 83,
                'bilinguisme': 95,
                'transmission_familiale': 80,
                'attitude_locuteurs': 'Positive'
            },
            'RÉUNIONNAIS': {
                'locuteurs_natifs': 550000,
                'locuteurs_seconde_langue': 50000,
                'tranches_age': {'0-14': 25, '15-64': 62, '65+': 13},
                'urbanisation': 92,
                'niveau_education': 80,
                'bilinguisme': 90,
                'transmission_familiale': 85,
                'attitude_locuteurs': 'Très positive'
            },
            'MAURICIEN': {
                'locuteurs_natifs': 1150000,
                'locuteurs_seconde_langue': 50000,
                'tranches_age': {'0-14': 20, '15-64': 70, '65+': 10},
                'urbanisation': 40,
                'niveau_education': 88,
                'bilinguisme': 85,
                'transmission_familiale': 90,
                'attitude_locuteurs': 'Très positive'
            },
            'SEYCHELLOIS': {
                'locuteurs_natifs': 90000,
                'locuteurs_seconde_langue': 5000,
                'tranches_age': {'0-14': 22, '15-64': 68, '65+': 10},
                'urbanisation': 55,
                'niveau_education': 90,
                'bilinguisme': 95,
                'transmission_familiale': 95,
                'attitude_locuteurs': 'Très positive'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🌍 ANALYSE COMPLÈTE DES CRÉOLES FRANÇAISES</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem;">Linguistique historique, géopolitique, sociolinguistique et perspectives d\'avenir</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_locuteurs = sum(self.creoles_data[creole]['locuteurs'] for creole in self.creoles_data)
            st.markdown(f"""
            <div class="academic-card haiti-card">
                <div style="color: {self.color_palette['HAÏTIEN']}; font-size: 1rem; font-weight: 600; text-align: center;">👥 LOCUTEURS TOTAUX</div>
                <div class="metric-value" style="color: {self.color_palette['HAÏTIEN']}; text-align: center;">{total_locuteurs:,}</div>
                <div style="color: #cccccc; text-align: center;">Locuteurs des créoles françaises</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="academic-card martinique-card">
                <div style="color: {self.color_palette['MARTINIQUAIS']}; font-size: 1rem; font-weight: 600; text-align: center;">🌐 RÉGIONS</div>
                <div class="metric-value" style="color: {self.color_palette['MARTINIQUAIS']}; text-align: center;">2</div>
                <div style="color: #cccccc; text-align: center;">Caraïbes et Océan Indien</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="academic-card guadeloupe-card">
                <div style="color: {self.color_palette['GUADELOUPÉEN']}; font-size: 1rem; font-weight: 600; text-align: center;">🏛️ STATUTS</div>
                <div class="metric-value" style="color: {self.color_palette['GUADELOUPÉEN']}; text-align: center;">3</div>
                <div style="color: #cccccc; text-align: center;">Officiel, régional, national</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="academic-card reunion-card">
                <div style="color: {self.color_palette['RÉUNIONNAIS']}; font-size: 1rem; font-weight: 600; text-align: center;">📚 VARIÉTÉS</div>
                <div class="metric-value" style="color: {self.color_palette['RÉUNIONNAIS']}; text-align: center;">6</div>
                <div style="color: #cccccc; text-align: center;">Créoles principales documentées</div>
            </div>
            """, unsafe_allow_html=True)

    def create_linguistic_comparison(self):
        """Crée une comparaison linguistique complète"""
        st.markdown('<h3 class="section-title">🔤 ANALYSE LINGUISTIQUE COMPARÉE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Composition du Lexique</div>', unsafe_allow_html=True)
            self.create_lexical_composition_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 Vitalité Linguistique</div>', unsafe_allow_html=True)
            self.create_vitality_chart()
        
        # Analyse détaillée par créole
        st.markdown('<div class="subsection-title">🔍 Analyse Détailée par Créole</div>', unsafe_allow_html=True)
        self.create_detailed_linguistic_analysis()

    def create_lexical_composition_chart(self):
        """Graphique de composition lexicale adapté au fond noir"""
        creoles = list(self.linguistic_data.keys())
        
        fig = go.Figure()
        
        # Ajouter les pourcentages pour chaque source
        sources = ['vocabulaire_francais', 'influences_africaines', 'influences_autres']
        noms_sources = ['Français', 'Africaines', 'Autres']
        
        for i, (source, nom) in enumerate(zip(sources, noms_sources)):
            valeurs = [self.linguistic_data[creole][source] for creole in creoles]
            fig.add_trace(go.Bar(
                name=nom,
                x=creoles,
                y=valeurs,
                marker_color=self.data_colors[source],
                text=[f"{v}%" for v in valeurs],
                textposition='auto',
                textfont=dict(color='white', size=12, weight='bold')
            ))
        
        fig.update_layout(
            barmode='stack',
            title='Composition Lexicale des Créoles Françaises',
            xaxis_title='Créoles',
            yaxis_title='Pourcentage (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            )
        )
        
        # Améliorer la lisibilité des axes
        fig.update_xaxes(
            tickfont=dict(size=12, color='#ffffff', family="Arial Black"),
            title_font=dict(size=14, color='#ffffff', family="Arial Black"),
            gridcolor='#333333',
            zerolinecolor='#444444'
        )
        fig.update_yaxes(
            tickfont=dict(size=12, color='#ffffff', family="Arial Black"),
            title_font=dict(size=14, color='#ffffff', family="Arial Black"),
            gridcolor='#333333',
            zerolinecolor='#444444'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_vitality_chart(self):
        """Graphique de vitalité linguistique adapté au fond noir"""
        creoles = list(self.linguistic_data.keys())
        vitalite = [self.linguistic_data[creole]['vitalite'] for creole in creoles]
        standardisation = [self.linguistic_data[creole]['standardisation'] for creole in creoles]
        
        fig = go.Figure()
        
        for i, creole in enumerate(creoles):
            fig.add_trace(go.Scatter(
                x=[vitalite[i]],
                y=[standardisation[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[creole], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[creole],
                textposition="middle center",
                textfont=dict(color='white', size=14, weight='bold', family="Arial Black"),
                name=creole,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Vitalité vs Standardisation',
            xaxis_title='Vitalité (%)',
            yaxis_title='Standardisation (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(range=[80, 100], tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(range=[65, 90], tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_linguistic_analysis(self):
        """Analyse linguistique détaillée avec onglets"""
        creoles = list(self.creoles_data.keys())
        tabs = st.tabs(creoles)
        
        for i, creole in enumerate(creoles):
            with tabs[i]:
                couleur = self.color_palette[creole]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{creole}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.creoles_data[creole]['pays']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques linguistiques
                    st.metric("Locuteurs", f"{self.creoles_data[creole]['locuteurs']:,}")
                    st.metric("Statut", self.creoles_data[creole]['statut_officiel'])
                    st.metric("Vitalité", f"{self.linguistic_data[creole]['vitalite']}%")
                    
                    # Exemple de texte
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Exemple:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.creoles_data[creole]['texte_exemple']}</div>
                        <div style="color: #cccccc; margin-top: 0.5rem; font-weight: 500;">{self.creoles_data[creole]['traduction']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques linguistiques
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Caractéristiques:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for caract in self.creoles_data[creole]['caracteristiques_linguistiques']:
                        st.markdown(f"<li>{caract}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                    
                    # Influences
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Influences:</div>
                        <div style="color: #ffffff; font-weight: 500;">{', '.join(self.creoles_data[creole]['influences'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Complexité', 'Vitalité', 'Standardisation']
                    valeurs = [
                        self.linguistic_data[creole]['complexite_grammaticale'] * 10,
                        self.linguistic_data[creole]['vitalite'],
                        self.linguistic_data[creole]['standardisation']
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=creole
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12, family="Arial Black"),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12, family="Arial Black"),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14, family="Arial Black"),
                        showlegend=False,
                        height=300,
                        title=f"Profil Linguistique - {creole}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_historical_analysis(self):
        """Analyse historique approfondie"""
        st.markdown('<h3 class="section-title">⏳ ANALYSE HISTORIQUE ET CHRONOLOGIQUE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📅 Chronologie Historique</div>', unsafe_allow_html=True)
            self.create_historical_timeline()
        
        with col2:
            st.markdown('<div class="subsection-title">🗺️ Expansion Géographique</div>', unsafe_allow_html=True)
            self.create_geographical_expansion_map()
        
        # Analyse par période
        st.markdown('<div class="subsection-title">📊 Évolution par Période</div>', unsafe_allow_html=True)
        self.create_period_analysis()

    def create_historical_timeline(self):
        """Crée une timeline historique interactive adaptée au fond noir"""
        timeline_df = pd.DataFrame(self.timeline_data)
        
        fig = px.scatter(timeline_df, x='annee', y='importance', color='region',
                        size='importance', hover_name='evenement',
                        color_discrete_map=self.color_palette,
                        hover_data=['region', 'importance'])
        
        fig.update_layout(
            title='Chronologie du Développement des Créoles Françaises',
            xaxis_title='Année',
            yaxis_title='Importance historique',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_geographical_expansion_map(self):
        """Carte d'expansion géographique adaptée au fond noir"""
        # Coordonnées approximatives des régions
        regions_data = {
            'Caraïbes': {'lat': 18.5, 'lon': -72, 'size': 50, 'color': self.color_palette['Caraïbes']},
            'Océan Indien': {'lat': -20, 'lon': 57, 'size': 40, 'color': self.color_palette['Océan Indien']}
        }
        
        fig = go.Figure()
        
        for region, data in regions_data.items():
            fig.add_trace(go.Scattergeo(
                lon=[data['lon']],
                lat=[data['lat']],
                text=[region],
                marker=dict(
                    size=data['size'],
                    color=data['color'],
                    line=dict(width=2, color='#ffffff'),
                    opacity=0.9
                ),
                name=region
            ))
        
        fig.update_layout(
            title='Régions des Créoles Françaises',
            geo=dict(
                scope='world',
                showland=True,
                landcolor='#1a1a1a',
                countrycolor='#444444',
                showocean=True,
                oceancolor='#0a0a0a',
                bgcolor='#0a0a0a'
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_period_analysis(self):
        """Analyse par période historique adaptée au fond noir"""
        # Créer un DataFrame avec les périodes
        periods_data = [
            {'periode': 'Période de formation (1650-1750)', 'debut': 1650, 'fin': 1750, 'impact': 'Fondation', 'evenements': 'Formation des créoles'},
            {'periode': 'Expansion (1750-1850)', 'debut': 1750, 'fin': 1850, 'impact': 'Développement', 'evenements': 'Expansion et diversification'},
            {'periode': 'Pression (1850-1950)', 'debut': 1850, 'fin': 1950, 'impact': 'Récession', 'evenements': 'Pression du français standard'},
            {'periode': 'Renaissance (1950-2000)', 'debut': 1950, 'fin': 2000, 'impact': 'Revitalisation', 'evenements': 'Renaissance créole'},
            {'periode': 'Reconnaissance (2000-Présent)', 'debut': 2000, 'fin': 2024, 'impact': 'Institutionnalisation', 'evenements': 'Reconnaissance officielle'}
        ]
        
        df_periods = pd.DataFrame(periods_data)
        
        # Utiliser un graphique à barres horizontales
        fig = go.Figure()
        
        for impact in df_periods['impact'].unique():
            df_filtered = df_periods[df_periods['impact'] == impact]
            fig.add_trace(go.Bar(
                y=df_filtered['periode'],
                x=df_filtered['fin'] - df_filtered['debut'],
                orientation='h',
                name=impact,
                marker_color=self.data_colors[impact],
                text=[f"{row['evenements']}" for _, row in df_filtered.iterrows()],
                textposition='auto',
                textfont=dict(color='white', size=11, weight='bold'),
                hovertemplate='<b>%{y}</b><br>Durée: %{x} ans<br>%{text}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Évolution Historique des Créoles Françaises',
            xaxis_title='Durée (années)',
            yaxis_title='Période',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            barmode='stack',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Ajouter une explication
        st.markdown("""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">📋 LÉGENDE DES PÉRIODES</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <div style="display: inline-block; width: 15px; height: 15px; background-color: #ff4757; margin-right: 0.5rem; border: 1px solid #ffffff;"></div>
                    <strong style="color: #ffffff;">Fondation</strong> - Formation initiale des créoles
                </div>
                <div style="font-weight: 500;">
                    <div style="display: inline-block; width: 15px; height: 15px; background-color: #3498db; margin-right: 0.5rem; border: 1px solid #ffffff;"></div>
                    <strong style="color: #ffffff;">Développement</strong> - Expansion et diversification
                </div>
                <div style="font-weight: 500;">
                    <div style="display: inline-block; width: 15px; height: 15px; background-color: #95a5a6; margin-right: 0.5rem; border: 1px solid #ffffff;"></div>
                    <strong style="color: #ffffff;">Récession</strong> - Pression du français standard
                </div>
                <div style="font-weight: 500;">
                    <div style="display: inline-block; width: 15px; height: 15px; background-color: #2ecc71; margin-right: 0.5rem; border: 1px solid #ffffff;"></div>
                    <strong style="color: #ffffff;">Revitalisation</strong> - Renaissance culturelle
                </div>
                <div style="font-weight: 500;">
                    <div style="display: inline-block; width: 15px; height: 15px; background-color: #9b59b6; margin-right: 0.5rem; border: 1px solid #ffffff;"></div>
                    <strong style="color: #ffffff;">Institutionnalisation</strong> - Reconnaissance officielle
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def create_geopolitical_analysis(self):
        """Analyse géopolitique complète"""
        st.markdown('<h3 class="section-title">🏛️ ANALYSE GÉOPOLITIQUE ET STATUT JURIDIQUE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Statuts Juridiques Comparés</div>', unsafe_allow_html=True)
            self.create_legal_status_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎯 Usage Institutionnel</div>', unsafe_allow_html=True)
            self.create_institutional_usage_chart()
        
        # Analyse détaillée par pays
        st.markdown('<div class="subsection-title">🔍 Analyse par Territoire</div>', unsafe_allow_html=True)
        self.create_detailed_geopolitical_analysis()

    def create_legal_status_chart(self):
        """Graphique des statuts juridiques adapté au fond noir"""
        creoles = list(self.geopolitical_data.keys())
        statuts = []
        
        for creole in creoles:
            statut = self.geopolitical_data[creole]['statut_politique']
            if 'officielle' in statut.lower():
                statuts.append(3)
            elif 'national' in statut.lower():
                statuts.append(2)
            else:
                statuts.append(1)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=creoles,
            y=statuts,
            marker_color=[self.color_palette[creole] for creole in creoles],
            text=['Officiel' if s == 3 else 'National' if s == 2 else 'Régional' for s in statuts],
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold')
        ))
        
        fig.update_layout(
            title='Statut Juridique des Créoles Françaises',
            xaxis_title='Créoles',
            yaxis_title='Niveau de reconnaissance',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_institutional_usage_chart(self):
        """Graphique de l'usage institutionnel adapté au fond noir"""
        creoles = list(self.geopolitical_data.keys())
        
        usage_data = {
            'Gouvernement': [1 if self.geopolitical_data[creole]['usage_gouvernement'] in ['Oui', 'Limité', 'Informel'] else 0 for creole in creoles],
            'Justice': [1 if 'Oui' in self.geopolitical_data[creole]['usage_judiciaire'] else 0 for creole in creoles],
            'Éducation': [2 if 'Primaire' in self.geopolitical_data[creole]['usage_education'] else 1 if 'En développement' in self.geopolitical_data[creole]['usage_education'] else 0 for creole in creoles],
            'Médias': [2 if 'Forte' in self.geopolitical_data[creole]['presence_media'] else 1 if 'Moyenne' in self.geopolitical_data[creole]['presence_media'] else 0 for creole in creoles]
        }
        
        fig = go.Figure()
        
        couleurs_usage = ['#ff4757', '#3498db', '#2ecc71', '#f39c12']
        
        for i, (usage, valeurs) in enumerate(usage_data.items()):
            fig.add_trace(go.Bar(
                name=usage,
                x=creoles,
                y=valeurs,
                marker_color=couleurs_usage[i],
                text=valeurs,
                textposition='auto',
                textfont=dict(color='white', size=12, weight='bold')
            ))
        
        fig.update_layout(
            barmode='group',
            title='Usage Institutionnel des Créoles',
            xaxis_title='Créoles',
            yaxis_title='Niveau d\'usage',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_geopolitical_analysis(self):
        """Analyse géopolitique détaillée"""
        creoles = list(self.creoles_data.keys())
        tabs = st.tabs(creoles)
        
        for i, creole in enumerate(creoles):
            with tabs[i]:
                couleur = self.color_palette[creole]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations politiques
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{creole}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.creoles_data[creole]['pays']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques politiques
                    st.metric("Statut", self.geopolitical_data[creole]['statut_politique'])
                    st.metric("Reconnaissance", self.geopolitical_data[creole]['reconnaissance_internationale'])
                    st.metric("Usage Gouvernemental", self.geopolitical_data[creole]['usage_gouvernement'])
                    
                    # Contexte historique
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Contexte Historique:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.creoles_data[creole]['contexte_historique']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Usage institutionnel
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Usage Institutionnel:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Justice: {self.geopolitical_data[creole]['usage_judiciaire']}</li>
                            <li>Éducation: {self.geopolitical_data[creole]['usage_education']}</li>
                            <li>Médias: {self.geopolitical_data[creole]['presence_media']}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Politiques linguistiques
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Politiques Linguistiques:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.geopolitical_data[creole]['politiques_linguistiques']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques géopolitiques
                    categories = ['Reconnaissance', 'Usage Gov.', 'Usage Justice', 'Usage Éducation', 'Présence Médias']
                    valeurs = [
                        3 if self.geopolitical_data[creole]['reconnaissance_internationale'] == 'Oui' else 1,
                        2 if self.geopolitical_data[creole]['usage_gouvernement'] in ['Oui', 'Limité'] else 1 if self.geopolitical_data[creole]['usage_gouvernement'] == 'Informel' else 0,
                        2 if self.geopolitical_data[creole]['usage_judiciaire'] == 'Oui' else 0,
                        2 if self.geopolitical_data[creole]['usage_education'] == 'Primaire' else 1 if self.geopolitical_data[creole]['usage_education'] in ['En développement', 'Optionnel', 'Informel'] else 0,
                        2 if self.geopolitical_data[creole]['presence_media'] == 'Forte' else 1 if self.geopolitical_data[creole]['presence_media'] == 'Moyenne' else 0
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=creole
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 3],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12, family="Arial Black"),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12, family="Arial Black"),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14, family="Arial Black"),
                        showlegend=False,
                        height=300,
                        title=f"Profil Géopolitique - {creole}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_demographic_analysis(self):
        """Analyse démographique complète"""
        st.markdown('<h3 class="section-title">👥 ANALYSE DÉMOGRAPHIQUE ET SOCIALE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Répartition des Locuteurs</div>', unsafe_allow_html=True)
            self.create_speakers_distribution_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 Transmission Intergénérationnelle</div>', unsafe_allow_html=True)
            self.create_transmission_chart()
        
        # Analyse détaillée par créole
        st.markdown('<div class="subsection-title">🔍 Analyse Démographique par Créole</div>', unsafe_allow_html=True)
        self.create_detailed_demographic_analysis()

    def create_speakers_distribution_chart(self):
        """Graphique de répartition des locuteurs adapté au fond noir"""
        creoles = list(self.demographic_data.keys())
        locuteurs_natifs = [self.demographic_data[creole]['locuteurs_natifs'] for creole in creoles]
        locuteurs_second = [self.demographic_data[creole]['locuteurs_seconde_langue'] for creole in creoles]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Locuteurs natifs',
            x=creoles,
            y=locuteurs_natifs,
            marker_color='#3498db',
            text=[f"{v:,}" for v in locuteurs_natifs],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.add_trace(go.Bar(
            name='Locuteurs seconde langue',
            x=creoles,
            y=locuteurs_second,
            marker_color='#ff4757',
            text=[f"{v:,}" for v in locuteurs_second],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            barmode='stack',
            title='Répartition des Locuteurs par Créole',
            xaxis_title='Créoles',
            yaxis_title='Nombre de locuteurs',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_transmission_chart(self):
        """Graphique de transmission intergénérationnelle adapté au fond noir"""
        creoles = list(self.demographic_data.keys())
        transmission = [self.demographic_data[creole]['transmission_familiale'] for creole in creoles]
        bilinguisme = [self.demographic_data[creole]['bilinguisme'] for creole in creoles]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Transmission familiale',
            x=creoles,
            y=transmission,
            marker_color='#2ecc71',
            text=[f"{v}%" for v in transmission],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.add_trace(go.Bar(
            name='Bilinguisme',
            x=creoles,
            y=bilinguisme,
            marker_color='#9b59b6',
            text=[f"{v}%" for v in bilinguisme],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            barmode='group',
            title='Transmission Familiale et Bilinguisme',
            xaxis_title='Créoles',
            yaxis_title='Pourcentage (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_demographic_analysis(self):
        """Analyse démographique détaillée"""
        creoles = list(self.creoles_data.keys())
        tabs = st.tabs(creoles)
        
        for i, creole in enumerate(creoles):
            with tabs[i]:
                couleur = self.color_palette[creole]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations démographiques
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{creole}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.creoles_data[creole]['pays']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques démographiques
                    st.metric("Locuteurs natifs", f"{self.demographic_data[creole]['locuteurs_natifs']:,}")
                    st.metric("Locuteurs seconde langue", f"{self.demographic_data[creole]['locuteurs_seconde_langue']:,}")
                    st.metric("Transmission familiale", f"{self.demographic_data[creole]['transmission_familiale']}%")
                    
                    # Pyramide des âges
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Répartition par âge:</div>
                        <div style="color: #ffffff; font-weight: 500;">
                            0-14 ans: {self.demographic_data[creole]['tranches_age']['0-14']}%<br>
                            15-64 ans: {self.demographic_data[creole]['tranches_age']['15-64']}%<br>
                            65+ ans: {self.demographic_data[creole]['tranches_age']['65+']}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques sociales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Caractéristiques Sociales:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Urbanisation: {self.demographic_data[creole]['urbanisation']}%</li>
                            <li>Niveau d'éducation: {self.demographic_data[creole]['niveau_education']}%</li>
                            <li>Bilinguisme: {self.demographic_data[creole]['bilinguisme']}%</li>
                            <li>Attitude des locuteurs: {self.demographic_data[creole]['attitude_locuteurs']}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques démographiques
                    categories = ['Transmission', 'Bilinguisme', 'Urbanisation', 'Éducation']
                    valeurs = [
                        self.demographic_data[creole]['transmission_familiale'],
                        self.demographic_data[creole]['bilinguisme'],
                        self.demographic_data[creole]['urbanisation'],
                        self.demographic_data[creole]['niveau_education']
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=creole
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12, family="Arial Black"),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12, family="Arial Black"),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14, family="Arial Black"),
                        showlegend=False,
                        height=300,
                        title=f"Profil Démographique - {creole}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_future_perspectives(self):
        """Analyse des perspectives d'avenir"""
        st.markdown('<h3 class="section-title">🔮 PERSPECTIVES D\'AVENIR</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📈 Tendances Actuelles</div>', unsafe_allow_html=True)
            self.create_trends_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎯 Projets de Revitalisation</div>', unsafe_allow_html=True)
            self.create_revitalization_projects()
        
        # Analyse détaillée par créole
        st.markdown('<div class="subsection-title">🔍 Recommandations par Créole</div>', unsafe_allow_html=True)
        self.create_recommendations()

    def create_trends_chart(self):
        """Graphique des tendances actuelles adapté au fond noir"""
        # Données simulées pour les tendances
        years = list(range(2000, 2025, 5))
        
        fig = go.Figure()
        
        for creole in self.creoles_data.keys():
            # Simuler des données de tendance
            base_value = self.linguistic_data[creole]['vitalite']
            trend_values = [base_value + i*0.5 for i in range(len(years))]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=trend_values,
                mode='lines+markers',
                name=creole,
                line=dict(color=self.color_palette[creole], width=3),
                marker=dict(size=8, color=self.color_palette[creole])
            ))
        
        fig.update_layout(
            title='Évolution de la Vitalité des Créoles (2000-2024)',
            xaxis_title='Année',
            yaxis_title='Indice de vitalité',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14, family="Arial Black"),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00d4ff',
                borderwidth=1,
                font=dict(color='white', size=12, family="Arial Black")
            ),
            xaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12, family="Arial Black"), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_revitalization_projects(self):
        """Affiche les projets de revitalisation"""
        projects_data = {
            'HAÏTIEN': {
                'projets': ['Standardisation orthographique', 'Enseignement bilingue', 'Médias créophones'],
                'financement': 'International et local',
                'acteurs': 'Gouvernement, ONG, Universités'
            },
            'MARTINIQUAIS': {
                'projets': ['Enseignement optionnel', 'Médias culturels', 'Festivals créoles'],
                'financement': 'Régional et européen',
                'acteurs': 'Collectivités, Associations'
            },
            'GUADELOUPÉEN': {
                'projets': ['Enseignement optionnel', 'Médias culturels', 'Documentation linguistique'],
                'financement': 'Régional et européen',
                'acteurs': 'Collectivités, Associations'
            },
            'RÉUNIONNAIS': {
                'projets': ['Enseignement optionnel', 'Médias locaux', 'Documentation linguistique'],
                'financement': 'Régional et européen',
                'acteurs': 'Collectivités, Associations'
            },
            'MAURICIEN': {
                'projets': ['Standardisation', 'Médias créoles', 'Littérature'],
                'financement': 'Privé et gouvernemental',
                'acteurs': 'ONG, Universités, Médias'
            },
            'SEYCHELLOIS': {
                'projets': ['Enseignement primaire', 'Médias nationaux', 'Documentation'],
                'financement': 'Gouvernemental',
                'acteurs': 'Gouvernement, Universités'
            }
        }
        
        creoles = list(projects_data.keys())
        tabs = st.tabs(creoles)
        
        for i, creole in enumerate(creoles):
            with tabs[i]:
                couleur = self.color_palette[creole]
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                    <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">Projets de Revitalisation - {creole}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Projets Principaux:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for projet in projects_data[creole]['projets']:
                        st.markdown(f"<li>{projet}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Financement:</div>
                        <div style="color: #ffffff; font-weight: 500;">{projects_data[creole]['financement']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Acteurs Clés:</div>
                        <div style="color: #ffffff; font-weight: 500;">{projects_data[creole]['acteurs']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    def create_recommendations(self):
        """Affiche les recommandations par créole"""
        recommendations_data = {
            'HAÏTIEN': {
                'priorite': 'Renforcement de l\'enseignement bilingue',
                'actions': ['Formation des enseignants', 'Production de matériel pédagogique', 'Intégration dans le système éducatif formel'],
                'defis': ['Ressources limitées', 'Standardisation', 'Reconnaissance internationale']
            },
            'MARTINIQUAIS': {
                'priorite': 'Reconnaissance officielle',
                'actions': ['Campagnes de sensibilisation', 'Documentation linguistique', 'Médias spécialisés'],
                'defis': ['Dominance du français', 'Manque de standardisation', 'Attitudes ambivalentes']
            },
            'GUADELOUPÉEN': {
                'priorite': 'Transmission intergénérationnelle',
                'actions': ['Programmes familiaux', 'Activités culturelles', 'Médias communautaires'],
                'defis': ['Urbanisation', 'Médias dominants', 'Manque de matériel éducatif']
            },
            'RÉUNIONNAIS': {
                'priorite': 'Standardisation et documentation',
                'actions': ['Corpus linguistique', 'Dictionnaires', 'Outils numériques'],
                'defis': ['Variétés dialectales', 'Influences multiples', 'Ressources limitées']
            },
            'MAURICIEN': {
                'priorite': 'Reconnaissance institutionnelle',
                'actions': ['Statut officiel', 'Enseignement formel', 'Médias nationaux'],
                'defis': ['Plurilinguisme', 'Influence anglaise', 'Standardisation']
            },
            'SEYCHELLOIS': {
                'priorite': 'Développement de ressources',
                'actions': ['Matériel éducatif avancé', 'Documentation', 'Technologies linguistiques'],
                'defis': ['Population limitée', 'Ressources', 'Formation']
            }
        }
        
        creoles = list(recommendations_data.keys())
        tabs = st.tabs(creoles)
        
        for i, creole in enumerate(creoles):
            with tabs[i]:
                couleur = self.color_palette[creole]
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                    <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">Recommandations - {creole}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Priorité:</div>
                        <div style="color: #ffffff; font-weight: 500;">{recommendations_data[creole]['priorite']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Actions Recommandées:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for action in recommendations_data[creole]['actions']:
                        st.markdown(f"<li>{action}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Défis Principaux:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for defi in recommendations_data[creole]['defis']:
                        st.markdown(f"<li>{defi}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)

    def run(self):
        """Exécute l'application dashboard"""
        self.display_header()
        
        # Onglets principaux
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔤 Analyse Linguistique", "⏳ Analyse Historique", "🏛️ Analyse Géopolitique", "👥 Analyse Démographique", "🔮 Perspectives d'Avenir"])
        
        with tab1:
            self.create_linguistic_comparison()
        
        with tab2:
            self.create_historical_analysis()
        
        with tab3:
            self.create_geopolitical_analysis()
        
        with tab4:
            self.create_demographic_analysis()
        
        with tab5:
            self.create_future_perspectives()
        
        # Pied de page
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 1rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 8px; border: 1px solid #333333;">
            <p style="color: #ffffff; font-weight: 500;">📊 Dashboard d'Analyse des Créoles Françaises</p>
            <p style="color: #cccccc; font-size: 0.9rem;">Données à titre informatif • Mis à jour en 2024</p>
        </div>
        """, unsafe_allow_html=True)

# Lancement de l'application
if __name__ == "__main__":
    analyzer = CreoleAnalyzer()
    analyzer.run()