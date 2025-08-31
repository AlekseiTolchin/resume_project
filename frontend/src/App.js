import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import ResumesPage from './pages/ResumesPage';
import ResumeDetailPage from './pages/ResumeDetailPage';

function App() {
  const [auth, setAuth] = useState(false);
  const [selectedResume, setSelectedResume] = useState(null);

  if (!auth) return <LoginPage setAuth={setAuth} />;

  if (selectedResume)
    return <ResumeDetailPage id={selectedResume} goBack={() => setSelectedResume(null)} />;

  return (
    <ResumesPage onOpenResume={setSelectedResume} />
  );
}

export default App;
