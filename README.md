# docs101

La documentación técnica de la suite 101, escrita para leerse sin ser
programador: mapas, decisiones y medidas. Se publica sola en
https://docs101.pages.dev con cada commit a `main`.

## Cómo se agrega una página

1. Un archivo `paginas/AAAA-MM-DD-slug.html` con el cuerpo de la página:
   empieza con `<title>` (el nombre de la página), sigue su `<style>` y luego
   el contenido. Sin `<html>`, `<head>` ni `<body>`: `armar.py` los pone.
2. El primer `<p class="lede">` es el resumen que aparece en la portada.
3. `python3 armar.py --probar` comprueba; `python3 armar.py` escribe `dist/`.

Cada página vive en `https://docs101.pages.dev/<slug>/`. La portada lista las
páginas de la más nueva a la más vieja.

## Secretos del repositorio (los pone Mike)

`CLOUDFLARE_API_TOKEN` (permiso Pages:Edit) y `CLOUDFLARE_ACCOUNT_ID`, los
mismos que wall101. Sin ellos el flujo se detiene en «Publicar».
