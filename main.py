class Cadastro:
    def __init__(self, email, nome_usuario, senha):
        self.email = email
        self.nome_usuario = nome_usuario
        self.senha = senha
    
    def validar(self):
        """Valida os dados do cadastro"""
        if "@" not in self.email:
            return False, "Email inválido!"
        if len(self.senha) < 6:
            return False, "Senha deve ter no mínimo 6 caracteres!"
        if len(self.nome_usuario) < 3:
            return False, "Nome de usuário deve ter no mínimo 3 caracteres!"
        return True, "Cadastro válido!"
    
    def __str__(self):
        return f"Email: {self.email} | Usuário: {self.nome_usuario}"