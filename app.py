import streamlit as st
from google import genai
from google.genai import types
import json

API_KEY = "AQ.Ab8RN6IDKkUEcafct5BG-qsqV2mu1eocFyMxMcMbOWpwQwz_Kg"
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="무료 자소서 레고 블록 빌더", layout="wide")
st.title("🧱 자소서 레고 블록 (Prompt Refactoring) 빌더")
st.caption("Google Gemini 무료 API를 활용하여 프롬프트 리팩토링 공식을 구현한 프로그램입니다.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 1. 경험 입력하기")
    role = st.text_input("지원하는 직무/포지션을 입력하세요", placeholder="예: 구조설계 인턴, 마케팅 신입")
    raw_experience = st.text_area(
        "자신의 경험을 자유롭게 적어주세요", 
        placeholder="예: 3학년 때 과제 하다가 애들이랑 의견 안 맞아서 싸웠는데 내가 양보하고 밤새서 결국 A 받음",
        height=200
    )
    
    submit_button = st.button("🚀 레고 블록 조립 및 자소서 생성", use_container_width=True)

if submit_button:
    if not role or not raw_experience:
        st.error("직무와 경험을 모두 입력해주세요!")
    else:
        with st.spinner("무료 AI 엔진이 작동 중입니다..."):
            
            refactor_system_prompt = """
            당신은 사용자의 모호한 입력을 받아 [Instruction], [Context], [Output Indicator] 구조의 완벽한 프롬프트로 재조립하는 프롬프트 엔지니어입니다.
            반드시 아래 지정된 JSON 포맷으로만 답변하세요. 다른 텍스트는 절대 출력하지 마세요.

            {
              "Instruction": "직무에 맞는 자소서 작성 지시문",
              "Context": "사용자의 경험 배경과 갈등 해결/성과 중심의 맥락 요약",
              "Output_Indicator": "글자 수 및 STAR 기법 등의 형식 지정"
            }
            """
            
            user_input_content = f"직무: {role}\n사용자 경험: {raw_experience}"
            
            response_refactor = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input_content,
                config=types.GenerateContentConfig(
                    system_instruction=refactor_system_prompt,
                    response_mime_type="application/json"
                ),
            )
            
            refactored_data = json.loads(response_refactor.text)
            
            final_instruction = refactored_data["Instruction"]
            final_context = refactored_data["Context"]
            final_indicator = refactored_data["Output_Indicator"]
            
            final_prompt = f"""
            [Instruction]: {final_instruction}
            [Context]: {final_context}
            [Output Indicator]: {final_indicator}
            """
            
            response_cover_letter = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=final_prompt,
                config=types.GenerateContentConfig(
                    system_instruction="당신은 채용 담당자의 마음을 사로잡는 전문 자기소개서 작가입니다. 제출된 프롬프트 구조에 맞춰 작성하세요."
                ),
            )
            
            final_cover_letter = response_cover_letter.text

        with col2:
            st.subheader("✨ 2. 프롬프트 리팩토링 결과 (Before & After)")
            
            st.error(f"❌ **Bad Prompt (사용자의 원래 입력)**\n\n> \"{role} 자소서 써줘. 내용은 {raw_experience}\"\n\n👉 *문제점: [Missing Audience] [Missing Format] [Too Abstract]*")
            
            st.success("🟢 **Good Prompt (AI가 재조립한 레고 블록)**")
            st.info(f"**[Instruction]**\n{final_instruction}")
            st.info(f"**[Context]**\n{final_context}")
            st.info(f"**[Output Indicator]**\n{final_indicator}")
            
            st.markdown("---")
            
            st.subheader("📝 3. 최종 생성된 자기소개서")
            st.write(final_cover_letter)