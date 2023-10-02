import json
import requests
import concurrent.futures
import os

def download_file(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"Saved: {save_path}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading file: {str(e)}")

def main(har_file_path):
    with open(har_file_path, "r", encoding="utf-8") as har_file:
        har_data = json.load(har_file)
    
    entries = har_data.get("log", {}).get("entries", [])
    
    download_tasks = []
    
    for entry in entries:
        request_url = entry.get("request", {}).get("url")
        if request_url:
            save_path = os.path.dirname(__file__) + "/" + "/".join(request_url.split("/")[3:len(request_url.split("/"))])  # ファイル名を取得
            dir = "/".join(save_path.split("/")[0:-1]) + "/"  # 作りたいディレクトリ名
            os.makedirs(dir, exist_ok=True)
            download_tasks.append((request_url, save_path))
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # ファイルのダウンロードを並列実行
        futures = [executor.submit(download_file, url, save_path) for url, save_path in download_tasks]
        
        # 完了したタスクをチェックし、エラーを処理
        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                print(f"Error in downloading: {future.exception()}")

if __name__ == "__main__":
    har_file_path = "C:/Users/PC部/Downloads/suika/aiueo/suika-game.app.har"  # Harファイルのパスを指定
    main(har_file_path)
