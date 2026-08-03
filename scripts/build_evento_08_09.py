from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "docs/hubspot-implementation/entrega-final-plano-a/developer-files"
OUT_HTML = ROOT / "evento-08-09-marca-valor.html"
OUT_DEV_HTML = DEV / "evento-marca-valor.html"
OUT_DEV_CSS = DEV / "evento-marca-valor.css"
OUT_DEV_JS = DEV / "evento-marca-valor.js"
REPORT = ROOT / "docs/hubspot-implementation/entrega-final-plano-a/RELATORIO-EVENTO-08-09-MARCA-VALOR.md"

SOURCE_PREVIEW = ROOT / "index.html"
SOURCE_HTML = DEV / "evento-modelos-negocio.html"
SOURCE_CSS = DEV / "evento-modelos-negocio.css"
SOURCE_JS = DEV / "evento-modelos-negocio.js"

FORM_ID_PLACEHOLDER = "09082026-0000-4000-8000-000000000001"
EVENT_URL = "https://ffidelis16.github.io/next-sessions-lp/evento-08-09-marca-valor.html"

# Substituições editoriais canônicas. As imagens permanecem as mesmas nesta fase,
# conforme decisão do projeto; fotos e logos de pessoas/marcas são provisórios.
REPLACEMENTS: list[tuple[str, str]] = [
    ("Evento presencial Nuvemshop Next · 26/08", "Encontro presencial Nuvemshop Next · 08/09"),
    ("Evento presencial Nuvemshop Next Â· 26/08", "Encontro presencial Nuvemshop Next · 08/09"),
    ("Evento presencial · 26/08", "Encontro presencial · 08/09"),
    ("Evento presencial · 26 de agosto", "Encontro presencial · 8 de setembro"),
    ("26 de agosto, quarta", "8 de setembro, terça"),
    ("26 de agosto", "8 de setembro"),
    ("26/08", "08/09"),
    ("18h30 às 22h", "8h30 às 12h30"),
    ("18h30 - 19h", "8h30 - 9h"),
    ("18h30", "8h30"),
    ("19h00", "9h"),
    ("19h10", "9h10"),
    ("19h50", "9h50"),
    ("20h20", "10h20"),
    ("20h30", "10h30"),
    ("Novas frentes de receita no e-commerce | Nuvemshop Next", "Marca, valor percebido e margem | Nuvemshop Next"),
    ("Encontro presencial e reservado em São Paulo. Veja como marcas cresceram com assinatura, B2B e exportação sem depender de um só canal. 60 lugares.", "Encontro presencial em São Paulo sobre como produto, comunicação e experiência constroem valor percebido e ajudam marcas a sustentar margem."),
    ("Eventos presenciais exclusivos | Nuvemshop Next", "Quando a marca sustenta valor | Nuvemshop Next"),
    ("Encontros reservados para founders e líderes de e-commerce. Conteúdo prático, troca entre pares e lugares limitados.", "Uma manhã presencial sobre como tornar diferenciais mais claros, fortalecer valor percebido e reduzir a dependência de desconto."),
    ("Você cresceu até onde seu modelo", "Quando a marca sustenta valor,"),
    ("Você cresceu até onde este modelo", "Quando a marca sustenta valor,"),
    ("alcança?", "o preço deixa de decidir sozinho."),
    ("alcança.", "o preço deixa de decidir sozinho."),
    ("A pergunta agora é qual nova frente faz sentido para o seu momento: assinatura, B2B ou exportação. Uma noite com marcas que já tomaram essa decisão, para você separar uma expansão viável de uma aposta precipitada.", "Uma manhã sobre como produto, posicionamento, comunicação e experiência constroem valor percebido — com os bastidores de marcas que transformaram diferenciação em escolha."),
    ("Evento presencial e reservado. 60 lugares.", "Encontro presencial e gratuito. Lugares limitados. Participação confirmada por e-mail."),
    ("Confirmar minha presença", "Quero participar"),
    ("Ver programação da noite", "Ver programação da manhã"),
    ("Para quem já domina um modelo e está diante do próximo.", "Para quem entrega valor, mas ainda precisa torná-lo evidente."),
    ("60 lugares para founders e líderes de e-commerce com operação rodando, avaliando novas frentes de receita.", "Uma sala para lideranças de marcas em crescimento que querem sustentar margem, fortalecer diferenciação e reduzir a dependência de desconto."),
    ("Seu canal principal é forte, mas o próximo ciclo não pode depender só dele.", "Seu produto tem diferenciais, mas o cliente ainda compara principalmente preço."),
    ("Assinatura, B2B ou exportação já são hipótese, mas falta critério para priorizar.", "Promoções geram volume, mas pressionam margem e percepção."),
    ("Você quer ouvir quem já colocou uma dessas frentes de pé antes de levar a pauta ao time.", "A marca cresceu, mas posicionamento, comunicação e experiência já não avançam no mesmo ritmo."),
    ("A tese da noite", "A tese da manhã"),
    ("Diversificar não é abrir tudo.", "Premium não é parecer mais caro."),
    ("É escolher a frente certa primeiro.", "É tornar o valor mais fácil de perceber."),
    ("Assinatura, B2B e exportação ampliam receita e reduzem a dependência de um só canal. Mas cada uma exige decisões próprias de operação, margem, oferta e time.", "O cliente forma sua percepção antes de comparar o número final. Produto, oferta, comunicação, atendimento e experiência enviam sinais — e eles precisam apontar para a mesma direção."),
    ("A noite existe para você sair com critério para comparar essas frentes, não com mais uma tendência para discutir depois.", "Quando esses sinais se reforçam, a marca ganha espaço para sustentar sua proposta sem deixar que o desconto faça o trabalho sozinho."),
    ("O playbook da noite", "A programação"),
    ("Uma sequência,", "Da construção do valor"),
    ("não uma grade.", "aos bastidores de quem fez."),
    ("Cada momento tem uma função: entender o tema, ver como funciona na prática e trocar com quem está na mesma decisão.", "Uma manhã para entender os fundamentos, observar casos reais e conversar com quem enfrenta decisões semelhantes."),
    ("Fundadores e operadores que ajudam a responder, na prática, como novas frentes de receita saem da ideia e entram na operação.", "Especialistas e lideranças que conectam marca, comunicação e experiência às decisões reais de uma operação em crescimento."),
    ("A experiência", "Networking"),
    ("A noite fecha com", "A conversa continua"),
    ("uma taça na mão.", "depois do palco."),
    ("Depois da conversa, o networking ganha uma degustação de vinho guiada por sommelier. Um encerramento sensorial, à altura de quem está na sala.", "A programação reserva um período aberto para conversar com outras lideranças sobre marca, margem e os desafios de tornar valor perceptível em operações reais."),
    ("Critérios para decidir,", "Você não sai com uma fórmula."),
    ("não uma lista de tendências.", "Sai com critérios melhores."),
    ("Marcas na sala", "Marcas na conversa"),
    ("Uma sala reservada na", "Uma manhã presencial na"),
    ("Uma noite presencial no escritório da Nuvemshop, em São Paulo. Para troca direta entre lojistas, fundadores e time Next.", "No escritório da Nuvemshop, em São Paulo. Um encontro para aproximar lideranças, especialistas e marcas que enfrentam decisões semelhantes."),
    ("Antes de confirmar sua presença", "Antes de solicitar sua participação"),
    ("Algumas informações práticas para você decidir com segurança e organizar sua ida.", "Informações práticas para você entender o formato e organizar sua ida."),
    ("Depoimentos de quem já passou por uma edição do Next.", "Depoimentos de participantes de encontros presenciais da Nuvemshop Next."),
    ("Última chamada", "O encontro"),
    ("60 lugares.", "70 lugares."),
    ("Uma conversa que não acontece em palco grande, em webinar ou em blog. Acontece na sala, entre quem está tomando decisões parecidas agora.", "Uma sala para quem quer fazer o valor aparecer. Marca forte não elimina o preço da decisão; evita que ele seja o único argumento."),
    ("Ao confirmar, você recebe a programação e os detalhes de acesso por e-mail.", "Ao enviar seus dados, sua pré-inscrição será registrada. A participação será confirmada por e-mail."),
    ("Confirmar presença", "Quero participar"),
    ("Confirme sua presença no evento. A programação e os detalhes de acesso chegam por e-mail.", "Preencha seus dados para registrar sua pré-inscrição. As vagas são limitadas, e a participação será confirmada por e-mail."),
    # Tópicos / pilares
    ("Assinatura", "Produto e oferta"),
    ("Quando faz sentido virar recorrência, e o que precisa estar pronto para sustentar.", "A base concreta que torna uma proposta superior defensável."),
    ("B2B", "Comunicação e identidade"),
    ("Como abrir atacado sem confundir canal novo com operação duplicada.", "Como tornar diferenciais legíveis sem depender de adjetivos ou promessas genéricas."),
    ("Exportação", "Experiência e consistência"),
    ("Exportar começa na operação, não no idioma. O que avaliar antes de entrar em um novo mercado.", "Onde o valor se confirma — ou se perde — ao longo da jornada do cliente."),
    # Speakers e programação
    ("Amanda Aliperti", "Gutto Paixão"),
    ("Fundadora · PWRD by Coffee", "Diretor de Marketing e Performance · Weethub"),
    ("Opera D2C, atacado, assinatura e exportação em paralelo. Na palestra, mostra como montou essa estrutura e o que decidir primeiro.", "Mostra como produto, comunicação e experiência precisam contar a mesma história para transformar diferenciação em valor percebido."),
    ("Beatriz Daniel", "Caroline Domingues"),
    ("Sua Mesa Suas Vontades", "Nuvemshop"),
    ("No painel, o que muda quando a assinatura vira pilar do negócio: operação, oferta e relação com o cliente.", "Conduz a abertura e conecta o tema às decisões de marcas em crescimento."),
    ("Carolina Hebeisen", "Katharina Neves"),
    ("Housewhey", "Mica Chocolates"),
    ("Cofundadora e diretora de marketing. No painel, como a marca virou referência em suplementação clean label e o que sustenta a recorrência.", "Compartilha os bastidores de uma marca que tornou produto, identidade e experiência mais consistentes e reconhecíveis."),
    ("Gustavo Batista", "Ângela Coelho da Fonseca"),
    ("Conduz a conversa e conecta os casos ao contexto das marcas da comunidade Next.", "Participa do painel sobre valor percebido. Descrição do case em validação."),
    ("Recepção dos convidados e primeira rodada de networking.", "Recepção dos convidados e primeira rodada de conversas."),
    ("Por que abrir novas frentes exige discutir modelo de receita, não só canal.", "Por que valor percebido, marca e margem precisam ser discutidos juntos."),
    ("D2C, atacado, assinatura e exportação", "Como transformar diferenciação em valor percebido"),
    ("Amanda Aliperti abre os bastidores da PWRD by Coffee: as decisões que permitiram rodar D2C, atacado, assinatura e exportação em paralelo, e o que cada uma custou antes de dar certo.", "Produto, comunicação e experiência precisam contar a mesma história. Gutto Paixão apresenta os sinais que ajudam uma marca a justificar sua proposta, fortalecer percepção de valor e reduzir a dependência de desconto."),
    ("O painel · Receita que se renova", "O que o cliente percebe antes de olhar o preço"),
    ("Os bastidores de quem transformou assinatura em pilar do negócio, e os números por trás da decisão.", "Nos bastidores de marcas que conquistaram atenção e reconhecimento, as decisões que tornaram produto, identidade e experiência mais consistentes — e o que isso mudou na relação com o cliente."),
    ("Fechamento da conversa e principais critérios para comparar assinatura, B2B e exportação no seu contexto.", "Fechamento da conversa e síntese dos critérios que ajudam a tornar o valor mais claro e a margem menos dependente de desconto."),
    ("Networking, com degustação", "Networking"),
    ("A noite não termina na palestra. O momento de troca ganha uma degustação de vinho guiada por sommelier, para aproximar quem está na sala.", "Um tempo aberto para conversar com outras lideranças sobre marca, margem e os desafios de tornar valor perceptível em operações reais."),
    # Takeaways
    ("Como avaliar se assinatura, B2B ou exportação faz sentido para o seu estágio atual.", "Identificar onde sua marca perde valor percebido."),
    ("Quais mudanças de operação, oferta e time cada frente pode exigir.", "Diferenciar mudança estrutural de ajuste cosmético."),
    ("Onde estão os riscos de dispersão, complexidade e canibalização.", "Entender como produto, comunicação e experiência precisam se reforçar."),
    ("O que perguntar internamente antes de transformar ideia em projeto.", "Avaliar quais sinais sustentam uma proposta premium."),
    ("Como operações parecidas decidiram por onde começar, e o que separou o timing certo da aposta prematura.", "Reconhecer onde o desconto está compensando uma diferenciação pouco visível."),
    # FAQ
    ("Sim. É um evento gratuito para convidados.", "Sim. O encontro é gratuito e presencial, com lugares limitados."),
    ("Não. É uma sala reservada, para um grupo selecionado de lojistas e convidados.", "A página tem distribuição ampliada, mas a participação é voltada a lideranças e marcas com aderência ao tema do encontro."),
    ("Sim. Em geral, reservamos até 2 convites por marca, para manter o perfil da sala.", "A disponibilidade para acompanhantes será informada na confirmação da participação."),
    ("Confirmar presença garante meu lugar?", "Enviar meus dados garante meu lugar?"),
    ("Sim. Ao preencher o formulário, sua presença fica confirmada enquanto houver disponibilidade na sala.", "Não. O envio registra sua pré-inscrição. A participação será confirmada por e-mail."),
    ("O que acontece depois que confirmo?", "O que acontece depois da pré-inscrição?"),
    ("Você recebe por e-mail a confirmação, a programação e as informações de acesso ao escritório.", "Você recebe por e-mail o retorno sobre a participação. Caso seja confirmada, enviaremos também a programação e os detalhes de acesso."),
    ("Uma noite pensada para a troca, com uma degustação de vinho guiada por sommelier para aproximar quem está na sala.", "A programação reserva duas horas para conversas entre lideranças, especialistas e marcas participantes."),
]


