import streamlit as st
import datetime
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="사무실 PC 전용 출퇴근 관리", page_icon="🏢", layout="centered")

# 2. CSS 모바일 접속 차단
st.markdown("""
    <style>
    @media (max-width: 768px) {
        .main { display: none !important; }
        body::before {
            content: "❌ 본 시스템은 사무실 PC 웹 브라우저에서만 접속할 수 있습니다.";
            display: flex; justify-content: center; align-items: center;
            height: 100vh; font-size: 18px; font-weight: bold;
            color: #d9534f; text-align: center; padding: 20px; background-color: #f8d7da;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏢 팀 출퇴근 및 휴가 관리 시스템")
st.caption("※ 본 시스템은 사무실 PC 환경에서만 정상 작동합니다.")
st.divider()

# 3. 데이터 저장 설정
DATA_FILE = "attendance_log.csv"
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["날짜", "이름", "구분", "기록시간", "비고"])
    df_init.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# 4. 팀원 명단 (팀원 이름에 맞게 수정하세요)
TEAM_MEMBERS = ["신순천", "이은혜", "김수현", "이지성", "박지영","최주희","박민경","김다솔"]

with st.form("attendance_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        member_name = st.selectbox("👤 팀원 이름", TEAM_MEMBERS)
    with col2:
        record_type = st.radio("📌 구분", ["출근", "퇴근", "휴가(연차)", "반차"], horizontal=True)
    
    note = st.text_input("💬 비고 (선택 사항)", placeholder="예: 오전 반차, 외근 등")
    submit_btn = st.form_submit_button("제출하기", use_container_width=True)

if submit_btn:
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    
    new_record = pd.DataFrame([{
        "날짜": current_date, "이름": member_name, "구분": record_type,
        "기록시간": current_time, "비고": note
    }])
    
    new_record.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
    st.success(f"✅ [{member_name}] 님의 {record_type} 기록이 완료되었습니다! ({current_time})")

st.divider()

st.subheader("📊 오늘의 출퇴근 기록 현황")
if os.path.exists(DATA_FILE):
    df_logs = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    today_df = df_logs[df_logs["날짜"] == today_str]
    st.dataframe(today_df, use_container_width=True)