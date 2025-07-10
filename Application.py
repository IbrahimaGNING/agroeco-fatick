import streamlit as st
import pandas as pd
import pickle

# === Configuration générale et style CSS global ===
st.set_page_config(page_title="🌾 Prédiction agroécologique", layout="centered")


custom_css = """

<style>
/* ... (ton CSS existant reste inchangé) ... */

/* Curseur main (pointer) pour les menus déroulants */
div[data-baseweb="select"] > div {
    cursor: pointer !important;
}

/* Curseur texte (normal) pour les champs numériques */
input[type="number"] {
    cursor: text !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #e3efef !important;
}
[data-testid="stSidebar"] {
    background-color: #f2f2f2;
    color: #000000;
}
[data-testid="stMarkdownContainer"] {
    color: #2c3e50;
}
h1, h2, h3 {
    color: #6082B6;
}
input, select, textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
}
button[kind="primary"] {
    background-color: #6082B6;
    color: white;
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

# === Interface principale ===
def main():
    # En-tête stylisée
    st.markdown("""
    <div style="background-color:#31333F; padding:12px; border-radius: 8px;margin-bottom: 30px;"">
        <h1 style="font-family:serif; color:#D5E8D4; text-align:center;">
            🌱 Prédiction conjointe de l’adoption des pratiques agroécologiques 🌱
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # 🧾 Texte d’intro sans cadre
    st.markdown("""
    <p style="text-align: justify; font-size: 17px;">
    Cette application prédit les pratiques agroécologiques qu’un producteur de la région de Fatick est susceptible d’adopter,
    en fonction de sa zone géographique et de ses caractéristiques socio-économiques et institutionnelles. Renseignez les champs ci-dessous, puis cliquez sur le bouton 
    de prédiction pour connaître les résultats.
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    # Sidebar : formulaire
    st.sidebar.markdown("### 🧾 Informations du producteur")
    arrondissements = ['Diakhao', 'Diofior', 'Diouroup', 'Fimala', 'Ndiob', 'Niakhar', 'Tattaguine']
    arrond = st.sidebar.selectbox("📍 Arrondissement", arrondissements)
    sexe = st.sidebar.selectbox("👤 Sexe", ["Homme", "Femme"])
    educ = st.sidebar.selectbox("🎓 Niveau d'éducation", ["Aucun", "Primaire", "Secondaire", "Universitaire"])
    formation = st.sidebar.selectbox("📘 A-t-il reçu une formation ?", ["Oui", "Non"])
    ONG = st.sidebar.selectbox("🏢 Présence d'une ONG ?", ["Oui", "Non"])
    Subvention = st.sidebar.selectbox("💸 A-t-il reçu une subvention ?", ["Oui", "Non"])
    revenu = st.sidebar.selectbox("💰 Revenu annuel", ["<100 000", "100 000 - 300 000", "300 000 - 500 000", "500 000 - 700 000", "> 700 000"])
    age = st.sidebar.number_input("🎂 Âge du producteur", min_value=0, max_value=100, value=30)
    superficie = st.sidebar.number_input("🌾 Superficie exploitée (ha)", min_value=0.0, value=1.0)

    # 🔘 Bouton de prédiction
    if st.button("🚀 Lancez la prédiction"):
        df = preprocess_input(age, sexe, educ, formation, ONG, superficie, revenu, Subvention, arrond)
        proba = model.predict_proba(df).toarray()[0]
        pred = model.predict(df).toarray()[0]

        pratiques = [
            "Monoculture avec des cultures annuelles",
            "Rotation des cultures",
            "Culture en association ou intercalaire",
            "Défrichement pour l’agriculture"
        ]

        st.markdown("### ✅ Résultat pour chaque pratique :")

        for i in range(4):
            label = pratiques[i]
            p = proba[i]
            if pred[i] == 1:
                st.markdown(f"""<div style="background-color:#e0f9eb; padding:10px; border-left:5px solid #2ECC71;">
                <strong>🟢 {label}</strong><br>Adoptera probablement cette pratique. <em>({p:.1%} de probabilité)</em>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background-color:#ffecec; padding:10px; border-left:5px solid #E74C3C;">
                <strong>🔴 {label}</strong><br>N’adoptera probablement pas cette pratique. <em>({p:.1%} de probabilité)</em>
                </div>""", unsafe_allow_html=True)

        # Résumé global
        st.divider()
        pratiques_adoptees = [pratiques[i] for i in range(4) if pred[i] == 1]
        if pratiques_adoptees:
            st.success(f"📝 Le producteur a de fortes chances d’adopter : **{', '.join(pratiques_adoptees)}**.")
        else:
            st.warning("⚠️ Le modèle prédit que le producteur n’adoptera aucune des quatre pratiques.")

# === Lancement ===
if __name__ == "__main__":
    main()
