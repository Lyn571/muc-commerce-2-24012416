from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有 {int(metrics['用户数']):,} 名用户。"
    if any(word in normalized for word in ["流失率", "流失情况", "流失人数"]):
        return (
            f"总体流失率为 {metrics['流失率']:.1%}，"
            f"共 {int(metrics['流失人数']):,} 名用户流失。"
        )
    if any(word in normalized for word in ["偏好品类", "品类用户", "哪个品类", "用户最多"]):
        top = category_df.loc[category_df["用户数"].idxmax()]
        return f"用户最多的偏好品类是 {top['PreferedOrderCat']}，共有 {int(top['用户数']):,} 名用户。"
    if any(word in normalized for word in ["生命周期", "阶段风险", "风险最高", "阶段流失"]):
        risk = segment_df.loc[segment_df["流失率"].idxmax()]
        return (
            f"生命周期风险最高的是“{risk['TenureGroup']}”，"
            f"流失率为 {risk['流失率']:.1%}（{int(risk['流失人数'])}/{int(risk['用户数'])} 人）。"
        )
    if any(word in normalized for word in ["订单", "平均下单"]):
        return f"全体用户平均订单数为 {metrics['平均订单数']:.2f} 单，中位数为 {metrics['订单数中位数']:.0f} 单。"
    return "暂未识别该问题。可以询问总用户数、总体流失率、偏好品类、生命周期风险或平均订单数。"
