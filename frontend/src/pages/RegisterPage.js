import React, { useState } from 'react';
import { register } from '../api/api';

function RegisterPage({ onRegisterSuccess, onCancel }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await register(email, password);
      if (onRegisterSuccess) onRegisterSuccess();
    } catch {
      setError('Ошибка регистрации');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Регистрация</h2>
      <div>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Зарегистрироваться</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: 8 }}>Отмена</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </form>
  );
}

export default RegisterPage;
