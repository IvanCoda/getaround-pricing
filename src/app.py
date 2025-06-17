import gradio as gr
import pandas as pd
import joblib

# === Charger modèle et données ===
model = joblib.load("model_final.joblib")
df = pd.read_csv("../data/get_around_pricing_project.csv").drop(columns=["Unnamed: 0"])

# Options dynamiques
model_keys = sorted(df["model_key"].dropna().unique().tolist())
paint_colors = sorted(df["paint_color"].dropna().unique().tolist())

# === Fonction de prédiction ===
def predict_price(
    model_key, mileage, engine_power, fuel, paint_color, car_type,
    private_parking_available, has_gps, has_air_conditioning,
    automatic_car, has_getaround_connect, has_speed_regulator, winter_tires
):
    input_dict = {
        "model_key": model_key,
        "mileage": mileage,
        "engine_power": engine_power,
        "fuel": fuel,
        "paint_color": paint_color,
        "car_type": car_type,
        "private_parking_available": private_parking_available,
        "has_gps": has_gps,
        "has_air_conditioning": has_air_conditioning,
        "automatic_car": automatic_car,
        "has_getaround_connect": has_getaround_connect,
        "has_speed_regulator": has_speed_regulator,
        "winter_tires": winter_tires
    }
    df_input = pd.DataFrame([input_dict])
    prediction = model.predict(df_input)[0]
    return round(prediction, 2)

# === Interface Gradio ===
iface = gr.Interface(
    fn=predict_price,
    inputs=[
        gr.Dropdown(choices=model_keys, label="Model Key"),
        gr.Number(label="Mileage"),
        gr.Number(label="Engine Power"),
        gr.Radio(["diesel", "petrol", "hybrid", "electric"], label="Fuel"),
        gr.Dropdown(choices=paint_colors, label="Paint Color"),
        gr.Radio(["sedan", "convertible", "coupe", "suv", "van"], label="Car Type"),
        gr.Checkbox(label="Private Parking Available"),
        gr.Checkbox(label="Has GPS"),
        gr.Checkbox(label="Has Air Conditioning"),
        gr.Checkbox(label="Automatic Car"),
        gr.Checkbox(label="Has Getaround Connect"),
        gr.Checkbox(label="Has Speed Regulator"),
        gr.Checkbox(label="Winter Tires"),
    ],
    outputs="number",
    title="🚗 Getaround - Price Predictor",
    description="Entrez les caractéristiques de votre voiture pour estimer le prix de location journalier (€)."
)

# === Lancer l'app ===
if __name__ == "__main__":
    iface.launch()
