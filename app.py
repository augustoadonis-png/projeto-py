from flask import Flask, render_template, request, jsonify
from main import Cadastro

app = Flask(__name__)

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    """Processa o cadastro"""
    try:
        dados = request.get_json()
        email = dados.get('email', '').strip()
        nome_usuario = dados.get('nome_usuario', '').strip()
        senha = dados.get('senha', '').strip()
        
        # Cria um objeto Cadastro
        cadastro = Cadastro(email, nome_usuario, senha)
        
        # Valida os dados
        valido, mensagem = cadastro.validar()
        
        if not valido:
            return jsonify({'sucesso': False, 'mensagem': mensagem}), 400
        
        # Se chegou aqui, está tudo certo!
        return jsonify({
            'sucesso': True, 
            'mensagem': 'Cadastro realizado com sucesso!',
            'usuario': str(cadastro)
        }), 201
        
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': f'Erro: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
