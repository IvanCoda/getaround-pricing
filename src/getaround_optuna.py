import pandas as pd
import joblib
import optuna
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

# === Données & preprocessing ===

df = pd.read_csv("get_around_pricing_project.csv").drop(columns=["Unnamed: 0"])
X = df.drop(columns=["rental_price_per_day"])
y = df["rental_price_per_day"]

categorical_features = ["model_key", "fuel", "paint_color", "car_type"]
preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)],
    remainder="passthrough"
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# === Optuna Objective ===

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 20),
        "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.3),
        "subsample": trial.suggest_float("subsample", 0.1, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.1, 1.0),
        "random_state": 42
    }

    model = Pipeline([
        ("preprocessing", preprocessor),
        ("regressor", XGBRegressor(**params))
    ])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return mean_absolute_error(y_test, y_pred)


# === Lancer l’optimisation Optuna ===

def run_optuna(n_trials=500):
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    return study.best_params, study.best_value


# === Logging MLflow ===

def log_with_mlflow(model, params, mae, r2):
    with mlflow.start_run(run_name="XGB - Optuna"):
        mlflow.log_params(params)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R2", r2)
        mlflow.sklearn.log_model(model, artifact_path="xgb_optuna_model")


# === Script principal ===

if __name__ == "__main__":
    print("🚀 Lancement de l’optimisation avec Optuna...")
    best_params, best_mae = run_optuna(n_trials=500)

    print("\n🎯 Meilleurs hyperparamètres trouvés :")
    for k, v in best_params.items():
        print(f"  {k} = {v}")

    print(f"\n✅ Meilleur MAE trouvé pendant l'optimisation : {best_mae:.2f}")

    # Entraînement final avec les meilleurs paramètres
    final_model = Pipeline([
        ("preprocessing", preprocessor),
        ("regressor", XGBRegressor(**best_params))
    ])
    final_model.fit(X_train, y_train)
    y_pred = final_model.predict(X_test)

    final_mae = mean_absolute_error(y_test, y_pred)
    final_r2 = r2_score(y_test, y_pred)

    print(f"\n📊 Performances finales sur le test set :")
    print(f"MAE : {final_mae:.2f}")
    print(f"R²  : {final_r2:.2f}")

    # Sauvegarde
    joblib.dump(final_model, "model_final.joblib")
    print("\n💾 Modèle final sauvegardé sous 'model_final.joblib'")

    # Log MLflow
    log_with_mlflow(final_model, best_params, final_mae, final_r2)
    print("📦 Modèle loggé dans MLflow")
