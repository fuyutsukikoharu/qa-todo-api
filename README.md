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

##  技术栈

- **语言**：Python 3.11
- **测试框架**：Pytest
- **网络请求**：Requests (封装 Session 保持会话)
- **报告生成**：Allure Report
- **容器化**：Docker / Docker Compose
- **CI/CD**：GitHub Actions
- **目标服务**：FastAPI (Uvicorn)

---

##  快速开始

### 方式一：使用 Docker (推荐，一键启动)
无需本地配置 Python 环境，直接使用 Docker Compose 启动 API 服务并运行自动化测试：

```bash
docker compose up --build
```

*(注：测试运行结束后，Allure 原始结果将自动挂载到本地 `./allure-results` 目录。)*

### 方式二：本地开发环境运行

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 启动后端服务：
   ```bash
   uvicorn app.main:app --reload
   ```
3. 运行测试并生成报告：
   ```bash
   pytest --alluredir=./allure-results
   allure serve allure-results
   ```

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
```

---

##  核心测试设计 & Bug 记录

本项目在测试用例设计上采用了多种黑盒测试方法：
1. **等价类划分与边界值分析**：针对 `title` 字段测试了缺失、空字符串、纯空格、256 超长字符、特殊字符、非法数据类型等。
2. **状态流转与异常处理**：测试获取、更新、删除不存在的 ID，验证系统是否正确返回 404。
3. **安全与鉴权**：模拟无 Token、错误 Token 发起请求，验证后端是否拦截并返回 401。
4. **幂等性验证**：连续发起相同的 PUT 更新和 DELETE 删除，验证系统数据状态是否一致，防止脏数据。

###  发现的真实缺陷记录 (Bug Log)
在构建自动化用例过程中，发现并复现了以下后端产品缺陷（已在测试代码中使用 `@pytest.mark.xfail` ）：
- [ ] **鉴权失效**：无 Token 或错误 Token 时，依然能成功创建数据 (返回 201)。
- [ ] **参数校验缺失**：传入空字符串 `""`、纯空格 `"   "` 或超长字符时，未进行拦截，直接写入数据库。

---

##  CI/CD 流程

每次将代码 Push 到 `main` 分支时，GitHub Actions 会自动触发以下流程：
1. 检出代码并配置 Python 3.11 环境。
2. 安装依赖并后台启动 FastAPI 服务。
3. 使用 `curl` 轮询等待服务健康就绪。
4. 执行全量 Pytest 测试用例。
5. 生成 Allure 报告并自动发布到 `gh-pages` 分支（即顶部的在线报告链接）。