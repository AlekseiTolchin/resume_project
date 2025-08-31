//import React, { useState } from 'react';
//import { login, setAccessToken } from '../api/api';
//
//function LoginPage({ setAuth }) {
//  const [email, setEmail] = useState('');
//  const [password, setPassword] = useState('');
//  const [error, setError] = useState('');
//
//  const handleLogin = async (e) => {
//    e.preventDefault();
//    try {
//      const res = await login(email, password);
//      setAccessToken(res.access_token);
//      setAuth(true);
//    } catch {
//      setError('Ошибка авторизации');
//    }
//  };
//
//  return (
//    <form onSubmit={handleLogin}>
//      <div>
//        <label>Email:
//          <input value={email} onChange={e=>setEmail(e.target.value)} type="email"/>
//        </label>
//      </div>
//      <div>
//        <label>Пароль:
//          <input value={password} onChange={e=>setPassword(e.target.value)} type="password"/>
//        </label>
//      </div>
//      {error && <div style={{color:'red'}}>{error}</div>}
//      <button type="submit">Войти</button>
//    </form>
//  );
//}
//
//export default LoginPage;

import React, { useState } from 'react';
import { login, setAccessToken } from '../api/api';
import RegisterPage from './RegisterPage'; // см. ниже

function LoginPage({ setAuth }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await login(email, password);
      setAccessToken(res.access_token);
      setAuth(true);
    } catch {
      setError('Ошибка авторизации');
    }
  };

  if (showRegister) {
    // показываем форму регистрации
    return (
      <RegisterPage
        onRegisterSuccess={() => setShowRegister(false)} // после регистрации возвращаемся к логину
        onCancel={() => setShowRegister(false)}
      />
    );
  }

  return (
    <form onSubmit={handleLogin}>
      <div>
        <input
          value={email}
          onChange={e => setEmail(e.target.value)}
          type="email"
          placeholder="Email"
          required
        />
      </div>
      <div>
        <input
          value={password}
          onChange={e => setPassword(e.target.value)}
          type="password"
          placeholder="Пароль"
          required
        />
      </div>
      <button type="submit">Войти</button>
      {/* КНОПКА РЕГИСТРАЦИЯ */}
      <button type="button" onClick={() => setShowRegister(true)} style={{ marginLeft: 8 }}>
        Зарегистрироваться
      </button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </form>
  );
}

export default LoginPage;