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

# Test the token with backend - with retry mechanism
headers = {"Authorization": f"Bearer {token}"}

def check_auth_with_retry():
    """Check authentication with retry mechanism"""
    try:
        response = requests.get(f"{API_BASE}/auth-status", headers=headers, timeout=5)
        if response.status_code == 200:
            return True, None
        else:
            return False, f"Auth check failed: {response.status_code}"
    except Exception as e:
        return False, f"Auth check error: {str(e)}"

# Check authentication status
auth_valid, auth_error = check_auth_with_retry()
if not auth_valid:
    st.warning(f"⚠️ Authentication issue detected: {auth_error}")
    st.info("💡 The app will continue to work, but if you experience issues, please refresh from the dashboard.")
    st.markdown("[🔄 Return to Dashboard](http://localhost:3000/dashboard)")

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
    
    # Add clear database option
    col1, col2 = st.columns([2, 1])
    with col1:
        url = st.text_input("Website URL")
    with col2:
        if st.button("🗑️ Clear DB", help="Clear all stored documents"):
            with st.spinner("Clearing database..."):
                try:
                    clear_res = requests.post(f"{API_BASE}/clear-all", headers=headers)
                    if clear_res.status_code == 200:
                        st.success("✅ Database cleared!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to clear database")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
    
    if st.button("Scrape & Replace") and url:
        with st.spinner("Scraping website and replacing old data..."):
            try:
                # Add timeout and show progress
                with st.empty():
                    st.info("🔄 Clearing old data and scraping new website...")
                    res = requests.post(f"{API_BASE}/scrape", json={"url": url}, headers=headers, timeout=120)
                    
                if res.status_code == 200:
                    result = res.json()
                    if result.get("success"):
                        st.success("✅ Website scraped successfully! Old data cleared.")
                        st.info("💡 Now you can ask questions about this website only.")
                        st.balloons()
                    else:
                        st.error("❌ Failed to scrape website")
                elif res.status_code == 401:
                    st.error("🔐 Authentication session expired during scraping.")
                    st.info("💡 This can happen with long scraping operations. Please try again.")
                    st.markdown("[🔄 Return to Dashboard](http://localhost:3000/dashboard)")
                    
                    # Option to retry with same token
                    if st.button("🔄 Retry Scraping", key="retry_scrape"):
                        st.rerun()
                else:
                    st.error(f"❌ Scraping failed: {res.text}")
                    st.info("💡 You can try again or check if the URL is accessible.")
            except requests.exceptions.Timeout:
                st.error("⏰ Scraping timed out (120 seconds). The website might be too large or slow.")
                st.info("💡 Try again with a simpler page or check your internet connection.")
            except Exception as e:
                st.error(f"⚠️ Unexpected error during scraping: {e}")
                st.info("💡 Please try again or contact support if the issue persists.")
    
    # Show info about current behavior
    st.info("💡 **Note:** Scraping will clear all previous data and only keep the new website content.")


# =========================
# 💬 Chat Interface
# =========================
st.header("💬 Chat")

# Get available sources for display (but only show if multiple sources exist)
try:
    sources_response = requests.get(f"{API_BASE}/sources", headers=headers, timeout=5)
    if sources_response.status_code == 200:
        available_sources = sources_response.json().get("sources", [])
        if len(available_sources) > 1:  # Only show if multiple sources
            st.info(f"📚 Available sources: {', '.join(available_sources)}")
    else:
        available_sources = []
except:
    available_sources = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], dict):
            # Just show the answer, hide source info
            st.write(msg["content"]["answer"])
        else:
            st.write(msg["content"])

# Handle new prompt
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{API_BASE}/chat", json={"prompt": prompt}, headers=headers, timeout=60)
            if res.status_code == 200:
                response_data = res.json()
                response_content = {
                    "answer": response_data.get("answer", ""),
                    "sources_used": response_data.get("sources_used", []),
                    "num_documents": response_data.get("num_documents", 0)
                }
                
                # Display just the answer (no source info)
                with st.chat_message("assistant"):
                    st.write(response_content["answer"])
                
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
            elif res.status_code == 401:
                # More detailed error info for debugging
                error_detail = res.text if res.text else "Unknown authentication error"
                st.error(f"Authentication error: {error_detail}")
                response = "🔐 Authentication expired. Please refresh from the dashboard: http://localhost:3000/dashboard"
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
            else:
                response = f"❌ Error {res.status_code}: {res.text}"
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
        except Exception as e:
            response = f"⚠️ Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
