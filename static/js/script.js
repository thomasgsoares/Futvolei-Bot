// script.js

const chatHistory = document.getElementById('chatHistory');
const promptInput = document.getElementById('promptInput');
const sendButton = document.getElementById('sendButton');
const chatEndpoint = '/chat'; // Rota do Flask

// Adiciona o evento 'Enter' para enviar
promptInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

/**
 * Adiciona uma nova mensagem ao histórico do chat.
 * @param {string} text - O conteúdo da mensagem.
 * @param {('user'|'ia')} sender - Quem enviou a mensagem.
 */
function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'ia-message');
    
    // Adiciona o texto e formata quebras de linha (opcionalmente)
    messageDiv.innerHTML = text.replace(/\n/g, '<br>');
    
    chatHistory.appendChild(messageDiv);
    
    // Mantém a rolagem no final
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * Envia a mensagem do usuário para o back-end e recebe a resposta da IA.
 */
async function sendMessage() {
    const prompt = promptInput.value.trim();
    if (prompt === '') return;

    // 1. Desabilita a interface e exibe a mensagem do usuário
    sendButton.disabled = true;
    promptInput.value = '';
    appendMessage(prompt, 'user');

    try {
        // 2. Faz a chamada POST para o servidor Flask
        const response = await fetch(chatEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });

        // 3. Processa a resposta
        const data = await response.json();
        
        // 4. Exibe a resposta da IA
        const iaResponse = data.response || "Erro: Não foi possível obter uma resposta.";
        appendMessage(iaResponse, 'ia');

    } catch (error) {
        console.error('Erro na comunicação com o servidor:', error);
        appendMessage("Desculpe, houve um erro de conexão com o servidor.", 'ia');
    } finally {
        // 5. Reabilita a interface
        sendButton.disabled = false;
        promptInput.focus();
    }
}