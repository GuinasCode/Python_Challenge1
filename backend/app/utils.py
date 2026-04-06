import base64
import html

status = ["Pendente", "Em preparo", "Pronto", "Entregue"]

STATUS_COLORS = {
    "Pendente": {"color": "#DC2626", "background": "#FEE2E2"},
    "Em preparo": {"color": "#D97706", "background": "#FEF3C7"},
    "Pronto": {"color": "#16A34A", "background": "#DCFCE7"},
    "Entregue": {"color": "#6B7280", "background": "#F3F4F6"},
}

CATEGORY_PRESETS = {
    "Pratos executivos": {"order": 1, "background": "#F59E0B", "foreground": "#FFF7ED"},
    "Bebidas": {"order": 2, "background": "#2563EB", "foreground": "#EFF6FF"},
    "Sobremesas": {"order": 3, "background": "#DB2777", "foreground": "#FDF2F8"},
    "Sem categoria": {"order": 99, "background": "#475569", "foreground": "#F8FAFC"},
}


def category_order(name: str) -> int:
    return CATEGORY_PRESETS.get(name, CATEGORY_PRESETS["Sem categoria"])["order"]


def guess_category_name(item_name: str) -> str:
    normalized = item_name.lower()

    if any(keyword in normalized for keyword in ["coca", "suco", "água", "agua", "refrigerante", "chá", "cha", "café", "cafe"]):
        return "Bebidas"
    if any(keyword in normalized for keyword in ["mousse", "petit", "sorvete", "doce", "pudim", "bolo"]):
        return "Sobremesas"
    return "Pratos executivos"


def _initials(label: str) -> str:
    parts = [part for part in label.replace("-", " ").split() if part]
    if not parts:
        return "RD"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[1][0]}".upper()


def build_placeholder_image(label: str, category_name: str | None = None) -> str:
    category_name = category_name or "Sem categoria"
    preset = CATEGORY_PRESETS.get(category_name, CATEGORY_PRESETS["Sem categoria"])
    initials = html.escape(_initials(label))
    safe_label = html.escape(label)
    safe_category = html.escape(category_name)
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="320" height="220" viewBox="0 0 320 220">
      <defs>
        <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="{preset["background"]}"/>
          <stop offset="100%" stop-color="#111827"/>
        </linearGradient>
      </defs>
      <rect width="320" height="220" rx="24" fill="url(#bg)"/>
      <circle cx="74" cy="74" r="42" fill="rgba(255,255,255,0.16)"/>
      <text x="74" y="86" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="white">{initials}</text>
      <text x="28" y="154" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="white">{safe_label}</text>
      <text x="28" y="184" font-family="Arial, sans-serif" font-size="14" fill="{preset["foreground"]}">{safe_category}</text>
    </svg>
    '''.strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"
