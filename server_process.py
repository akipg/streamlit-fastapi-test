import subprocess
import requests
import socket
import os
import time

class Server:
    def __init__(self, host="127.0.0.1", port=None):
        self.__protocol = "http"
        self.__host = host
        self.__port = port
        self.__process = None

        self.gui = ServerGUI()

    # デストラクタ
    def __del__(self):
        if self.process is not None:
            print(f"Killing the server {self.base_url} with PID:{self.process.pid} process...")
            self.force_stop_server()

    # FastAPIサーバーを別プロセスで起動する関数
    def start_server(self, wait_for_start=True):
        if self.port is None:
            self.__port = self.get_free_port()
        print("Starting server...")
        if os.name == 'posix':
            # Linux or MacOS
            self.__process = subprocess.Popen(
                ["exec", "uvicorn", "server:app", "--host", "{self.host}", f"--port", str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )   
        else:
            # Windows
            self.__process = subprocess.Popen(
                ["uvicorn", "server:app", "--host", self.host, f"--port", str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        print(f"Server started on {self.base_url} with PID:{self.process.pid}")
        
        if wait_for_start:
            timeout = 2
            interval = 0.1
            while True:
                if self.get_server_status_via_api():
                    print("Server is running.")
                    break
                if timeout <= 0:
                    print("Failed to start server.")
                    break
                timeout -= interval
                time.sleep(interval)
                print("Waiting for server to start...")

        return self.process, self.port

    def get_request(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        return response

    # ランダムな空きポートを取得する関数
    def get_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
        
    def get_server_status(self):
        if self.process is not None:
            return True
        else:
            return False

    def get_server_status_via_api(self):
        try:
            response = self.get_request("health")
            print(response)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.ConnectionError as e:
            print(e)
            return False

    # FastAPIサーバーをAPIで終了させる関数
    def stop_server_via_api(self):
        try:
            response = requests.post(f"{self.base_url}/shutdown")
            if response.status_code == 200:
                self.__process = None
                print("Server is shutting down.")
            else:
                print(f"Failed to shutdown server: {response.status_code}")
        except requests.ConnectionError:
            print("Failed to connect to the server.")
        except Exception as e:
            print(e)

    # FastAPIサーバーを強制終了させる関数（killメソッド）
    def force_stop_server(self):
        if self.process is not None:
            self.process.kill()  # プロセスを強制終了
            self.__process = None

    def scaffold_gui(self):
        import streamlit as st

        @st.fragment
        def __scaffold_gui_fragment(self):
            st.title("FastAPI")

            status = st.empty()
            startstop_button = st.empty()

            if self.process is None:
                status.write("Server is stopped.")
                if startstop_button.button("Start Server"):
                    if self.process is None:
                        with st.spinner("Starting server..."):
                            self.start_server()
                    else:
                        status.write("Server is already running.")
                    # fragmentをリロード
                    st.rerun(scope="fragment")
            else:
                status.write(f"Server started on {self.base_url} with PID:{self.process.pid}")
                if startstop_button.button("Stop Server"):
                    self.force_stop_server()
                    # fragmentをリロード
                    st.rerun(scope="fragment")
        
        __scaffold_gui_fragment(self)


       

    @property
    def protocol(self):
        return self.__protocol
    
    @property
    def host(self):
        return self.__host
    
    @property
    def port(self):
        return self.__port
    
    @property
    def process(self):
        return self.__process

    @property
    def base_url(self):
        return f"{self.protocol}://{self.host}:{self.port}"

class ServerGUI:
    def __init__(self) -> None:
        self.status = None
        self.message = None