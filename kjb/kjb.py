import os
import tkinter as tk

example1 = "예시) C:/ProgramData/ETL_src/"
example2 = "예시) D:/ETL_src/src/"

def replace_text_in_kjb():
    old_text = old_text_entry.get()
    new_text = new_text_entry.get()
    
    # 현재 폴더 내의 모든 kjb 파일 찾기
    current_directory = os.getcwd()
    kjb_files = [f for f in os.listdir(current_directory) if f.endswith('.kjb')]
    print(kjb_files)
    for kjb_file in kjb_files:
        kjb_file_path = os.path.join(current_directory, kjb_file)
        with open(kjb_file_path, 'r') as file:
            kjb_content = file.read()
        
        # 특정 텍스트 교체
        new_content = kjb_content.replace(old_text, new_text)
        
        # 파일에 쓰기
        with open(kjb_file_path, 'w') as file:
            file.write(new_content)

def on_entry_click(event, entry):
    if entry.get() == example1 or entry.get() == example2:
        entry.delete(0, "end")
        entry.insert(0, "")

def on_focusout(event, entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)

# Tkinter UI 생성
root = tk.Tk()
root.title("KJB Text Replacement")

old_text_label = tk.Label(root, text="바꾸기 전 :")
old_text_label.grid(row=0, column=0, padx=10, pady=5)
old_text_entry = tk.Entry(root, width=40)
old_text_entry.insert(0, example1)
old_text_entry.bind("<FocusIn>", lambda event: on_entry_click(event, old_text_entry))
old_text_entry.bind("<FocusOut>", lambda event: on_focusout(event, old_text_entry, example1))
old_text_entry.grid(row=0, column=1, padx=10, pady=5)

new_text_label = tk.Label(root, text="바꾸기 후 :")
new_text_label.grid(row=1, column=0, padx=10, pady=5)
new_text_entry = tk.Entry(root, width=40)
new_text_entry.insert(0, example2)
new_text_entry.bind("<FocusIn>", lambda event: on_entry_click(event, new_text_entry))
new_text_entry.bind("<FocusOut>", lambda event: on_focusout(event, new_text_entry, example2))
new_text_entry.grid(row=1, column=1, padx=10, pady=5)

replace_button = tk.Button(root, text="Replace Text", command=replace_text_in_kjb)
replace_button.grid(row=2, columnspan=2, padx=10, pady=5)

root.mainloop()
