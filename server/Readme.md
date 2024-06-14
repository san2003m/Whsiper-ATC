
# SERVER
python의 Flask를 기반으로, pytorch 설치가 필요합니다.
Client로부터 업로드 받은 음성파일의 음성인식을 실시하고, DB서버로 결과를 Query 합니다.

## db_query.py
DB 접근 코드입니다. .env파일을 별도로 생성하여, 접근 환경을 설정할 필요가 있습니다.

## web.py
Flask 기반의 서버 실행 파일입니다. 아래 코드로 실행 가능합니다.
* python ./web.py

기본 Port로 10100번으로 설정되어 있습니다. 코드 수정을 통해 원하는 Port로 수정가능합니다.

## requierment.txt
사용하는 데 필요한 pip 라이브러리 목록입니다. 아래 코드로 설치 가능합니다.
* pip install -r requierment.txt
