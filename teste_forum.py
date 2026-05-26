"""
SISTEMA DE FÓRUM COLABORATIVO
Demonstração de POO com Herança e Polimorfismo

Conceitos implementados:
1. Classe Abstrata (Membro)
2. Herança (MembroComum, MembroContribuidor, Moderador, Admin)
3. Polimorfismo (criar_topico() diferente em cada classe)
4. Composição (Topico, Resposta, Categoria)
5. Encapsulamento com reputação e níveis
"""

from forum import (
    Membro, MembroComum, MembroContribuidor, Moderador, Admin,
    Topico, Resposta, Categoria, Plataforma
)


def exemplo_1_membros():
    """Demonstra os diferentes tipos de membros."""
    print("\n" + "="*70)
    print("EXEMPLO 1: TIPOS DE MEMBROS E HERANÇA")
    print("="*70)
    
    # Criar membros de diferentes tipos
    comum = MembroComum("João Silva", "joao@email.com", "Desenvolvedor iniciante")
    contribuidor = MembroContribuidor("Maria Santos", "maria@email.com", "Engenheira de software")
    moderador = Moderador("Lucas Oliveira", "lucas@email.com", "Moderador experiente")
    admin = Admin("Arthur Admin", "arthur@email.com", "Administrador da plataforma")
    
    print(f"\n✓ Membros criados:")
    print(f"  {comum}")
    print(f"  {contribuidor}")
    print(f"  {moderador}")
    print(f"  {admin}")
    
    # Ganhando reputação
    print(f"\n--- Ganhando Reputação ---")
    comum.ganhar_reputacao(150)
    comum.atualizar_nivel()
    print(f"Após ganhar 150 pts: {comum}")
    
    contribuidor.ganhar_reputacao(300)
    print(f"Contribuidor: {contribuidor}")


def exemplo_2_topicos():
    """Demonstra POLIMORFISMO: cada tipo cria tópico diferente."""
    print("\n" + "="*70)
    print("EXEMPLO 2: CRIAÇÃO DE TÓPICOS (POLIMORFISMO)")
    print("="*70)
    
    comum = MembroComum("Pedro", "pedro@email.com")
    contribuidor = MembroContribuidor("Ana", "ana@email.com")
    moderador = Moderador("Bruno Mod", "bruno@email.com")
    admin = Admin("Sistema", "admin@email.com")
    
    # POLIMORFISMO: cada tipo cria tópico de forma diferente
    print(f"\n--- Tópico de Membro Comum ---")
    t1 = comum.criar_topico(
        "Dúvida: Como começar com Python?",
        "Sou iniciante e gostaria de saber por onde começar...",
        ["python", "iniciante"]
    )
    print(f"Criado: {t1}")
    print(f"Fixado: {t1.fixado} | Destacado: {t1.destacado}")
    print(f"Reputação de {comum.nome}: {comum.reputacao}")
    
    print(f"\n--- Tópico de Contribuidor (DESTACADO) ---")
    t2 = contribuidor.criar_topico(
        "Tutorial: Boas práticas em Python",
        "Aqui estão as melhores práticas que aprendi...",
        ["python", "tutorial", "boas-práticas"]
    )
    print(f"Criado: {t2}")
    print(f"Fixado: {t2.fixado} | Destacado: {t2.destacado} ⭐")
    print(f"Reputação de {contribuidor.nome}: {contribuidor.reputacao}")
    
    print(f"\n--- Tópico de Moderador (COM SELO) ---")
    t3 = moderador.criar_topico(
        "Aviso: Novas regras do forum",
        "A partir de agora, todos os posts devem...",
        ["anúncio", "regras"]
    )
    print(f"Criado: {t3}")
    print(f"Por moderador: {t3.por_moderador} 🔨")
    
    print(f"\n--- Tópico de Admin (FIXADO) ---")
    t4 = admin.criar_topico(
        "Bem-vindo ao novo fórum!",
        "Este é nosso novo sistema de discussão...",
        ["admin", "bemvindo"]
    )
    print(f"Criado: {t4}")
    print(f"Fixado: {t4.fixado} 📌 | Por admin: {t4.por_admin} 👑")
    
    # Votações
    print(f"\n--- Sistema de Votação ---")
    comum.upvote() if hasattr(comum, 'upvote') else None
    t1.upvote()
    t1.upvote()
    t1.downvote()
    print(f"Tópico 1: {t1.votos_positivos} upvotes, {t1.votos_negativos} downvotes")


