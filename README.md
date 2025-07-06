# CursorTest

## Table of Contents
- [2025/7/06](#202576)
    - [Conditional (Ternary) Operator ? :](#1-conditional-ternary-operator--)
    - [Logical AND Operator &&](#2-logical-and-operator-)
    - [Logical OR Operator ||](#3-logical-or-operator-)
    - [Nullish Coalescing Operator ??](#4-nullish-coalescing-operator-)
- [2025/7/07](#202577)
- [2025/7/08](#202578)
- [2025/7/09](#202579)
- [2025/7/10](#2025710)
- [2025/7/11](#2025711)
- [2025/7/12](#2025712)
- [2025/7/13](#2025713)
- [2025/7/14](#2025714)
- [2025/7/15](#2025715)
- [2025/7/16](#2025716)
- [2025/7/17](#2025717)
- [2025/7/18](#2025718)
- [2025/7/19](#2025719)
- [2025/7/20](#2025720)
- [2025/7/21](#2025721)
- [2025/7/22](#2025722)
- [2025/7/23](#2025723)
- [2025/7/24](#2025724)
- [2025/7/25](#2025725)
- [2025/7/26](#2025726)
- [2025/7/27](#2025727)
- [2025/7/28](#2025728)
- [2025/7/29](#2025729)
- [2025/7/30](#2025730)
- [2025/7/31](#2025731)

## 2025/7/06

### Frequently Used JavaScript Operators in React

#### 1. Conditional (Ternary) Operator ? :

三項演算子は「条件 ? 真の場合の値 : 偽の場合の値」という形で使います。

```javascript
// Basic usage
const isLoggedIn = true;
const message = isLoggedIn ? "ようこそ！" : "ログインしてください";
console.log(message); // "ようこそ！"

// Example in React
function Greeting({ user }) {
  return (
    <div>
      {user ? <h1>こんにちは、{user.name}さん！</h1> : <h1>ゲストさん、ようこそ！</h1>}
    </div>
  );
}

// Nested ternary (be careful, can get complex)
const age = 20;
const status = age >= 18 ? "大人" : age >= 13 ? "ティーン" : "子供";
```

#### 2. Logical AND Operator &&

`&&`は「左側が真の場合のみ右側を実行する」という短絡評価を行います。

```javascript
// Basic usage
const name = "田中";
const greeting = name && `こんにちは、${name}さん！`;
console.log(greeting); // "こんにちは、田中さん！"

// falsy value on the left
const emptyName = "";
const greeting2 = emptyName && `こんにちは、${emptyName}さん！`;
console.log(greeting2); // "" (empty string)

// Example in React
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

// Combine multiple conditions
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

#### 3. Logical OR Operator ||

`||`は「左側がfalsyの場合に右側の値を返す」という短絡評価を行います。

```javascript
// Setting default values
const userName = userInput || "ゲスト";
const displayName = user.name || "名無し";

// Example in React
function Product({ product }) {
  return (
    <div>
      <h3>{product.name || "商品名なし"}</h3>
      <p>価格: ¥{product.price || 0}</p>
    </div>
  );
}
```

#### 4. Nullish Coalescing Operator ??

`??`は`null`または`undefined`の場合のみ右側の値を返します（`||`と異なり、`0`や空文字列は有効な値として扱います）。

```javascript
// Difference between || and ??
const count = 0;
console.log(count || 10); // 10 (0 is falsy)
console.log(count ?? 10); // 0 (0 is a valid value)

// Example in React
function Counter({ count }) {
  return (
    <div>
      現在の数: {count ?? 0}
    </div>
  );
}
```

#### Summary

- **Conditional (Ternary) Operator `? :`**: Choose between two values based on a condition
- **Logical AND `&&`**: Only display/execute if the condition is true
- **Logical OR `||`**: Set default values
- **Nullish Coalescing `??`**: Use default only for `null`/`undefined`

By combining these operators, you can write more concise and readable code in your React components.




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