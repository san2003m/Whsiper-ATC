#녹음프로그램에서 올라온, 음성파일을 업로드 받고, 학습된 모델을 이용해 STT를 실시함.
#DB서버로 시간, 호출부호, 음성인식 내용, 파일경로를 INSERT해줌.


import subprocess
from flask import Flask, request, jsonify
import os
from transformers import pipeline
import ffmpeg

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        # 필요한 변수 : 시간(mariadb_datetime), 호출부호(callsign), 음성인식 내용(asr_result), 파일경로(filepath)
        callsign = f"{filename}"
        print(callsign[0]+callsign[1]+callsign[2]+callsign[3])
        callsign=callsign[0]+callsign[1]+callsign[2]+callsign[3]
        #파일이름에서 시간을 추출하는 코드
        import re
        from datetime import datetime

        # 정규 표현식을 사용하여 날짜와 시간 추출
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})', filename)

        if match:
            # 추출한 부분을 각 변수에 할당
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            hour = match.group(4)
            minute = match.group(5)
            second = match.group(6)
            
            # datetime 객체 생성
            dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            
            # MariaDB DATETIME 형식으로 변환
            mariadb_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
            
            print(mariadb_datetime)
        else:
            print("파일 이름에서 날짜와 시간을 추출할 수 없습니다.")

        print(filepath)

        file.save(filepath)
        pipe = pipeline(model="san2003m/whisper-small-atc")
        def transcribe(audio):
          global asr_result
          asr_result = pipe(audio)["text"]
          print("ASR Result:",asr_result)
        transcribe(filepath)
        DB_filepath = f"{UPLOAD_FOLDER}/{filename}"
        print(DB_filepath)

        ##DB 송출단
        import db_query as db
        from dotenv import load_dotenv
        dotenv_path = '.env'
        # .env 파일 로드
        load_dotenv(dotenv_path)
        query_command="INSERT INTO ATC (time,radio_code,script,path) VALUES"+f"('{mariadb_datetime}','{callsign}','{asr_result}','{DB_filepath}')"
        db.save_data_to_mariadb(query_command)
        ##DB 송출단 끝

    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=10100)
