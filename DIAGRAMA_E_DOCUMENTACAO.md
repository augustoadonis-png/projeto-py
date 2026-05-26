# SISTEMA DE FÓRUM COLABORATIVO - POO
## Data: 26/05/2026 (Segunda Versão)

---

## 📊 DIAGRAMA DE CLASSES

```
┌────────────────────────┐
│    MEMBRO (ABC)        │  ← Classe Abstrata
├────────────────────────┤
│ - nome                 │
│ - email                │
│ - bio                  │
│ - reputacao            │
│ - data_registro        │
│ - ativo                │
│ - tópicos_criados[]    │
│ - respostas_dadas[]    │
├────────────────────────┤
│ + ganhar_reputacao()   │
│ + perder_reputacao()   │
│ + criar_topico()★      │ ← Abstrato
│ + moderar()★           │ ← Abstrato
│ + responder()          │
└──────────┬─────────────┘
           │
    ┌──────┼──────────┬────────────┐
    │      │          │            │
    ▼      ▼          ▼            ▼
┌─────┐ ┌──┐ ┌─────┐ ┌────────┐
│  1  │ │2 │ │  3  │ │   4    │
└─────┘ └──┘ └─────┘ └────────┘
```

### Subclasses:

**1. MembroComum**
- Nível: Bronze → Prata → Ouro
- Pode criar tópicos normais
- Pode responder
- Não pode moderar
- Ganha 5 pts ao criar tópico

**2. MembroContribuidor** (extends MembroComum)
- Nível: Ouro ⭐
- Tópicos com destaque automático
- Pode editar tópicos
- Não pode moderar
- Ganha 10 pts ao criar tópico

**3. Moderador** (extends Membro)
- Nível: Platina 🔨
- Pode moderar (remover tópicos)
- Pode suspender usuários
- Pode adicionar áreas de moderação
- Tópicos com selo de moderador
- Ganha 15 pts ao criar tópico

**4. Admin** (extends Membro)
- Nível: Diamante 👑
- Controle total
- Pode banir permanentemente
- Tópicos fixados automaticamente
- Registro completo de logs
- Ganha 20 pts ao criar tópico

---

## 🔑 CONCEITOS DE POO IMPLEMENTADOS

### 1. **HERANÇA**
```python
class MembroComum(Membro):
    def __init__(self, nome, email, bio=""):
        super().__init__(nome, email, bio)
        self.nivel = "Bronze"
```
- Membro é a **superclasse**
- MembroComum, MembroContribuidor, Moderador, Admin são **subclasses**
- Cada uma herda atributos e métodos da superclasse

### 2. **POLIMORFISMO**
Cada subclasse implementa `criar_topico()` de forma diferente:

```python
# MembroComum
def criar_topico(self, ...):
    topico = Topico(...)
    # Tópico normal
    return topico

# MembroContribuidor
def criar_topico(self, ...):
    topico = Topico(...)
    topico.destacado = True  # ⭐ Diferente!
    return topico

# Admin
def criar_topico(self, ...):
    topico = Topico(...)
    topico.fixado = True     # 📌 Diferente!
    return topico
```

### 3. **CLASSE ABSTRATA**
```python
class Membro(ABC):
    @abstractmethod
    def criar_topico(self, ...): pass
    
    @abstractmethod
    def moderar(self, item): pass
```
- Não pode ser instanciada diretamente
- Força subclasses a implementar métodos obrigatórios

### 4. **ENCAPSULAMENTO**
```python
- Atributos privados: _id_contador
- Propriedades públicas: nome, email, reputacao
- Métodos para controlar acesso: ganhar_reputacao(), perder_reputacao()
```

### 5. **COMPOSIÇÃO**
```python
class Topico:
    - autor: Membro
    - respostas: List[Resposta]
    - tags: List[str]

class Categoria:
    - moderador_chefe: Moderador
    - tópicos: List[Topico]

class Plataforma:
    - membros: List[Membro]
    - categorias: List[Categoria]
```

---

## 📋 ESTRUTURA DE DADOS ADICIONAL

### Classe Topico
- id (único)
- autor
- titulo
- conteudo
- tags
- data_criacao
- votos_positivos / votos_negativos
- respostas[]
- Status: removido, editado, fixado, destacado, por_moderador, por_admin

### Classe Resposta
- id
- autor
- conteudo
- topico (referência)
- votos
- marcada_como_melhor

### Classe Categoria
- nome
- descricao
- moderador_chefe
- tópicos[]

### Classe Plataforma
- nome
- membros[]
- categorias[]
- tópicos_todos[]

---

## 💼 SISTEMA DE REPUTAÇÃO

| Ação | Pontos |
|------|--------|
| Criar tópico (Comum) | +5 |
| Criar tópico (Contribuidor) | +10 |
| Criar tópico (Moderador) | +15 |
| Criar tópico (Admin) | +20 |
| Responder | +2 |
| Resposta marcada como melhor | +10 |
| Comentário upvotado | +1 |

---

## 🎯 REQUISITOS ATENDIDOS

✅ Mínimo de 3 classes: 4 subclasses de Membro + 3 classes auxiliares = 7 classes
✅ Implementação de herança: Estrutura hierárquica clara
✅ Superclasse abstrata: Membro (ABC)
✅ super().__init__(...): Usado em todas as subclasses
✅ Polimorfismo: criar_topico() diferente em cada tipo
✅ Composição: Post, Resposta, Categoria, Plataforma
✅ Encapsulamento: Controle de acesso via métodos
✅ Código testável: arquivo teste_forum.py com 6 exemplos

---

## 🚀 COMO USAR

```bash
python teste_forum.py
```

Ou importar no seu código:
```python
from forum import MembroComum, Moderador, Admin, Plataforma

# Criar plataforma
plataforma = Plataforma("Meu Fórum")

# Criar membros
usuario = MembroComum("João", "joao@email.com")
plataforma.registrar_membro(usuario)

# Criar tópico
topico = usuario.criar_topico(
    "Meu primeiro tópico",
    "Conteúdo aqui...",
    ["tag1", "tag2"]
)

# Responder
resposta = usuario.responder(topico, "Ótimo tópico!")
```

---

## 📈 MELHORIAS FUTURAS (v3, v4)

- Sistema de notificações
- Busca de tópicos (por tag, autor, data)
- Sistema de mensagens privadas
- Backup e restore de dados
- Dashboard de estatísticas
- Interface web com Flask
- Banco de dados (SQLite/PostgreSQL)
- Autenticação com JWT
- Sistema de reportes

---

**Desenvolvido por: Aluno**
**Data: 26/05/2026**
**Versão: 2.0**
