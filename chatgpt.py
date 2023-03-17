import tkinter as tk
import time
import random
import queue
import openai
import os
import sys
import pygame
from datetime import datetime
from gtts import gTTS
from speech_recognition import Microphone, Recognizer, UnknownValueError
from credentials import API_KEY

LANGUAGE = 'pt-BR'  # Defina a língua padrão aqui

class ChatGPT():

    def __init__(self):
        self.rec = Recognizer()
        self.mic = Microphone()
        #self.mixer_lock = threading.Lock()    

    
    def voice_to_text(self, source, language=LANGUAGE):
        print('Ajustando ao ambiente...')

        self.rec.adjust_for_ambient_noise(source, duration=0.5)
        print('Ouvindo...')
        audio = self.rec.listen(source)

        try:
            print('Fazendo o reconhecimento da fala...')
            text = self.rec.recognize_google(audio, language=language)
            return text.capitalize()
        except UnknownValueError:
            pass

    def text_to_voice(self, text, language=LANGUAGE, slow=False, volume=1.0):
        print('Convertendo texto em fala...')
        tts = gTTS(text, lang=language, tld='com.br', slow=slow)
        filename = str(int(datetime.now().timestamp())) + '.mp3'
        tts.save(filename)
        self.play_audio(filename, volume)

    def play_audio(self, filename, volume=1.0):
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

        if os.path.exists(filename):
            os.remove(filename)


    def chat_gpt_conv(self, prompt, n_tokens, api_key, language=LANGUAGE):
        openai.api_key = api_key
        print('Pensando...')
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0,
            max_tokens=n_tokens,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response['choices'][0]['text']
    
    def save_conversation(self):
        with open("conversation.txt", "w") as f:
            f.write(self.text_widget.get(1.0, "end"))


class ChatGPT_GUI(ChatGPT):

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("ChatGPT")
        self.app_is_active = True
        self.running = True

        self.master.protocol("WM_DELETE_WINDOW", self.exit_app)

        self.text_widget = tk.Text(self.master, wrap='word')
        self.text_widget.grid(row=0, column=0, columnspan=5, sticky='nsew')
        
        self.entry_widget = tk.Entry(self.master)
       
        self.entry_widget.grid(row=1, column=0, columnspan=5, sticky='ew')
        self.entry_widget.bind('<Return>', self.send_text)

        self.speech_button = tk.Button(self.master, text="Falar", command=self.speech_input)
        self.speech_button.grid(row=2, column=0)

        self.save_button = tk.Button(self.master, text="Salvar conversa", command=self.save_conversation)
        self.save_button.grid(row=2, column=1)
        self.volume_label = tk.Label(self.master, text="Volume (0.0 a 1.0):")
        self.volume_label.grid(row=2, column=2)

        self.volume_var = tk.DoubleVar(value=1.0)
        self.volume_entry = tk.Entry(self.master, textvariable=self.volume_var, width=5)
        self.volume_entry.grid(row=2, column=3)

        self.slow_label = tk.Label(self.master, text="Velocidade da fala:")
        self.slow_label.grid(row=3, column=0)

        self.slow_var = tk.BooleanVar()
        self.slow_checkbox = tk.Checkbutton(self.master, text="Lenta", variable=self.slow_var)
        self.slow_checkbox.grid(row=3, column=1)

        self.stop_button = tk.Button(self.master, text="Parar leitura", command=self.stop_voice)
        self.stop_button.grid(row=3, column=2)

        self.exit_button = tk.Button(self.master, text="Sair", command=self.exit_app)
        self.exit_button.grid(row=3, column=3)

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=1)
        self.master.rowconfigure(0, weight=1)

    def stop_voice(self):
        if pygame.mixer.get_init():  # Verifique se o mixer está inicializado
            pygame.mixer.music.stop()

    def exit_app(self):
        self.running = False
        self.app_is_active = False
        
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        self.master.quit()
        self.master.destroy()
        sys.exit(0)

    def send_text(self, event):
        user_text = self.entry_widget.get()
        self.text_widget.insert('end', f"Você: {user_text}\n")
        self.entry_widget.delete(0, 'end')

        response = self.chat_gpt_conv(
            prompt=user_text,
            api_key=API_KEY,
            n_tokens=4000
        )
        self.text_widget.insert('end', f"ChatGPT: {response}\n")

    def speech_input(self):
        try:
            with self.mic as source:
                prompt = self.voice_to_text(source)
                if prompt is not None:
                    self.text_widget.insert('end', f"Você: {prompt}\n")
                    response = self.chat_gpt_conv(
                        prompt=prompt,
                        api_key=API_KEY,
                        n_tokens=4000
                    )
                    if response is not None:
                        self.text_widget.insert('end', f"ChatGPT: {response}\n")
                        self.text_to_voice(response, slow=self.slow_var.get(), volume=self.volume_var.get())
        finally:
            if self.mic.stream:
                self.mic.exit(None, None, None)

def save_conversation(self):
    with open("conversation.txt", "w") as f:
        f.write(self.text_widget.get(1.0, "end"))

def handle_exception(exc_type, exc_value, exc_traceback):
    print("Ocorreu uma exceção:")
    print("Tipo:", exc_type)
    print("Valor:", exc_value)
    print("Rastreamento:", exc_traceback)
    chat_gpt_gui.exit_app()

if __name__ == "__main__":
    root = tk.Tk()
    chat_gpt_gui = ChatGPT_GUI(root)
    sys.excepthook = handle_exception
    root.mainloop()