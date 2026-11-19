"""Rendert die Bildwelt (tools/art/art.html) nach assets/img als WebP in zwei Breiten (Responsive Images) plus JPEG-Fallback.
Aufruf: python3 tools/art/render.py   (benötigt Playwright/Chromium und Pillow)"""
import asyncio, pathlib, io
from PIL import Image
from playwright.async_api import async_playwright
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE.parent.parent / "assets" / "img"
# Name, Motiv, Thema, Breite, Höhe, Seed, Ausgabebreiten
JOBS = [("hero-light", "hero-light", "light", 1600, 1100, 4, (800, 1600)), ("tech-dark", "hero-dark", "dark", 1600, 1100, 3, (800, 1600))]
for name, k, s in (("card-erp", "curve", 2), ("card-s4", "towers", 5), ("card-dyn", "towers", 9), ("card-ora", "towers", 13), ("card-cut", "streaks", 4), ("card-ki", "wave", 6)):
    for t in ("light", "dark"): JOBS.append((f"{name}-{t}", k, t, 840, 480, s, (420, 840)))
JOBS.append(("band-dark", "streaks", "dark", 1400, 900, 8, (700, 1400)))

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for name, k, t, w, h, s, widths in JOBS:
            await pg.set_viewport_size({"width": w, "height": h})
            await pg.goto(f"file://{HERE}/art.html?k={k}&t={t}&w={w}&h={h}&s={s}"); await pg.wait_for_function("document.title==='done'")
            im = Image.open(io.BytesIO(await pg.screenshot())).convert("RGB")
            for ww in widths:
                r = im.resize((ww, round(h * ww / w)), Image.LANCZOS)
                r.save(OUT / f"{name}-{ww}.webp", "WEBP", quality=80, method=6)
            im.resize((widths[-1], round(h * widths[-1] / w)), Image.LANCZOS).save(OUT / f"{name}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
        await b.close()
    print(len(JOBS), "Motive gerendert nach", OUT)

asyncio.run(main())
