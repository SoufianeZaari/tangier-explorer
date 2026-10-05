import json
import gradio as gr
import ollama

# 1. Chargement des données
with open("spots.json") as f:
    SPOTS = json.load(f)

# 2. Prompt système (Persona Tanjaoui)
SYSTEM = """Nta guide touristique tanjaoui 9dim, katfhem bzzaf f Tanja w katdwi b Darija tanjawiya drayfa. 
3ti l'user circuit mtiye9, w 9ol lih fin ymchi khatwa b khatwa 3la 7ssab l'we9t w l'vibe li khtar, w sta3mel ghir l'amakin li m3tayin lik."""

def build_route(vibe, duration):
    filtered = [s for s in SPOTS if s["category"] == vibe]

    spots_text = "\n".join(
        f"- {s['name']} ({s['area']}): {s['description']}"
        for s in filtered[:30]
    )
    user_msg = f"Vibe: {vibe}\nDuration: {duration}\nUse ONLY these spots:\n{spots_text}\n\nBuild my walking route!"

    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
        ],
    )
    return response["message"]["content"]

# 3. Le texte Markdown à intégrer
ABOUT_MARKDOWN = """
### 🌍 3lach Open-Source AI? (Theme: Touch Grass)
- **Zero Internet / Edge-Ready:** F zne9at d l'Medina l'9dima wla wst ghabat Perdicaris reseau kaymchi; l'app katb9a khdama 100% offline.
- **Privacy kamla:** Makatseft ta data l chi cloud server dyal chirakat kbar; kolchi kay-runni f laptop dyalek.
- **Zero Cost:** Bla flous l'abonnement wla credit d l'API; open-weight models b7al Gemma 3 kaykhelliw ay wa7ed ybni des solutions wa3rin.
- **Touch Grass:** L'hadaf machi tb9a lasseq f l'ecran, walakin l'AI ykhetet lik f thwani bach tsed l'pc w tkhrej tmecha f l'hwa d Tanja.

---
**Tech Stack:** Google Gemma 3 (4B) via Ollama | Gradio | 148 spots locaux f `spots.json`
"""

# 4. Interface Gradio b Blocks (bach tzid fiha l'Markdown)
with gr.Blocks(title="Tangier Explorer 🧭") as demo:
    gr.Markdown("# Tangier Explorer 🧭")
    gr.Markdown("**Guide offline l Tanja — khtar vibe w sir tmecha!**")
    
    with gr.Row():
        vibe_input = gr.Dropdown(
            choices=["history", "food", "hidden", "sea", "nature", "culture"],
            label="Vibe dyal l'khrouj",
            value="history"
        )
        duration_input = gr.Radio(
            choices=["1h", "2h", "half-day"],
            label="Ch7al mn w9t 3ndek?",
            value="1h"
        )
    
    btn = gr.Button("🧭 Generi l'Itinéraire", variant="primary")
    output = gr.Textbox(label="🗺️️ Route dyalek", lines=10)
    
    btn.click(fn=build_route, inputs=[vibe_input, duration_input], outputs=output)
    
    gr.Markdown(ABOUT_MARKDOWN)

if __name__ == "__main__":
    demo.launch()