const API_URL = "http://localhost:8000/api"; // подставьте ваш адрес, если другой

let accessToken = null;

export function setAccessToken(token) {
    accessToken = token;
}

function getHeaders() {
    return accessToken
        ? { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' }
        : { 'Content-Type': 'application/json' };
}

// Авторизация
export async function login(email, password) {
    const data = new URLSearchParams();
    data.append('username', email);
    data.append('password', password);

    const response = await fetch(`${API_URL}/auth/token`, {
        method: 'POST',
        body: data,
        headers: {},
    });
    if (!response.ok) throw new Error('Authorization failed');
    return await response.json();
}

// Регистрация
export async function register(email, password) {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error('Registration failed');
    return await response.json();
}

// Получить список резюме
export async function fetchResumes() {
    const response = await fetch(`${API_URL}/resumes/`, {
        headers: getHeaders(),
    });
    if (!response.ok) throw new Error('Fetch resumes failed');
    return await response.json();
}

// Получить одно резюме
export async function fetchResume(id) {
    const response = await fetch(`${API_URL}/resumes/${id}`, {
        headers: getHeaders(),
    });
    if (!response.ok) throw new Error('Resume not found');
    return await response.json();
}

// Создать резюме
export async function createResume(data) {
    const response = await fetch(`${API_URL}/resumes/`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Create resume failed');
    return await response.json();
}

// Обновить резюме
export async function updateResume(id, data) {
    const response = await fetch(`${API_URL}/resumes/${id}`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Update failed');
    return await response.json();
}

// Удалить резюме
export async function deleteResume(id) {
    const response = await fetch(`${API_URL}/resumes/${id}`, {
        method: 'DELETE',
        headers: getHeaders(),
    });
    if (!response.ok) throw new Error('Delete failed');
    return true;
}

// Улучшить резюме
export async function improveResume(id, text) {
    const response = await fetch(`${API_URL}/resumes/${id}/improve`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ content: text }),
    });
    if (!response.ok) throw new Error('Improve failed');
    return await response.json();
}
