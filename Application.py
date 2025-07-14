import streamlit as st
import pandas as pd
import pickle
from streamlit_option_menu import option_menu

# === Configuration générale et style CSS global ===
st.set_page_config(
    page_title="🌾 Prédiction agroécologique", 
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
/* Importation de Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Variables CSS pour la cohérence */
:root {
    --primary-color: #2E8B57;
    --secondary-color: #90EE90;
    --accent-color: #FFD700;
    --text-dark: #2c3e50;
    --text-light: #7f8c8d;
    --background-light: #f8fffe;
    --background-card: #ffffff;
    --success-color: #27AE60;
    --error-color: #E74C3C;
    --warning-color: #F39C12;
    --border-radius: 12px;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Fond principal */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0fff0 100%) !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Navigation styling */
.stMenu {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 15px !important;
    padding: 0.5rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
}

/* Titre principal */
.main-title {
    background: linear-gradient(135deg, var(--primary-color) 0%, #228B22 100%);
    padding: 3rem 2rem;
    border-radius: var(--border-radius);
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
    text-align: center;
    position: relative;
    overflow: hidden;
}

.main-title::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.3;
}

.main-title h1 {
    color: white !important;
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

.main-title .subtitle {
    color: #e8f5e8;
    font-size: 1.3rem;
    margin-top: 0.5rem;
    font-weight: 300;
    position: relative;
    z-index: 1;
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, rgba(46, 139, 87, 0.1) 0%, rgba(34, 139, 34, 0.1) 100%);
    border-radius: var(--border-radius);
    padding: 3rem 2rem;
    margin-bottom: 3rem;
    text-align: center;
    border: 2px solid rgba(46, 139, 87, 0.2);
}

.hero-title {
    font-size: 2.5rem;
    color: var(--primary-color);
    font-weight: 600;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: var(--text-light);
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Feature cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.feature-card {
    background: var(--background-card);
    border-radius: var(--border-radius);
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: all 0.3s ease;
    border: 1px solid rgba(46, 139, 87, 0.1);
    text-align: center;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(46, 139, 87, 0.15);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.feature-description {
    color: var(--text-light);
    line-height: 1.6;
}

/* Description */
.description-box {
    background: var(--background-card);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    margin-bottom: 2rem;
    border-left: 4px solid var(--primary-color);
}

.description-box p {
    color: var(--text-dark);
    font-size: 1.1rem;
    line-height: 1.6;
    margin: 0;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fffe 100%) !important;
    border-right: 1px solid #e0e0e0;
}

[data-testid="stSidebar"] .css-1d391kg {
    padding: 2rem 1rem;
}

/* Sidebar title */
.sidebar-title {
    background: linear-gradient(135deg, var(--primary-color) 0%, #228B22 100%);
    color: white !important;
    padding: 1rem;
    border-radius: var(--border-radius);
    margin-bottom: 1.5rem;
    text-align: center;
    font-weight: 600;
    box-shadow: var(--shadow);
}

/* Form styling */
.stSelectbox > div > div {
    background: var(--background-card);
    border: 2px solid #e0e0e0;
    border-radius: var(--border-radius);
    transition: all 0.3s ease;
}

.stSelectbox > div > div:hover {
    border-color: var(--primary-color);
    box-shadow: 0 0 10px rgba(46, 139, 87, 0.2);
}

.stNumberInput > div > div > input {
    background: var(--background-card);
    border: 2px solid #e0e0e0;
    border-radius: var(--border-radius);
    transition: all 0.3s ease;
}

.stNumberInput > div > div > input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 10px rgba(46, 139, 87, 0.2);
}

/* Bouton de prédiction */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color) 0%, #228B22 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: var(--border-radius) !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(46, 139, 87, 0.3) !important;
}

/* Cartes de résultats */
.result-card {
    background: var(--background-card);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease;
}

.result-card:hover {
    transform: translateY(-2px);
}

