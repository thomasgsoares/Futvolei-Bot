# app.py

import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

# --- Configuração do Flask ---
app = Flask(__name__)

# --- Configuração da API do Gemini ---
# ⚠️ IMPORTANTE: SUBSTITUA 'SUA_CHAVE_REAL_AQUI' PELA SUA CHAVE REAL DO GEMINI.
# Esta é a principal causa de erros de inicialização.
GEMINI_API_KEY = "AIzaSyDw1AArRRvtOuDeQPfhojj3y6IwCscxb0U" 

# Variáveis globais para o chat e erros de inicialização
chat = None 
init_error = None 

# Bloco de inicialização
try:
    if GEMINI_API_KEY == "SUA_CHAVE_REAL_AQUI" or not GEMINI_API_KEY:
        raise ValueError("API Key não foi configurada. Por favor, substitua a placeholder pela sua chave real.")
    
    # 1. Inicializa o cliente Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Define as instruções do sistema para o especialista em futevôlei
    FUTEVOLEI_SYSTEM_INSTRUCTION = (
        "Você é um assistente especialista em futevôlei. "
        "Seu objetivo é responder a todas as perguntas sobre regras, "
        "técnicas (como shark attack, toque, bloqueio, etc.), história e "
        "jogadores famosos de futevôlei de forma clara e concisa."
    )

    config = types.GenerateContentConfig(
        system_instruction=FUTEVOLEI_SYSTEM_INSTRUCTION
    )

    # 2. Cria a instância do chat (mantém o histórico)
    chat = client.chats.create(model="gemini-2.5-flash", config=config)
    print("✅ Cliente Gemini e Chat inicializados com sucesso.")

# Captura erros de API ou qualquer falha na inicialização
except Exception as e:
    # Armazena o erro para ser retornado no endpoint /chat
    init_error = f"Erro ao inicializar a API: Verifique sua chave ou conexão. Detalhe: {e}"
    print(f"❌ ERRO GRAVE DE INICIALIZAÇÃO: {init_error}")

# --- Rotas do Flask ---

@app.route('/')
def index():
    """Rota principal que renderiza o template HTML."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    """
    Rota que recebe a pergunta do front-end, processa com o Gemini
    e retorna a resposta.
    """
    # Para ter certeza que a função acessa o objeto chat global.
    global chat 
    
    # 1. Verifica se a inicialização falhou
    if init_error:
        # Se falhou (ex: chave inválida), retorna o erro específico
        return jsonify({"response": f"ERRO DE CONFIGURAÇÃO: {init_error}"}), 500

    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '').strip()

        if not user_prompt:
            return jsonify({"response": "Por favor, digite sua pergunta."}), 400

        # 2. Envia a mensagem para o Gemini (o objeto 'chat' está garantido)
        print(f"Processando prompt: {user_prompt}")
        response = chat.send_message(user_prompt)
        
        # 3. Retorna a resposta do Gemini
        return jsonify({"response": response.text})

    except Exception as e:
        # Captura erros durante a chamada (ex: problemas de rede ou cota)
        error_msg = f"Erro em tempo de execução com a IA: {e}"
        print(f"❌ ERRO EM TEMPO REAL: {error_msg}")
        return jsonify({"response": "Desculpe, ocorreu um erro durante a comunicação com a IA."}), 500

if __name__ == '__main__':
    # Garante que as pastas de arquivos estáticos existem
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
        
    # Executa o servidor Flask
    app.run(debug=True)