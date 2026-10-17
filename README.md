# Todo-API 自动化测试框架与 CI/CD 实践

![API Tests](https://github.com/fuyutsukikoharu/qa-todo-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pytest](https://img.shields.io/badge/Test-Pytest-green)
![Docker](https://img.shields.io/badge/Deploy-Docker-blue)
![Allure](https://img.shields.io/badge/Report-Allure-orange)

这是一个基于 FastAPI 构建的 Todo 后端接口自动化测试项目。项目从基础的功能测试出发，扩展至边界值、异常处理、安全鉴权及幂等性测试，并打通了 **Docker 容器化部署** 与 **GitHub Actions 持续集成 (CI)** 全链路。

🔗 **[ 查看在线 Allure 测试报告](https://fuyutsukikoharu.github.io/qa-todo-api/)**

---

##  测试成果概览

- **用例总数**：34 个（覆盖功能、边界、异常、鉴权、幂等）
- **测试通过率**：100%（包含 5 个标记为 `xfail` 的已知预期缺陷）
- **Bug 挖掘**：通过自动化脚本成功捕获 **4 个后端真实缺陷**（详见下文）。
- **执行效率**：全量接口测试在 CI 中平均耗时 40s 以内（含环境拉起）。

---

## 🛠 技术栈

- **语言**：Python 3.11
- **测试框架**：Pytest
- **网络请求**：Requests (封装 Session 保持会话)
- **报告生成**：Allure Report
- **容器化**：Docker / Docker Compose
- **CI/CD**：GitHub Actions
- **目标服务**：FastAPI (Uvicorn)

---

##  项目架构

```text
qa-todo-api/
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI 工作流
├── app/
│   └── main.py                 # FastAPI 后端服务源码
├── tests/                      # 测试用例库
│   ├── conftest.py             # 全局 Fixture (鉴权、数据前置/清理)
│   ├── test_todo_crud.py       # 基础 CRUD 功能测试
│   ├── test_boundary.py        # 等价类与边界值参数校验
│   ├── test_auth.py            # 鉴权拦截与安全测试
│   └── test_exception_idempotency.py # 异常场景与接口幂等性
├── Dockerfile                  # 镜像构建文件
├── docker-compose.yml          # 容器编排 (API 服务 + 测试执行)
├── pytest.ini                  # Pytest 全局配置
└── requirements.txt            # 依赖库