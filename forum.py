from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Membro(ABC):
    """
    Classe abstrata que representa um membro da plataforma.
    
    Superclasse com atributos e métodos comuns.
    Subclasses: MembroComum, MembroContribuidor, Moderador, Admin
    """
    
    def __init__(self, nome: str, email: str, bio: str = ""):
        self.nome = nome
        self.email = email
        self.bio = bio
        self.reputacao = 0
        self.data_registro = datetime.now().strftime("%d/%m/%Y")
        self.ativo = True
        self.tópicos_criados: List['Topico'] = []
        self.respostas_dadas: List['Resposta'] = []
    
    def ganhar_reputacao(self, pontos: int):
        """Ganha pontos de reputação."""
        self.reputacao += pontos
    
    def perder_reputacao(self, pontos: int):
        """Perde pontos de reputação."""
        self.reputacao = max(0, self.reputacao - pontos)
    
    @abstractmethod
    def criar_topico(self, titulo: str, conteudo: str, tags: List[str]) -> 'Topico':
        """Método abstrato: criar um tópico."""
        pass
    
    @abstractmethod
    def moderar(self, item):
        """Método abstrato: capacidade de moderar."""
        pass
    
    def responder(self, topico: 'Topico', conteudo: str) -> 'Resposta':
        """Responde a um tópico."""
        if not self.ativo:
            print(f"⚠ {self.nome} está suspenso.")
            return None
        
        resposta = Resposta(self, conteudo, topico)
        self.respostas_dadas.append(resposta)
        topico.respostas.append(resposta)
        self.ganhar_reputacao(2)
        return resposta
    
    def __str__(self) -> str:
        return f"{self.nome} ({self.__class__.__name__}) - Reputação: {self.reputacao}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.nome}')"


class MembroComum(Membro):
    """
    Membro básico da plataforma.
    Pode criar tópicos e responder, mas não pode moderar.
    """
    
    def __init__(self, nome: str, email: str, bio: str = ""):
        super().__init__(nome, email, bio)
        self.nivel = "Bronze"
    
    def criar_topico(self, titulo: str, conteudo: str, tags: List[str]) -> 'Topico':
        """Cria um novo tópico."""
        if not self.ativo:
            print(f"⚠ {self.nome} está suspenso e não pode criar tópicos.")
            return None
        
        topico = Topico(self, titulo, conteudo, tags)
        self.tópicos_criados.append(topico)
        self.ganhar_reputacao(5)
        return topico
    
    def moderar(self, item):
        """Membro comum não pode moderar."""
        print(f"⚠ {self.nome} não tem permissão para moderar.")
        return False
    
    def atualizar_nivel(self):
        """Atualiza nível baseado em reputação."""
        if self.reputacao >= 100:
            self.nivel = "Prata"
        if self.reputacao >= 500:
            self.nivel = "Ouro"
    
    def __str__(self) -> str:
        return f"{self.nome} [{self.nivel}] - Rep: {self.reputacao}"


class MembroContribuidor(Membro):
    """
    Membro que contribui bastante e tem mais privilégios.
    Pode criar e editar tópicos, mas ainda não modera.
    """
    
    def __init__(self, nome: str, email: str, bio: str = ""):
        super().__init__(nome, email, bio)
        self.nivel = "Ouro"
        self.tópicos_editados = 0
    
    def criar_topico(self, titulo: str, conteudo: str, tags: List[str]) -> 'Topico':
        """Cria tópico com destaque automático."""
        topico = Topico(self, titulo, conteudo, tags)
        topico.destacado = True  # Tópicos de contribuidores têm destaque
        self.tópicos_criados.append(topico)
        self.ganhar_reputacao(10)  # Ganha mais reputação
        return topico
    
    def editar_topico(self, topico: 'Topico', novo_conteudo: str) -> bool:
        """Pode editar tópicos (seus ou de outros)."""
        topico.conteudo = novo_conteudo
        topico.editado = True
        topico.ultima_edicao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.tópicos_editados += 1
        print(f"✓ {self.nome} editou o tópico: {topico.titulo}")
        return True
    
    def moderar(self, item):
        """Contribuidor ainda não pode moderar."""
        print(f"⚠ {self.nome} não tem permissão para moderar.")
        return False
    
    def __str__(self) -> str:
        return f"🌟 {self.nome} [Contribuidor] - Rep: {self.reputacao}"


