# 自動テンプレート生成システム
## Auto Template Generator System

### 使用方法 (How to Use)

**簡単3ステップ:**
1. 学習したい技術名を入力
2. 自動生成されたプロンプトをコピー
3. そのまま送信

### 自動生成フォーマット (Auto-Generation Format)

#### パターン1: 単一技術学習
```
入力: [技術名]
出力: 完成したプロンプト
```

#### パターン2: 複数技術比較
```
入力: [技術A] vs [技術B]
出力: 比較学習プロンプト
```

#### パターン3: 問題解決
```
入力: [技術名] [問題内容]
出力: 問題解決プロンプト
```

### 技術分類と自動トピック設定 (Auto Topic Classification)

#### フロントエンド技術 (Frontend Technologies)
```
技術例: React, Vue, Angular, Next.js, Nuxt.js, Svelte
→ 自動トピック: "Frontend Development"
→ 自動テンプレート: 基本学習プロンプト
```

#### バックエンド技術 (Backend Technologies)
```
技術例: Node.js, Express, Django, Flask, FastAPI, Spring
→ 自動トピック: "Backend Development"
→ 自動テンプレート: 基本学習プロンプト
```

#### データベース技術 (Database Technologies)
```
技術例: MongoDB, PostgreSQL, Redis, GraphQL, Prisma
→ 自動トピック: "Database Management"
→ 自動テンプレート: 基本学習プロンプト
```

#### DevOps・インフラ技術 (DevOps/Infrastructure)
```
技術例: Docker, Kubernetes, AWS, CI/CD, Terraform
→ 自動トピック: "DevOps and Infrastructure"
→ 自動テンプレート: 深掘りプロンプト
```

#### CSS・スタイリング技術 (CSS/Styling)
```
技術例: Tailwind CSS, Styled Components, SCSS, CSS Grid
→ 自動トピック: "Modern CSS Techniques"
→ 自動テンプレート: 基本学習プロンプト
```

### 自動プロンプト生成ルール (Auto Prompt Generation Rules)

#### ルール1: 技術名のみ入力
```
入力例: "TypeScript"

自動生成プロンプト:
【日付】: January 17, 2025
【学習トピック】: "Frontend Development"
【技術項目】: "TypeScript"
【質問内容】: TypeScriptの基本概念と実用的な使い方を学びたい

以下の要求に従って回答してください：
1. `technical_format_specification.md`で定義した形式に従って技術解説を作成
2. 回答内容を`README.md`の指定日付セクションに追加
3. `Table of Contents`を更新
4. 各技術について「なぜ必要なのか？」から始める問題解決型の説明
5. 実用的なコード例（基本→実用→React）を含める
6. 技術の比較・使い分けの指針を提供
```

#### ルール2: 複数技術入力（"vs"を含む）
```
入力例: "React vs Vue vs Angular"

自動生成プロンプト:
【日付】: January 17, 2025
【比較技術】: React vs Vue vs Angular
【比較観点】: パフォーマンス、学習コスト、エコシステム、適用場面
【プロジェクト文脈】: 中規模Webアプリケーション開発

以下の形式で比較分析を作成してください：
1. 各技術の基本特徴
2. 具体的な実装例
3. 性能・機能比較表
4. 使用場面別の推奨技術
5. 学習・導入コスト
6. 将来性・コミュニティ

技術形式仕様に従い、README.mdに追加してください。
```

#### ルール3: 問題関連キーワード入力
```
入力例: "React Hook エラー"
問題キーワード: エラー、問題、トラブル、バグ、解決

自動生成プロンプト:
【日付】: January 17, 2025
【問題状況】: React Hookに関するエラーが発生している
【技術スタック】: React
【エラー内容】: [具体的なエラー内容を入力してください]
【試した解決策】: [これまでに試したことを入力してください]

以下の流れで問題解決型の学習コンテンツを作成してください：
1. 問題の技術的背景
2. 根本原因の分析
3. 複数の解決策とその比較
4. 推奨解決策の実装例
5. 今後の予防策
6. 関連する技術知識

形式化してREADME.mdに追加してください。
```

### 使用例 (Usage Examples)

#### 例1: 単一技術
```
あなたの入力: "GraphQL"

生成されるプロンプト:
【日付】: January 17, 2025
【学習トピック】: "Backend Development"
【技術項目】: "GraphQL"
【質問内容】: GraphQLの基本概念とREST APIとの違い、実用的な使い方を学びたい

以下の要求に従って回答してください：
1. `technical_format_specification.md`で定義した形式に従って技術解説を作成
2. 回答内容を`README.md`の指定日付セクションに追加
3. `Table of Contents`を更新
4. 各技術について「なぜ必要なのか？」から始める問題解決型の説明
5. 実用的なコード例（基本→実用→React）を含める
6. 技術の比較・使い分けの指針を提供
```

#### 例2: 比較学習
```
あなたの入力: "useState vs useReducer"

生成されるプロンプト:
【日付】: January 17, 2025
【比較技術】: useState vs useReducer
【比較観点】: 使用場面、コードの可読性、パフォーマンス、保守性
【プロジェクト文脈】: React状態管理

以下の形式で比較分析を作成してください：
1. 各技術の基本特徴
2. 具体的な実装例
3. 性能・機能比較表
4. 使用場面別の推奨技術
5. 学習・導入コスト
6. 将来性・コミュニティ

技術形式仕様に従い、README.mdに追加してください。
```

#### 例3: 深掘り学習
```
あなたの入力: "Docker 詳しく"

生成されるプロンプト:
【日付】: January 17, 2025
【深掘り技術】: Docker
【学習レベル】: 中級
【特定質問】: Dockerの内部実装と実際のプロジェクトでの使用方法を詳しく学びたい

以下の観点で深掘り解説を作成してください：
1. 技術的な背景と歴史
2. 内部実装の仕組み
3. パフォーマンスの考慮点
4. 実際のプロジェクトでの使用例
5. よくある問題とその解決方法
6. 最新のベストプラクティス

形式は`technical_format_specification.md`に従い、README.mdの該当日付に追加してください。
```

### 超簡単モード (Ultra Simple Mode)

以下の形式で入力するだけ：

```
【学習】: [技術名]
【比較】: [技術A] vs [技術B]
【問題】: [技術名] [問題内容]
【深掘り】: [技術名] 詳しく
```

例：
- `【学習】: Tailwind CSS`
- `【比較】: Next.js vs Gatsby`
- `【問題】: TypeScript 型エラー`
- `【深掘り】: Webpack 詳しく`

### 自動認識キーワード (Auto-Recognition Keywords)

#### 学習意図キーワード
- 学習、教えて、覚えたい、勉強、基本、入門
- → 基本学習プロンプト生成

#### 比較意図キーワード
- vs、対、比較、違い、どっち、選び方
- → 比較学習プロンプト生成

#### 問題解決キーワード
- エラー、問題、トラブル、バグ、解決、困った、助けて
- → 問題解決プロンプト生成

#### 深掘り意図キーワード
- 詳しく、深く、高度、上級、内部、仕組み、原理
- → 深掘りプロンプト生成

### 使い方の流れ (Usage Flow)

1. **技術名を入力**
   ```
   例: "React Hook"
   ```

2. **自動生成されたプロンプトが表示される**
   ```
   【日付】: January 17, 2025
   【学習トピック】: "Frontend Development"
   【技術項目】: "React Hook"
   ...
   ```

3. **プロンプトをそのままコピー&送信**

4. **私が形式化してREADME.mdに追加**

これで学習がさらに効率化されます！