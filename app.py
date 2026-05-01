from src.ds_e2e_project.pipeline.prediction_pipeline import PredictionPipeline
import gradio as gr
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────
#  Model
# ─────────────────────────────────────────────

MODEL = PredictionPipeline()

FEATURE_COLUMNS = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",          # matches your YAML exactly
    "sulphates",
    "alcohol",
]

def predict_quality(
    fixed_acidity,
    volatile_acidity,
    citric_acid,
    residual_sugar,
    chlorides,
    free_sulfur_dioxide,
    total_sulfur_dioxide,
    density,
    ph,
    sulphates,
    alcohol,
):
    input_df = pd.DataFrame(
        [[
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
            chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
            density, ph, sulphates, alcohol,
        ]],
        columns=FEATURE_COLUMNS,
    )

    score = float(MODEL.predict(input_df)[0])

    score = round(score, 2)

    # ── Human-readable label ─────────────────────────────
    if score >= 7:
        label = "🍷 Excellent"
        color = "#2ecc71"
    elif score >= 5:
        label = "🥂 Good"
        color = "#f39c12"
    else:
        label = "😕 Below Average"
        color = "#e74c3c"

    summary = (
        f"### Predicted Quality Score: **{score} / 10**\n\n"
        f"**Rating:** {label}\n\n"
        f"> *Score range: 3 (worst) → 9 (best)*"
    )
    return summary


# ─────────────────────────────────────────────
#  UI layout
# ─────────────────────────────────────────────
with gr.Blocks(
    title="Wine Quality Predictor",
    theme=gr.themes.Soft(primary_hue="red", secondary_hue="orange"),
    css="""
        .title { text-align: center; font-size: 2rem; margin-bottom: 0.2rem; }
        .subtitle { text-align: center; color: #888; margin-bottom: 1.5rem; }
        .predict-btn { background: #8B0000 !important; }
    """,
) as demo:

    gr.Markdown("# 🍷 Wine Quality Predictor", elem_classes="title")
    gr.Markdown(
        "Fill in the physicochemical properties of your wine and get an instant quality prediction.",
        elem_classes="subtitle",
    )

    with gr.Row():
        # ── Column 1: Acidity & Sugar ───────────────────
        with gr.Column():
            gr.Markdown("### 🧪 Acidity & Sugar")
            fixed_acidity = gr.Slider(
                4.0, 16.0, value=7.4, step=0.1,
                label="Fixed Acidity (g/dm³)",
                info="Tartaric acid concentration",
            )
            volatile_acidity = gr.Slider(
                0.1, 1.6, value=0.5, step=0.01,
                label="Volatile Acidity (g/dm³)",
                info="Acetic acid – high levels give vinegar taste",
            )
            citric_acid = gr.Slider(
                0.0, 1.0, value=0.3, step=0.01,
                label="Citric Acid (g/dm³)",
                info="Adds freshness and flavour",
            )
            residual_sugar = gr.Slider(
                0.9, 15.5, value=2.5, step=0.1,
                label="Residual Sugar (g/dm³)",
                info="Sugar remaining after fermentation",
            )

        # ── Column 2: Minerals & Additives ─────────────
        with gr.Column():
            gr.Markdown("### ⚗️ Minerals & Additives")
            chlorides = gr.Slider(
                0.01, 0.2, value=0.08, step=0.001,
                label="Chlorides (g/dm³)",
                info="Salt content",
            )
            free_sulfur_dioxide = gr.Slider(
                1.0, 72.0, value=15.0, step=1.0,
                label="Free SO₂ (mg/dm³)",
                info="Prevents microbial growth & oxidation",
            )
            total_sulfur_dioxide = gr.Slider(
                6.0, 290.0, value=46.0, step=1.0,
                label="Total SO₂ (mg/dm³)",
                info="Total sulphur dioxide",
            )
            sulphates = gr.Slider(
                0.3, 2.0, value=0.6, step=0.01,
                label="Sulphates (g/dm³)",
                info="Wine stabiliser",
            )

        # ── Column 3: Physical Properties ──────────────
        with gr.Column():
            gr.Markdown("### 🔬 Physical Properties")
            density = gr.Slider(
                0.990, 1.004, value=0.996, step=0.0001,
                label="Density (g/cm³)",
                info="Depends on alcohol & sugar content",
            )
            ph = gr.Slider(
                2.7, 4.0, value=3.3, step=0.01,
                label="pH",
                info="Acidity scale (lower = more acidic)",
            )
            alcohol = gr.Slider(
                8.0, 15.0, value=10.5, step=0.1,
                label="Alcohol (% vol)",
                info="Percentage of alcohol by volume",
            )

    with gr.Row():
        predict_btn = gr.Button(
            "🍷  Predict Quality", variant="primary", scale=1, elem_classes="predict-btn"
        )

    output = gr.Markdown(label="Prediction")

    predict_btn.click(
        fn=predict_quality,
        inputs=[
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
            chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
            density, ph, sulphates, alcohol,
        ],
        outputs=output,
    )

    gr.Examples(
        examples=[
            [7.4, 0.70, 0.00, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4],
            [6.3, 0.30, 0.34, 1.6, 0.049, 14, 132, 0.9940, 3.30, 0.49, 9.5],
            [8.1, 0.28, 0.40, 6.9, 0.050, 30, 97,  0.9951, 3.26, 0.44, 10.1],
        ],
        inputs=[
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
            chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
            density, ph, sulphates, alcohol,
        ],
        label="📋 Example Wines",
    )

if __name__ == "__main__":
    demo.launch()