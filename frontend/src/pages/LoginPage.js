import React, { useState } from 'react';
import { login, setAccessToken } from '../api/api';

function LoginPage({ setAuth }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

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

  return (
    <form onSubmit={handleLogin}>
      <div>
        <label>Email:
          <input value={email} onChange={e=>setEmail(e.target.value)} type="email"/>
        </label>
      </div>
      <div>
        <label>Пароль:
          <input value={password} onChange={e=>setPassword(e.target.value)} type="password"/>
        </label>
      </div>
      {error && <div style={{color:'red'}}>{error}</div>}
      <button type="submit">Войти</button>
    </form>
  );
}

export default LoginPage;