import streamlit as st
import requests
from datetime import datetime

# 1. 구글 폼 정보 설정
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeyOpkMkODDZzTWYpg7ZSH0rGyVTDl_hQPeRx6gVL7Itv7jaA/formResponse"

ENTRY_NAME = "entry.776814274"   # 이름
ENTRY_TYPE = "entry.31772546"    # 구분 (출근/퇴근)
ENTRY_TIME = "entry.1693067728"  # 시각

# 2. 실제 직원 8명의 이름과 개인 비밀번호
USER_DB = {
    "신순천": "7632",
    "이은혜": "7633",
    "김수현": "7635",
    "이지성": "7636",
    "박지영": "7641",
    "최주희": "7643",
    "박민경": "7644",
    "김다솔": "7647"
}

st.set_page_config(page_title="출퇴근 기록 시스템", page_icon="⏰")

st.title("⏰ 출퇴근 기록 시스템")

# 사용자 입력 (이름 선택 및 비밀번호 입력)
col_input1, col_input2 = st.columns(2)

with col_input1:
    user_name = st.selectbox("성함을 선택하세요", ["선택하세요"] + list(USER_DB.keys()))

with col_input2:
    input_password = st.text_input("비밀번호", type="password", placeholder="비밀번호 4자리 입력")

col1, col2 = st.columns(2)

def send_attendance(name, attendance_type):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        ENTRY_NAME: name,
        ENTRY_TYPE: attendance_type,
        ENTRY_TIME: now_str
    }
    
    try:
        response = requests.post(FORM_URL, data=payload)
        if response.status_code == 200:
            st.success(f"🎉 [{name}]님 [{attendance_type}] 처리 완료! ({now_str})")
        else:
            st.error(f"⚠️ 전송 실패 (상태 코드: {response.status_code})")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# 개인별 비밀번호 검증 후 전송
def validate_and_send(attendance_type):
    pw = input_password.strip()
    
    if user_name == "선택하세요":
        st.warning("성함을 선택해 주세요.")
    elif not pw:
        st.warning("비밀번호를 입력해 주세요.")
    elif USER_DB.get(user_name) != pw:
        st.error("🔒 비밀번호가 올바르지 않습니다.")
    else:
        send_attendance(user_name, attendance_type)

# 출근 버튼
with col1:
    if st.button("☀️ 출근하기", use_container_width=True):
        validate_and_send("출근")

# 퇴근 버튼
with col2:
    if st.button("🌙 퇴근하기", use_container_width=True):
        validate_and_send("퇴근")
