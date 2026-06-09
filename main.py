# Sistema tipo Reddit com POO e Herança

from datetime import datetime

class Usuario:
    """Superclasse que representa um usuário do sistema."""
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.data_criacao = datetime.now()
    
    def exibir_perfil(self):
        """Exibe informações do usuário."""
        return f"@{self.username} ({self.email}) - Membro desde {self.data_criacao.strftime('%d/%m/%Y')}"


class Conteudo:
    """Superclasse para conteúdos que podem ser votados (Posts e Comentários)."""
    
    def __init__(self, autor, texto):
        self.autor = autor
        self.texto = texto
        self.upvotes = 0
        self.downvotes = 0
        self.data_criacao = datetime.now()
    
    def upvotar(self):
        """Adiciona um upvote."""
        self.upvotes += 1
    
    def downvotar(self):
        """Adiciona um downvote."""
        self.downvotes += 1
    
    def calcular_pontuacao(self):
        """Calcula a pontuação líquida do conteúdo."""
        return self.upvotes - self.downvotes
    
    def exibir_conteudo(self):
        """Exibe o conteúdo com votação."""
        pontuacao = self.calcular_pontuacao()
        return f"{self.texto}\n👤 {self.autor.username} | 👍 {self.upvotes} 👎 {self.downvotes} | Pontuação: {pontuacao}"


class Post(Conteudo):
    """Subclasse de Conteudo com título e comentários."""
    
    def __init__(self, autor, titulo, texto):
        super().__init__(autor, texto)
        self.titulo = titulo
        self.comentarios = []
    
    def adicionar_comentario(self, comentario):
        """Adiciona um comentário ao post."""
        self.comentarios.append(comentario)
    
    def exibir_post(self):
        """Exibe o post completo."""
        pontuacao = self.calcular_pontuacao()
        info = f"\n{'='*60}\n"
        info += f"📰 TÍTULO: {self.titulo}\n"
        info += f"👤 Por: {self.autor.username} | {self.data_criacao.strftime('%d/%m/%Y %H:%M')}\n"
        info += f"📝 {self.texto}\n"
        info += f"👍 {self.upvotes} 👎 {self.downvotes} | Pontuação: {pontuacao}\n"
        
        if self.comentarios:
            info += f"\n💬 {len(self.comentarios)} Comentário(s):\n"
            for i, coment in enumerate(self.comentarios, 1):
                info += f"  {i}. {coment.exibir_comentario()}\n"
        
        info += f"{'='*60}\n"
        return info


class Comentario(Conteudo):
    """Subclasse de Conteudo para comentários em posts."""
    
    def __init__(self, autor, texto, post):
        super().__init__(autor, texto)
        self.post = post
    
    def exibir_comentario(self):
        """Exibe o comentário de forma simplificada."""
        pontuacao = self.calcular_pontuacao()
        return f"@{self.autor.username}: {self.texto} [👍 {self.upvotes} 👎 {self.downvotes}]"


class Reddit:
    """Gerenciador da rede social tipo Reddit."""
    
    def __init__(self):
        self.posts = []
        self.usuarios = []
    
    def criar_usuario(self, username, email):
        """Cria um novo usuário."""
        usuario = Usuario(username, email)
        self.usuarios.append(usuario)
        return usuario
    
    def criar_post(self, autor, titulo, texto):
        """Cria um novo post."""
        post = Post(autor, titulo, texto)
        self.posts.append(post)
        return post
    
    def exibir_feed(self):
        """Exibe todos os posts em ordem de pontuação."""
        posts_ordenados = sorted(self.posts, key=lambda p: p.calcular_pontuacao(), reverse=True)
        feed = "\n" + "🔥 FEED REDDIT 🔥".center(60) + "\n"
        for post in posts_ordenados:
            feed += post.exibir_post()
        return feed


# ============ TESTES DO SISTEMA ============

def main():
    reddit = Reddit()
    
    # Criando usuários
    user1 = reddit.criar_usuario("Gutovx","gutovx@reddit.com")
    user2 = reddit.criar_usuario("Sr master","sr_master@reddit.com")
    user3 = reddit.criar_usuario("Midnight fire","midnight_fire@reddit.com")
    
    # Exibindo perfis
    print("\n--- Usuários do Sistema ---")
    print(user1.exibir_perfil())
    print(user2.exibir_perfil())
    print(user3.exibir_perfil())
    
    # Criando posts
    post1 = reddit.criar_post(user1, "palmeras ou flamengo", "Palmeiras não tem mundial")
    post2 = reddit.criar_post(user2, "cs e melhor que overwatch", "fallen top global")
    post3 = reddit.criar_post(user3, "brasil vai ser hexa em 2026", "com toda certeza")
    
    # Adicionando comentários
    coment1 = Comentario(user2, "Concordo!", post1)
    coment2 = Comentario(user3, "inveja foda ", post1)
    coment3 = Comentario(user1, "Concordo grande fallen", post2)
    coment4 = Comentario(user1, "vamo ney", post3)
    
    post1.adicionar_comentario(coment1)
    post1.adicionar_comentario(coment2)
    post2.adicionar_comentario(coment3)
    post3.adicionar_comentario(coment4)
    
    # Votando em conteúdos (Testando Polimorfismo)
    print("\n--- Votando em Posts e Comentários ---")
    post1.upvotar()
    post1.upvotar()
    post1.upvotar()
    post1.downvotar()
    
    post2.upvotar()
    post2.upvotar()
    
    coment1.upvotar()
    coment1.upvotar()
    coment2.upvotar()
    
    print("✅ Votos adicionados!")
    
    # Exibindo feed
    print(reddit.exibir_feed())
    
    # Demonstração de Herança
    print("\n--- Demonstração de Herança ---")
    print(f"Post herda de Conteudo:")
    print(f"  - Método da superclasse: calcular_pontuacao() = {post1.calcular_pontuacao()}")
    print(f"  - Atributo próprio: titulo = '{post1.titulo}'")
    print(f"\nComentario herda de Conteudo:")
    print(f"  - Método da superclasse: calcular_pontuacao() = {coment1.calcular_pontuacao()}")
    print(f"  - Atributo próprio: texto = '{coment1.texto}'")


if __name__ == "__main__":
    main()
 