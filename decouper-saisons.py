"""
Script: découpeur de photos de saisons pour scellant-asphalte.ca
- Ouvre saisons-source.jpg
- Découpe en 4 panneaux égaux
- Garde seulement le haut (65%) pour exclure le texte
- Optimise la taille et la qualité
- Sauvegarde les 4 fichiers avec les bons noms
- Met à jour index.html automatiquement
"""

from PIL import Image
import os
import re

# ── Config ─────────────────────────────────────────────────────────────
SOURCE_FILE = "saisons-source.jpg"   # image source (à placer ici)
CROP_TOP_PCT = 0.63                  # garder les 63% supérieurs (pas le texte)
OUTPUT_QUALITY = 85                  # qualité JPEG (1-95)
OUTPUT_WIDTH = 600                   # largeur finale de chaque photo

SAISONS = [
    ("saison-automne.jpg",   "Automne — asphalte mouillé avec fissures"),
    ("saison-hiver.jpg",     "Hiver — asphalte gelé avec glace dans les fissures"),
    ("saison-printemps.jpg", "Printemps — dommages de sel sur asphalte"),
    ("saison-ete.jpg",       "Été — asphalte grisé et oxydé par le soleil"),
]

# ── Traitement des images ───────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(script_dir, SOURCE_FILE)

if not os.path.exists(source_path):
    print(f"❌ Fichier introuvable : {source_path}")
    print(f"   → Place l'image source dans le dossier et nomme-la '{SOURCE_FILE}'")
    input("Appuie sur Entrée pour quitter...")
    exit(1)

print(f"✅ Image source trouvée : {SOURCE_FILE}")
img = Image.open(source_path).convert("RGB")
w, h = img.size
print(f"   Dimensions : {w} x {h} px")

panel_w = w // 4
crop_h  = int(h * CROP_TOP_PCT)

print(f"\n🔪 Découpage en 4 panneaux ({panel_w}px chacun, hauteur conservée : {crop_h}px)...")

for i, (filename, desc) in enumerate(SAISONS):
    left   = i * panel_w
    right  = left + panel_w
    box    = (left, 0, right, crop_h)
    panel  = img.crop(box)

    # Redimensionner proprement
    ratio       = OUTPUT_WIDTH / panel.width
    new_height  = int(panel.height * ratio)
    panel       = panel.resize((OUTPUT_WIDTH, new_height), Image.LANCZOS)

    out_path = os.path.join(script_dir, filename)
    panel.save(out_path, "JPEG", quality=OUTPUT_QUALITY, optimize=True)

    size_kb = os.path.getsize(out_path) // 1024
    print(f"   ✅ {filename}  →  {OUTPUT_WIDTH}x{new_height}px  ({size_kb} KB)")

# ── Mise à jour du HTML ─────────────────────────────────────────────────
html_path = os.path.join(script_dir, "index.html")

if not os.path.exists(html_path):
    print("\n⚠️  index.html introuvable — mise à jour HTML ignorée.")
else:
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    replacements = [
        # Automne
        (
            r'<!-- Remplacez src par votre photo d.*?automne -->[\s\n]*<div class="cycle-photo-placeholder">[\s\n]*<span>🌧.*?</span>[\s\n]*<small>.*?</small>[\s\n]*</div>',
            '<img src="saison-automne.jpg" alt="Asphalte mouillé en automne avec infiltration d\'eau" class="cycle-photo" loading="lazy">'
        ),
        # Hiver
        (
            r'<!-- Remplacez src par votre photo d.*?hiver -->[\s\n]*<div class="cycle-photo-placeholder">[\s\n]*<span>❄️.*?</span>[\s\n]*<small>.*?</small>[\s\n]*</div>',
            '<img src="saison-hiver.jpg" alt="Asphalte gelé en hiver avec glace dans les fissures" class="cycle-photo" loading="lazy">'
        ),
        # Printemps
        (
            r'<!-- Remplacez src par votre photo de.*?poule -->[\s\n]*<div class="cycle-photo-placeholder">[\s\n]*<span>🌡️.*?</span>[\s\n]*<small>.*?</small>[\s\n]*</div>',
            '<img src="saison-printemps.jpg" alt="Dommages de sel sur asphalte au printemps" class="cycle-photo" loading="lazy">'
        ),
        # Été
        (
            r'<!-- Remplacez src par votre photo d.*?été -->[\s\n]*<div class="cycle-photo-placeholder">[\s\n]*<span>☀️.*?</span>[\s\n]*<small>.*?</small>[\s\n]*</div>',
            '<img src="saison-ete.jpg" alt="Asphalte grisé et oxydé par le soleil en été" class="cycle-photo" loading="lazy">'
        ),
    ]

    original = html
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    if html != original:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("\n✅ index.html mis à jour — les placeholders remplacés par les vraies photos !")
    else:
        print("\n⚠️  Aucun placeholder trouvé dans index.html (peut-être déjà mis à jour ?)")

print("\n🎉 Terminé ! Lance ensuite : git add . && git commit -m 'photos saisons' && git push")
input("\nAppuie sur Entrée pour fermer...")
