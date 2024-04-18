import os
import subprocess
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

example1 = "예시) 192.168.0.1"
example2 = "예시 ) MyDb"
example3 = "1234"
example4 = "postgres"
example5 = "예시) examplepassword"

def replace_text_in_ktr(new_server, new_database, new_port, new_username, new_password,encr_bat_path):

    new_password = encrypt_password(new_password, encr_bat_path)
    # 정규 표현식 패턴 설정
    server_pattern = r"<server>(.*?)<\/server>"
    database_pattern = r"<database>(.*?)<\/database>"
    port_pattern = r"<port>(.*?)<\/port>"
    username_pattern = r"<username>(.*?)<\/username>"
    password_pattern = r"<password>(.*?)<\/password>"

    server_replacement = f"<server>{new_server}</server>"
    database_replacement = f"<database>{new_database}</database>"
    port_replacement = f"<port>{new_port}</port>"
    username_replacement = f"<username>{new_username}</username>"
    password_replacement = f"<password>{new_password}</password>"
    
    # 현재 작업 디렉토리
    current_directory = os.path.dirname(os.path.realpath(__file__))
 
    # 현재 디렉토리 내의 모든 .ktr 파일 찾기
    ktr_files = [f for f in os.listdir(current_directory) if f.endswith('.ktr')]
    
    for ktr_file in ktr_files:
        ktr_file_path = os.path.join(current_directory, ktr_file)
        
        # 파일 열기
        try:
            with open(ktr_file_path, 'r', encoding='utf-8') as file:
                ktr_content = file.read()
        except UnicodeDecodeError:
            print(f"Error: Unable to decode file '{ktr_file_path}' with 'utf-8' encoding. Trying 'cp949' encoding.")
            try:
                with open(ktr_file_path, 'r', encoding='cp949') as file:
                    ktr_content = file.read()
            except UnicodeDecodeError:
                messagebox.showerror("오류", f"'{ktr_file_path}' 파일을 읽을 수 없습니다.")
                return
        
        # 특정 텍스트 교체
        ktr_content = re.sub(server_pattern, server_replacement, ktr_content)
        ktr_content = re.sub(database_pattern, database_replacement, ktr_content)
        ktr_content = re.sub(port_pattern, port_replacement, ktr_content)
        ktr_content = re.sub(username_pattern, username_replacement, ktr_content)
        ktr_content = re.sub(password_pattern, password_replacement, ktr_content)
        
        # 파일에 쓰기
        with open(ktr_file_path, 'w', encoding='utf-8') as file:
            file.write(ktr_content)
    
    # 작업 완료 알림
    messagebox.showinfo("완료", "텍스트 교체가 완료되었습니다.")

def on_entry_click(event, entry):
    if entry.get() in [example1,example2,example5]:
        entry.delete(0, "end")
        entry.insert(0, "")
    

def on_focusout(event, entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)

def encrypt_password(password, encr_bat_path):
    try:
        output = subprocess.check_output([encr_bat_path, '-kettle', password], stderr=subprocess.STDOUT, shell=True)
        encrypted_password = output.decode('cp949').strip()  # cp949 인코딩 사용
        return encrypted_password
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode('cp949'))  # 오류 메시지 디코딩
        return None

def select_encr_bat_file():
    encr_bat_path = filedialog.askopenfilename(title="Select Encr.bat File", filetypes=(("Batch files", "*.bat"), ("All files", "*.*")))
    if encr_bat_path:
        encr_bat_entry.delete(0, tk.END)
        encr_bat_entry.insert(0, encr_bat_path)

def encrypt_password_button_click():
    password = encrypt_password(password, encr_bat_path)
    encr_bat_path = encr_bat_entry.get()
    if password and encr_bat_path:
        encrypted_password = encrypt_password(password, encr_bat_path)
        if encrypted_password:
            print("암호화된 비밀번호:", encrypted_password)  # 결과를 터미널에 출력
            result_label.config(text=f"암호화된 비밀번호: {encrypted_password}")
        else:
            result_label.config(text="암호화에 실패했습니다.")
    else:
        result_label.config(text="비밀번호 또는 Encr.bat 파일을 선택하세요.")



# Tkinter UI 생성
root = tk.Tk()
root.title("KTR Text Replacement")

new_server_label = tk.Label(root, text="새로운 서버 주소:")
new_server_label.grid(row=0, column=0, padx=10, pady=5)
new_server_entry = tk.Entry(root, width=40)
new_server_entry.insert(0, example1)
new_server_entry.bind("<FocusIn>", lambda event: on_entry_click(event, new_server_entry))
new_server_entry.bind("<FocusOut>", lambda event: on_focusout(event, new_server_entry, example1))
new_server_entry.grid(row=0, column=1, padx=10, pady=5)

new_database_label = tk.Label(root, text="새로운 데이터베이스:")
new_database_label.grid(row=1, column=0, padx=10, pady=5)
new_database_entry = tk.Entry(root, width=40)
new_database_entry.insert(0, example2)
new_database_entry.bind("<FocusIn>", lambda event: on_entry_click(event, new_database_entry))
new_database_entry.bind("<FocusOut>", lambda event: on_focusout(event, new_database_entry, example2))
new_database_entry.grid(row=1, column=1, padx=10, pady=5)

new_port_label = tk.Label(root, text="새로운 포트:")
new_port_label.grid(row=2, column=0, padx=10, pady=5)
new_port_entry = tk.Entry(root, width=40)
new_port_entry.insert(0, example3)
new_port_entry.bind("<FocusIn>", lambda event: on_entry_click(event, new_port_entry))
new_port_entry.bind("<FocusOut>", lambda event: on_focusout(event, new_port_entry, example3))
new_port_entry.grid(row=2, column=1, padx=10, pady=5)

new_username_label = tk.Label(root, text="새로운 사용자 이름:")
new_username_label.grid(row=3, column=0, padx=10, pady=5)
new_username_entry = tk.Entry(root, width=40)
new_username_entry.insert(0, example4)
new_username_entry.bind("<FocusIn>", lambda event: on_entry_click(event, new_username_entry))
new_username_entry.bind("<FocusOut>", lambda event: on_focusout(event, new_username_entry, example4))
new_username_entry.grid(row=3, column=1, padx=10, pady=5)

new_password_label = tk.Label(root, text="새로운 비밀번호:")
new_password_label.grid(row=4, column=0, padx=10, pady=5)
 
new_password_entry = tk.Entry(root, width=40)
new_password_entry.insert(0, example5)
new_password_entry.bind("<FocusIn>", lambda event: on_entry_click(event, new_password_entry))
new_password_entry.bind("<FocusOut>", lambda event: on_focusout(event, new_password_entry, example5))
new_password_entry.grid(row=4, column=1, padx=10, pady=5)

encr_bat_label = tk.Label(root, text="Encr.bat 파일:")
encr_bat_label.grid(row=6, column=0, padx=10, pady=5)
encr_bat_entry = tk.Entry(root)
encr_bat_entry.grid(row=6, column=1, padx=10, pady=5)
encr_bat_button = tk.Button(root, text="파일 선택", command=select_encr_bat_file)
encr_bat_button.grid(row=6, column=2, padx=5, pady=5)

replace_button = tk.Button(root, text="Replace Text", command=lambda: replace_text_in_ktr(
    new_server_entry.get(), new_database_entry.get(), new_port_entry.get(), 
    new_username_entry.get(), new_password_entry.get(),encr_bat_entry.get()))
replace_button.grid(row=8, columnspan=2, padx=10, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=9, columnspan=2, padx=10, pady=5)

root.mainloop()
