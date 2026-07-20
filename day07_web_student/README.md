# 第 7 天学生项目：电商用户分析 Web 系统

## 学生信息

- 姓名：李晓丰
- 学号：24012416
- 专题方向：B（投诉与流失）
- 已完成功能：登录/退出与访问控制、4 张指标卡、2 张真实图表、偏好品类筛选、5 类离线规则问答、当前筛选 CSV 导出
- 选择的拓展任务：C（Flask 自动化测试）；同时完成 A（导出当前筛选 CSV）
- 尚未解决的问题：无

## 运行方法

在本项目目录打开 VS Code 终端，依次执行：

```powershell
python -m pip install -r requirements.txt
python app.py
```

浏览器访问：`http://127.0.0.1:5000`

- 用户名：`student`
- 密码：`day07`

## 核心功能说明

1. `app.py`：登录、退出、看板、离线问答接口和 CSV 下载路由。
2. `services/data_service.py`：从 3 个 CSV 读取指标，完成 KPI、品类筛选和生命周期风险洞察。
3. `services/qa_service.py`：回答总用户数、流失率、偏好品类、生命周期风险和订单 5 类问题。
4. `templates/dashboard.html`：展示 4 张 KPI 卡、2 张真实图表、筛选表格和洞察。

## 拓展任务

### A：导出当前筛选 CSV

登录后先在看板选择品类，再点击“导出当前筛选 CSV”。也可直接访问：

`http://127.0.0.1:5000/download?category=Fashion`

关键实现：`app.py` 的 `/download` 路由和 `services/data_service.py` 的 `export_category_rows()`。

### C：Flask 自动化测试

运行：

```powershell
python -m unittest discover -s tests -v
```

测试覆盖：正确登录、未登录拦截、登录后看板、`/api/ask` JSON、品类筛选和 CSV 导出。

拓展证据文件：`tests/test_app.py`、`test_result.txt`。

## 验收截图

- `screenshots/01_login.png`
- `screenshots/02_dashboard.png`
- `screenshots/03_interaction.png`
- `screenshots/04_assistant.png`

截图可在本机运行项目后按以上页面重新截取；代码和自动化测试不依赖截图运行。
