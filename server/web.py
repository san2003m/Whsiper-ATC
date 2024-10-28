import subprocess
from flask import Flask, request, jsonify
import os
from transformers import pipeline
import uuid
import re
from datetime import datetime
import ffmpeg
import threading
from flask_cors import CORS  # CORS 모듈 추가

app = Flask(__name__)

# CORS 설정
CORS(app, resources={r"/upload": {"origins": "*", "supports_credentials": True}})  # 특정 출처 허용

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 파일 처리 함수 (별도의 스레드에서 실행)
def process_file(filepath, original_filename):
    # 호출부호(callsign)는 업로드 받은 원본 파일 이름의 앞 4자리를 사용
    callsign = original_filename[:4]
    print(f"Callsign: {callsign}")

    # 파일 이름에서 시간을 추출하는 코드
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})', original_filename)
    if match:
        year, month, day = match.group(1), match.group(2), match.group(3)
        hour, minute, second = match.group(4), match.group(5), match.group(6)
        dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        mariadb_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Extracted Time: {mariadb_datetime}")
    else:
        print("파일 이름에서 날짜와 시간을 추출할 수 없습니다.")
        return

    # 음성 파일을 STT 모델에 넘겨서 텍스트로 변환 (Whisper 모델 사용)
    def transcribe(audio_path):
        pipe = pipeline(model="san2003m/whisper-small-atc")
        result = pipe(audio_path)
        return result["text"]

    asr_result = transcribe(filepath)
    print(f"ASR Result: {asr_result}")
    DB_filepath = os.path.join(UPLOAD_FOLDER, os.path.basename(filepath))
    print(f"DB Filepath: {DB_filepath}")

    ## DB에 저장하는 함수
    def save_to_db(mariadb_datetime, callsign, asr_result, DB_filepath):
        import db_query as db
        from dotenv import load_dotenv
        load_dotenv('.env')
        query_command = (
            "INSERT INTO ATC (time, radio_code, script, path) "
            f"VALUES ('{mariadb_datetime}', '{callsign}', '{asr_result}', '{DB_filepath}')"
        )
        db.save_data_to_mariadb(query_command)

    # DB에 데이터 저장
    save_to_db(mariadb_datetime, callsign, asr_result, DB_filepath)


# 음성 파일을 업로드 받고, 처리하는 엔드포인트
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # 고유한 파일명을 생성 (UUID 추가)
        original_filename = file.filename
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

        # 파일을 저장
        filepath = "/var/www/html/"+filepath # 웹서버의 루트 디렉토리에 저장
        file.save(filepath)
        print(f"File saved to: {filepath}")

        # 별도의 스레드에서 파일 처리 시작
        threading.Thread(target=process_file, args=(filepath, original_filename)).start()

    # 클라이언트에 즉시 응답 반환
    return jsonify({'message': 'File uploaded successfully. Processing will continue in background.'}), 200

if __name__ == '__main__':
    context = ('/home/san2003m/whisper_atc_recording/fullchain.pem', '/home/san2003m/whisper_atc_recording/privkey.pem') 
    app.run(host="0.0.0.0", debug=True, port=10100, threaded=True, ssl_context=context)  # 멀티스레드 처리 활성화
