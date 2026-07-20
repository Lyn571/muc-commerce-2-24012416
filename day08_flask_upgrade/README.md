# 第8天学生项目：Flask数据看板强化

## 学生信息

- 姓名：李晓丰
- 学号：24012416
- 已完成路由或接口：`/health`、`/api/metrics`、`/api/categories`、`/api/ask`统一400错误响应
- 测试文件：`tests/test_api.py`，共5项接口测试
- 尚未解决的问题：无

## 运行方法

在项目根目录执行：

```powershell
python -m pip install -r requirements.txt
python validate_day08_environment.py
python app.py
```

浏览器访问 `http://127.0.0.1:5000`。

- 用户名：`student`
- 密码：`day07`

## 接口说明

- `GET /health`：无需登录，返回服务健康状态。
- `GET /api/metrics`：登录后返回4张指标卡，保留`label`、`value`、`note`。
- `GET /api/categories`：登录后返回全部品类记录。
- `GET /api/categories?category=Fashion`：登录后仅返回Fashion记录。
- `POST /api/ask`：登录后进行离线数据问答；空问题返回统一400 JSON。

接口中的数据均由`services/data_service.py`读取CSV并计算，不在路由中硬编码指标。

## 自动化测试

执行：

```powershell
python -m unittest discover -s tests -v
```

测试覆盖：健康检查、未登录接口拦截、指标接口、品类筛选接口、统一400错误响应。

## 提交前检查

```powershell
python validate_day08_environment.py
python validate_day08_submission.py
python -m unittest discover -s tests -v
```

不要提交`.venv/`、`__pycache__/`、`.env`、真实密钥或缓存文件。
