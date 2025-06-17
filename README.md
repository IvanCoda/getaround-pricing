**Projet Data Science - Déploiement de Modèle**

![Getaround Workflow](assets/workflow.png)

## 📌 Sommaire
- [Objectifs](#-objectifs)
- [Structure du Projet](#-structure-du-projet)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Déploiement](#-déploiement)
- [Contributing](#-contributing)

## 🎯 Objectifs
1. Analyser l'impact des retards entre locations
2. Déterminer le seuil optimal pour minimiser les conflits
3. Déployer un modèle de prédiction de prix journalier

## 🏗️ Structure du Projet

getaround-pricing-project/
├── data/
│   ├── get_around_pricing_project.csv
│   └── get_around_delay_analysis.xlsx
│
├── model/                          
│   └── model_final.joblib
│
├── src/                           
│   ├── app.py
│   ├── dashboard.py
│   └── getaround_optuna.py
│
├── getaround_eda.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/<ton-username>/getaround-pricing-project.git
cd getaround-pricing-project
```

### 2. Créer un environnement virtuel

python -m venv getaround-env
source getaround-env/bin/activate

### 3. Installer les dépendances

pip install -r requirements.txt

## 🚀 Utilisation

### 1. Lancer l'application Gradio (interface de prédiction en ligne)

```bash
python src/app.py
```

Une interface web s’ouvrira automatiquement dans ton navigateur.
Tu pourras y renseigner les caractéristiques d’un véhicule pour obtenir une estimation du prix de location journalier.

### 2. Lancer le dashboard interactif (Streamlit)

```bash
streamlit run src/dashboard.py
```

Tu pourras :

    - Visualiser les retards par type de check-in
    - Tester différents seuils de délai minimum entre deux locations
    - Estimer le manque à gagner associé aux retards
    - Obtenir une recommandation automatique de seuil optimal

### 3. Tester l’API localement (FastAPI)

```bash
uvicorn main:app --reload
```

Puis envoie une requête POST à /predict via :

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
        "input": [{
          "model_key": "Citroën",
          "mileage": 150000,
          "engine_power": 60,
          "fuel": "diesel",
          "paint_color": "black",
          "car_type": "sedan",
          "private_parking_available": true,
          "has_gps": false,
          "has_air_conditioning": true,
          "automatic_car": false,
          "has_getaround_connect": true,
          "has_speed_regulator": true,
          "winter_tires": false
        }]
      }'
```

## Déploiement

### 1. Application Gradio sur Hugging Face

L'application Gradio (`src/app.py`) peut être déployée gratuitement sur [Hugging Face Spaces](https://huggingface.co/spaces).

#### Étapes recommandées :
1. Crée un nouveau Space :  
   👉 https://huggingface.co/new-space  
   - **SDK** : `Gradio`
   - **Nom du Space** : `getaround-pricing`
   - Connecte ton repo GitHub si disponible

2. Assure-toi que ces fichiers sont présents dans le repo :
   - `app.py` dans `src/`
   - `model_final.joblib` dans `model/`
   - `requirements.txt` à la racine
   - `README.md` (description du projet)


---

### 2. Déploiement local (API FastAPI)

Si tu préfères tester l'API en local :

```bash
uvicorn main:app --reload
```

## 🤝 Contributing

Ce projet a été réalisé dans un cadre pédagogique et personnel.  
Les contributions ne sont pas ouvertes pour le moment, mais vous pouvez toujours forker le projet ou me contacter pour échanger !

Merci d’avoir pris le temps de le lire ✨




