import React from 'react';

function ResumeItem({ resume, onOpen, onDelete }) {
  return (
    <li>
      <span style={{fontWeight: 'bold'}}>{resume.title}</span>
      <button onClick={onOpen}>Открыть</button>
      <button onClick={onDelete}>Удалить</button>
    </li>
  );
}

export default ResumeItem;
