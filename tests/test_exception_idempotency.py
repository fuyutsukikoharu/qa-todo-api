import allure
import pytest


@allure.feature("Todo API")
@allure.story("异常场景与幂等性")
class TestExceptionAndIdempotency:

    def test_get_nonexistent_todo(self, api_client, base_url, auth_headers):
        """获取不存在的 ID"""
        resp = api_client.get(f"{base_url}/todos/999999999", headers=auth_headers)
        assert resp.status_code == 404

    def test_get_invalid_id_format(self, api_client, base_url, auth_headers):
        """获取非法格式的 ID (如字符串)"""
        resp = api_client.get(f"{base_url}/todos/abc", headers=auth_headers)
        assert resp.status_code in [400, 404, 422]

    def test_update_nonexistent_todo(self, api_client, base_url, auth_headers):
        """更新不存在的 ID"""
        resp = api_client.put(f"{base_url}/todos/999999999", json={"title": "test"}, headers=auth_headers)
        assert resp.status_code == 404

    def test_delete_nonexistent_todo(self, api_client, base_url, auth_headers):
        """删除不存在的 ID"""
        resp = api_client.delete(f"{base_url}/todos/999999999", headers=auth_headers)
        assert resp.status_code == 404

    def test_delete_negative_id(self, api_client, base_url, auth_headers):
        """删除负数 ID"""
        resp = api_client.delete(f"{base_url}/todos/-1", headers=auth_headers)
        assert resp.status_code in [400, 404]

    def test_repeated_delete(self, api_client, base_url, auth_headers, created_todo):
        """重复删除同一个 ID"""
        url = f"{base_url}/todos/{created_todo['id']}"
        resp1 = api_client.delete(url, headers=auth_headers)
        assert resp1.status_code in [200, 204]
        # 第二次删除
        resp2 = api_client.delete(url, headers=auth_headers)
        assert resp2.status_code == 404  # 依据 RESTful 规范，重复删除返回 404

    def test_idempotent_put(self, api_client, base_url, auth_headers, created_todo):
        """幂等性：连续 PUT 同一个 ID，结果应一致"""
        url = f"{base_url}/todos/{created_todo['id']}"
        payload = {"title": "幂等测试", "completed": True}

        resp1 = api_client.put(url, json=payload, headers=auth_headers)
        assert resp1.status_code == 200

        resp2 = api_client.put(url, json=payload, headers=auth_headers)
        assert resp2.status_code == 200
        assert resp2.json()["title"] == "幂等测试"
        assert resp2.json()["completed"] is True

    def test_idempotent_delete(self, api_client, base_url, auth_headers, created_todo):
        """幂等性：连续 DELETE，第一次成功，第二次 404"""
        url = f"{base_url}/todos/{created_todo['id']}"
        resp1 = api_client.delete(url, headers=auth_headers)
        assert resp1.status_code in [200, 204]

        resp2 = api_client.delete(url, headers=auth_headers)
        assert resp2.status_code == 404

    def test_create_duplicate_title(self, api_client, base_url, auth_headers):
        """重复创建相同 title (取决于业务，是否允许重复)"""
        title = "唯一性测试标题"
        resp1 = api_client.post(f"{base_url}/todos", json={"title": title}, headers=auth_headers)
        assert resp1.status_code == 201

        resp2 = api_client.post(f"{base_url}/todos", json={"title": title}, headers=auth_headers)
        # 如果业务不允许重复 title，应返回 400；如果允许则返回 201
        assert resp2.status_code in [201, 400]

    def test_huge_id_boundary(self, api_client, base_url, auth_headers):
        """边界值：超大 ID (如 2147483647)"""
        resp = api_client.get(f"{base_url}/todos/2147483647", headers=auth_headers)
        assert resp.status_code == 404