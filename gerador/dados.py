# Dados do consultório usados em todas as páginas e nos dados estruturados.
# Mantenha só informações confirmadas pelo Dr. Daniel.

SITE = "https://danielnegrelle.com.br"
NOME = "Dr. Daniel Bonato Negrelle"
NOME_CURTO = "Dr. Daniel Negrelle"
AREA = "Cirurgia e Traumatologia Bucomaxilofacial"
CRO = "CRO-PR 16620"
ESPECIALISTA = f"Especialista em {AREA}"
HOSPITAL = "Hospital São Lucas"
ENDERECO = {
    "rua": "Av. João Gualberto, 1946",
    "local": "Hospital São Lucas",
    "bairro": "Alto da Glória",
    "cep": "80030-001",
    "cidade": "Curitiba",
    "uf": "PR",
    "pais": "BR",
}
TELEFONE = "(41) 3022-0654"
TELEFONE_E164 = "+554130220654"
WHATSAPP = "5541999864486"
WHATSAPP_TXT = "(41) 99986-4486"
EMAIL = "contato@danielnegrelle.com.br"
# Horário de atendimento, igual ao Perfil da Empresa no Google.
HORARIO_TXT = "Segunda a sexta, das 8h às 12h e das 14h às 18h"
HORARIO_LD = [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": o, "closes": c} for o, c in (("08:00", "12:00"), ("14:00", "18:00"))]
MAPA = "https://maps.app.goo.gl/6ii9CHAXPysA7Gi29"
