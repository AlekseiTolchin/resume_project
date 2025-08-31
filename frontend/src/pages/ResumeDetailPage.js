import React, { useEffect, useState } from 'react';
import { fetchResume, updateResume, improveResume } from '../api/api';

function ResumeDetailPage({ id, goBack }) {
  const [resume, setResume] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const [improvedText, setImprovedText] = useState('');

  useEffect(() => {
    fetchResume(id).then(r => {
      setResume(r);
      setEditTitle(r.title);       // <-- добавляем поле для изменения названия
      setEditContent(r.content);
    });
  }, [id]);

  const handleSave = async () => {
    await updateResume(id, { title: editTitle, content: editContent });
    const updated = await fetchResume(id);
    setResume(updated);
    setEditTitle(updated.title);   // обновляем title после сохранения
    setEditContent(updated.content);
  };

  const handleImprove = async () => {
    const result = await improveResume(id, editContent);
    setImprovedText(result.content);
  };

  if (!resume) return <div>Загрузка...</div>;

  return (
    <div>
      <input
        type="text"
        value={editTitle}
        onChange={e => setEditTitle(e.target.value)}
        style={{ width: '100%', fontWeight: 'bold', marginBottom: '8px' }}
        placeholder="Название резюме"
      />
      <textarea
        value={editContent}
        onChange={e => setEditContent(e.target.value)}
        rows={8}
        style={{width:'100%'}}
      />
      <br />
      <button onClick={handleSave}>Сохранить</button>
      <button onClick={handleImprove}>Улучшить</button>
      {improvedText && (
        <div>
          <h4>Улучшенная версия:</h4>
          <pre>{improvedText}</pre>
        </div>
      )}
      <br />
      <button onClick={goBack}>Назад к списку</button>
    </div>
  );
}

export default ResumeDetailPage;