def replace_all(text: str) -> tuple[str, list[str], int]:
    missing: list[str] = []
    total = 0
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            total += count
        else:
            missing.append(old)
    return text, missing, total


def technical_updates(text: str, *, is_preview: bool = False) -> str:
    # IDs, datas e capacidade. O Form ID é deliberadamente fictício e sintaticamente válido.
    text = re.sub(r"bdb0ccad-d2b3-471a-adf1-9187057e1ab3", FORM_ID_PLACEHOLDER, text)
    text = re.sub(r"TOTAL:\s*60", "TOTAL: 70", text)
    text = re.sub(r"BASE_OCCUPIED:\s*\d+", "BASE_OCCUPIED: 29", text)
    text = re.sub(r"LAST_THRESHOLD:\s*\d+", "LAST_THRESHOLD: 10", text)
    text = re.sub(r"new Date\('2026-08-26T18:30:00-03:00'\)", "new Date('2026-09-08T08:30:00-03:00')", text)
    text = re.sub(r"new Date\('2026-07-11T09:00:00-03:00'\)", "new Date('2026-08-04T09:00:00-03:00')", text)
    text = text.replace("2026-08-26T18:30:00-03:00", "2026-09-08T08:30:00-03:00")
    text = text.replace("2026-08-25T18:30:00-03:00", "2026-09-08T08:30:00-03:00")
    text = text.replace("2026-07-11T09:00:00-03:00", "2026-08-04T09:00:00-03:00")
    text = text.replace("evento-modelos-negocio.css", "evento-marca-valor.css")
    text = text.replace("evento-modelos-negocio.js", "evento-marca-valor.js")
    text = text.replace("evento-modelos-negocio-page", "evento-marca-valor-page")
    text = text.replace("/next/novas-frentes-de-receita", "/next/marca-valor-percebido")
    if is_preview:
        text = text.replace("https://ffidelis16.github.io/next-sessions-lp/", EVENT_URL)
    return text


