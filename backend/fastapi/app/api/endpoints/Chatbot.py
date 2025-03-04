import os
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai

router = APIRouter()

# 환경변수에서 API 키 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY:", openai.api_key)

company_name = "네이버"
# 정의한 링크들. 링크는 앞뒤에 +++을 붙여서 react에서 링크로 만들 예정.
LINKS = {
    "로그인": "+++https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/+++", # 로그인
    "회원가입": "+++https://nid.naver.com/user2/join/agree?lang=ko_KR&realname=+++", # 회원가입 
    "비밀번호찾기": "+++https://nid.naver.com/user2/help/pwInquiry?lang=ko_KR+++", #비밀번호 찾기
    "회사소개": "+++https://www.navercorp.com/naver/naverMain+++", # 회사 소개 페이지
    "company_name": "네이버", # 회사 이름
    "company_address": "경기 성남시 분당구 정자일로 95",
        # 회사에 대한 설명
    "company_intro": "네이버는 전자상거래, 클라우드, 인공지능(AI), 모바일 애플리케이션 등 혁신적인 기술을 기반으로 다양한 사업을 확장하고 있습니다. 특히, 네이버 웹툰, 네이버 파이낸셜, 네이버 클라우드와 같은 서비스는 국내외에서 높은 평가를 받고 있습니다.고객 중심의 혁신을 추구하며, 사용자들의 생활을 보다 편리하고 풍요롭게 만드는 디지털 플랫폼을 제공하는 네이버는 앞으로도 지속적으로 성장하며, 글로벌 시장에서도 강력한 입지를 다질 것입니다.",
    "quote_request": "+++https://help.naver.com/inquiry/home.help+++" # 견적 문의
}

# 요청 데이터 모델
class ChatRequest(BaseModel):
    user_message: str

# 응답 데이터 모델 (답변,링크정보 같이 반환)
class ChatResponse(BaseModel):
    reply: str
    links: dict

@router.post("/chat", response_model=ChatResponse)
            # "대화 시작시  '안녕하세요? 무엇을 도와드릴까요?' 로그인, 회원가입, 비밀번호 재설정, 회사 소개, 견적 요청 등을 물어보세요.'라고 해야합니다."
async def chat_endpoint(request: ChatRequest):
    try:
        system_prompt = (
            f"당신은 {company_name}의 고객 지원 로봇입니다. 사용자가 질문을 하면 적절한 답변을 제공해야 합니다.\n"
            "만약 사용자가 로그인, 회원가입, 비밀번호 재설정, 회사 정보, 견적 요청 등에 대해 질문하면, "
            "적절한 답변을 제공해야 합니다.\n"
            "예를 들어 로그인에 대한 질문이 들어오면,+++https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/+++로 이동하라고 답변해야 합니다.\n"
            "링크는 주소 앞뒤에 +++을 붙여서 대답합니다.\ n"
            "만약 사용자가 이 외의 질문을 한다면  \n"
            
            
        )
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": request.user_message
            }
        ]
       
        print("요청 메시지:", messages)
        response = await asyncio.to_thread(
            lambda: openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
        )
        print("응답:", response)
        chatbot_reply = response.choices[0].message.content
        
        # 만약 GPT의 응답에 링크 정보가 없으면, 미리 정의한 LINKS를 함께 반환
        return ChatResponse(reply=chatbot_reply, links=LINKS)
    except Exception as e:
        print("앤드포인트 오류:", e)
        raise HTTPException(status_code=500, detail=str(e))
