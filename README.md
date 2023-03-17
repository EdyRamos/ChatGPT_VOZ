# ChatGPT_VOZ

ChatGPT_VOZ é um assistente conversacional simples e amigável, baseado no GPT-3 da OpenAI. Desenvolvido em Python, este projeto utiliza o Tkinter para criar uma interface gráfica de usuário intuitiva.

## Recursos

- Interface gráfica amigável para interação
- Suporte para entrada de texto e voz
- Texto para voz usando gTTS (Google Text-to-Speech)
- Reconhecimento de voz usando a API do Google
- Configuração personalizável de volume e velocidade da fala

## Instalação

1. Clone este repositório:
git clone https://github.com/seu_usuario/ChatGPT_VOZ.git

2. Instale as dependências:
```python
pip install -r requirements.txt
```

3. Adicione sua chave da API OpenAI em `credentials.py`:
```python
API_KEY = "sua_chave_da_api_aqui"
```
4. Execute o programa:
```python
python chatgpt.py
```

# Uso
1. Digite sua mensagem ou Aperte o botão "falar" na interface do aplicativo.
2. A resposta gerada pelo ChatGPT será exibida na tela e lida em voz alta.
3. Salve a conversa no arquivo 'conversation.txt' clicando no botão "Salvar conversa".

# Licença
Este projeto está licenciado sob a licença MIT.
