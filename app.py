import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. 인증 스코프 설정 (Drive 및 Spreadsheets 권한 포함)
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_google_sheet():
    # Secrets의 [gcp_service_account] 섹션을 딕셔너리로 로드
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
    client = gspread.authorize(creds)
    
    # Secrets의 ID값 로드 후 open_by_key로 열기
    sheet_id = st.secrets["spreadsheet"]
    sheet = client.open_by_key(sheet_id).worksheet("시트1")
    return sheet

# 시트 객체 호출
try:
    sheet = get_google_sheet()
    st.success("🎉 구글 시트 연동 성공!")
except Exception as e:
    st.error(f"연동 실패 상세 오류: {e}")
