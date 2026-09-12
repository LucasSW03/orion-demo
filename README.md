# orion-demo

Demo del sitio web de **Orión Aviation Center** (concepto v1, por [Krimisa](https://krimisa.com.ar)).
Online en **https://orion.krimisa.com.ar** vía GitHub Pages.

- `mockup/index.html` — fuente del sitio (formato artifact, sin `<html>`/`<body>`).
- `scripts/build.py` — genera `dist/` con el HTML completo, imágenes, `robots.txt` (noindex) y `CNAME`.
- `.github/workflows/deploy-demo.yml` — cada push a `main` construye y publica.

Este repo es público porque GitHub Pages lo requiere en el plan gratuito. El material comercial (pitch, propuesta, research) vive en el repo privado `Orion_Aviation`.

```bash
python scripts/build.py && python -m http.server 8765 --directory dist
```
