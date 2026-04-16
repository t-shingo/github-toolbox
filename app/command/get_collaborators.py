import csv
import os
from dotenv import load_dotenv
from github import Github, GithubException

# .env ファイルを読み込む
load_dotenv()

# 環境変数から設定を取得
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
ORG_NAME = os.getenv("GITHUB_ORG_NAME")
OUTPUT_FILE = "export/collaborators_list.csv"

def export_collaborators():
    if not ACCESS_TOKEN:
        print("Error: GITHUB_ACCESS_TOKEN が設定されていません。")
        return

    # GitHubクライアントの初期化
    g = Github(ACCESS_TOKEN)
    
    try:
        # 組織を取得
        org = g.get_organization(ORG_NAME)
        print(f"Checking repositories for {ORG_NAME}...")
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Repository", "Login", "Role (Permission)", "Type"])
            
            # 組織の全リポジトリをループ
            for repo in org.get_repos():
                print(f"Processing: {repo.name}...", end=" ", flush=True)
                
                try:
                    # コラボレーター一覧を取得
                    collaborators = repo.get_collaborators()
                    count = 0
                    
                    for collab in collaborators:
                        # 権限情報を取得 (admin, write, read 等)
                        permission = repo.get_collaborator_permission(collab)
                        
                        writer.writerow([
                            repo.name,
                            collab.login,
                            permission,
                            collab.type
                        ])
                        count += 1
                    print(f"Done ({count} members)")
                        
                except GithubException as e:
                    # 権限不足などで取得できないリポジトリがある場合のスキップ
                    print(f"Skipped (Error: {e.data.get('message')})")
                    continue

        print(f"\n完了！結果は {OUTPUT_FILE} に保存されました。")

    except GithubException as e:
        print(f"GitHub API エラー: {e}")

if __name__ == "__main__":
    export_collaborators()