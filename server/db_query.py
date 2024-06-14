import os
from dotenv import load_dotenv
import pymysql

dotenv_path = '.env'
# .env 파일 로드
load_dotenv(dotenv_path)

def save_data_to_mariadb(command):
    try:
        # 환경 변수에서 데이터베이스 정보 가져오기
        host = os.getenv('MARIA_DB_HOST')
        port = int(os.getenv('MARIA_DB_PORT'))
        user = os.getenv('MARIA_DB_USER')
        password = os.getenv('MARIA_DB_PASSWORD')
        database = os.getenv('MARIA_DB_DATABASE')
        table = os.getenv('')

        # MariaDB 서버에 연결
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection:
            with connection.cursor() as cursor:
                # 데이터 저장을 위한 SQL INSERT 문
                sql = command
                cursor.execute(sql)
            # 트랜잭션 커밋
            connection.commit()
            print("Data saved successfully.")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    # finally: #Error 발생, 이유 파악할 것
    #     # 연결 닫기
    #     if connection:
    #         connection.close()