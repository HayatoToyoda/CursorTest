# Flask Web Application

このプロジェクトは、Flaskフレームワークを使用して作成された基本的なWebアプリケーションです。モダンなUIデザインと基本的なAPI機能を含んでいます。

## 🚀 特徴

- **シンプルなWebアプリケーション**: ホームページとアバウトページ
- **RESTful API**: JSONレスポンスのAPIエンドポイント
- **レスポンシブデザイン**: モバイルフレンドリーなUI
- **モダンなCSS**: グラデーションとアニメーションを使用
- **インタラクティブ機能**: JavaScriptによるAPI呼び出し

## 📁 プロジェクト構造

```
flask/
├── app.py              # メインアプリケーション
├── requirements.txt    # Python依存関係
├── README.md          # このファイル
├── templates/         # Jinja2テンプレート
│   ├── index.html     # ホームページ
│   └── about.html     # アバウトページ
└── static/           # 静的ファイル
    └── css/
        └── style.css  # スタイルシート
```

## 🛠️ セットアップ手順

### 1. 依存関係のインストール

```bash
# 仮想環境を作成（推奨）
python -m venv venv

# 仮想環境を有効化
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt
```

### 2. アプリケーションの実行

```bash
# 基本的な実行
python app.py

# デバッグモードで実行
export FLASK_DEBUG=True  # Linux/Mac
set FLASK_DEBUG=True     # Windows
python app.py

# カスタムポートで実行
export PORT=8000  # Linux/Mac
set PORT=8000     # Windows
python app.py
```

### 3. アプリケーションへのアクセス

ブラウザで以下のURLにアクセスしてください：
- ホームページ: http://localhost:5000/
- アバウトページ: http://localhost:5000/about
- API エンドポイント: http://localhost:5000/api/hello?name=YourName

## 🔧 API エンドポイント

### GET /api/hello

簡単な挨拶APIエンドポイントです。

**パラメータ:**
- `name` (オプション): 挨拶する名前（デフォルト: "World"）

**レスポンス例:**
```json
{
    "message": "Hello, John!",
    "status": "success"
}
```

**使用例:**
```bash
curl "http://localhost:5000/api/hello?name=Flask"
```

## 🎨 カスタマイズ

### スタイルの変更
`static/css/style.css`ファイルを編集してアプリケーションの外観をカスタマイズできます。

### 新しいページの追加
1. `templates/`フォルダに新しいHTMLファイルを作成
2. `app.py`に新しいルートを追加
3. 必要に応じてナビゲーションメニューを更新

### API エンドポイントの追加
`app.py`ファイルに新しいルート関数を追加してAPIを拡張できます。

## 🚀 本番環境へのデプロイ

### Heroku へのデプロイ

1. `Procfile`を作成:
```
web: python app.py
```

2. Heroku CLIを使用してデプロイ:
```bash
heroku create your-app-name
git push heroku main
```

### Docker での実行

1. `Dockerfile`を作成:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

2. Dockerイメージをビルドして実行:
```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

## 📋 要件

- Python 3.7以上
- Flask 2.3.3
- その他の依存関係は`requirements.txt`を参照

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題や質問がある場合は、GitHubのIssuesページで報告してください。

---

**Happy Coding! 🎉**