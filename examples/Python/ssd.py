import sys

from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]

    arch = [
        tk.Box("input", xlabel=3, ylabel=300, zlabel=300, width=2, height=48, depth=48, caption="Input"),
        tk.Image("image", "../LaTex/fcn8s/cats.jpg", location="input-east", offset=(0, 0, 0), width=8, height=8),
        tk.Box("backbone", location="input", offset=(3, 0, 0), width=32, height=24, depth=24),
        tk.Text("VGG16", location="backbone-north", offset=(0, 1.5, 0)),
        tk.Connection("input", "backbone"),

        tk.Conv2D("Conv4_3", out_channel=512, out_width=38, activation="relu",
                  location="backbone", offset=(0, 0, 0), width=8, height=24, depth=24,
                  caption="Conv4-3"),

        tk.Conv2D("Conv6", out_channel=1024, out_width=19, activation="relu",
                  location="backbone-east", offset=(2, 0, 0), width=16, height=16, depth=16),
        tk.Connection("backbone", "Conv6"),
        tk.Conv2D("Conv7", out_channel=1024, out_width=19, activation="relu", color='cyan', bandcolor='blue',
                  location="Conv6-east", offset=(1, 0, 0), width=16, height=16, depth=16),
        tk.Connection("Conv6", "Conv7"),

        tk.Conv2D("Conv8_1", out_channel=256, out_width=19, activation="relu", color='cyan', bandcolor='blue',
                  location="Conv7-east", offset=(2, 0, 0), width=8, height=16, depth=16),
        tk.Connection("Conv7", "Conv8_1"),
        tk.Conv2D("Conv8_2", out_channel=512, out_width=10, activation="relu", color='pink', bandcolor='red',
                  location="Conv8_1-east", offset=(1, 0, 0), width=12, height=12, depth=12),
        tk.Connection("Conv8_1", "Conv8_2"),

        tk.Conv2D("Conv9_1", out_channel=128, out_width=10, activation="relu", color='cyan', bandcolor='blue',
                  location="Conv8_2-east", offset=(2, 0, 0), width=6, height=12, depth=12),
        tk.Connection("Conv8_2", "Conv9_1"),
        tk.Conv2D("Conv9_2", out_channel=256, out_width=5, activation="relu", color='pink', bandcolor='red',
                  location="Conv9_1-east", offset=(1, 0, 0), width=8, height=8, depth=8),
        tk.Connection("Conv9_1", "Conv9_2"),

        tk.Conv2D("Conv10_1", out_channel=128, out_width=5, activation="relu", color='cyan', bandcolor='blue',
                  location="Conv9_2-east", offset=(2, 0, 0), width=6, height=8, depth=8),
        tk.Connection("Conv9_2", "Conv10_1"),
        tk.Conv2D("Conv10_2", out_channel=256, out_width=3, activation="relu",
                  location="Conv10_1-east", offset=(1, 0, 0), width=8, height=6, depth=6),
        tk.Connection("Conv10_1", "Conv10_2"),

        tk.Conv2D("Conv11_1", out_channel=128, out_width=3, activation="relu", color='cyan', bandcolor='blue',
                  location="Conv10_2-east", offset=(2, 0, 0), width=6, height=6, depth=6),
        tk.Connection("Conv10_2", "Conv11_1"),
        tk.Conv2D("Conv11_2", out_channel=256, out_width=1, activation="relu",
                  location="Conv11_1-east", offset=(1, 0, 0), width=8, height=4, depth=4),
        tk.Connection("Conv11_1", "Conv11_2"),

        tk.Anchor("c0", location="Conv11_2", offset=(4, -6, 0)),
        tk.Text("38x38x4", location="Conv11_2", offset=(2.5, -5.8, 0)),
        tk.Connection("Conv4_3", "c0", origin_loc="southeast", linestyle="double", path="|-"),

        tk.Anchor("c1", location="Conv11_2", offset=(4, -5, 0)),
        tk.Text("19x19x6", location="Conv11_2", offset=(2.5, -4.8, 0)),
        tk.Connection("Conv7", "c1", origin_loc="southeast", linestyle="double", path="|-"),

        tk.Anchor("c2", location="Conv11_2", offset=(4, -4, 0)),
        tk.Text("10x10x6", location="Conv11_2", offset=(2.5, -3.8, 0)),
        tk.Connection("Conv8_2", "c2", origin_loc="southeast", linestyle="double", path="|-"),

        tk.Anchor("c3", location="Conv11_2", offset=(4, -3, 0)),
        tk.Text("5x5x6", location="Conv11_2", offset=(2.5, -2.8, 0)),
        tk.Connection("Conv9_2", "c3", origin_loc="southeast", linestyle="double", path="|-"),

        tk.Anchor("c4", location="Conv11_2", offset=(4, -2, 0)),
        tk.Text("3x3x4", location="Conv11_2", offset=(2.5, -1.8, 0)),
        tk.Connection("Conv10_2", "c4", origin_loc="southeast", linestyle="double", path="|-"),

        tk.Anchor("c5", location="Conv11_2", offset=(4, 0, 0)),
        tk.Text("1x1x4", location="Conv11_2", offset=(2.5, 0.2, 0)),
        tk.Connection("Conv11_2", "c5", linestyle="double"),

        tk.Rectangle("agg", location="Conv11_2", offset=(5, -3, 0), width=2, height=8, caption="8732 Boxes"),
        tk.Rectangle("nms", location="agg", offset=(4, 0, 0), width=2, height=8, caption="NMS"),
        tk.Connection("agg", "nms"),

        tk.Anchor("reg_head", location="backbone", offset=(8, 9, 0)),
        tk.Box("feature", xlabel="$N_{f}$", caption="feature map",
               location="reg_head", offset=(2, 0, 0), width=8, height=8, depth=8),
        tk.Text("Box Prediction Head", location="feature-south", offset=(0, -4, 0), fontsize="large"),
        tk.Conv2D("loc_head", out_channel="$N_{a}*4$", caption="cx cy w d",
                  location="feature-east", offset=(4, 0, 0), width=4, height=8, depth=8),
        tk.Conv2D("cls_head", out_channel="$N_{a}*N_{c}$", caption="pc",
                  location="feature-east", offset=(4, -4, 0), width=4, height=8, depth=8),
        tk.Connection("feature", "loc_head"),
        tk.Connection("feature", "cls_head"),

        tk.Legend(
            items=[
                (tk.Conv2D("3x3conv", activation="relu"), "3x3 Conv"),
                (tk.Conv2D("1x1conv", activation="relu", color='cyan', bandcolor='blue'), "1x1 Conv"),
                (tk.Conv2D("1x1conv", activation="relu", color='pink', bandcolor='red'), "3x3 strde2 Conv"),
                (tk.Connection((0, 0, 0), (1, 0, 0), linestyle="double"), "Box Prediction Head"),
            ],
            location="north east",
            offset=(0, 2, 0),
            scale=3,
        )

    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
