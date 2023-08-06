from newsworthycharts import SerialChart
from newsworthycharts.storage import DictStorage


def test_color_function():
    container = {}
    ds = DictStorage(container)
    c = SerialChart(800, 500, storage=ds)
    data = [
      ["2016-01-01", -4],
      ["2017-01-01", 4],
      ["2018-01-01", None],
      ["2019-01-01", -1]
    ]
    c.color_fn = "positive_negative"
    c.data.append(data)
    c.type = "bars"
    # highlighting a bar should not affect this color rule
    c.highlight = "2019-01-01"

    c.render("test", "png")

    neutral_color = c._style["neutral_color"]
    pos_color = c._style["positive_color"]
    neg_color = c._style["negative_color"]
    bar_colors = [bar.get_facecolor() for bar in c.ax.patches]
    assert(bar_colors[0] == neg_color)
    assert(bar_colors[1] == pos_color)
    assert(bar_colors[2] == neutral_color)
    assert(bar_colors[3] == neg_color)
