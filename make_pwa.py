# -*- coding: utf-8 -*-
"""Build pwa/index.html from the single-file HTML app and inject PWA tags."""
from pathlib import Path

base = Path(__file__).resolve().parent
src = (base.parent / "html" / "明理ClearLogic.html").read_text(encoding="utf-8")

head = """
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="明理">
<meta name="mobile-web-app-capable" content="yes">
<style>
@media (display-mode: standalone){
  .sidebar{padding-top:calc(26px + env(safe-area-inset-top))}
  .topbar{padding-top:calc(18px + env(safe-area-inset-top))}
}
</style>
"""

registration = """
<script>
if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  });
}
</script>
"""

out = src.replace("</head>", head + "</head>", 1).replace("</body>", registration + "</body>", 1)
(base / "index.html").write_text(out, encoding="utf-8", newline="\n")
print(f"wrote {base / 'index.html'} ({(base / 'index.html').stat().st_size} bytes)")
