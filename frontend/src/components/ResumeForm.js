import React, { useState } from 'react';

function ResumeForm({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ title, content });
    setTitle('');
    setContent('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          placeholder="Название"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <textarea
          placeholder="Текст резюме"
          value={content}
          onChange={e => setContent(e.target.value)}
          rows={6}
          required
        />
      </div>
      <button type="submit">Сохранить</button>
    </form>
  );
}

export default ResumeForm;
