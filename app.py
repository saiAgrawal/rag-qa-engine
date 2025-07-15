import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"  # FastAPI backend URL

# =========================
# ✅ Clerk Auth Token Check
# =========================
query_params = st.query_params
token = query_params.get("token", "")

# Basic token validation
if not token:
    st.error("❌ Authentication required")
    st.info("👆 Please access this app through the dashboard at http://localhost:3000/dashboard")
    st.markdown("### How to access:")
    st.markdown("1. Go to [Dashboard](http://localhost:3000/dashboard)")
    st.markdown("2. Sign in with your account") 
    st.markdown("3. Click 'Open RAG Q&A Engine' button")
    st.stop()

# Test the token with backend - simplified
headers = {"Authorization": f"Bearer {token}"}

headers = {"Authorization": f"Bearer {token}"}

# =========================
# UI Setup
# =========================
st.set_page_config(
    page_title="RAG Q&A Engine", 
    layout="wide",
    page_icon="🧠"
)

# Header with logo and user profile dropdown
col1, col2, col3 = st.columns([1, 6, 2])
with col1:
    # Display the logo if it exists, otherwise use emoji
    try:
        st.image("artificial-intelligence_11802096.png", width=80)
    except:
        st.markdown("# 🧠")

with col2:
    st.title("🔍 RAG Q&A Engine")
    st.markdown("*Your intelligent document analysis companion*")

with col3:
    # Get user info from the token
    user_info = None
    try:
        user_response = requests.get(f"{API_BASE}/user-info", headers=headers)
        if user_response.status_code == 200:
            user_info = user_response.json()
    except:
        pass
    
    # User Profile Dropdown
    if user_info and user_info.get("user_id"):
        user_name = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}".strip()
        if not user_name:
            user_name = user_info.get('email', 'User')
    else:
        user_name = "User"
    
    # Profile dropdown with selectbox
    profile_option = st.selectbox(
        "Profile",
        [user_name, "🚪 Sign Out"],
        key="profile_dropdown",
        label_visibility="collapsed"
    )
    
    if profile_option == "🚪 Sign Out":
        # Clear session state and redirect
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.success("✅ Signing out...")
        st.markdown(
            """
            <meta http-equiv="refresh" content="1;url=http://localhost:3000" />
            <script>
                setTimeout(function(){
                    window.parent.location.href = 'http://localhost:3000';
                }, 1000);
            </script>
            """, 
            unsafe_allow_html=True
        )
        st.stop()

# =========================
# 📄 Sidebar - User Profile & Upload Files
# =========================
with st.sidebar:
    # User Profile Section
    st.markdown("### 👤 User Profile")
    
    # Try to get user info from the token
    user_info = None
    try:
        # Make a request to get user info from backend
        user_response = requests.get(f"{API_BASE}/user-info", headers=headers)
        if user_response.status_code == 200:
            user_info = user_response.json()
    except:
        pass
    
    # Display user info
    if user_info and user_info.get("user_id"):
        col1, col2 = st.columns([1, 3])
        with col1:
            # Display avatar or placeholder
            if user_info.get("image_url"):
                st.image(user_info["image_url"], width=60)
            else:
                st.markdown("🧑‍💼")
        
        with col2:
            if user_info.get("first_name") or user_info.get("last_name"):
                st.markdown(f"**{user_info.get('first_name', '')} {user_info.get('last_name', '')}**".strip())
            if user_info.get("email"):
                st.markdown(f"📧 {user_info['email']}")
            st.markdown(f"🆔 {user_info['user_id'][:8]}...")
    else:
        # Fallback display
        st.info("� **Authenticated User**")
        if token.startswith("session_"):
            token_parts = token.split("_")
            if len(token_parts) >= 3:
                st.markdown(f"🆔 {token_parts[1][:8]}...")
    
    # Status and actions
    st.success("🟢 **Status:** Online")
    
    # Sign out button
    if st.button("🚪 **Sign Out**", type="secondary", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.success("✅ Successfully signed out!")
        st.info("Redirecting to home page...")
        st.markdown(
            """
            <meta http-equiv="refresh" content="2;url=http://localhost:3000" />
            <script>
                setTimeout(function(){
                    window.parent.location.href = 'http://localhost:3000';
                }, 2000);
            </script>
            """, 
            unsafe_allow_html=True
        )
        st.stop()
    
    st.markdown("---")
    
    # Upload Documents Section
    st.header("�📄 Upload Documents")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["pdf", "docx", "txt", "md"])

    if uploaded_files and st.button("Process Documents"):
        for file in uploaded_files:
            files = {"file": (file.name, file, file.type)}
            try:
                res = requests.post(f"{API_BASE}/upload", files=files, headers=headers)
                if res.status_code == 200:
                    st.success(f"✅ Uploaded: {file.name}")
                elif res.status_code == 401:
                    st.error("🔐 Authentication expired. Please refresh from the dashboard.")
                    st.markdown("[🔄 Return to Dashboard](http://localhost:3000/dashboard)")
                else:
                    st.error(f"❌ {file.name} — {res.text}")
            except Exception as e:
                st.error(f"⚠️ Upload error for {file.name}: {e}")

# =========================
# 🌐 Sidebar - Scrape Website
# =========================
    st.header("🌐 Scrape Website")
    url = st.text_input("Website URL")
    if st.button("Scrape") and url:
        with st.spinner("Scraping..."):
            try:
                res = requests.post(f"{API_BASE}/scrape", json={"url": url}, headers=headers)
                if res.status_code == 200:
                    st.success("✅ Website scraped and embedded!")
                elif res.status_code == 401:
                    st.error("🔐 Authentication expired. Please refresh from the dashboard.")
                    st.markdown("[🔄 Return to Dashboard](http://localhost:3000/dashboard)")
                else:
                    st.error(f"❌ Error: {res.text}")
            except Exception as e:
                st.error(f"⚠️ Scraping error: {e}")


# =========================
# 💬 Chat Interface
# =========================
st.header("💬 Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new prompt
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{API_BASE}/chat", json={"prompt": prompt}, headers=headers)
            if res.status_code == 200:
                response = res.json().get("answer", "")
            elif res.status_code == 401:
                response = "🔐 Authentication expired. Please refresh from the dashboard: http://localhost:3000/dashboard"
            else:
                response = f"❌ Error: {res.text}"
        except Exception as e:
            response = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
