"""第三天下午 Pandas 学生实验：淘宝全品类全国数据。"""

from pathlib import Path

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_CANDIDATES = [
    SCRIPT_DIR / "data" / "淘宝全品类全国数据.csv",
    SCRIPT_DIR / "淘宝全品类全国数据.csv",
    Path.cwd() / "data" / "淘宝全品类全国数据.csv",
]
DATA_PATH = next((path for path in DATA_CANDIDATES if path.exists()), None)
OUTPUT_DIR = SCRIPT_DIR / "day3_pandas_results"


def section(title):
    """打印醒目的任务标题。"""
    print(f"\n{'=' * 18} {title} {'=' * 18}")


def load_data():
    """读取数据并检查文件是否存在。"""
    if DATA_PATH is None:
        checked = "\n".join(str(path) for path in DATA_CANDIDATES)
        raise FileNotFoundError(f"未找到淘宝数据文件，已检查：\n{checked}")
    return pd.read_csv(DATA_PATH)


def main():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 180)
    pd.set_option("display.float_format", lambda value: f"{value:,.2f}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 任务1：读取数据并完成初步观察
    df = load_data()
    section("任务1：读取数据并完成初步观察")
    print("数据规模：", df.shape)
    print("字段名：", df.columns.tolist())
    print("\n前5行：")
    print(df.head(5))
    print("\n数据结构：")
    df.info()
    print(
        f"\n文字答案：本数据每一行代表一条淘宝商品记录，"
        f"共有{df.shape[0]:,}行、{df.shape[1]}列。"
    )

    # 任务2：查看字段类型与缺失值
    section("任务2：字段类型与缺失值")
    print("字段类型：")
    print(df.dtypes)
    missing_report = pd.DataFrame({
        "缺失数量": df.isna().sum(),
        "缺失率(%)": (df.isna().mean() * 100).round(1),
    }).sort_values(["缺失数量", "缺失率(%)"], ascending=False)
    print("\n缺失值报告：")
    print(missing_report)
    print(
        "\n分析说明：商品价格是数值字段，可直接进行筛选、排序、均值和中位数统计；"
        "商品销量是包含“+人付款”和“万”等文字的分档字段，暂不宜直接计算精确平均销量。"
    )

    # 任务3：选择列与选择行
    section("任务3：选择列与选择行")
    price_series = df["商品价格"]
    print("df['商品价格'] 的类型：", type(price_series))
    product_view = df[["商品id", "一级品类", "商品价格", "省份", "商品销量"]]
    print("product_view 的类型：", type(product_view))
    print("\n指定五列前5行：")
    print(product_view.head())
    print("\nloc 选择前5行指定列：")
    print(df.loc[0:4, ["一级品类", "商品价格", "省份"]])
    print("\niloc 选择前5行、前4列：")
    print(df.iloc[0:5, 0:4])
    print(
        "\n区别：df['商品价格'] 返回一维 Series；"
        "df[['商品价格']] 返回保留列结构的二维 DataFrame。"
    )

    # 任务4：条件筛选与排序
    section("任务4：条件筛选与排序")
    guangdong = df[df["省份"] == "广东"]
    condition = (df["省份"] == "广东") & (df["商品价格"] >= 1000)
    selected_columns = [
        "商品id", "一级品类", "二级品类", "商品价格", "省份", "商品销量"
    ]
    guangdong_high_price = (
        df.loc[condition, selected_columns]
        .sort_values("商品价格", ascending=False)
    )
    print("广东商品数：", len(guangdong))
    print("\n广东且价格不低于1000元的商品（价格最高前10条）：")
    print(guangdong_high_price.head(10))

    zhejiang_or_jiangsu = df[df["省份"].isin(["浙江", "江苏"])]
    print("\n浙江或江苏商品数：", zhejiang_or_jiangsu.shape[0])

    # 任务5：描述性统计与分组统计
    section("任务5：描述性统计与分组统计")
    price_description = df["商品价格"].describe().round(2)
    print("商品价格描述性统计：")
    print(price_description)
    print("\n一级品类商品数：")
    print(df["一级品类"].value_counts())

    category_summary = (
        df.groupby("一级品类")
        .agg(
            商品数=("商品id", "size"),
            平均价格=("商品价格", "mean"),
            中位价格=("商品价格", "median"),
        )
        .sort_values("平均价格", ascending=False)
        .round(2)
    )
    print("\n一级品类汇总：")
    print(category_summary)

    highest_category = category_summary.index[0]
    highest_average = category_summary.iloc[0]["平均价格"]
    lowest_category = category_summary.index[-1]
    lowest_average = category_summary.iloc[-1]["平均价格"]
    conclusion_1 = (
        f"在本数据集的{len(df):,}条商品记录中，按一级品类对商品价格进行分组统计后，"
        f"{highest_category}的平均标价最高，为{highest_average:.2f}元；"
        f"{lowest_category}的平均标价为{lowest_average:.2f}元。"
        "该结论只反映样本商品标价，不代表实际成交金额、销量或全网用户偏好。"
    )
    print("\n规范结论1：", conclusion_1)

    # 挑战任务：广东与江苏的“省份—类别”小结
    section("挑战任务：省份—类别小结")
    provinces = ["广东", "江苏"]
    subset = df[df["省份"].isin(provinces)]
    province_summary = (
        subset.groupby("省份")
        .agg(
            商品数=("商品id", "size"),
            平均价格=("商品价格", "mean"),
            中位价格=("商品价格", "median"),
        )
        .round(2)
    )

    top_categories = {}
    for province in provinces:
        counts = subset.loc[subset["省份"] == province, "一级品类"].value_counts()
        top_categories[province] = counts.index[0] if not counts.empty else "无数据"
    province_summary["最常见一级品类"] = pd.Series(top_categories)

    print(province_summary)
    for province in provinces:
        print(f"{province}最常见一级品类：{top_categories[province]}")

    high_province = province_summary["平均价格"].idxmax()
    low_province = province_summary["平均价格"].idxmin()
    conclusion_2 = (
        f"在广东和江苏的样本商品中，{high_province}商品的平均标价高于{low_province}，"
        f"两省最常见一级品类分别为广东的{top_categories['广东']}和江苏的{top_categories['江苏']}。"
    )
    boundary = (
        "该比较仅基于本数据集收录的商品及其标价，未控制品类结构差异，"
        "不能推断两省真实消费水平、实际成交额或整体电商市场情况。"
    )
    print("\n规范结论2：", conclusion_2)
    print("结论边界：", boundary)

    # 导出结果，便于截图和提交
    missing_report.to_csv(OUTPUT_DIR / "missing_report.csv", encoding="utf-8-sig")
    guangdong_high_price.to_csv(
        OUTPUT_DIR / "guangdong_high_price.csv", index=False, encoding="utf-8-sig"
    )
    category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", encoding="utf-8-sig")
    province_summary.to_csv(OUTPUT_DIR / "province_summary.csv", encoding="utf-8-sig")
    (OUTPUT_DIR / "conclusions.txt").write_text(
        "规范结论1：\n" + conclusion_1 + "\n\n规范结论2：\n" + conclusion_2
        + "\n\n结论边界：\n" + boundary,
        encoding="utf-8",
    )

    # 最终验收
    assert df.shape == (25000, 15), "数据规模应为25000行、15列"
    assert 930 < df["商品价格"].mean() < 950, "商品价格均值与手册自查值不符"
    assert all((OUTPUT_DIR / name).exists() for name in [
        "missing_report.csv", "guangdong_high_price.csv",
        "category_summary.csv", "province_summary.csv", "conclusions.txt"
    ])
    print(f"\n全部任务完成，结果文件已保存到：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
