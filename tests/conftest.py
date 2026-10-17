import os
import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TOKEN = os.getenv("API_TOKEN", "test-token")

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {TOKEN}"})
    return session

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def created_todo(api_client, base_url):
    resp = api_client.post(f"{base_url}/todos", json={"title": "fixture-todo"})
    assert resp.status_code == 201
    todo = resp.json()
    yield todo
    api_client.delete(f"{base_url}/todos/{todo['id']}")

import os
import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TOKEN = os.getenv("API_TOKEN", "test-token")

# 1. 建议增加一个 base_url 的 fixture，因为你的测试用例里用的是 base_url 参数
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

# 2. 修改 api_client，自动注入 Token
@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    # 自动加上 Authorization 头
    # 注意：这里需要确认后端要求的格式，通常是 Bearer，也有可能是直接 Token 或者 Bearer 后面不加空格
    session.headers.update({
        "Authorization": f"Bearer {TOKEN}"
    })
    yield session
    session.close()

# 3. 如果有些测试需要单独测鉴权（不带 Token），可以在用例里直接用 requests 发，或者专门写一个不带 Token 的 fixture

@pytest.fixture(scope="session")
def auth_headers():
    # 这里返回你的 Token 头
    return {"Authorization": f"Bearer {TOKEN}"}