def generate_text(source: Path, target: Path, *, preview: bool = False) -> tuple[int, list[str]]:
    raw = source.read_text(encoding="utf-8-sig")
    updated, missing, count = replace_all(raw)
    updated = technical_updates(updated, is_preview=preview)
    target.write_text(updated, encoding="utf-8")
    return count, missing


def main() -> None:
    for source in (SOURCE_PREVIEW, SOURCE_HTML, SOURCE_CSS, SOURCE_JS):
        if not source.exists():
            raise FileNotFoundError(f"Arquivo-fonte não encontrado: {source.relative_to(ROOT)}")

    preview_count, preview_missing = generate_text(SOURCE_PREVIEW, OUT_HTML, preview=True)
    html_count, html_missing = generate_text(SOURCE_HTML, OUT_DEV_HTML)
    js_count, js_missing = generate_text(SOURCE_JS, OUT_DEV_JS)

    css = SOURCE_CSS.read_text(encoding="utf-8-sig")
    css = technical_updates(css)
    OUT_DEV_CSS.write_text(css, encoding="utf-8")

    report_lines = [
        "# Relatório de geração — Evento 08/09 · Marca, valor percebido e margem",
        "",
        "## Arquivos gerados",
        "",
        f"- `{OUT_HTML.relative_to(ROOT)}` — preview standalone, mantendo os mesmos assets da edição anterior.",
        f"- `{OUT_DEV_HTML.relative_to(ROOT)}` — template HubSpot duplicado.",
        f"- `{OUT_DEV_CSS.relative_to(ROOT)}` — CSS duplicado.",
        f"- `{OUT_DEV_JS.relative_to(ROOT)}` — JS duplicado e adaptado.",
        "",
        "## Configuração provisória",
        "",
        f"- Portal ID: `8180620`.",
        f"- Form ID fictício: `{FORM_ID_PLACEHOLDER}`.",
        "- Evento: `2026-09-08T08:30:00-03:00`.",
        "- Capacidade: `70` lugares.",
        "- BASE_OCCUPIED provisório: `29`; preservar apenas como configuração técnica de rascunho até validação operacional.",
        "- Endereço, mapa, hero e local reutilizam a edição anterior.",
        "",
        "## Resultado das substituições",
        "",
        f"- Preview: {preview_count} ocorrências substituídas.",
        f"- Template HubSpot: {html_count} ocorrências substituídas.",
        f"- JavaScript: {js_count} ocorrências substituídas.",
        "",
        "## Pendências antes de publicação",
        "",
        "- Trocar o Form ID fictício pelo formulário real.",
        "- Validar a curva de ocupação das 70 cadeiras com a operação.",
        "- Substituir fotos de palestrantes e logos quando os assets da edição forem entregues; nesta versão permanecem provisórios.",
        "- Validar a descrição do case de Ângela Coelho da Fonseca/Jogê.",
        "- Confirmar política de gravação e eventual bloco institucional/comercial.",
        "",
        "## Strings não encontradas",
        "",
        "A lista abaixo não indica necessariamente erro: algumas strings aparecem apenas no HTML ou apenas no JS.",
        "",
    ]
    missing = sorted(set(preview_missing + html_missing + js_missing))
    report_lines.extend(f"- `{item}`" for item in missing)
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Gerado: {OUT_HTML.relative_to(ROOT)}")
    print(f"Gerado: {OUT_DEV_HTML.relative_to(ROOT)}")
    print(f"Gerado: {OUT_DEV_CSS.relative_to(ROOT)}")
    print(f"Gerado: {OUT_DEV_JS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
