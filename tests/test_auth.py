import allure
import pytest

@allure.feature("Todo API")
@allure.story("鉴权与权限")
class TestAuth:

    def test_no_token(self, api_client, base_url):
        """无 Token"""
        resp = api_client.post(f"{base_url}/todos", json={"title": "x"})
        assert resp.status_code == 401

    def test_empty_token(self, api_client, base_url):
        """Token 为空"""
        resp = api_client.post(f"{base_url}/todos", json={"title": "x"}, headers={"Authorization": ""})
        assert resp.status_code == 401

    def test_invalid_token(self, api_client, base_url):
        """错误 Token"""
        resp = api_client.post(f"{base_url}/todos", json={"title": "x"}, headers={"Authorization": "Bearer wrong_token_123"})
        assert resp.status_code == 401

    def test_malformed_token(self, api_client, base_url):
        """格式错误 Token (缺少 Bearer)"""
        resp = api_client.post(f"{base_url}/todos", json={"title": "x"}, headers={"Authorization": "invalid_format_token"})
        assert resp.status_code == 401

    @pytest.mark.skip(reason="需结合真实过期Token机制或Mock")
    def test_expired_token(self, api_client, base_url):
        """过期 Token"""
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.expired..."
        resp = api_client.post(f"{base_url}/todos", json={"title": "x"}, headers={"Authorization": f"Bearer {expired_token}"})
        assert resp.status_code == 401