import streamlit as st
import time

from server_process import Server

# Streamlitアプリケーション
def main():
    st.logo("C:/Users/vanch/.vscode/extensions/rust-lang.rust-analyzer-0.3.2121-win32-x64/icon.png")
    st.title("FastAPI Server Control with Streamlit")

    if "app_runs" not in st.session_state:
        st.session_state.app_runs = 0
        st.session_state.fragment_runs = 0
    st.session_state.app_runs += 1
    st.write(f"Full app says it ran {st.session_state.app_runs} times.")

    if "server" not in st.session_state:
        st.session_state['server'] = Server()
    
    server = st.session_state['server']


    # if server.process is None:
    #     server.start_server()


    server.scaffold_gui()

if __name__ == "__main__":
    main()
