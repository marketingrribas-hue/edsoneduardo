import sys, glob, os
from PIL import Image
dias = sys.argv[1:]
W = 360; H = 450
rows = []
for d in dias:
    fs = [f"out/dia_{int(d):02d}/dia{int(d):02d}_carrossel_{i}.png" for i in range(1,6)] + [f"out/dia_{int(d):02d}/dia{int(d):02d}_card.png"]
    rows.append(fs)
sheet = Image.new("RGB", (W*6 + 50, (H+10)*len(rows)), (60,60,60))
for r, fs in enumerate(rows):
    for c, f in enumerate(fs):
        im = Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)
        sheet.paste(im, (c*W + (50 if c == 5 else 0), r*(H+10)))
os.makedirs("previews", exist_ok=True)
name = f"previews/dias_{dias[0]}-{dias[-1]}.jpg"
sheet.save(name, quality=85); print(name)
