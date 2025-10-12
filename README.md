# 🦔 고슴도치 상담봇 (2학기 캡스톤 프로젝트 코드 v5)

Groq Cloud 기반 한국어 상담 챗봇 서버

이 프로젝트는 경북소프트웨어고등학교 2학기 캡스톤 프로젝트
“고슴도치 (Hedgehog)”의 AI 상담 기능을 담당하는 백엔드 서버입니다.

FastAPI와 Groq Cloud API를 이용해 실시간 WebSocket 상담을 지원하며,
사용자의 감정과 상황에 맞는 따뜻한 한국어 응답을 제공합니다.

## 🧠 프로젝트 개요

프로젝트명: 고슴도치 (Hedgehog)

버전: Code v5

담당 파트: AI 상담 챗봇 (Groq 연동)

목표:
학생의 감정이나 고민을 공감적으로 받아주고,
따뜻한 말투로 상담해주는 AI 챗봇 개발

## ⚙️ 주요 기능
기능	설명
💬 실시간 대화 (WebSocket)	/ws 엔드포인트를 통해 양방향 대화
🤖 Groq Cloud API 연동	llama-3.1-8b-instant 모델 사용
🩵 감정형 응답 시스템	따뜻하고 공감력 있는 한국어 답변 생성
🧹 대화 내역 관리	최근 10개의 메시지만 유지
🔒 불필요한 외국어 필터링	정규표현식을 이용해 한국어만 유지
🧩 기술 스택
항목	사용 기술
백엔드 프레임워크	FastAPI
모델 API	Groq Cloud (llama-3.1-8b-instant)
실시간 통신	WebSocket
요청 라이브러리	httpx
언어 필터링	re (정규표현식)
배포 환경	Python 3.10+, Ubuntu
🔧 실행 방법
1️⃣ 환경 세팅
python -m venv venv
source venv/bin/activate    # (Windows: venv\Scripts\activate)
pip install fastapi uvicorn httpx

2️⃣ API Key 설정

.env 파일을 만들어 아래처럼 입력합니다:

GROQ_API_KEY=your_groq_api_key


⚠️ 절대 코드에 직접 키를 넣지 말고 .env 또는 환경 변수로 관리하세요.

3️⃣ 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

4️⃣ WebSocket 테스트 (간단한 HTML)
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>고슴도치 상담봇</title></head>
<body>
  <h2>🦔 고슴도치 상담봇</h2>
  <textarea id="chat" rows="10" cols="60" readonly></textarea><br>
  <input id="msg" placeholder="메시지를 입력하세요" size="60">
  <button onclick="send()">전송</button>

  <script>
    const ws = new WebSocket("ws://localhost:8000/ws");
    const chat = document.getElementById("chat");
    const msg = document.getElementById("msg");

    ws.onmessage = (event) => chat.value += "AI: " + event.data + "\n";
    function send() {
      ws.send(msg.value);
      chat.value += "나: " + msg.value + "\n";
      msg.value = "";
    }
  </script>
</body>
</html>

## 📜 코드 요약
▶ main.py
@app.websocket("/ws")
async def chat_with_groq(websocket: WebSocket):
    await websocket.accept()
    ...
    response = await client.post(GROQ_API_URL, headers=headers, json=payload)
    reply = korean_text(result["choices"][0]["message"]["content"])
    await websocket.send_text(reply)


conversation 리스트로 최근 대화 맥락 유지

Groq API (llama-3.1-8b-instant)로 답변 생성

korean_text()로 한국어만 필터링

WebSocket으로 클라이언트에 전송

## 💡 향후 개선 예정

 사용자 감정 분석 기능 추가

 대화 히스토리 DB 저장 (MongoDB 연동)

 UI와 연결 (React Native or React Web)

 감정 통계 시각화 기능

## 👩‍💻 개발 정보

개발자: 이시삼

소속: 경북소프트웨어고등학교 인공지능소프트웨어과

프로젝트: 2학기 캡스톤 “고슴도치 – 고독사 예방 앱”"# Hedgehug-FastAPI" 
