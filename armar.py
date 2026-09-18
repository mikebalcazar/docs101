#!/usr/bin/env python3
"""Arma docs101: lee paginas/*.html y escribe dist/.

Cada página es un archivo paginas/AAAA-MM-DD-slug.html con el cuerpo de la
página tal cual (sin <html>, <head> ni <body>): empieza con <title>…</title>,
sigue con su <style> y luego el contenido. Este script la envuelve en el
documento completo con la barra de docs101, y arma la portada con una
tarjeta por página (título, fecha y su primer párrafo con clase «lede»).

    python3 armar.py          → dist/index.html y dist/<slug>/index.html
    python3 armar.py --probar → sólo comprueba, sin escribir

Una página sin <title> o sin párrafo «lede» detiene el armado: la portada
necesita las dos cosas para decir de qué trata.
"""
import html, re, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PAGINAS, DIST, IMG = RAIZ / "paginas", RAIZ / "dist", RAIZ / "img"
NOMBRE = "docs101"
FORMA = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9-]+)\.html$")
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def leer(p: Path):
    m = FORMA.match(p.name)
    if not m:
        sys.exit(f"{p.name}: el nombre debe ser AAAA-MM-DD-slug.html")
    cuerpo = p.read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", cuerpo, re.S)
    lede = re.search(r'<p class="lede">(.*?)</p>', cuerpo, re.S)
    if not t or not t.group(1).strip():
        sys.exit(f"{p.name}: falta <title>")
    if not lede:
        sys.exit(f'{p.name}: falta el párrafo <p class="lede"> con el resumen')
    aa, mm, dd, slug = m.groups()
    return {
        "slug": slug,
        "clave": f"{aa}{mm}{dd}",
        "fecha": f"{int(dd)}-{MESES[int(mm) - 1]}-{aa}",
        "titulo": html.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip(),
        "resumen": html.unescape(re.sub(r"<[^>]+>", "", lede.group(1))).strip(),
        "cuerpo": re.sub(r"<title>.*?</title>\s*", "", cuerpo, count=1, flags=re.S),
    }


BARRA_CSS = """
<style>
.d101-barra{font-family:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif;font-size:14px;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:12px 20px;border-bottom:1px solid rgba(127,140,151,.35)}
.d101-barra a{color:inherit;text-decoration:none;font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:12px}
.d101-barra a:hover{text-decoration:underline}
.d101-barra .que{opacity:.7;font-size:13px}
</style>"""

BARRA = f"""<nav class="d101-barra"><a href="/">{NOMBRE}</a><span class="que">documentación técnica de la suite 101</span></nav>"""


def envolver(titulo: str, contenido: str, descripcion: str = "") -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{html.escape(descripcion)}">
<title>{html.escape(titulo)} · {NOMBRE}</title>
{BARRA_CSS}
</head>
<body style="margin:0">
{BARRA}
{contenido}
</body>
</html>
"""


PORTADA_CSS = """
<style>
:root{--fondo:#F3F6F8;--sup:#FFFFFF;--linea:#D5DDE3;--tinta:#152028;--tinta-2:#4B5A66;--tinta-3:#7F8C97;--marca:#0080C1;--marca-oscuro:#0B1A24}
@media (prefers-color-scheme: dark){:root{--fondo:#0F171D;--sup:#172229;--linea:#2C3B46;--tinta:#EEF3F6;--tinta-2:#B3C0CA;--tinta-3:#7F919E;--marca:#3AA3DC;--marca-oscuro:#EEF3F6}}
body{background:var(--fondo);color:var(--tinta);font-family:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif;font-size:16px;line-height:1.55}
.pag{max-width:900px;margin:0 auto;padding:40px 20px 64px}
.eyebrow{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--tinta-3);font-weight:600;margin:0 0 10px}
h1{font-family:"Familjen Grotesk","IBM Plex Sans",sans-serif;font-size:clamp(30px,5vw,44px);line-height:1.08;margin:0 0 12px;color:var(--marca-oscuro)}
p.lede{font-size:18px;color:var(--tinta-2);max-width:62ch;margin:0 0 30px}
.lista{display:grid;gap:14px}
.tarjeta{display:block;background:var(--sup);border:1px solid var(--linea);border-left:4px solid var(--marca);border-radius:10px;padding:16px 18px;color:inherit;text-decoration:none}
.tarjeta:hover{border-color:var(--marca)}
.tarjeta .fecha{font-size:12.5px;color:var(--tinta-3);letter-spacing:.04em}
.tarjeta h2{font-family:"Familjen Grotesk","IBM Plex Sans",sans-serif;font-size:22px;margin:4px 0 6px}
.tarjeta p{margin:0;color:var(--tinta-2);font-size:15px;max-width:70ch}
.pie{margin-top:40px;font-size:13px;color:var(--tinta-3)}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">"""


def tarjeta(x) -> str:
    return f"""<a class="tarjeta" href="/{x['slug']}/">
<div class="fecha">{x['fecha']}</div>
<h2>{html.escape(x['titulo'])}</h2>
<p>{html.escape(x['resumen'])}</p>
</a>"""


def armar(solo_probar: bool = False) -> int:
    paginas = sorted((leer(p) for p in PAGINAS.glob("*.html")), key=lambda x: x["clave"], reverse=True)
    if not paginas:
        sys.exit("no hay páginas en paginas/")
    vistos = set()
    for x in paginas:
        if x["slug"] in vistos:
            sys.exit(f"dos páginas con el mismo slug: {x['slug']}")
        vistos.add(x["slug"])
    if solo_probar:
        print(f"ok: {len(paginas)} páginas con título y resumen")
        return len(paginas)
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    if IMG.exists():
        shutil.copytree(IMG, DIST / "img")
    for x in paginas:
        d = DIST / x["slug"]
        d.mkdir()
        (d / "index.html").write_text(envolver(x["titulo"], x["cuerpo"], x["resumen"]), encoding="utf-8")
    portada = f"""{PORTADA_CSS}
<div class="pag">
<p class="eyebrow">Suite 101 · documentación técnica</p>
<h1>Cómo está hecha la suite 101</h1>
<p class="lede">Mapas, decisiones y medidas de la plataforma, escritas para leerse sin ser programador. Cada página sale del código desplegado, no de un plan.</p>
<div class="lista">
{chr(10).join(tarjeta(x) for x in paginas)}
</div>
<div class="pie">{len(paginas)} {'página' if len(paginas) == 1 else 'páginas'} · se arma solo con cada commit a main</div>
</div>"""
    (DIST / "index.html").write_text(envolver("Documentación técnica", portada, "Cómo está hecha la suite 101"), encoding="utf-8")
    print(f"dist/: {len(paginas)} páginas")
    return len(paginas)


if __name__ == "__main__":
    armar(solo_probar="--probar" in sys.argv)
