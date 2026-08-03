from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "evento-08-09-marca-valor.html",
    ROOT / "docs/hubspot-implementation/entrega-final-plano-a/developer-files/evento-marca-valor.html",
    ROOT / "docs/hubspot-implementation/entrega-final-plano-a/developer-files/evento-marca-valor.js",
]
REPORT = ROOT / "docs/hubspot-implementation/entrega-final-plano-a/RELATORIO-EVENTO-08-09-MARCA-VALOR.md"

REPLACEMENTS = [
    # URLs sociais: a imagem continua no diretório raiz do GitHub Pages.
    (
        "https://ffidelis16.github.io/next-sessions-lp/evento-08-09-marca-valor.htmlog-eventos-nuvemshop-next.jpg",
        "https://ffidelis16.github.io/next-sessions-lp/og-eventos-nuvemshop-next.jpg",
    ),
    # Tese: os cards são sinais, não modelos de negócio.
    (">Modelo 01<", ">Sinal 01<"),
    (">Modelo 02<", ">Sinal 02<"),
    (">Modelo 03<", ">Sinal 03<"),
    # Cards de speakers. Imagens permanecem provisórias nesta versão.
    ("alt=\"Gutto Paixão, fundadora da PWRD by Coffee\"", "alt=\"Imagem provisória do card de Gutto Paixão\""),
    ("alt=\"Caroline Domingues, Nuvemshop\"", "alt=\"Imagem provisória do card de Caroline Domingues\""),
    ("alt=\"Katharina Neves, Mica Chocolates\"", "alt=\"Imagem provisória do card de Katharina Neves\""),
    ("alt=\"Ângela Coelho da Fonseca, Nuvemshop\"", "alt=\"Imagem provisória do card de Ângela Coelho da Fonseca\""),
    (">Katharina Neves</div><div class=\"spk__role\">Mica Chocolates<",
     ">Katharina Neves</div><div class=\"spk__role\">Coordenadora de Canais Digitais · Mica Chocolates<"),
    (">Ângela Coelho da Fonseca</div><div class=\"spk__role\">Nuvemshop<",
     ">Ângela Coelho da Fonseca</div><div class=\"spk__role\">CEO e Diretora Criativa · Jogê<"),
    # Programação: corrige cascatas causadas por substituições globais.
    ("<div class=\"tl__who\">Ângela Coelho da Fonseca · Nuvemshop</div>",
     "<div class=\"tl__who\">Caroline Domingues · Nuvemshop</div>"),
    (
        "Gutto Paixão abre os bastidores da PWRD by Coffee: as decisões que permitiram rodar Como transformar diferenciação em valor percebido em paralelo, e o que cada uma custou antes de dar certo.",
        "Produto, comunicação e experiência precisam contar a mesma história. Gutto Paixão apresenta os sinais que ajudam uma marca a justificar sua proposta, fortalecer a percepção de valor e reduzir a dependência de desconto.",
    ),
    ("<div class=\"tl__who\">Gutto Paixão · PWRD by Coffee</div>",
     "<div class=\"tl__who\">Gutto Paixão · Weethub</div>"),
    (
        "Caroline Domingues (Nuvemshop) + Katharina Neves (Mica Chocolates) · Mediação: Ângela Coelho da Fonseca",
        "Caroline Domingues + Katharina Neves · Mica Chocolates + Ângela Coelho da Fonseca · Jogê",
    ),
    (
        "Fechamento da conversa e principais critérios para comparar assinatura, Comunicação e identidade e exportação no seu contexto.",
        "Fechamento da conversa e síntese dos critérios que ajudam a tornar o valor mais claro e a margem menos dependente de desconto.",
    ),
    # Takeaway corrompido pela substituição de termos globais.
    (
        "Como avaliar se assinatura, Comunicação e identidade ou exportação faz sentido para o seu estágio atual.",
        "Identificar onde sua marca perde valor percebido.",
    ),
    # Assets visuais mantidos da edição anterior: alt descreve o arquivo real e sinaliza provisoriedade.
    ("src=\"logo-pwrd.png\" alt=\"PWRD by Coffee\"", "src=\"logo-pwrd.png\" alt=\"PWRD by Coffee — imagem provisória\""),
    ("src=\"logo-suamesa.png\" alt=\"Nuvemshop\"", "src=\"logo-suamesa.png\" alt=\"Sua Mesa Suas Vontades — imagem provisória\""),
    ("src=\"logo-housewhey.png\" alt=\"Mica Chocolates\"", "src=\"logo-housewhey.png\" alt=\"Housewhey — imagem provisória\""),
    # FAQ e linguagem matutina.
    ("Quero participar garante meu lugar?", "Enviar meus dados garante meu lugar?"),
    ("Não. A noite é de conteúdo prático e troca entre pares.", "Não. A manhã é de conteúdo prático e troca entre pares."),
    # Valor estático antes da hidratação do JavaScript.
    ("data-seats-total>60</span>", "data-seats-total>70</span>"),
]


def fix_text(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS:
        hits = text.count(old)
        if hits:
            text = text.replace(old, new)
            count += hits

    # Configuração provisória de ocupação para 70 cadeiras.
    text = text.replace("Antes de D-45 a página permanece em 60", "Antes de D-35 a página permanece em 70")
    text = text.replace("EVENT_DAY:new Date('2026-08-26T00:00:00-03:00')", "EVENT_DAY:new Date('2026-09-08T00:00:00-03:00')")
    text = re.sub(
        r"SCHEDULE:\[\[[^\n]+?\]\],\n\s*FORCE_STATE",
        "SCHEDULE:[[35,48],[30,43],[25,37],[20,31],[15,24],[12,19],[10,15],[7,10],[5,7],[3,4],[1,2]],\n  FORCE_STATE",
        text,
    )
    return text, count


def main() -> None:
    total = 0
    for path in FILES:
        if not path.exists():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        text, count = fix_text(text)
        path.write_text(text, encoding="utf-8")
        total += count

    report = REPORT.read_text(encoding="utf-8") if REPORT.exists() else "# Relatório da edição 08/09\n"
    report += (
        "\n## Correções de QA aplicadas\n\n"
        f"- {total} correções editoriais pontuais aplicadas após a geração.\n"
        "- Open Graph e Twitter Image corrigidos para reutilizar o asset raiz.\n"
        "- Programação reconciliada com Caroline Domingues, Gutto Paixão, Katharina Neves e Ângela Coelho da Fonseca.\n"
        "- Curva técnica provisória adaptada para 70 cadeiras e evento em 08/09.\n"
        "- Imagens e logos da edição anterior permanecem explicitamente provisórios.\n"
    )
    REPORT.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
