import time
import pyperclip
import win32clipboard

def get_clipboard_text():
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Error getting clipboard text: {e}")
        return None

def get_clipboard_files():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        print(data,type(data))
        file_paths = data.split('\0')
        file_paths = [fp for fp in file_paths if fp]  # 去除空路径
        return file_paths
    except TypeError:
        return []
    finally:
        win32clipboard.CloseClipboard()

def clear_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

def do_something(text, filepaths):
    # 在这里执行你需要的操作
    print(f"Text: {text}")
    print(f"File paths: {filepaths}")

if __name__ == "__main__":
    text = None
    filepaths = None

    while True:
        current_text = get_clipboard_text()
        current_files = get_clipboard_files()

        if current_text and not filepaths:
            text = current_text
            print(f"Detected text: {text}")

        if current_files and not text:
            filepaths = current_files
            print(f"Detected files: {filepaths}")

        if text and filepaths:
            do_something(text, filepaths)
            text = None
            filepaths = None
            clear_clipboard()
            print("Clipboard cleared")

        time.sleep(1)  # 每秒检查一次剪贴板内容
