import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. 구글 시트 연동 설정
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    sheet_url = st.secrets["spreadsheet"]
    sheet = client.open_by_url(sheet_url).시트1
    return sheet

# 2. 직원 정보 설정 (이름: 숫자 4자리 비밀번호)
USER_DB = {
    "신순천": "7632",
    "이은혜": "7633",
    "김수현": "7635",
    "이지성": "7636",
    "박지영": "7641",
    "최주희": "7643",
    "박민경": "7644",
    "김다솔": "7647",
}

st.set_page_config(page_title="사무실 근태 관리 시스템", page_icon="⏰")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

# --- 로그인 화면 ---
if not st.session_state["logged_in"]:
    st.title("🔒 근태 관리 시스템 - 로그인")
    
    with st.form("login_form"):
        user_name = st.text_input("이름")
        password = st.text_input("비밀번호 (숫자 4자리)", type="password", max_chars=4)
        submit_button = st.form_submit_button("로그인")
        
        if submit_button:
            # 이름 존재 여부 확인 및 비밀번호 일치 검증
            if user_name in USER_DB and USER_DB[user_name] == password:
                st.session_state["logged_in"] = True
                st.session_state["user_name"] = user_name
                st.success(f"{user_name}님 환영합니다!")
                st.rerun()
            else:
                st.error("이름 또는 비밀번호(숫자 4자리)가 올바르지 않습니다.")

# --- 메인 출퇴근 화면 ---
else:
    user_name = st.session_state["user_name"]
    
    st.title("⏰ 사무실 출퇴근 관리")
    st.write(f"접속자: **{user_name}** 님")
    
    if st.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["user_name"] = None
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("☀️ 출근하기", use_container_width=True):
            try:
                sheet = get_google_sheet()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 구글 시트에 기록: [이름, 구분, 시각]
                sheet.append_row([user_name, "출근", now])
                st.success(f"[{now}] {user_name}님 출근 등록 완료!")
            except Exception as e:
                st.error(f"구글 시트 저장 실패: {e}")

    with col2:
        if st.button("🌙 퇴근하기", use_container_width=True):
            try:
                sheet = get_google_sheet()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([user_name, "퇴근", now])
                st.info(f"[{now}] {user_name}님 퇴근 등록 완료!")
            except Exception as e:
                st.error(f"구글 시트 저장 실패: {e}")
