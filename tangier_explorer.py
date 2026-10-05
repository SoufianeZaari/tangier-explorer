import json
import gradio as gr
import ollama

# 1. Load spots
with open("spots.json") as f:
    SPOTS = json.load(f)

# System prompt dyal l'guide Tanjaoui
SYSTEM = """Nta guide touristique tanjaoui 9dim, katfhem bzzaf f Tanja w katdwi b Darija tanjawiya drayfa. 
3ti l'user circuit mtiye9, w 9ol lih fin ymchi khatwa b khatwa 3la 7ssab l'we9t w l'vibe li khtar, w sta3mel ghir l'amakin li m3tayin lik."""

def build_route(vibe, duration):
    # Filter spots b vibe
    filtered = [s for s in SPOTS if s["category"] == vibe]

    # Build spots text
    spots_text = "\n".join(
        f"- {s['name']} ({s['area']}): {s['description']}"
        for s in filtered[:30]
    )
    user_msg = f"Vibe: {vibe}\nDuration: {duration}\nUse ONLY these spots:\n{spots_text}\n\nBuild my walking route!"

    # Call Ollama
    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
        ],
    )
    return response["message"]["content"]

# Gradio Interface
demo = gr.Interface(
    fn=build_route,
    inputs=[
        gr.Dropdown(
            choices=["history", "food", "hidden", "sea", "nature", "culture"],
            label="Vibe dyal l'khrouj",
        ),
        gr.Radio(
            choices=["1h", "2h", "half-day"],
            label="Ch7al mn w9t 3ndek?",
        ),
    ],
    outputs=gr.Textbox(label="🗺️ Route dyalek"),
    title="Tangier Explorer 🧭",
    description="Guide offline l Tanja — khtar vibe w sir tmecha!",
)

demo.launch()