class Moderador(Membro):
    """
    Moderador da plataforma.
    Pode moderar tópicos, resposta e usuários.
    """
    
    def __init__(self, nome: str, email: str, bio: str = ""):
        super().__init__(nome, email, bio)
        self.nivel = "Platina"
        self.areas_moderacao: List[str] = []
        self.tópicos_removidos = 0
        self.usuarios_suspensos = []
    
    def criar_topico(self, titulo: str, conteudo: str, tags: List[str]) -> 'Topico':
        """Moderador cria tópico com selo de moderador."""
        topico = Topico(self, titulo, conteudo, tags)
        topico.por_moderador = True
        self.tópicos_criados.append(topico)
        self.ganhar_reputacao(15)
        return topico
    
    def moderar(self, topico: 'Topico') -> bool:
        """Remove/fecha um tópico."""
        if topico.removido:
            print(f"⚠ Tópico já foi removido.")
            return False
        
        topico.removido = True
        self.tópicos_removidos += 1
        print(f"✓ {self.nome} removeu: {topico.titulo}")
        return True
    
    def adicionar_area(self, area: str):
        """Adiciona uma área de moderação."""
        if area not in self.areas_moderacao:
            self.areas_moderacao.append(area)
            print(f"✓ {self.nome} agora modera: {area}")
    
    def suspender_membro(self, membro: Membro, motivo: str):
        """Suspende um membro."""
        membro.ativo = False
        self.usuarios_suspensos.append({
            "membro": membro.nome,
            "motivo": motivo,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        print(f"✓ {membro.nome} foi suspenso. Motivo: {motivo}")
    
    def __str__(self) -> str:
        return f"🔨 Moderador {self.nome} - Rep: {self.reputacao} - Áreas: {len(self.areas_moderacao)}"


class Admin(Membro):
    """
    Administrador da plataforma.
    Tem controle total sobre tudo.
    """
    
    def __init__(self, nome: str, email: str, bio: str = ""):
        super().__init__(nome, email, bio)
        self.nivel = "Diamante"
        self.logs_admin: List[str] = []
    
    def criar_topico(self, titulo: str, conteudo: str, tags: List[str]) -> 'Topico':
        """Admin cria tópico fixado automaticamente."""
        topico = Topico(self, titulo, conteudo, tags)
        topico.fixado = True
        topico.por_admin = True
        self.tópicos_criados.append(topico)
        self.registrar_log(f"Tópico fixado criado: {titulo}")
        self.ganhar_reputacao(20)
        return topico
    
    def moderar(self, topico: 'Topico') -> bool:
        """Admin pode deletar permanentemente."""
        topico.removido = True
        topico.deletado_permanentemente = True
        self.registrar_log(f"Tópico deletado permanentemente: {topico.titulo}")
        return True
    
    def banir_permanentemente(self, membro: Membro, motivo: str):
        """Bani permanente de um membro."""
        membro.ativo = False
        self.registrar_log(f"Membro banido permanentemente: {membro.nome}. Motivo: {motivo}")
        print(f"🚫 {membro.nome} foi BANIDO PERMANENTEMENTE")
    
    def registrar_log(self, descricao: str):
        """Registra uma ação no log."""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.logs_admin.append(f"[{timestamp}] {descricao}")
    
    def exibir_logs(self) -> str:
        """Exibe logs de admin."""
        display = f"\n{'='*60}\n"
        display += f"LOGS DO ADMIN: {self.nome}\n"
        display += f"{'='*60}\n"
        if not self.logs_admin:
            display += "Nenhuma ação registrada.\n"
        else:
            for log in self.logs_admin[-10:]:
                display += f"{log}\n"
        display += f"{'='*60}\n"
        return display
    
    def __str__(self) -> str:
        return f"👑 ADMIN {self.nome} - Rep: {self.reputacao}"


class Topico:
    """Representa um tópico/discussão na plataforma."""
    
    _id_contador = 0
    
    def __init__(self, autor: Membro, titulo: str, conteudo: str, tags: List[str]):
        Topico._id_contador += 1
        self.id = Topico._id_contador
        self.autor = autor
        self.titulo = titulo
        self.conteudo = conteudo
        self.tags = tags
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.votos_positivos = 0
        self.votos_negativos = 0
        self.respostas: List['Resposta'] = []
        self.visualizacoes = 0
        
        # Status
        self.removido = False
        self.deletado_permanentemente = False
        self.editado = False
        self.ultima_edicao = None
        
        # Destaque
        self.fixado = False
        self.destacado = False
        self.por_moderador = False
        self.por_admin = False
    
    def upvote(self):
        """Vota positivamente."""
        self.votos_positivos += 1
    
    def downvote(self):
        """Vota negativamente."""
        self.votos_negativos += 1
    
    def exibir(self) -> str:
        """Exibe o tópico formatado."""
        if self.removido:
            return "[TÓPICO REMOVIDO]"
        
        if self.deletado_permanentemente:
            return "[TÓPICO DELETADO PERMANENTEMENTE]"
        
        display = f"\n{'='*60}\n"
        
        # Ícones especiais
        if self.fixado:
            display += "📌 [FIXADO] "
        if self.destacado:
            display += "⭐ [DESTACADO] "
        if self.por_moderador:
            display += "🔨 [POR MODERADOR] "
        if self.por_admin:
            display += "👑 [POR ADMIN] "
        
        display += f"\nTÓPICO #{self.id}: {self.titulo}\n"
        display += f"{'='*60}\n"
        display += f"Autor: {self.autor.nome}\n"
        display += f"Data: {self.data_criacao}\n"
        display += f"Tags: {', '.join(self.tags) if self.tags else 'Sem tags'}\n"
        
        if self.editado:
            display += f"Editado em: {self.ultima_edicao}\n"
        
        display += f"\n{self.conteudo}\n"
        display += f"\n👍 {self.votos_positivos} | 👎 {self.votos_negativos}\n"
        display += f"👁️ {self.visualizacoes} visualizações\n"
        display += f"💬 {len(self.respostas)} respostas\n"
        display += f"{'='*60}\n"
        
        return display
    
    def __str__(self) -> str:
        return f"Tópico #{self.id}: {self.titulo}"


class Resposta:
    """Representa uma resposta a um tópico."""
    
    _id_contador = 0
    
    def __init__(self, autor: Membro, conteudo: str, topico: Topico):
        Resposta._id_contador += 1
        self.id = Resposta._id_contador
        self.autor = autor
        self.conteudo = conteudo
        self.topico = topico
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.votos_positivos = 0
        self.votos_negativos = 0
        self.respostas_ao_comentario: List['Resposta'] = []
        self.marcada_como_melhor = False
    
    def marcar_como_melhor(self):
        """Marca essa resposta como a melhor."""
        self.marcada_como_melhor = True
        self.autor.ganhar_reputacao(10)  # Bonus de reputação
        print(f"✓ Resposta de {self.autor.nome} marcada como melhor resposta!")
    
    def exibir(self) -> str:
        """Exibe a resposta formatada."""
        marca = "🏆 " if self.marcada_como_melhor else ""
        return (f"{marca}💬 {self.autor.nome}: {self.conteudo}\n"
                f"   Data: {self.data_criacao} | "
                f"👍 {self.votos_positivos} | 👎 {self.votos_negativos}\n")
    
    def __str__(self) -> str:
        return f"Resposta #{self.id} por {self.autor.nome}"


class Categoria:
    """Representa uma categoria/seção da plataforma."""
    
    def __init__(self, nome: str, descricao: str, moderador_chefe: Moderador):
        self.nome = nome
        self.descricao = descricao
        self.moderador_chefe = moderador_chefe
        self.tópicos: List[Topico] = []
        self.criada_em = datetime.now().strftime("%d/%m/%Y")
    
    def adicionar_topico(self, topico: Topico):
        """Adiciona um tópico à categoria."""
        if topico not in self.tópicos:
            self.tópicos.append(topico)
    
    def listar_topicos(self) -> str:
        """Lista tópicos da categoria."""
        listing = f"\n{'='*60}\n"
        listing += f"CATEGORIA: {self.nome}\n"
        listing += f"Descrição: {self.descricao}\n"
        listing += f"Moderador: {self.moderador_chefe.nome}\n"
        listing += f"Criada em: {self.criada_em}\n"
        listing += f"Tópicos: {len(self.tópicos)}\n"
        listing += f"{'='*60}\n"
        
        if not self.tópicos:
            listing += "Nenhum tópico ainda.\n"
        else:
            for topico in self.tópicos[-5:]:
                if not topico.removido:
                    marca = "📌" if topico.fixado else "⭐" if topico.destacado else "•"
                    listing += f"  {marca} {topico.titulo} ({len(topico.respostas)} respostas)\n"
        
        listing += f"{'='*60}\n"
        return listing
    
    def __str__(self) -> str:
        return f"{self.nome} ({len(self.tópicos)} tópicos)"


class Plataforma:
    """Gerenciador central da plataforma."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.membros: List[Membro] = []
        self.categorias: List[Categoria] = []
        self.tópicos_todos: List[Topico] = []
    
    def registrar_membro(self, membro: Membro):
        """Registra um novo membro."""
        if membro not in self.membros:
            self.membros.append(membro)
            print(f"✓ {membro.nome} se registrou em {self.nome}")
    
    def criar_categoria(self, nome: str, descricao: str, moderador: Moderador):
        """Cria uma nova categoria."""
        categoria = Categoria(nome, descricao, moderador)
        self.categorias.append(categoria)
        print(f"✓ Categoria '{nome}' criada!")
        return categoria
    
    def exibir_membros(self) -> str:
        """Exibe todos os membros."""
        display = f"\n{'='*60}\n"
        display += f"MEMBROS EM {self.nome}\n"
        display += f"{'='*60}\n"
        
        # Ordena por reputação
        membros_ordenados = sorted(self.membros, key=lambda x: x.reputacao, reverse=True)
        
        for i, membro in enumerate(membros_ordenados, 1):
            status = "✅" if membro.ativo else "🚫"
            display += f"{i}. {status} {membro}\n"
        
        display += f"{'='*60}\n"
        return display
    
    def exibir_categorias(self) -> str:
        """Exibe todas as categorias."""
        display = f"\n{'='*60}\n"
        display += f"CATEGORIAS EM {self.nome}\n"
        display += f"{'='*60}\n"
        
        for categoria in self.categorias:
            display += f"  • {categoria}\n"
        
        display += f"{'='*60}\n"
        return display
    
    def __str__(self) -> str:
        return f"{self.nome} ({len(self.membros)} membros, {len(self.categorias)} categorias)"