def exemplo_3_respostas():
    """Demonstra sistema de respostas e comentários."""
    print("\n" + "="*70)
    print("EXEMPLO 3: RESPOSTAS E INTERAÇÕES")
    print("="*70)
    
    # Criar membros
    autor = MembroComum("Lucas", "lucas@email.com")
    resposta1 = MembroComum("Carlos", "carlos@email.com")
    resposta2 = MembroContribuidor("Diana", "diana@email.com")
    
    # Criar tópico
    topico = autor.criar_topico(
        "Como fazer login com JWT?",
        "Alguém pode me ajudar com autenticação JWT?",
        ["jwt", "autenticação", "backend"]
    )
    
    print(f"\nTópico criado: {topico}")
    print(f"Visualizações iniciais: {topico.visualizacoes}")
    
    # Responder
    print(f"\n--- Adicionando Respostas ---")
    r1 = resposta1.responder(topico, "JWT é um padrão de autenticação seguro. Você pode usar a biblioteca PyJWT.")
    print(f"Resposta 1 adicionada. Reputação de {resposta1.nome}: {resposta1.reputacao}")
    
    r2 = resposta2.responder(topico, "Recomendo estudar esta documentação: https://jwt.io/")
    print(f"Resposta 2 adicionada. Reputação de {resposta2.nome}: {resposta2.reputacao}")
    
    r3 = resposta1.responder(topico, "Concordo com Diana, a documentação é excelente!")
    
    # Marcar como melhor resposta
    print(f"\n--- Marcando Melhor Resposta ---")
    r2.marcar_como_melhor()  # Resposta 2
    print(f"Reputação de {resposta2.nome} agora: {resposta2.reputacao}")
    
    # Exibir tópico completo
    print(topico.exibir())
    print(f"Respostas:")
    for resposta in topico.respostas:
        print(resposta.exibir())


def exemplo_4_moderacao():
    """Demonstra capacidades de moderação."""
    print("\n" + "="*70)
    print("EXEMPLO 4: MODERAÇÃO E PERMISSÕES")
    print("="*70)
    
    comum = MembroComum("Troll", "troll@email.com")
    moderador = Moderador("Carlos Mod", "carlos@email.com")
    admin = Admin("System Admin", "admin@email.com")
    
    # Membro comum tenta moderar (não pode)
    print(f"\n--- Tentativa de Moderação por Comum ---")
    topico_ruim = comum.criar_topico(
        "Spam demais!",
        "Conteúdo inapropriado...",
        ["spam"]
    )
    comum.moderar(topico_ruim)  # Não funciona
    
    # Moderador remove tópico
    print(f"\n--- Moderador Removendo Tópico ---")
    moderador.moderar(topico_ruim)
    print(topico_ruim.exibir())  # Mostra como removido
    
    # Suspender usuário
    print(f"\n--- Suspensão de Usuário ---")
    print(f"Status de {comum.nome}: Ativo = {comum.ativo}")
    moderador.suspender_membro(comum, "Spam repetido")
    print(f"Status de {comum.nome}: Ativo = {comum.ativo}")
    
    # Admin bani permanente
    print(f"\n--- Ban Permanente pelo Admin ---")
    spam_bot = MembroComum("Bot Spam", "bot@email.com")
    admin.banir_permanentemente(spam_bot, "Bot automatizado")
    print(f"Status de {spam_bot.nome}: Ativo = {spam_bot.ativo}")


