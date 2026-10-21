# 开发指南

本文面向开发者：项目结构、如何新增命令、LLM provider 接口、代码规范工具链。

## 项目结构

```
app/
├── core/            # 基础设施：config（配置加载）、bot（Application 组装）、web（Flask health check）
├── handlers/
│   ├── commands/    # 斜杠命令，每个文件一个模块，自动注册
│   ├── messages/    # 消息处理器（非命令消息），自动注册
│   ├── error.py     # 全局错误处理器，异常上报给 MASTER_ID
│   └── permissions.py  # 权限 guard：require_authorized / require_master
├── services/        # 业务服务，实例在 run.py 创建后注入 bot_data
│   └── llm/         # 统一 LLM 接口：base.py + providers/ + factory.py
├── scheduled/       # JobQueue 定时任务（喝水/上下班提醒）
└── data/            # 数据文件（yaml），由 services 加载
```

## 新增一个命令

1. 在 `app/handlers/commands/` 下新建 `<name>.py`。
2. 模块中定义 `async def` 处理函数和 `register(application)` 函数，后者调用 `application.add_handler(CommandHandler("name", handler))`。
3. 无需手动注册到任何列表——`app/handlers/commands/__init__.py` 通过 `pkgutil.iter_modules` 自动发现并导入所有模块，存在可调用的 `register` 即注册。
4. 命令内通过 `context.bot_data.get("xxx_service")` 取服务；服务实例在 `run.py` 的 `bot_data` 字典中注入。
5. 需要权限的命令使用 `app/handlers/permissions.py` 的 guard：
   - `await require_authorized(update, context)`：master 或指定群组可用，拒绝时自动回复
   - `await require_master(update, silent=...)`：仅 master；`silent=True` 时静默拒绝（如 `/admin`）

消息处理器（非命令）同理放在 `app/handlers/messages/`，用 `MessageHandler(filters.XXX, handler)` 注册。

## Deprecated 功能的约定

**弃用功能不删代码**：保留文件，在模块顶部加 `DEPRECATED = True` 标记，discovery 机制会打印跳过提示且不注册。现有例子：`draw.py`、`scholar.py`。

注意：被标记的模块仍会被 **import**（discovery 需要读 flag），所以其顶层 import 必须能在当前依赖下通过——不要在 deprecated 模块的模块级引用已删除的符号；必要时把 import 挪进函数体。

## LLM Provider 接口

所有 LLM 调用走统一接口 `app/services/llm/base.py` 中的 `LLMService`：

```python
class LLMService(ABC):
    def get_response(self, prompt: str, system_prompt: str | None = None) -> str: ...
```

- 实现在 `app/services/llm/providers/` 下，每个 provider 一个文件。`openai.py` 是参考实现（OpenAI 已弃用，代码保留作模板）。
- `factory.py` 的 `create_llm_service()` 读 `config.yaml` 的 `LLM:` section 并返回实例；`LLM.PROVIDER` 为空/未知/未配置时返回 `None`，命令侧须对 `None` 降级回复（现有命令已处理）。
- `LLM:` section 在 `config.py` 中是**可选**的（`config.get("LLM", {})`），缺失不会导致启动崩溃。
- 新增 provider：在 `providers/` 新建文件实现 `LLMService`，在 `factory.py` 的 provider 分支表中注册，并在 `config.template.yaml` 的 `LLM:` section 注释中补充可用值。

## 工具链

```bash
uv sync                                 # 安装依赖（含 dev 依赖 ruff）
uv run ruff check .                     # lint
uv run ruff format .                    # 格式化
git config core.hooksPath .githooks     # 启用 pre-commit 钩子（每个 clone 一次）
```

- ruff 配置在 `pyproject.toml` 的 `[tool.ruff]`：`target-version = "py311"`，规则集 `E,F,I,UP,B`，`line-length = 120`。
- `.githooks/pre-commit` 会在每次 `git commit` 前对暂存的 `.py` 文件运行 `ruff format` 并重新暂存；uv/ruff 不可用时跳过、不阻断提交。
- deprecated 模块（draw.py/scholar.py）在 ruff `per-file-ignores` 中放宽了 E501，保持原样不迁移、不格式化重写。

## 定时任务

`app/scheduled/reminders.py` 的 `schedule_reminders(job_queue)` 在 `run_bot` 中调用。需要 `[job-queue]` extra 依赖（已在 pyproject 中声明 `python-telegram-bot[job-queue]`）。

- `run_daily(callback, time_obj, days=...)`：每日定点；`time_obj` 为带 tzinfo 的 `datetime.time`
- `run_once(callback, when, data={...}, name=...)`：一次性任务；回调内通过 `job.data` 读取参数（PTB v20+ 改名，旧版叫 `job.context`）

## 错误处理

`app/handlers/error.py` 是全局兜底：未捕获的 handler 异常会汇总 update/chat_data/user_data/traceback 发给 `MASTER_ID`，长消息按换行边界切分（≤4096/条）。
