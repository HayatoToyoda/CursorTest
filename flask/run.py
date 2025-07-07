#!/usr/bin/env python3
"""
Flask Application Runner
アプリケーションを実行するためのスクリプト

使用方法:
    python run.py                # 通常モードで実行
    python run.py --debug        # デバッグモードで実行
    python run.py --port 8000    # カスタムポートで実行
"""

import argparse
import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from app import app
except ImportError as e:
    print(f"エラー: アプリケーションのインポートに失敗しました: {e}")
    print("必要な依存関係がインストールされていることを確認してください:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Flask Application Runner')
    parser.add_argument('--debug', action='store_true', 
                       help='デバッグモードで実行')
    parser.add_argument('--port', type=int, default=5000,
                       help='ポート番号 (デフォルト: 5000)')
    parser.add_argument('--host', default='0.0.0.0',
                       help='ホスト (デフォルト: 0.0.0.0)')
    
    args = parser.parse_args()
    
    # 環境変数の設定
    if args.debug:
        os.environ['FLASK_DEBUG'] = 'True'
    
    os.environ['PORT'] = str(args.port)
    
    print("=" * 50)
    print("🚀 Flask Application Starting...")
    print("=" * 50)
    print(f"📍 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🐛 Debug: {'Enabled' if args.debug else 'Disabled'}")
    print(f"🌐 URL: http://localhost:{args.port}")
    print("=" * 50)
    print("終了するには Ctrl+C を押してください")
    print("=" * 50)
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n👋 アプリケーションが正常に終了しました。")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()