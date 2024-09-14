from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 创建一个 Line 图表
line = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

# 添加 X 轴数据
line.add_xaxis(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])

# 添加左侧 Y 轴的折线图数据
line.add_yaxis(
    "Left Y-Axis",
    [10, 20, 15, 30, 25, 35],
    yaxis_index=0,  # 指定左侧 Y 轴
    label_opts=opts.LabelOpts(is_show=False)
)

# 添加右侧 Y 轴的折线图数据
line.add_yaxis(
    "Right Y-Axis",
    [100, 200, 150, 300, 250, 350],
    yaxis_index=1,  # 指定右侧 Y 轴
    label_opts=opts.LabelOpts(is_show=False)
)

# 设置 Y 轴的范围和名称
line.extend_axis(
    yaxis=opts.AxisOpts(
        name="Right Y-Axis",
        type_="value",
        min_=0,  # 右侧 Y 轴最小值
        max_=400,  # 右侧 Y 轴最大值
        position="right"
    )
)

# 设置左侧 Y 轴的范围
line.set_global_opts(
    yaxis_opts=opts.AxisOpts(
        name="Left Y-Axis",
        min_=0,  # 左侧 Y 轴最小值
        max_=50,  # 左侧 Y 轴最大值
        position="left"
    ),
    title_opts=opts.TitleOpts(title="Multi Y-Axis Line Chart")
)

# 渲染图表
line.render()
