from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "evento-08-09-marca-valor.html",
    ROOT / "docs/hubspot-implementation/entrega-final-plano-a/developer-files/evento-marca-valor.html",
]

PAIRS = [
    (
        "Evento presencial e reservado. <span data-seats-total>70</span> lugares.",
        "Encontro presencial e gratuito. <span data-seats-total>70</span> lugares. Participação confirmada por e-mail.",
    ),
    (
        "<span data-seats-total>70</span> lugares para founders e líderes de e-commerce com operação rodando, avaliando novas frentes de receita.",
        "<span data-seats-total>70</span> lugares para lideranças de marcas em crescimento que querem sustentar margem, fortalecer diferenciação e reduzir a dependência de desconto.",
    ),
]

for path in FILES:
    text = path.read_text(encoding="utf-8")
    for old, new in PAIRS:
        if old not in text:
            raise RuntimeError(f"Trecho não encontrado em {path}: {old}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