.result-positive {
    border-left: 5px solid var(--success-color);
    background: linear-gradient(135deg, #e8f5e8 0%, #f0fff0 100%);
}

.result-negative {
    border-left: 5px solid var(--error-color);
    background: linear-gradient(135deg, #ffebee 0%, #ffeef0 100%);
}

.result-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.result-description {
    color: var(--text-light);
    font-size: 0.95rem;
    line-height: 1.4;
}

/* Résumé global */
.summary-box {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border: 1px solid #ffeaa7;
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin-top: 2rem;
    box-shadow: var(--shadow);
}

.summary-success {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    border-color: #c3e6cb;
}

.summary-warning {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border-color: #ffeaa7;
}

/* Icônes emoji plus grandes */
.emoji-large {
    font-size: 1.3rem;
    margin-right: 0.5rem;
}

/* Divider personnalisé */
.custom-divider {
    height: 2px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #228B22 100%);
    border: none;
    border-radius: 1px;
    margin: 2rem 0;
}

/* Animation pour les résultats */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

/* Stats cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.stat-card {
    background: var(--background-card);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    text-align: center;
    box-shadow: var(--shadow);
    border: 1px solid rgba(46, 139, 87, 0.1);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.stat-label {
    color: var(--text-light);
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-title h1 {
        font-size: 2rem;
    }
    
    .description-box {
        padding: 1rem;
    }
    
    .result-card {
        padding: 1rem;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# === Chargement du modèle et scaler ===
@st.cache_resource
def load_model():
    with open("model_classifier_chain_svm.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

# === Prétraitement des données ===
def preprocess_input(age, sexe, educ, formation, ONG, superficie, revenu, subvention, arrond):
    sexe = 1 if sexe == "Homme" else 0
    formation = 1 if formation == "Oui" else 0
    ONG = 1 if ONG == "Oui" else 0
    subvention = 1 if subvention == "Oui" else 0

    educ_map = {"Aucun": 0, "Primaire": 1, "Secondaire": 2, "Universitaire": 3}
    revenu_map = {
        "<100 000": 0, "100 000 - 300 000": 1, "300 000 - 500 000": 2,
        "500 000 - 700 000": 3, "> 700 000": 4
    }

    input_data = {
        'age': age,
        'sexe': sexe,
        'educ': educ_map.get(educ, 0),
        'formation': formation,
        'ONG': ONG,
        'Superficie': superficie,
        'revenu': revenu_map.get(revenu, 0),
        'subvention': subvention
    }

    for a in ['Diakhao', 'Diofior', 'Diouroup', 'Fimala', 'Ndiob', 'Niakhar', 'Tattaguine']:
        input_data[f'arrond_{a}'] = 1 if arrond == a else 0

    df = pd.DataFrame([input_data])
    df[['age', 'Superficie']] = scaler.transform(df[['age', 'Superficie']])
    return df

# === Page d'accueil ===
def home_page():
    st.markdown("""
    <div class="main-title">
        <h1>🌱 Prédiction conjointe de l’adoption des pratiques agroécologiques</h1>
    </div>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🚀 Bienvenue dans l'avenir de l'agriculture</div>
    </div>
    """, unsafe_allow_html=True)

    # Statistiques
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">Pratiques analysées</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">7</div>
            <div class="stat-label">Arrondissements</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">MACHINE LEARNING</div>
            <div class="stat-label">Méthodologie utilisée</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    

    # Description détaillée
    st.markdown("""
    <div class="description-box">
        <h3 style="color: var(--primary-color); margin-bottom: 1rem;">📋 À propos de cette application</h3>
        <p>
           Cette application prédit les pratiques agroécologiques qu’un producteur du département de Fatick est susceptible d’adopter, en fonction de sa zone géographique et de ses caractéristiques socio-économiques et institutionnelles.
        </p>
        <p style="margin-top: 1rem;">
            <strong>Pratiques analysées :</strong> Monoculture, rotation des cultures, culture en association, 
            et défrichement pour l'agriculture. Chaque prédiction est accompagnée d'une probabilité 
            d'adoption et d'analyses détaillées pour faciliter la prise de décision.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Commencer la Prédiction", key="cta_button", use_container_width=True):
            st.query_params["page"] = "prediction"
            st.rerun()

# === Page de prédiction ===
def prediction_page():
    st.markdown("""
    <div class="main-title">
        <h1>🔮 Prédiction conjointe de l’adoption des pratiques agroécologiques</h1>
    </div>
    """, unsafe_allow_html=True)

    # Description dans une belle boîte
    st.markdown("""
    <div class="description-box">
        <p>
            <span class="emoji-large">🎯</span>
           Renseignez les champs de la barre latérale située à gauche, puis cliquez sur le bouton de prédiction pour connaître les résultats.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar : formulaire avec style amélioré
    st.sidebar.markdown("""
    <div class="sidebar-title">
        <span class="emoji-large">📋</span>Profil du Producteur
    </div>
    """, unsafe_allow_html=True)

    # Informations géographiques
    st.sidebar.markdown("**🗺️ Localisation**")
    arrondissements = ['Diakhao', 'Diofior', 'Diouroup', 'Fimala', 'Ndiob', 'Niakhar', 'Tattaguine']
    arrond = st.sidebar.selectbox("📍 Arrondissement", arrondissements)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**👤 Informations personnelles**")
    sexe = st.sidebar.selectbox("🚹 Sexe", ["Homme", "Femme"])
    age = st.sidebar.number_input("🎂 Âge", min_value=18, max_value=100, value=35, step=1)
    educ = st.sidebar.selectbox("🎓 Niveau d'éducation", ["Aucun", "Primaire", "Secondaire", "Universitaire"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📚 Formation et accompagnement**")
    formation = st.sidebar.selectbox("📖 Formation reçue", ["Oui", "Non"])
    ONG = st.sidebar.selectbox("🏢 Présence d'une ONG", ["Oui", "Non"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💰 Aspects économiques**")
    revenu = st.sidebar.selectbox("💵 Revenu annuel (FCFA)", 
                                 ["<100 000", "100 000 - 300 000", "300 000 - 500 000", 
                                  "500 000 - 700 000", "> 700 000"])
    Subvention = st.sidebar.selectbox("🎁 Subvention reçue", ["Oui", "Non"])
    superficie = st.sidebar.number_input("🌾 Superficie exploitée (ha)", min_value=0.1, max_value=50.0, value=2.5, step=0.1)

    st.sidebar.markdown("---")

    # Bouton de prédiction avec espacement
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.sidebar.button("🚀 Lancer la Prédiction", key="predict")

    # Section des résultats
    if predict_button:
        # Animation de chargement
        with st.spinner('🔄 Analyse en cours...'):
            df = preprocess_input(age, sexe, educ, formation, ONG, superficie, revenu, Subvention, arrond)
            proba = model.predict_proba(df).toarray()[0]
            pred = model.predict(df).toarray()[0]

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        
        # Titre des résultats
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: var(--primary-color); font-weight: 600;">
                📊 Résultats de la Prédiction
            </h2>
        </div>
        """, unsafe_allow_html=True)

        pratiques = [
            ("🌾", "Monoculture avec des cultures annuelles"),
            ("🔄", "Rotation des cultures"),
            ("🤝", "Culture en association ou intercalaire"),
            ("🪓", "Défrichement pour l'agriculture")
        ]

        # Affichage des résultats avec animations
        for i, (emoji, label) in enumerate(pratiques):
            p = proba[i]
            card_class = "result-positive" if pred[i] == 1 else "result-negative"
            status_emoji = "✅" if pred[i] == 1 else "❌"
            status_text = "Adoptée" if pred[i] == 1 else "Non adoptée"

            st.markdown(f"""
            <div class="result-card {card_class} fade-in-up">
                <div class="result-title">
                    {status_emoji} {emoji} {label}
                </div>
                <div class="result-description">
                    <strong>Statut:</strong> {status_text} 
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Résumé global amélioré
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        
        pratiques_adoptees = [pratiques[i][1] for i in range(4) if pred[i] == 1]
        total_pratiques = len(pratiques_adoptees)
        
        if pratiques_adoptees:
            summary_class = "summary-success"
            summary_icon = "🎉"
            summary_title = "Prédiction Positive"
            summary_text = f"Le producteur a de fortes chances d'adopter <strong>{total_pratiques}</strong> pratique(s) agroécologique(s):"
            pratiques_list = "<br>".join([f"• {pratique}" for pratique in pratiques_adoptees])
        else:
            summary_class = "summary-warning"
            summary_icon = "⚠️"
            summary_title = "Prédiction Neutre"
            summary_text = "Le modèle prédit que le producteur n'adoptera probablement aucune des pratiques analysées."
            pratiques_list = ""

        st.markdown(f"""
        <div class="summary-box {summary_class} fade-in-up">
            <h3 style="color: var(--text-dark); margin-bottom: 1rem;">
                {summary_icon} {summary_title}
            </h3>
            <p style="margin-bottom: 0.5rem; font-size: 1.1rem;">
                {summary_text}
            </p>
            {f'<div style="margin-top: 1rem; padding-left: 1rem;">{pratiques_list}</div>' if pratiques_list else ''}
        </div>
        """, unsafe_allow_html=True)

        # Informations supplémentaires
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #6c757d;">
            <small style="color: #6c757d;">
                <strong>💡 Note:</strong> Ces prédictions sont basées sur un modèle d'apprentissage automatique 
                entraîné sur des données du département de Fatick. Les résultats sont indicatifs et doivent être 
                interprétés dans le contexte local spécifique.
            </small>
        </div>
        """, unsafe_allow_html=True)



# === Interface principale ===
def main():
    # Vérifier les paramètres d'URL pour la navigation
    page_param = st.query_params.get("page", "home")
    
    # Navigation
    with st.container():
        selected = option_menu(
            menu_title=None,
            options=["🏠 Accueil", "🔮 Prédiction"],
            icons=["house", "graph-up"],
            menu_icon="cast",
            default_index=0 if page_param == "home" else 1,
            orientation="horizontal",
        )

    # Page routing direct
    if selected == "🏠 Accueil":
        home_page()
    elif selected == "🔮 Prédiction":
        prediction_page()

# === Lancement ===
if __name__ == "__main__":
    main()