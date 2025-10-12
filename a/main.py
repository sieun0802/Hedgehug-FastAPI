from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx
import traceback
import re


app = FastAPI()

# CORS 허용 설정 (필요에 따라 도메인 변경 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 예: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GROQ_API_KEY = GROQ_API_KEY
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def korean_text(text):
    return re.sub(r"[^가-힣0-9ㄱ-ㅎㅏ-ㅣ .,!?~\n]", "", text)
# 최대 대화 저장 수
MAX_HISTORY = 10

@app.websocket("/ws")
async def chat_with_groq(websocket: WebSocket):
    await websocket.accept()

    conversation = [
        {"role": "system", 
        "content":
        "당식은 한국어 전용 AI어시턴트입니다. "
        "절대 중국어,일본어,영어로 말하지 마세요,"
        "반드시 자연스러운 한국어만 사용하고,"
        "너는 따뜻하고 공감 능력이 높은 한국어 AI야. "
        "자연스러운 구어체와 존댓말을 사용해 대답해. "
        "짧고 부드럽게 표현하되 문맥을 고려해 답변해."
        }
    ]

    try:
        async with httpx.AsyncClient() as client:
            while True:
                user_input = await websocket.receive_text()
                conversation.append({"role": "user", "content": user_input})

                # 최근 대화만 유지
                conversation = conversation[-MAX_HISTORY:]

                # Groq API 호출
                response = await client.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": GROQ_MODEL,
                        "messages": conversation
                    },
                    timeout=30.0
                )

                if response.status_code != 200:
                    await websocket.send_text(f'Groq API 호출 실패: {response.text}') 
                    continue

                result = response.json()
                reply = korean_text(result["choices"][0]["message"]["content"])
                conversation.append({"role": "assistant", "content": reply})

                await websocket.send_text(reply)

    except WebSocketDisconnect:
        print("🔌 클라이언트 연결 종료")
    except Exception as e:
        print("❌ 에러 발생:", e)
        traceback.print_exc()
        await websocket.send_text("❌ 서버에서 에러가 발생했습니다.")


