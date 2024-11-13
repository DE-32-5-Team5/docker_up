from fastapi import FastAPI, HTTPException
import pymysql
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

app = FastAPI()

# MariaDB 연결 설정 (예시)
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://fiveguys:five2024$@mariadb_container:3551/parkingissue"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://fiveguys:five2024$@localhost:3551/parkingissue"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=100,  # 커넥션 풀 크기
    max_overflow=200,  # 최대 추가 커넥션
    pool_timeout=1,  # 커넥션을 얻을 때의 최대 대기 시간 (초)
    pool_recycle=3600,  # 1시간마다 커넥션을 재설정
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        db.begin()
        result = db.execute(text("SELECT SLEEP(1);"))
        result.fetchall()
        #db.commit()  # 트랜잭션 커밋
    finally:
        pass
        # 여기서 db.close()를 호출하지 않아 커넥션 누수 발생
        # db.close()

@app.get("/items/")
def read_items():
    #db = next(get_db())
    get_db()
    # ... 데이터베이스 쿼리 실행 ...
    return True

# MariaDB에서 SELECT SLEEP 쿼리를 수행하는 함수
def execute_sleep_query():
    try:
        # MariaDB에 연결
        connection = pymysql.connect(host="localhost", user="fiveguys", password="five2024$", db="parkingissue", charset='utf8', port = 3551)

        #with connection.cursor() as cursor:
            # N초 동안 대기하는 쿼리 실행
            #cursor.execute("SELECT SLEEP(0.1);")

        cursor = connection.cursor()
        cursor.execute("SELECT SLEEP(0.5);")
        #connection.close()

        return True
    except pymysql.MySQLError as e:
        print(f"Query failed: {e}")
        return False

# SLEEP 쿼리를 실행하는 엔드포인트
@app.get("/test-sleep-query")
def test_sleep_query():
    success = execute_sleep_query()
    if success:
        return {"status": "Query executed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Query execution failed")
