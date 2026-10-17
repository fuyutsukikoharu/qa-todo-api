import allure
import pytest


@allure.feature("Todo API")
@allure.story("参数校验与边界值")
class TestBoundary:

    @pytest.mark.parametrize("payload, desc", [
        ({"completed": False}, "缺失 title"),
        # 使用 pytest.param 精准标记这三个已知Bug，不影响其他正常用例
        pytest.param({"title": ""}, "title 为空字符串", marks=pytest.mark.xfail(reason="已知后端Bug")),
        pytest.param({"title": "   "}, "title 为纯空格", marks=pytest.mark.xfail(reason="已知后端Bug")),
        ({"title": None}, "title 为 null"),
        ({"title": 12345}, "title 为整数类型"),
        ({"title": True}, "title 为布尔类型"),
        ({"title": ["数组"]}, "title 为数组类型"),
        ({}, "请求体完全为空"),
    ])
    def test_create_todo_invalid_title(self, api_client, base_url, auth_headers, payload, desc):
        """验证非法参数，预期返回 400 或 422"""
        with allure.step(f"测试场景：{desc}"):
            resp = api_client.post(f"{base_url}/todos", json=payload, headers=auth_headers)
            assert resp.status_code in [400, 422], f"用例[{desc}] 失败，实际状态码：{resp.status_code}"

    def test_create_todo_max_length(self, api_client, base_url, auth_headers):
        """边界值：假设数据库允许最大长度为 255"""
        title_255 = "a" * 255
        resp = api_client.post(f"{base_url}/todos", json={"title": title_255}, headers=auth_headers)
        assert resp.status_code == 201

    @pytest.mark.xfail(reason="已知后端Bug：未校验超长字符，返回了201")
    def test_create_todo_exceed_max_length(self, api_client, base_url, auth_headers):
        """边界值：超过最大长度 256，预期拦截"""
        title_256 = "a" * 256
        resp = api_client.post(f"{base_url}/todos", json={"title": title_256}, headers=auth_headers)
        assert resp.status_code in [400, 422]

    def test_create_todo_special_characters(self, api_client, base_url, auth_headers):
        """测试特殊字符（包含 SQL 注入和 XSS 常见字符）"""
        special_title = "!@#$%^&*()_+{}|:<>?~`-=[]\\;',./\""
        resp = api_client.post(f"{base_url}/todos", json={"title": special_title}, headers=auth_headers)
        assert resp.status_code in [201, 400]  # 根据实际业务决定，一般允许特殊字符但要做转义