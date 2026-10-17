import allure
import requests

@allure.feature("Todo API")
@allure.story("创建待办")
def test_create_todo(api_client, base_url):
    resp = api_client.post(f"{base_url}/todos", json={"title": "学习 Pytest"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "学习 Pytest"
    assert data["completed"] is False

@allure.story("获取待办")
def test_get_todo(api_client, base_url, created_todo):
    resp = api_client.get(f"{base_url}/todos/{created_todo['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created_todo["id"]

@allure.story("鉴权失败")
def test_unauthorized(base_url):
    resp = requests.post(f"{base_url}/todos", json={"title": "x"})
    assert resp.status_code == 401


import allure


@allure.feature("Todo API")
@allure.story("基础CRUD")
class TestTodoCRUD:
    def test_create_todo(self, api_client, base_url, auth_headers):
        resp = api_client.post(f"{base_url}/todos", json={"title": "学习 Pytest"}, headers=auth_headers)
        assert resp.status_code == 201
        assert resp.json()["title"] == "学习 Pytest"

    def test_get_todo(self, api_client, base_url, auth_headers, created_todo):
        resp = api_client.get(f"{base_url}/todos/{created_todo['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == created_todo["id"]

    def test_update_todo(self, api_client, base_url, auth_headers, created_todo):
        update_data = {"title": "更新后的标题", "completed": True}
        resp = api_client.put(f"{base_url}/todos/{created_todo['id']}", json=update_data, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["title"] == "更新后的标题"
        assert resp.json()["completed"] is True

    def test_delete_todo(self, api_client, base_url, auth_headers, created_todo):
        resp = api_client.delete(f"{base_url}/todos/{created_todo['id']}", headers=auth_headers)
        assert resp.status_code in [200, 204]

    def test_get_deleted_todo(self, api_client, base_url, auth_headers, created_todo):
        # 先删除
        api_client.delete(f"{base_url}/todos/{created_todo['id']}", headers=auth_headers)
        # 再次获取应 404
        resp = api_client.get(f"{base_url}/todos/{created_todo['id']}", headers=auth_headers)
        assert resp.status_code == 404