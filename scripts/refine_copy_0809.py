from pathlib import Path

FILES = [
    Path("evento-08-09-marca-valor.html"),
    Path("docs/hubspot-implementation/entrega-final-plano-a/developer-files/evento-marca-valor.html"),
]

REPLACEMENTS = [
    (
        "A manhã começa com conteúdo, passa por experiências de marcas convidadas e termina com tempo aberto para troca entre os participantes.",
        "A manhã começa com conteúdo, passa por casos de marcas convidadas e termina com tempo aberto para troca entre os participantes.",
    ),
    (
        "Profissionais de marca, marketing e e-commerce que conhecem o tema na prática.",
        "Perspectivas de agência, plataforma e marcas para discutir o tema por ângulos diferentes.",
    ),
    (
        "Aborda como produto, comunicação e experiência se combinam para fortalecer o valor percebido.",
        "Apresenta os fundamentos de produto, comunicação e experiência que ajudam a sustentar valor percebido.",
    ),
    (
        "Conduz a abertura e organiza os principais pontos da conversa.",
        "Abre o encontro e conduz a conversa entre os diferentes pontos de vista.",
    ),
    (
        "Traz a perspectiva de uma marca que trabalha produto, identidade e experiência de forma integrada.",
        "Compartilha a experiência da Mica Chocolates na construção de uma marca com identidade própria.",
    ),
    (
        "Participa do painel sobre marca, valor percebido e experiência do cliente.",
        "Leva ao painel a experiência da Jogê em marca, produto e relação com o cliente.",
    ),
    (
        "Lideranças da Mica Chocolates e da Jogê compartilham escolhas, aprendizados e desafios na construção de marcas com identidade clara em mercados competitivos.",
        "Katharina Neves e Ângela Coelho da Fonseca conversam sobre decisões de produto, identidade e experiência que ajudam uma marca a ganhar clareza e reconhecimento.",
    ),
    (
        "Duas horas abertas para conversas entre participantes, especialistas e marcas convidadas.",
        "Duas horas reservadas para conversas entre participantes, especialistas e marcas convidadas.",
    ),
    (
        "Conteúdo primeiro. <span class=\"ac\">Conversa aberta depois.</span>",
        "Depois do conteúdo, <span class=\"ac\">a conversa continua.</span>",
    ),
    (
        "Depois das apresentações, a agenda reserva duas horas para perguntas, trocas e conversas entre participantes, especialistas e marcas convidadas.",
        "Depois das apresentações, a agenda reserva duas horas para perguntas e conversas entre participantes, especialistas e marcas convidadas.",
    ),
    (
        "Marcas que já participaram de encontros Nuvemshop Next",
        "Marcas que já participaram dos encontros da Nuvemshop Next",
    ),
    (
        "alt=\"PWRD by Coffee — imagem provisória\"",
        "alt=\"PWRD by Coffee\"",
    ),
    (
        "alt=\"Sua Mesa Suas Vontades — imagem provisória\"",
        "alt=\"Sua Mesa Suas Vontades\"",
    ),
    (
        "alt=\"Housewhey — imagem provisória\"",
        "alt=\"Housewhey\"",
    ),
    (
        "O encontro acontece no escritório da Nuvemshop, com programação presencial e espaço para as conversas depois do conteúdo.",
        "O encontro acontece no escritório da Nuvemshop, com espaço para acompanhar o conteúdo e conversar com os participantes depois das apresentações.",
    ),
    (
        "A manhã combina recepção, conteúdo, conversa com marcas convidadas e duas horas de networking.",
        "A manhã combina recepção, uma palestra, um painel com marcas convidadas e duas horas de networking.",
    ),
    (
        "Relatos de outras edições",
        "Outras edições",
    ),
    (
        "Quem já participou.",
        "Quem já participou",
    ),
    (
        "Relatos de encontros presenciais da Nuvemshop Next.",
        "Um relato sobre a experiência nos encontros presenciais da Nuvemshop Next.",
    ),
    (
        "Ao enviar seus dados, sua pré-inscrição será registrada. A participação será confirmada por e-mail.",
        "O envio registra seu interesse. A confirmação será feita por e-mail.",
    ),
]

for path in FILES:
    text = path.read_text(encoding="utf-8-sig")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text == original:
        raise RuntimeError(f"Nenhuma alteração aplicada em {path}")
    path.write_text(text, encoding="utf-8")
    print(f"Refinada: {path}")
