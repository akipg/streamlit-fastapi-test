import streamlit as st
import time

from server_process import Server

# Streamlitアプリケーション
def main():
    st.title("FastAPI Server Control with Streamlit")

    message = st.text("")

    # サーバーの状態管理
    if 'server' not in st.session_state:
        st.session_state['server'] = None
        st.session_state['server_port'] = None

    # サーバー起動ボタン
    if st.button("Start Server"):
        if st.session_state['server'] is None:
            with st.spinner("Starting server..."):
                server = Server()
                process, port = server.start_server()
                st.session_state['server'] = server
                st.session_state['server_port'] = port
                while True:
                    if server.get_server_status_via_api():
                        st.write("Server is running.")
                        break
                    time.sleep(0.5)
                message.write(f"Server started on http://127.0.0.1:{port} with PID:{process.pid}")
                
        else:
            message.write("Server is already running.")

    # サーバーAPIで停止ボタン
    if st.button("Stop Server via API"):
        if st.session_state['server'] is not None:
            st.session_state['server'].stop_server_via_api()
            st.session_state['server'] = None
            st.session_state['server_port'] = None
        else:
            st.write("No server is running.")

    # サーバー強制終了ボタン（killメソッド）
    if st.button("Force Stop Server"):
        if st.session_state['server'] is not None:
            st.session_state['server'].force_stop_server()
            st.session_state['server'] = None
            st.session_state['server_port'] = None
        else:
            st.write("No server is running.")

if __name__ == "__main__":
    main()
