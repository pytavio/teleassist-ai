DEFAULT_INTENCOES = [
    {
        "id": "consultar_fatura",
        "nome": "Consultar Fatura",
        "ativo": True,
        "frases": ["quanto devo", "valor da fatura", "quanto tenho que pagar", "minha fatura", "vencimento"]
    },
    {
        "id": "consumo_dados",
        "nome": "Consumo de Dados",
        "ativo": True,
        "frases": ["quanto de internet usei", "acabou minha internet", "meu pacote de dados", "consumo de dados"]
    },
    {
        "id": "mudar_plano",
        "nome": "Mudar Plano",
        "ativo": True,
        "frases": ["quero mudar meu plano", "trocar plano", "upgrade", "outro plano", "planos disponíveis"]
    },
    {
        "id": "suporte_sinal",
        "nome": "Suporte Técnico / Sinal",
        "ativo": True,
        "frases": ["sem sinal", "internet não funciona", "queda de sinal", "não consigo ligar", "rede caiu"]
    },
    {
        "id": "cancelar",
        "nome": "Cancelamento",
        "ativo": True,
        "frases": ["quero cancelar", "cancelar meu plano", "encerrar contrato", "quero sair"]
    },
    {
        "id": "falar_atendente",
        "nome": "Falar com Atendente",
        "ativo": True,
        "frases": ["quero falar com humano", "atendente", "falar com pessoa", "transferir"]
    },
    {
        "id": "recarga",
        "nome": "Recarga",
        "ativo": True,
        "frases": ["recarregar", "como recarrego", "recarga", "créditos"]
    },
    {
        "id": "negociar_debito",
        "nome": "Negociar Débito",
        "ativo": True,
        "frases": ["negociar dívida", "parcelar fatura", "estou com dívida", "débito em aberto", "acordo"]
    }
]

DEFAULT_ENTIDADES = [
    {"id": "tipo_plano", "nome": "Tipo de Plano", "valores": ["pré-pago", "pós-pago", "controle"]},
    {"id": "valor", "nome": "Valor Monetário", "valores": ["R$", "reais", "valor"]},
    {"id": "data", "nome": "Data / Período", "valores": ["vencimento", "mês", "hoje", "amanhã"]},
    {"id": "pacote", "nome": "Tipo de Pacote", "valores": ["internet", "ligações", "SMS", "dados"]}
]

DEFAULT_RESPOSTAS = {
    "consultar_fatura": [
        {"id": "cf_generico", "perfil": "generico", "texto": "Sua fatura atual é de R$ 89,90 com vencimento em 15 deste mês. Posso te ajudar com mais alguma coisa?", "score": 0.5},
        {"id": "cf_premium", "perfil": "premium", "texto": "Olá! Sua fatura premium é de R$ 189,90, já com os benefícios do seu plano. Vencimento em 15. Deseja ver o detalhamento?", "score": 0.5},
        {"id": "cf_inadimplente", "perfil": "inadimplente", "texto": "Entendo que você quer verificar sua fatura. Você possui um valor em aberto de R$ 89,90. Posso te ajudar a encontrar a melhor forma de regularizar isso. Vamos conversar?", "score": 0.5}
    ],
    "consumo_dados": [
        {"id": "cd_generico", "perfil": "generico", "texto": "Você utilizou 12GB dos 15GB do seu pacote mensal. Restam 3GB até o dia 30. Quer ativar um pacote adicional?", "score": 0.5},
        {"id": "cd_premium", "perfil": "premium", "texto": "Seu plano premium tem dados ilimitados. Atualmente você está na faixa de uso moderado. Nenhuma ação necessária!", "score": 0.5},
        {"id": "cd_churn", "perfil": "churn", "texto": "Você usou 12GB dos 15GB. Sei que o plano atual pode não estar sendo suficiente — que tal conhecer nossas opções com mais dados pelo mesmo preço?", "score": 0.5}
    ],
    "mudar_plano": [
        {"id": "mp_generico", "perfil": "generico", "texto": "Temos ótimas opções! Nosso plano Conecta 30GB sai por R$ 69,90 e o plano Total Ilimitado por R$ 99,90. Qual se encaixa melhor na sua rotina?", "score": 0.5},
        {"id": "mp_premium", "perfil": "premium", "texto": "Como cliente premium, você tem acesso antecipado ao nosso novo plano Elite com dados ilimitados + roaming nacional por R$ 149,90. Posso reservar pra você?", "score": 0.5},
        {"id": "mp_churn", "perfil": "churn", "texto": "Antes de mudar, quero te mostrar que podemos ajustar seu plano atual com um desconto exclusivo de fidelidade. Posso apresentar as condições?", "score": 0.5}
    ],
    "suporte_sinal": [
        {"id": "ss_generico", "perfil": "generico", "texto": "Sinto muito pelo inconveniente! Primeiro, tente reiniciar o aparelho e retirar/recolocar o chip. Se o problema persistir, vou registrar um chamado técnico para sua região.", "score": 0.5},
        {"id": "ss_insatisfeito", "perfil": "insatisfeito", "texto": "Entendo sua frustração e me desculpe por isso. Vou priorizar seu atendimento agora. Pode me confirmar seu CEP para verificar ocorrências na sua área?", "score": 0.5}
    ],
    "cancelar": [
        {"id": "ca_generico", "perfil": "generico", "texto": "Que pena que está pensando em cancelar! Antes de prosseguir, posso te apresentar algumas alternativas que talvez resolvam o que está incomodando?", "score": 0.5},
        {"id": "ca_churn", "perfil": "churn", "texto": "Entendo. Antes de cancelar, quero te fazer uma oferta exclusiva de retenção: 3 meses com 40% de desconto no seu plano atual. Posso detalhar?", "score": 0.5},
        {"id": "ca_premium", "perfil": "premium", "texto": "Como cliente premium há mais de 2 anos, sua saída seria uma grande perda pra nós. Posso transferir você agora para nosso time de relacionamento exclusivo?", "score": 0.5}
    ],
    "falar_atendente": [
        {"id": "fa_generico", "perfil": "generico", "texto": "Claro! Vou te transferir para um atendente humano. O tempo médio de espera agora é de 8 minutos. Deseja continuar?", "score": 0.5}
    ],
    "recarga": [
        {"id": "re_generico", "perfil": "generico", "texto": "Você pode recarregar pelo app TeleAssist, via PIX para a chave recarga@teleassist.com.br, ou em qualquer lotérica. Qual prefere?", "score": 0.5}
    ],
    "negociar_debito": [
        {"id": "nd_generico", "perfil": "generico", "texto": "Podemos parcelar seu débito em até 3x sem juros. Quer que eu gere o link de pagamento agora?", "score": 0.5},
        {"id": "nd_inadimplente", "perfil": "inadimplente", "texto": "Quero te ajudar a regularizar sua situação sem estresse. Temos uma proposta especial: entrada de 30% e o restante em 2x. Posso enviar no seu e-mail?", "score": 0.5}
    ],
    "fallback": [
        {"id": "fb_generico", "perfil": "generico", "texto": "Desculpe, não entendi muito bem sua solicitação. Pode reformular? Ou se preferir, posso te transferir para um atendente humano.", "score": 0.5}
    ]
}

PERFIS = ["Pós-pago Padrão", "Pré-pago", "Premium", "Inadimplente", "Em risco de churn", "Insatisfeito"]

PERFIL_MAP = {
    "Pós-pago Padrão": "generico",
    "Pré-pago": "generico",
    "Premium": "premium",
    "Inadimplente": "inadimplente",
    "Em risco de churn": "churn",
    "Insatisfeito": "insatisfeito"
}
