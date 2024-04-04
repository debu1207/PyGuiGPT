import os
from dotenv import load_dotenv
from tkinter import END
from openai import OpenAI
from customtkinter import set_appearance_mode, set_default_color_theme, CTk, CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkScrollableFrame, CTkTextbox, CTkImage
from PIL import Image
import pyperclip
import time


load_dotenv()
API_KEY= os.getenv('API_KEY')
current_path = os.path.dirname(os.path.realpath(__file__))
set_appearance_mode("light")
set_default_color_theme("green")

class Message():
    def __init__(self, window, prompt, message, row, height):
        self.window = window
        self.prompt = prompt
        self.message = message
        self.row = row
        self.height = height

        self.user = CTkLabel(
            self.window,
            text="YOU",
            width=50,
            height=20,
        )
        self.user.grid(row=self.row, column=0, padx=10, sticky='w')

        self.userPrompt = CTkTextbox(
            self.window,
            width=620,
            height=30,
        )
        self.userPrompt.grid(row=self.row +1, column=0, padx=5, pady=(0,10))
        self.userPrompt.insert(0.0, self.prompt)

        self.ai = CTkLabel(
            self.window,
            text="GPT",
            width=50,
            height=20,
        )
        self.ai.grid(row=self.row +2, column=0, padx=10, sticky='w')

        self.messageBox = CTkTextbox(
            self.window, 
            width=620,
            height=self.height,
            text_color='white',
            font=("Consolas", 15),
            fg_color="#064FA0"
        )
        self.messageBox.grid(row=self.row +3, column=0, columnspan=10, padx=5, pady=(0,5))
        self.messageBox.insert(0.0, self.message)

        self.copyIcon = CTkImage(Image.open(current_path + "\\copy.png"), size=(15, 20))
        self.copyBtn = CTkButton(
            self.window,
            text="",
            width=20,
            image=self.copyIcon,
            fg_color="#72AFF3",
            command=self.copyMessage
        )
        self.copyBtn.grid(row=self.row+4, column=0, sticky='w')
    
    def copyMessage(self):
        pyperclip.copy(self.message)
        self.copyStatus = CTkLabel(
            self.window,
            text = "Copied"
        )
        self.copyStatus.grid(row=self.row + 1, column = 0, padx=10)

class App(CTk):
    resPosX = 20
    frameRow = 0

    def __init__(self):
        super().__init__()

        # Define OpenAI client
        self.client = OpenAI(api_key = API_KEY)

        # Window configuration
        self.width = 720
        self.height = 580
        self.title("PyGuiGPT")
        self.geometry("720x580")
        self.resizable(False, False)

        # Set App Heading
        self.heading = CTkLabel(
            self, 
            text="PyGuiGPT",
            text_color="#0A57A9",
            corner_radius=20,
            font=("Consolas", 30)
        )
        self.heading.place(x=295, y=7)

        self.searchFrame = CTkFrame(
            self,
            width=665,
            height=50,
        )
        self.searchFrame.place(x=30, y=50)

        self.promptEntry = CTkEntry(
            self.searchFrame,
            width=565,
            height=30,
            takefocus = 1,
            font=("Consolas", 12)
        )
        self.promptEntry.place(x=15, y=10)

        self.searchIcon = CTkImage(Image.open(current_path + "\\search.png"), size=(15, 20))
        self.searchBtn = CTkButton(
            self.searchFrame, 
            text="",
            width=15,
            height=20,
            image=self.searchIcon,
            command=self.searchPrompt
        )
        self.searchBtn.place(x=585, y=10)

        self.clearIcon = CTkImage(Image.open(current_path + "\\remove.png"), size=(15, 20))
        self.clearBtn = CTkButton(
            self.searchFrame, 
            text="",
            width=15,
            height=20,
            image=self.clearIcon,
            command=self.clearPrompt
        )
        self.clearBtn.place(x=620, y=10)

        self.response = CTkScrollableFrame(
            self,
            width=642,
            height=400,
            scrollbar_button_color='grey', 
            scrollbar_button_hover_color='blue'
        )
        self.response.place(x=30, y=130)
        self.promptEntry.focus_force()
        self.update()

    def getTextboxHeight(self, message):
        words = message.split('\n')
        if len(words) == 1:
            return 5
        return len(words)

    def searchPrompt(self):
        PROMPT = self.promptEntry.get()
        self.clearPrompt()
        ai_res = self.comp(PROMPT, MaxToken=3000, outputs=3)
        messageHeight = self.getTextboxHeight(ai_res) * 15
        message_box = Message(self.response, PROMPT, ai_res, App.frameRow, messageHeight)
        App.frameRow += 5

    def clearPrompt(self):
        self.promptEntry.delete(0, END)
    
    def comp(self, PROMPT, MaxToken=50, outputs=3):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [
                {"role": "user", "content": PROMPT},
            ]
        )
        res = completion.choices
        output = res[0].message.content
        return output

if __name__ == "__main__":
    root = App()
    root.mainloop()