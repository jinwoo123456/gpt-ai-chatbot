from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# OpenAI API 키 불러오기
from dotenv import load_dotenv
load_dotenv()
import openai
from app.api.endpoints.Chatbot import router as chatbot_router

print("디버깅용========================================================")
print("OpenAI 파일경로:", openai.__file__)
print("OpenAI 버전:", openai.__version__)
print("디버깅용========================================================")


app = FastAPI()
# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,  # 자격 증명 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)
app.include_router(chatbot_router, prefix="/api")


# 테스트용
@app.get("/hello")
def hello():
    return {"message": "안녕하세요~"}
