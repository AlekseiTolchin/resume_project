import React, { useEffect, useState } from 'react';
import { fetchResumes, createResume, deleteResume } from '../api/api';
import ResumeForm from '../components/ResumeForm';
import ResumeItem from '../components/ResumeItem';

function ResumesPage({ onOpenResume }) {
  const [resumes, setResumes] = useState([]);
  const [showForm, setShowForm] = useState(false);

  const loadResumes = async () => {
    try {
      const items = await fetchResumes();
      setResumes(items);
    } catch (e) {
      alert('Не удалось загрузить резюме');
    }
  };

  useEffect(() => {
    loadResumes();
  }, []);

  const handleAdd = async (resume) => {
    await createResume(resume);
    setShowForm(false);
    loadResumes();
  };

  const handleDelete = async (id) => {
    await deleteResume(id);
    loadResumes();
  };

  return (
    <div>
      <h2>Ваши резюме</h2>
      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Отмена' : 'Добавить новое'}
      </button>
      {showForm && <ResumeForm onSubmit={handleAdd} />}
      <ul>
        {resumes.map(r => (
          <ResumeItem
            key={r.id}
            resume={r}
            onOpen={() => onOpenResume(r.id)}
            onDelete={() => handleDelete(r.id)}
          />
        ))}
      </ul>
    </div>
  );
}

export default ResumesPage;