def exemplo_5_categoria():
    """Demonstra sistema de categorias."""
    print("\n" + "="*70)
    print("EXEMPLO 5: CATEGORIAS E ORGANIZAÇÃO")
    print("="*70)
    
    # Criar membros
    moderador_python = Moderador("Expert Python", "python@email.com")
    moderador_web = Moderador("Expert Web", "web@email.com")
    
    usuarios = [
        MembroComum("Alice", "alice@email.com"),
        MembroComum("Bob", "bob@email.com"),
        MembroContribuidor("Carlos", "carlos@email.com"),
    ]
    
    # Criar categorias
    print(f"\n--- Criando Categorias ---")
    cat_python = Categoria("Python", "Discussões sobre Python", moderador_python)
    cat_web = Categoria("Web Development", "Front-end e Back-end", moderador_web)
    
    # Adicionar tópicos
    print(f"\n--- Adicionando Tópicos às Categorias ---")
    
    t1 = usuarios[0].criar_topico(
        "List comprehension ou for loop?",
        "Qual é mais pythônico?",
        ["python", "performance"]
    )
    cat_python.adicionar_topico(t1)
    
    t2 = usuarios[1].criar_topico(
        "Django vs FastAPI em 2026",
        "Qual framework escolher?",
        ["web", "python"]
    )
    cat_web.adicionar_topico(t2)
    
    t3 = usuarios[2].criar_topico(
        "React vs Vue.js",
        "Comparativo de frameworks front-end",
        ["web", "javascript"]
    )
    cat_web.adicionar_topico(t3)
    
    # Exibir categorias
    print(cat_python.listar_topicos())
    print(cat_web.listar_topicos())


def exemplo_6_plataforma_completa():
    """Demonstra a plataforma completa funcionando."""
    print("\n" + "="*70)
    print("EXEMPLO 6: PLATAFORMA COMPLETA")
    print("="*70)
    
    # Criar plataforma
    plataforma = Plataforma("DevForum 2026")
    
    # Registrar membros
    print(f"\n--- Registrando Membros ---")
    membros = {
        "comum1": MembroComum("João", "joao@email.com"),
        "comum2": MembroComum("Maria", "maria@email.com"),
        "contrib": MembroContribuidor("Pedro", "pedro@email.com"),
        "mod": Moderador("Silva", "silva@email.com"),
        "admin": Admin("Root", "root@email.com"),
    }
    
    for membro in membros.values():
        plataforma.registrar_membro(membro)
    
    # Criar categorias
    print(f"\n--- Criando Categorias ---")
    cat_tech = plataforma.criar_categoria(
        "Tecnologia",
        "Discussões sobre tecnologia em geral",
        membros["mod"]
    )
    
    # Simular atividade
    print(f"\n--- Atividade na Plataforma ---")
    
    # Ganhar reputação
    for _ in range(3):
        membros["comum1"].ganhar_reputacao(50)
    membros["comum1"].atualizar_nivel()
    
    # Criar tópicos
    t1 = membros["comum1"].criar_topico(
        "Qual linguagem aprender em 2026?",
        "Sou iniciante e gostaria de saber...",
        ["linguagens", "carreira"]
    )
    cat_tech.adicionar_topico(t1)
    
    t2 = membros["contrib"].criar_topico(
        "Tendências em AI e ML",
        "As tendências que veremos em 2026...",
        ["ia", "ml", "tendências"]
    )
    cat_tech.adicionar_topico(t2)
    
    # Respostas
    membros["comum2"].responder(t1, "Recomendo aprender Python!")
    membros["contrib"].responder(t1, "Python é excelente para iniciantes.")
    
    # Exibir estado
    print(plataforma.exibir_membros())
    print(plataforma.exibir_categorias())
    print(cat_tech.listar_topicos())
    
    # Exibir logs de admin
    membros["admin"].registrar_log("Plataforma iniciada com sucesso")
    membros["admin"].registrar_log(f"{len(membros)} membros registrados")
    print(membros["admin"].exibir_logs())


if __name__ == "__main__":
    # Executar todos os exemplos
    exemplo_1_membros()
    exemplo_2_topicos()
    exemplo_3_respostas()
    exemplo_4_moderacao()
    exemplo_5_categoria()
    exemplo_6_plataforma_completa()
    
    print("\n" + "="*70)
    print("FIM DA DEMONSTRAÇÃO")
    print("="*70)
    print(f"\n💡 Sistema com:")
    print(f"   • 4 tipos de membros diferentes (Herança)")
    print(f"   • Cada tipo cria tópicos de forma diferente (Polimorfismo)")
    print(f"   • Sistema de reputação e níveis")
    print(f"   • Moderação com diferentes permissões")
    print(f"   • Categorias e organização")
    print(f"   • Respostas e interações")
