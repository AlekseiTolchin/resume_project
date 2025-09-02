import pytest


@pytest.mark.asyncio
async def test_get_resumes(client, create_resume):
        """Получить список резюме текущего пользователя."""
        response = await client.get('/api/resumes/')
        assert response.status_code == 200
        resumes = response.json()
        assert isinstance(resumes, list)
        assert resumes[0]['title'] == 'Тестовое резюме'
        assert resumes[0]['content'] == 'Текст резюме'
        assert resumes[0]['user_id'] == 123


@pytest.mark.asyncio
async def test_get_resume(client, create_resume):
    """Получит одно резюме по id."""
    response = await client.get('/api/resumes/1')
    assert response.status_code == 200
    resume = response.json()
    assert resume['title'] == 'Тестовое резюме'
    assert resume['content'] == 'Текст резюме'
    assert resume['id'] == 1
    assert resume['user_id'] == 123


@pytest.mark.asyncio
async def test_create_resume(client):
    """Создать новое резюме"""
    payload = {
        'title': 'Тестовое резюме',
        'content': 'Текст резюме',
    }
    response = await client.post('/api/resumes/', json=payload)
    assert response.status_code == 201
    resume = response.json()
    assert resume['title'] == 'Тестовое резюме'
    assert resume['content'] == 'Текст резюме'
    assert resume['user_id'] == 123


@pytest.mark.asyncio
async def test_delete_resume(client, create_resume):
    """Удалить резюме по id"""
    response = await client.delete('/api/resumes/1')
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_resume(client, create_resume):
    """Полностью обновить резюме"""
    payload = {
        'title': 'Новое название',
        'content': 'Новый текст',
    }
    response = await client.put('/api/resumes/1', json=payload)
    assert response.status_code == 200
    resume = response.json()
    assert resume['title'] == 'Новое название'
    assert resume['content'] == 'Новый текст'


@pytest.mark.asyncio
async def test_partial_update_resume(client, create_resume):
    """Частично обновить резюме"""
    payload = {
        'title': 'Обновленное название'
    }
    response = await client.patch('/api/resumes/1', json=payload)
    assert response.status_code == 200
    resume = response.json()
    assert resume['title'] == 'Обновленное название'
    assert resume['content'] == 'Текст резюме'


@pytest.mark.asyncio
async def test_get_resumes_empty(client):
    """Возвратить пустой список при отсутствии резюме"""
    response = await client.get('/api/resumes/')
    assert response.status_code == 200
    resumes = response.json()
    assert resumes == []


@pytest.mark.asyncio
async def test_create_resume_invalid(client):
    """Создать резюме с невалидными данными"""
    payload = {'content': 'Текст резюме'}
    response = await client.post('/api/resumes/', json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_resume_not_found(client):
    """Удалить несуществующее резюме"""
    response = await client.delete('/api/resumes/9999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Resume not found or forbidden'


@pytest.mark.asyncio
async def test_get_resume_not_found(client):
    """Получить несуществующее резюме"""
    response = await client.get('/api/resumes/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Resume not found'
