import { useState } from 'react';

export default function Board() {

    function Square(){
      const[value, setValue] = useState(null);
      
      function handleClick() {
        // console.log('clicked!')
        setValue('X');
      }  
      return (
      <button 
        className="square"
        style={{ width: '60px', height: '60px', minWidth: '60px', minHeight: '60px' }}
        onClick={handleClick} 
      >
        {value}
      </button>
      );
    }
    
    return (
      <>
        <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      <div className="board-row">
        <Square />
        <Square />
        <Square />
      </div>
      </>
    );
  }

//   ありがとうございます。ご提示いただいたコードと問題について、以下の2点に分けて説明・対応策をお伝えします。

// ---

// ### ✅ **1. ボタンがクリック時に下にずれる問題**

// この現象は、`Square` コンポーネントが `useState` を使って状態を持っているにもかかわらず、`Board` コンポーネント内で直接定義されているため、**毎回新しいコンポーネントとして再生成されてしまう**ことが原因です。

// #### 🔧 解決方法：
// `Square` コンポーネントを `Board` の外に定義してください。以下のように修正します：

// ```jsx
// import { useState } from 'react';

// function Square() {
//   const [value, setValue] = useState(null);

//   function handleClick() {
//     setValue('X');
//   }

//   return (
//     <button
//       className="square"
//       style={{
//         width: '60px',
//         height: '60px',
//         minWidth: '60px',
//         minHeight: '60px',
//       }}
//       onClick={handleClick}
//     >
//       {value}
//     </button>
//   );
// }

// export default function Board() {
//   return (
//     <>
//       <div className="board-row">
//         <Square />
//         <Square />
//         <Square />
//       </div>
//       <div className="board-row">
//         <Square />
//         <Square />
//         <Square />
//       </div>
//       <div className="board-row">
//        Square />
//         <Square />
//       </div>
//     </>
//   );
// }
// ```

// これにより、各 `Square` が独立した状態を持ち、クリックしてもレイアウトが崩れなくなります。

// ---

// ### ⚠️ **2. 警告文について**

// ```
// WARN  Route "./components/ui/TabBarBackground.tsx" is missing the required default export.
// ```

// これは `TabBarBackground.tsx` ファイルに **`default export` が存在しない**ため、`expo-router` がルートとして認識できないという警告です。

// #### 🔧 解決方法：
// `TabBarBackground.tsx` に以下のような `default export` を追加してください：

// ```tsx
// export default backgroundColor: 'white', height: 50 }}>
//       {/* 任意の背景デザイン */}
//     </View>
//   );
// }
// ```

// または、もしこのファイルがまだ未完成であれば、**一時的に削除するか、ルーティング対象から除外**することで警告を回避できます。

// ---

// ### 次にどうしましょうか？

// - `Square` を外に出してもまだレイアウトが崩れる場合は、CSSのスタイルも確認できます。
// - `TabBarBackground.tsx` の役割や構成について詳しく知りたい場合は、そのコードを見せていただければアドバイスできます。

// 何か他にも気になる点はありますか？