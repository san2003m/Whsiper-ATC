import soundfile as sf
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from tkinter import messagebox
import requests
from pathlib import Path
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

class RecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Uploader")

        self.sr = 16000
        self.ch = 1
        self.subtype = 'MPEG_LAYER_III'
        master.geometry("886x491")
        self.create_widgets()

        load_dotenv('../.env')
        # self.update_db_status()

    def confirm(self):  # 공항코드 확인 누르면 행동
        in_text = self.entry_1.get()
        self.atc_code = in_text
        print(in_text)

    def upload_file(self):
        if not hasattr(self, 'atc_code'):
            messagebox.showwarning("Warning", "코드 입력 후 확인버튼을 눌러야 실행됩니다.")
        else:
            file_path = filedialog.askopenfilename()
            if file_path:
                filename = self.generate_filename(file_path)
                self.ser_up(file_path, filename)

    def ser_up(self, file_path, filename):
        # try:
            url = "http://kyunsan.iptime.org:10100/upload"
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f)}
                response = requests.post(url, files=files)
        #         print(response.text)  # 추가: 응답 결과 출력
        # except Exception as e:
        #     print(e)

    def generate_filename(self, file_path):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        extension = Path(file_path).suffix
        filename = f"{self.atc_code}_recording_{timestamp}{extension}"
        return filename

    # def check_db_connection(self):
    #     try:
    #         connection = mysql.connector.connect(
    #             host=os.getenv('MARIA_DB_HOST'),
    #             port=int(os.getenv('MARIA_DB_PORT')),
    #             user=os.getenv('MARIA_DB_USER'),
    #             password=os.getenv('MARIA_DB_PASSWORD'),
    #             database=os.getenv('MARIA_DB_DATABASE')
    #         )
    #         if connection.is_connected():
    #             db_server_status = "온라인"
    #             self.db_status_label.config(text=db_server_status, fg="green")
    #         connection.close()
    #     except Error as e:
    #         db_server_status = "오프라인"
    #         self.db_status_label.config(text=db_server_status, fg="red")
    #
    #     self.master.after(5000, self.check_db_connection)  # 5초마다 상태를 확인하도록 설정

    def create_widgets(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=491,
            width=886,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            390.0,
            491.0,
            fill="#359EE9",
            outline="")

        self.canvas.create_text(
            40.0,
            127.0,
            anchor="nw",
            text="항공교통관제 파일 업로드 서비스",
            fill="#FCFCFC",
            font=("NanumGothicExtraBold", 24 * -1)
        )

        self.canvas.create_text(
            40.0,
            182.0,
            anchor="nw",
            text="사용방법",
            fill="#FCFCFC",
            font=("NanumGothicExtraBold", 24 * -1)
        )

        self.canvas.create_text(
            12.0,
            454.0,
            anchor="nw",
            text="DB 서버 상태 :",
            fill="#FCFCFC",
            font=("NanumGothicExtraBold", 24 * -1)
        )

        self.db_status_label = Label(
            self.master,
            text="DB 서버 상태 확인 중...",
            fg="#FCFCFC",
            font=("NanumGothicExtraBold", 24 * -1),
            bg="#359EE9"
        )
        self.db_status_label.place(x=172.0, y=449.0)

        self.canvas.create_text(
            426.0,
            145.0,
            anchor="nw",
            text="호출코드 (ICAO Code 4자리)",
            fill="#000000",
            font=("NanumGothicExtraBold", 24 * -1)
        )

        self.canvas.create_text(
            53.0,
            226.0,
            anchor="nw",
            text="1. 호출부호를 입력한다.\n\n2. 파일 선택 버튼을 눌러 파일을 선택한다.\n\n3. 선택한 파일을 업로드한다.",
            fill="#FCFCFC",
            font=("NanumGothic", 18 * -1)
        )

        entry_image_1_path = relative_to_assets("entry_1.png")
        entry_image_1 = Image.open(entry_image_1_path)
        entry_image_1 = ImageTk.PhotoImage(entry_image_1)
        entry_bg_1 = self.canvas.create_image(596.5, 209.5, image=entry_image_1)
        self.entry_1 = Entry(self.master, bd=0, bg="#F1F5FF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=436.0, y=179.0, width=321.0, height=59.0)

        self.canvas.create_rectangle(
            40.0,
            160.0,
            100.0,
            165.0,
            fill="#FCFCFC",
            outline="")

        self.button_image_1_path = relative_to_assets("button_1.png")
        self.button_image_1 = Image.open(self.button_image_1_path)
        self.button_image_1 = ImageTk.PhotoImage(self.button_image_1)
        self.button_1 = Button(self.master, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.upload_file, relief="flat")
        self.button_1.place(x=456.0, y=265.0, width=141.0, height=45.0)

        self.button_image_2_path = relative_to_assets("button_2.png")
        self.button_image_2 = Image.open(self.button_image_2_path)
        self.button_image_2 = ImageTk.PhotoImage(self.button_image_2)
        self.button_2 = Button(self.master, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.confirm, relief="flat")
        self.button_2.place(x=774.0, y=182.0, width=93.44680786132812, height=61.0)

        # self.master.resizable(False, False)

    # def update_db_status(self):
    #     self.check_db_connection()
    #     self.master.after(5000, self.update_db_status)  # 5초마다 상태를 확인하도록 설정

if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()
