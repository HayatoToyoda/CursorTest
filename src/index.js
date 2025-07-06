import React from 'react';
import ReactDOM from 'react-dom/client';
import Profile from './Profile';
import ShoppingList from './ShoppingList';
import MyApp from './MyApp';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div>
      <Profile />
      <h2>Shopping List Example</h2>
      <ShoppingList />
      <hr />
      <MyApp />
    </div>
  </React.StrictMode>
); 