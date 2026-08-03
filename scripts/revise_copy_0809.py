from __future__ import annotations

import re
from pathlib import Path

FILES = [
    Path("evento-08-09-marca-valor.html"),
    Path("docs/hubspot-implementation/entrega-final-plano-a/developer-files/evento-marca-valor.html"),
]

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Encontro presencial em São Paulo sobre como produto, comunicação e experiência constroem valor percebido e ajudam marcas a sustentar margem.",
        "Encontro presencial em São Paulo sobre como marcas tornam seu valor mais claro, fortalecem a diferenciação e reduzem a dependência de desconto.",
    ),
    (
        "Uma manhã presencial sobre como tornar diferenciais mais claros, fortalecer valor percebido e reduzir a dependência de desconto.",
        "Uma manhã presencial sobre marca, valor percebido e margem, com conteúdo, casos e espaço para conversar com outras lideranças.",
    ),
    (
        "Eventos presenciais Nuvemshop Next — encontros exclusivos, com lugares limitados.",
        "Encontro presencial Nuvemshop Next, com lugares limitados.",
    ),
    (
        "Uma manhã sobre como produto, posicionamento, comunicação e experiência constroem valor percebido — com os bastidores de marcas que transformaram diferenciação em escolha.",
        "Uma manhã sobre como produto, posicionamento, comunicação e experiência ajudam o cliente a perceber valor. Com conteúdo prático, casos de marcas e tempo para conversar com outras lideranças.",
    ),
    (
        "Encontro presencial e gratuito. <span data-seats-total>70</span> lugares. Participação confirmada por e-mail.",
        "Encontro presencial e gratuito. <span data-seats-total>70</span> lugares. Participação sujeita à confirmação por e-mail.",
    ),
    (
        "Para quem entrega valor, mas ainda precisa torná-lo evidente.",
        "Para marcas que entregam mais do que o cliente percebe.",
    ),
    (
        "<span data-seats-total>70</span> lugares para lideranças de marcas em crescimento que querem sustentar margem, fortalecer diferenciação e reduzir a dependência de desconto.",
        "Uma sala com <span data-seats-total>70</span> lugares para lideranças de e-commerces em crescimento. A conversa passa por marca, margem e pelos desafios de sustentar uma proposta de valor mais clara.",
    ),
    (
        "Seu produto tem diferenciais, mas o cliente ainda compara principalmente preço.",
        "O produto tem diferenciais, mas a comparação ainda começa pelo preço.",
    ),
    (
        "Promoções geram volume, mas pressionam margem e percepção.",
        "As promoções ajudam a vender, mas pesam na margem.",
    ),
    (
        "A marca cresceu, mas posicionamento, comunicação e experiência já não avançam no mesmo ritmo.",
        "A operação cresceu, e a marca precisa acompanhar esse novo momento.",
    ),
    (
        "A tese da manhã",
        "A ideia central",
    ),
    (
        "Premium não é parecer mais caro. <span class=\"win\">É tornar o valor mais fácil de perceber.</span>",
        "Uma marca premium não é apenas a que cobra mais. <span class=\"win\">É a que deixa claro por que vale mais.</span>",
    ),
    (
        "O cliente forma sua percepção antes de comparar o número final. Produto, oferta, comunicação, atendimento e experiência enviam sinais — e eles precisam apontar para a mesma direção.",
        "O cliente forma uma impressão antes de comparar o preço. Produto, oferta, comunicação, atendimento e experiência constroem essa percepção. Quando esses pontos não conversam entre si, parte do valor se perde.",
    ),
    (
        "A base concreta que torna uma proposta superior defensável.",
        "O que a marca entrega e como organiza sua proposta.",
    ),
    (
        "Como tornar diferenciais legíveis sem depender de adjetivos ou promessas genéricas.",
        "A forma como o diferencial ganha clareza e consistência.",
    ),
    (
        "Onde o valor se confirma — ou se perde — ao longo da jornada do cliente.",
        "O que confirma, na prática, a promessa feita ao cliente.",
    ),
    (
        "Quando esses sinais se reforçam, a marca ganha espaço para sustentar sua proposta sem deixar que o desconto faça o trabalho sozinho.",
        "Quando esses elementos trabalham juntos, o valor fica mais claro e o preço deixa de carregar sozinho a decisão.",
    ),
    (
        "Da construção do valor <span class=\"ac\">aos bastidores de quem fez.</span>",
        "Fundamentos, casos e conversas <span class=\"ac\">para colocar o tema em perspectiva.</span>",
    ),
    (
        "Uma manhã para entender os fundamentos, observar casos reais e conversar com quem enfrenta decisões semelhantes.",
        "A manhã começa com conteúdo, passa por experiências de marcas convidadas e termina com tempo aberto para troca entre os participantes.",
    ),
    (
        "Especialistas e lideranças que conectam marca, comunicação e experiência às decisões reais de uma operação em crescimento.",
        "Profissionais de marca, marketing e e-commerce que conhecem o tema na prática.",
    ),
    (
        "Mostra como produto, comunicação e experiência precisam contar a mesma história para transformar diferenciação em valor percebido.",
        "Aborda como produto, comunicação e experiência se combinam para fortalecer o valor percebido.",
    ),
    (
        "Conduz a abertura e conecta o tema às decisões de marcas em crescimento.",
        "Conduz a abertura e organiza os principais pontos da conversa.",
    ),
    (
        "Compartilha os bastidores de uma marca que tornou produto, identidade e experiência mais consistentes e reconhecíveis.",
        "Traz a perspectiva de uma marca que trabalha produto, identidade e experiência de forma integrada.",
    ),
    (
        "Participa do painel sobre valor percebido. Descrição do case em validação.",
        "Participa do painel sobre marca, valor percebido e experiência do cliente.",
    ),
    (
        "<div class=\"tl__t\">Welcome</div><div class=\"tl__d\">Recepção dos convidados e primeira rodada de conversas.</div>",
        "<div class=\"tl__t\">Recepção</div><div class=\"tl__d\">Chegada dos convidados e início das conversas.</div>",
    ),
    (
        "Por que valor percebido, marca e margem precisam ser discutidos juntos.",
        "Uma introdução ao tema e à programação da manhã.",
    ),
    (
        "Como transformar diferenciação em valor percebido",
        "Como construir e comunicar valor percebido",
    ),
    (
        "Produto, comunicação e experiência precisam contar a mesma história. Gutto Paixão apresenta os sinais que ajudam uma marca a justificar sua proposta, fortalecer a percepção de valor e reduzir a dependência de desconto.",
        "Uma conversa sobre produto, comunicação e experiência, e sobre como esses elementos ajudam a sustentar uma proposta premium.",
    ),
    (
        "O que o cliente percebe antes de olhar o preço",
        "Como o valor da marca aparece na prática",
    ),
    (
        "Nos bastidores de marcas que conquistaram atenção e reconhecimento, as decisões que tornaram produto, identidade e experiência mais consistentes — e o que isso mudou na relação com o cliente.",
        "Lideranças da Mica Chocolates e da Jogê compartilham escolhas, aprendizados e desafios na construção de marcas com identidade clara em mercados competitivos.",
    ),
    (
        "Caroline Domingues + Katharina Neves · Mica Chocolates + Ângela Coelho da Fonseca · Jogê",
        "Caroline Domingues, Nuvemshop; Katharina Neves, Mica Chocolates; Ângela Coelho da Fonseca, Jogê",
    ),
    (
        "<div class=\"tl__t\">O que levar daqui</div><div class=\"tl__d\">Fechamento da conversa e síntese dos critérios que ajudam a tornar o valor mais claro e a margem menos dependente de desconto.</div>",
        "<div class=\"tl__t\">Síntese da manhã</div><div class=\"tl__d\">Retomada dos principais pontos antes do período de networking.</div>",
    ),
    (
        "Um tempo aberto para conversar com outras lideranças sobre marca, margem e os desafios de tornar valor perceptível em operações reais.",
        "Duas horas abertas para conversas entre participantes, especialistas e marcas convidadas.",
    ),
    (
        "<span class=\"tl__k\" style=\"color:var(--blue-400)\">Networking</span>",
        "<span class=\"tl__k\" style=\"color:var(--blue-400)\">A experiência</span>",
    ),
    (
        "A conversa continua <span class=\"ac\">depois do palco.</span>",
        "Conteúdo primeiro. <span class=\"ac\">Conversa aberta depois.</span>",
    ),
    (
        "A programação reserva um período aberto para conversar com outras lideranças sobre marca, margem e os desafios de tornar valor perceptível em operações reais.",
        "Depois das apresentações, a agenda reserva duas horas para perguntas, trocas e conversas entre participantes, especialistas e marcas convidadas.",
    ),
    (
        "O que você leva",
        "Para levar à operação",
    ),
    (
        "Você não sai com uma fórmula. <span class=\"ac\">Sai com critérios melhores.</span>",
        "Ideias para olhar a marca <span class=\"ac\">com mais critério.</span>",
    ),
    (
        "Identificar onde sua marca perde valor percebido.",
        "Identificar onde a marca deixa de traduzir a qualidade do que entrega.",
    ),
    (
        "Diferenciar mudança estrutural de ajuste cosmético.",
        "Separar mudanças estruturais de ajustes apenas cosméticos.",
    ),
    (
        "Entender como produto, comunicação e experiência precisam se reforçar.",
        "Entender como produto, comunicação e experiência podem trabalhar na mesma direção.",
    ),
    (
        "Avaliar quais sinais sustentam uma proposta premium.",
        "Reconhecer os sinais que ajudam a sustentar uma proposta premium.",
    ),
    (
        "Reconhecer onde o desconto está compensando uma diferenciação pouco visível.",
        "Perceber quando o desconto está ocupando o lugar da diferenciação.",
    ),
    (
        "Marcas na conversa",
        "Marcas que já participaram de encontros Nuvemshop Next",
    ),
    (
        "No escritório da Nuvemshop, em São Paulo. Um encontro para aproximar lideranças, especialistas e marcas que enfrentam decisões semelhantes.",
        "O encontro acontece no escritório da Nuvemshop, com programação presencial e espaço para as conversas depois do conteúdo.",
    ),
    (
        "Antes de solicitar sua participação",
        "Antes de participar",
    ),
    (
        "Informações práticas para você entender o formato e organizar sua ida.",
        "Veja as principais informações sobre inscrição, horário e local.",
    ),
    (
        "A página tem distribuição ampliada, mas a participação é voltada a lideranças e marcas com aderência ao tema do encontro.",
        "O encontro é voltado a lideranças e marcas com aderência ao tema. Como os lugares são limitados, a participação é confirmada por e-mail.",
    ),
    (
        "Enviar meus dados garante meu lugar?",
        "Enviar a pré-inscrição garante meu lugar?",
    ),
    (
        "Não. O envio registra sua pré-inscrição. A participação será confirmada por e-mail.",
        "Não. O envio registra seu interesse. Como a sala tem capacidade limitada, a confirmação é enviada por e-mail.",
    ),
    (
        "Você recebe por e-mail o retorno sobre a participação. Caso seja confirmada, enviaremos também a programação e os detalhes de acesso.",
        "Você recebe um retorno por e-mail. Se a participação for confirmada, enviaremos também a programação e os detalhes de acesso.",
    ),
    (
        "O evento será gravado?",
        "Como será a programação?",
    ),
    (
        "Não. O valor está em estar na sala.",
        "A manhã combina recepção, conteúdo, conversa com marcas convidadas e duas horas de networking.",
    ),
    (
        "Vai ter apresentação comercial?",
        "Preciso chegar às 8h30?",
    ),
    (
        "Não. A manhã é de conteúdo prático e troca entre pares.",
        "A recepção começa às 8h30, e o conteúdo às 9h. Chegar no início ajuda a acompanhar a programação completa.",
    ),
    (
        "A programação reserva duas horas para conversas entre lideranças, especialistas e marcas participantes.",
        "Das 10h30 às 12h30, a agenda fica aberta para conversas entre participantes, especialistas e marcas convidadas.",
    ),
    (
        "Uma noite pensada para a troca, com degustação de vinho guiada por sommelier.",
        "Das 10h30 às 12h30, a agenda fica aberta para conversas entre participantes, especialistas e marcas convidadas.",
    ),
    (
        "Prova de par",
        "Relatos de outras edições",
    ),
    (
        "Quem já esteve na sala.",
        "Quem já participou.",
    ),
    (
        "Depoimentos de participantes de encontros presenciais da Nuvemshop Next.",
        "Relatos de encontros presenciais da Nuvemshop Next.",
    ),
    (
        "Uma sala para quem quer fazer o valor aparecer. Marca forte não elimina o preço da decisão; evita que ele seja o único argumento.",
        "Uma manhã para entender como a marca pode tornar seu valor mais claro e depender menos de desconto.",
    ),
    (
        "<h3 class=\"modal__title\" id=\"formTitle\">Quero participar</h3>",
        "<h3 class=\"modal__title\" id=\"formTitle\">Solicitar participação</h3>",
    ),
    (
        "Preencha seus dados para registrar sua pré-inscrição. As vagas são limitadas, e a participação será confirmada por e-mail.",
        "Preencha seus dados para registrar seu interesse. Como a sala tem capacidade limitada, a confirmação será enviada por e-mail.",
    ),
    (
        "/* Networking (degustação) — slot de foto entra em .exp__media quando houver */",
        "/* Experiência e networking: a imagem atual é provisória */",
    ),
    (
        "EVENTO PRESENCIAL · 08/09 — Modelos de negócio",
        "EVENTO PRESENCIAL · 08/09 · Marca e valor percebido",
    ),
]


def revise(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    original = text
    applied = 0

    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            applied += count

    # As fotos continuam provisórias. Evita identificar visualmente pessoas erradas no texto alternativo.
    text = re.sub(r'alt="Imagem provisória do card de [^"]+"', 'alt=""', text)

    # A imagem da edição anterior permanece como apoio visual, sem atribuir vinho à experiência atual.
    text = text.replace(
        'alt="Taça de vinho tinto sob luz suave numa noite de networking"',
        'alt=""',
    )

    if text == original:
        raise RuntimeError(f"Nenhuma alteração aplicada em {path}")

    path.write_text(text, encoding="utf-8")
    print(f"{path}: {applied} substituições aplicadas")


for target in FILES:
    revise(target)
