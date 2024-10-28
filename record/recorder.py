import sounddevice as sd
import soundfile as sf
from tkinter import *
import tkinter as tk
import threading
from queue import Queue
from datetime import datetime
from tkinter import messagebox
import requests
from pathlib import Path
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import certifi

class RecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")

        self.recording = False
        self.q = Queue()

        self.sr = 16000
        self.ch = 1
        self.subtype = 'MPEG_LAYER_III'
        master.geometry("886x491")
        self.create_widgets()
        # master.bind('<Control-KeyPress>', self.start_recording_key)
        # master.bind('<Alt-KeyPress>', self.stop_recording_key)

        load_dotenv('../.env')
        self.update_db_status()
        self.update_time()  # 현재 시간 업데이트 시작

    def confirm(self):  # 공항코드 확인 누르면 행동
        in_text = self.entry_1.get()
        if in_text == "":
            messagebox.showwarning("Callsign Confirm", "호출부호를 입력해주세요.")
            return
        else:
            self.atc_code = in_text
            print(in_text)
            msg = "호출부호가 " + in_text + "로 설정되었습니다."
            messagebox.showwarning("Callsign Confirm", msg)

    def start_recording_key(self, event):
        self.start_recording()
        print("공항코드 :", self.atc_code)

    def stop_recording_key(self, event):
        self.stop_recording()

    def start_recording(self):
        if not hasattr(self, 'atc_code'):
            messagebox.showwarning("Warning", "코드 입력 후 확인버튼을 눌러야 실행됩니다.")
        else:
            if not self.recording:
                self.recording = True
                threading.Thread(target=self.record).start()
                self.button_1.config(state=tk.DISABLED)
                self.button_3.config(state=tk.NORMAL)
                # 녹음 시작 시 상태 텍스트를 변경하고 빨간색으로 설정
                self.status_label.config(text="녹음 중..", fg="red")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            threading.Thread(target=self.ser_up).start()
            self.button_1.config(state=tk.NORMAL)
            self.button_3.config(state=tk.DISABLED)
            # 녹음 정지 시 상태 텍스트를 녹음준비로 변경하고 기본 색상으로 설정
            self.status_label.config(text="녹음준비", fg="black")

    def ser_up(self):
        try:
            print("start Upload... Filename : " + self.filename)
            url = "https://home.kyunsan.com:10100/upload"
            with open(self.filename, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, verify=certifi.where())
                print(response.text + "filename : " + self.filename)  # 추가: 응답 결과 출력

            # 업로드가 성공적으로 완료되면 현재 시간을 업데이트
            if response.status_code == 200:
                now = datetime.now()
                timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
                self.recent_upload_label.config(text=timestamp)
            else:
                print("Upload Failed filename : " + self.filename)

        except Exception as e:
            print(e)

    def generate_filename(self):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"{self.atc_code}_recording_{timestamp}.mp3"
        return self.filename

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self.recording:
            self.q.put(indata.copy())

    def record(self):
        try:
            filename = self.generate_filename()
            with sf.SoundFile(filename, 'w', self.sr, self.ch, self.subtype) as f:
                with sd.InputStream(samplerate=self.sr, channels=self.ch, callback=self.callback):
                    while self.recording:
                        f.write(self.q.get())
        except Exception as e:
            print(e)

    def check_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('MARIA_DB_HOST'),
                port=int(os.getenv('MARIA_DB_PORT')),
                user=os.getenv('MARIA_DB_USER'),
                password=os.getenv('MARIA_DB_PASSWORD'),
                database=os.getenv('MARIA_DB_DATABASE')
            )
            if connection.is_connected():
                db_server_status = "온라인"
                self.db_status_label.config(text=db_server_status, fg="green")
            connection.close()
        except Error as e:
            db_server_status = "오프라인"
            self.db_status_label.config(text=db_server_status, fg="red")

        self.master.after(5000, self.check_db_connection)  # 5초마다 상태를 확인하도록 설정

    def update_time(self):
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        self.time_label.config(text=timestamp)
        self.master.after(1000, self.update_time)  # 1초마다 시간 업데이트

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
            text="항공교통관제 음성인식 서비스",
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
            643.0,
            471.0,
            anchor="nw",
            text="Recent Upload : ",
            fill="#000000",
            font=("NanumGothicExtraBold", 13 * -1)
        )

        # Recent Upload 시간과 날짜를 업데이트할 레이블 생성
        self.recent_upload_label = Label(
            self.master,
            text="0000/00/00 00:00:00",
            fg="#000000",
            font=("NanumGothicExtraBold", 13 * -1),
            bg="#FFFFFF"
        )
        self.recent_upload_label.place(x=743.0, y=465.9)

        self.canvas.create_text(
            440.0,
            145.0,
            anchor="nw",
            text="호출부호 (Callsign)",
            fill="#000000",
            font=("NanumGothicExtraBold", 24 * -1)
        )

        # 녹음 준비 상태 레이블 생성
        self.status_label = Label(
            self.master,
            text="녹음준비",
            fg="black",
            font=("NanumGothicExtraBold", 15 * -1),
            bg="#FFFFFF"
        )
        self.status_label.place(x=695.0, y=155.0)

        self.canvas.create_text(
            53.0,
            226.0,
            anchor="nw",
            text="1. Callsign을 입력한다.\n\n*관제소 - ICAO Code, 항공기 - Callsign\n\n2. 녹음키를 누른 후 녹음을 진행한다\n\n3. 녹음이 끝났으면, 정지버튼을 누른다.",
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
        self.button_1 = Button(self.master, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.start_recording, relief="flat")
        self.button_1.place(x=456.0, y=265.0, width=141.0, height=45.0)

        self.button_image_2_path = relative_to_assets("button_2.png")
        self.button_image_2 = Image.open(self.button_image_2_path)
        self.button_image_2 = ImageTk.PhotoImage(self.button_image_2)
        self.button_2 = Button(self.master, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.confirm, relief="flat")
        self.button_2.place(x=774.0, y=182.0, width=93.44680786132812, height=61.0)

        self.button_image_3_path = relative_to_assets("button_3.png")
        self.button_image_3 = Image.open(self.button_image_3_path)
        self.button_image_3 = ImageTk.PhotoImage(self.button_image_3)
        self.button_3 = Button(self.master, image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.stop_recording, relief="flat")
        self.button_3.place(x=660.0, y=265.0, width=141.0, height=45.0)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_2 = self.canvas.create_image(201.0, 71.0, image=self.image_image_2)

        # 현재 시간을 표시할 레이블 추가
        self.time_label = Label(
            self.master,
            text="00:00:00",
            fg="#FFFFFF",
            font=("NanumGothicExtraBold", 60 * -1),
            bg="#369EEA"
        )
        self.time_label.place(x=70.0, y=380.0)

    def update_db_status(self):
        self.check_db_connection()
        self.master.after(5000, self.update_db_status)  # 5초마다 상태 확인함

if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()
