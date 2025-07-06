# CursorTest

## Table of Contents
- [2025/7/06](#2025-7-06)
    1.condiotional ? operator
    1.logical && syntax
- [2025/7/07](#2025-7-07)
- [2025/7/08](#2025-7-08)
- [2025/7/09](#2025-7-09)
- [2025/7/10](#2025-7-10)
- [2025/7/11](#2025-7-11)
- [2025/7/12](#2025-7-12)
- [2025/7/13](#2025-7-13)
- [2025/7/14](#2025-7-14)
- [2025/7/15](#2025-7-15)
- [2025/7/16](#2025-7-16)
- [2025/7/17](#2025-7-17)
- [2025/7/18](#2025-7-18)
- [2025/7/19](#2025-7-19)
- [2025/7/20](#2025-7-20)
- [2025/7/21](#2025-7-21)
- [2025/7/22](#2025-7-22)
- [2025/7/23](#2025-7-23)
- [2025/7/24](#2025-7-24)
- [2025/7/25](#2025-7-25)
- [2025/7/26](#2025-7-26)
- [2025/7/27](#2025-7-27)
- [2025/7/28](#2025-7-28)
- [2025/7/29](#2025-7-29)
- [2025/7/30](#2025-7-30)
- [2025/7/31](#2025-7-31)

## 2025/7/06

### Reactでよく使うJavaScript演算子の解説

#### 1. 三項演算子（条件演算子）`? :`

三項演算子は「条件 ? 真の場合の値 : 偽の場合の値」という形で使います。

```javascript
// 基本的な使い方
const isLoggedIn = true;
const message = isLoggedIn ? "ようこそ！" : "ログインしてください";
console.log(message); // "ようこそ！"

// Reactでの使用例
function Greeting({ user }) {
  return (
    <div>
      {user ? <h1>こんにちは、{user.name}さん！</h1> : <h1>ゲストさん、ようこそ！</h1>}
    </div>
  );
}

// ネストした三項演算子（複雑になるので注意）
const age = 20;
const status = age >= 18 ? "大人" : age >= 13 ? "ティーン" : "子供";
```

#### 2. 論理積演算子 `&&`

`&&`は「左側が真の場合のみ右側を実行する」という短絡評価を行います。

```javascript
// 基本的な使い方
const name = "田中";
const greeting = name && `こんにちは、${name}さん！`;
console.log(greeting); // "こんにちは、田中さん！"

// 左側がfalsyの場合
const emptyName = "";
const greeting2 = emptyName && `こんにちは、${emptyName}さん！`;
console.log(greeting2); // "" (空文字列)

// Reactでの使用例
function UserProfile({ user }) {
  return (
    <div>
      {user && (
        <div>
          <h2>{user.name}</h2>
          <p>{user.email}</p>
        </div>
      )}
    </div>
  );
}

// 複数の条件を組み合わせる
function ProductCard({ product }) {
  return (
    <div>
      {product && product.inStock && product.price > 0 && (
        <button>カートに追加</button>
      )}
    </div>
  );
}
```

#### 3. 論理和演算子 `||`

`||`は「左側がfalsyの場合に右側の値を返す」という短絡評価を行います。

```javascript
// デフォルト値の設定
const userName = userInput || "ゲスト";
const displayName = user.name || "名無し";

// Reactでの使用例
function Product({ product }) {
  return (
    <div>
      <h3>{product.name || "商品名なし"}</h3>
      <p>価格: ¥{product.price || 0}</p>
    </div>
  );
}
```

#### 4. Nullish合体演算子 `??`

`??`は`null`または`undefined`の場合のみ右側の値を返します（`||`と異なり、`0`や空文字列は有効な値として扱います）。

```javascript
// || と ?? の違い
const count = 0;
console.log(count || 10); // 10 (0はfalsyなので)
console.log(count ?? 10); // 0 (0は有効な値なので)

// Reactでの使用例
function Counter({ count }) {
  return (
    <div>
      現在の数: {count ?? 0}
    </div>
  );
}
```

#### まとめ

- **三項演算子 `? :`**: 条件に応じて2つの値のどちらかを選択
- **論理積 `&&`**: 条件が真の場合のみ何かを表示/実行
- **論理和 `||`**: デフォルト値の設定
- **Nullish合体 `??`**: `null`/`undefined`の場合のみデフォルト値を使用

これらの演算子を組み合わせることで、Reactコンポーネントでより簡潔で読みやすいコードを書くことができます。




## 2025/7/07
Content for July 7, 2025

## 2025/7/08
Content for July 8, 2025

## 2025/7/09
Content for July 9, 2025

## 2025/7/10
Content for July 10, 2025

## 2025/7/11
Content for July 11, 2025

## 2025/7/12
Content for July 12, 2025

## 2025/7/13
Content for July 13, 2025

## 2025/7/14
Content for July 14, 2025

## 2025/7/15
Content for July 15, 2025

## 2025/7/16
Content for July 16, 2025

## 2025/7/17
Content for July 17, 2025

## 2025/7/18
Content for July 18, 2025

## 2025/7/19
Content for July 19, 2025

## 2025/7/20
Content for July 20, 2025

## 2025/7/21
Content for July 21, 2025

## 2025/7/22
Content for July 22, 2025

## 2025/7/23
Content for July 23, 2025

## 2025/7/24
Content for July 24, 2025

## 2025/7/25
Content for July 25, 2025

## 2025/7/26
Content for July 26, 2025

## 2025/7/27
Content for July 27, 2025

## 2025/7/28
Content for July 28, 2025

## 2025/7/29
Content for July 29, 2025

## 2025/7/30
Content for July 30, 2025

## 2025/7/31
Content for July 31, 2025