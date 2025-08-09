import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


DEFAULT_CJK_CANDIDATES = [
    "/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf",
    "/usr/share/fonts/truetype/arphic-gkai00mp/gkai00mp.ttf",
    "C:\\Windows\\Fonts\\msyh.ttc",
    "C:\\Windows\\Fonts\\simsun.ttc",
]


def register_cjk_font(
    candidates=None,
    registered_name="CJKCodeFont",
    fallback="Courier"
):
    candidates = candidates or DEFAULT_CJK_CANDIDATES
    for p in candidates:
        if not os.path.exists(p):
            continue
        try:
            if p.lower().endswith(".ttc"):
                try:
                    pdfmetrics.registerFont(
                        TTFont(registered_name, p, subfontIndex=0)
                    )
                except TypeError:
                    pdfmetrics.registerFont(TTFont(registered_name, p))
            else:
                pdfmetrics.registerFont(TTFont(registered_name, p))
            print(f"Registered {registered_name} font from {p}")
            return registered_name
        except (TypeError, OSError, ValueError):
            continue
    return fallback
