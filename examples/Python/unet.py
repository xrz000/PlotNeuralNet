import sys

from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = [
        tk.Image("input", "../LaTex/fcn8s/cats.jpg"),

        tk.Conv2D(name='conv_0', out_width=570, out_channel=64, activation="relu",
                  offset=(3, 0, 0), location="input", width=2, height=40, depth=40),
        tk.Connection("input", "conv_0", origin_loc=None),
        tk.Conv2D(name='conv_1', out_width=568, out_channel=64, activation="relu",
                  offset=(0, 0, 0), location="conv_0-east", width=2, height=40, depth=40),
        tk.Pool(name="pool_b1", offset=(1, -6, 0), location="conv_1-south",
                width=2, height=20, depth=20, opacity=0.5),
        tk.Connection("conv_1", "pool_b1", origin_loc="east", target_loc="north", path="-|"),

        tk.Conv2D(name='conv_2', out_width=282, out_channel=128, activation="relu",
                  offset=(0, 0, 0), location="pool_b1-east", width=4, height=20, depth=20),
        tk.Conv2D(name='conv_3', out_width=280, out_channel=128, activation="relu",
                  offset=(0, 0, 0), location="conv_2-east", width=4, height=20, depth=20),
        tk.Pool(name="pool_b2", offset=(1, -5, 0), location="conv_3-south",
                width=4, height=10, depth=10, opacity=0.5),
        tk.Connection("conv_3", "pool_b2", origin_loc="east", target_loc="north", path="-|"),

        tk.Conv2D(name='conv_4', out_width=138, out_channel=256, activation="relu",
                  offset=(0, 0, 0), location="pool_b2-east", width=6, height=10, depth=10),
        tk.Conv2D(name='conv_5', out_width=136, out_channel=256, activation="relu",
                  offset=(0, 0, 0), location="conv_4-east", width=6, height=10, depth=10),
        tk.Pool(name="pool_b3", offset=(1, -4, 0), location="conv_5-south",
                width=6, height=5, depth=5, opacity=0.5),
        tk.Connection("conv_5", "pool_b3", origin_loc="east", target_loc="north", path="-|"),

        tk.Conv2D(name='conv_6', out_width=66, out_channel=512, activation="relu",
                  offset=(0, 0, 0), location="pool_b3-east", width=8, height=5, depth=5),
        tk.Conv2D(name='conv_7', out_width=64, out_channel=512, activation="relu",
                  offset=(0, 0, 0), location="conv_6-east", width=8, height=5, depth=5),
        tk.Pool(name="pool_b4", offset=(1, -3, 0), location="conv_7-south",
                width=8, height=4, depth=4, opacity=0.5),
        tk.Connection("conv_7", "pool_b4", origin_loc="east", target_loc="north", path="-|"),

        tk.Conv2D(name='conv_8', out_width=30, out_channel=1024, activation="relu",
                  offset=(0, 0, 0), location="pool_b4-east", width=10, height=4, depth=4),
        tk.Conv2D(name='conv_9', out_width=28, out_channel=1024, activation="relu",
                  offset=(0, 0, 0), location="conv_8-east", width=10, height=4, depth=4),

        tk.ConvTranspose2D(name='unpool_b1', out_channel=512, offset=(1, 3, 0), location="conv_9-northeast", width=8, height=5, depth=5),
        tk.Connection("conv_9", "unpool_b1", path='|-'),
        tk.Ball("concat_b1", location="unpool_b1-east", offset=(1, 0, 0), logo="||"),
        tk.Connection("unpool_b1", "concat_b1"),
        tk.Box("concat_1", location="concat_b1-east", offset=(1, 0, 0), xlabel=1024, width=10, height=5, depth=5),
        tk.Connection("concat_b1", "concat_1"),
        tk.Connection('conv_7', 'concat_b1', origin_loc="north", target_loc="north", origin_pos=1.5, target_pos=2,
                      color="blue", linestyle="double", path="|-|"),
        tk.Conv2D(name='conv_10', out_width=54, out_channel=512, activation="relu",
                  offset=(1, 0, 0), location="concat_1-east", width=8, height=5, depth=5),
        tk.Connection("concat_1", "conv_10"),
        tk.Conv2D(name='conv_11', out_width=52, out_channel=512, activation="relu",
                  offset=(0, 0, 0), location="conv_10-east", width=8, height=5, depth=5),


        tk.ConvTranspose2D(name='unpool_b2', out_channel=256, offset=(1, 5, 0), location="conv_11-northeast", width=6, height=10, depth=10),
        tk.Connection("conv_11", "unpool_b2", path='|-'),
        tk.Ball("concat_b2", location="unpool_b2-east", offset=(1, 0, 0), logo="||"),
        tk.Connection("unpool_b2", "concat_b2"),
        tk.Box("concat_2", location="concat_b2-east", offset=(1, 0, 0), xlabel=512, width=8, height=10, depth=10),
        tk.Connection("concat_b2", "concat_2"),
        tk.Connection('conv_5', 'concat_b2', origin_loc="north", target_loc="north", origin_pos=1, target_pos=4,
                      color="blue", linestyle="double", path="|-|"),
        tk.Conv2D(name='conv_12', out_width=102, out_channel=256, activation="relu",
                  offset=(1, 0, 0), location="concat_2-east", width=6, height=10, depth=10),
        tk.Connection("concat_2", "conv_12"),
        tk.Conv2D(name='conv_13', out_width=100, out_channel=256, activation="relu",
                  offset=(0, 0, 0), location="conv_12-east", width=6, height=10, depth=10),

        tk.ConvTranspose2D(name='unpool_b3', out_channel=128, offset=(2, 6, 0), location="conv_13-northeast", width=4, height=20, depth=20),
        tk.Connection("conv_13", "unpool_b3", path='|-'),
        tk.Ball("concat_b3", location="unpool_b3-east", offset=(1, 0, 0), logo="||"),
        tk.Connection("unpool_b3", "concat_b3"),
        tk.Box("concat_3", location="concat_b3-east", offset=(1, 0, 0), xlabel=256, width=6, height=20, depth=20),
        tk.Connection("concat_b3", "concat_3"),
        tk.Connection('conv_3', 'concat_b3', origin_loc="north", target_loc="north", origin_pos=1, target_pos=6,
                      color="blue", linestyle="double", path="|-|"),
        tk.Conv2D(name='conv_14', out_width=198, out_channel=128, activation="relu",
                  offset=(1, 0, 0), location="concat_3-east", width=4, height=20, depth=20),
        tk.Connection("concat_3", "conv_14"),
        tk.Conv2D(name='conv_15', out_width=196, out_channel=128, activation="relu",
                  offset=(0, 0, 0), location="conv_14-east", width=4, height=20, depth=20),

        tk.ConvTranspose2D(name='unpool_b4', out_channel=64, offset=(2, 8, 0), location="conv_15-northeast", width=2, height=40, depth=40),
        tk.Connection("conv_15", "unpool_b4", path='|-'),
        tk.Ball("concat_b4", location="unpool_b4-east", offset=(2, 0, 0), logo="||"),
        tk.Connection("unpool_b4", "concat_b4"),
        tk.Box("concat_4", location="concat_b4-east", offset=(2, 0, 0), xlabel=128, width=4, height=40, depth=40),
        tk.Connection("concat_b4", "concat_4"),
        tk.Connection('conv_1', 'concat_b4', origin_loc="north", target_loc="north", origin_pos=1, target_pos=8,
                      color="blue", linestyle="double", path="|-|"),
        tk.Conv2D(name='conv_16', out_width=390, out_channel=64, activation="relu",
                  offset=(2, 0, 0), location="concat_4-east", width=2, height=40, depth=40),
        tk.Connection("concat_4", "conv_16"),
        tk.Conv2D(name='conv_17', out_width=388, out_channel=64, activation="relu",
                  offset=(0, 0, 0), location="conv_16-east", width=2, height=40, depth=40),
        tk.Conv2D(name='conv_18', out_width=388, out_channel=2,
                  offset=(2, 0, 0), location="conv_17-east", width=1, height=40, depth=40),
        tk.Connection("conv_17", "conv_18"),

        tk.Softmax(name="softmax", out_channel=2, offset=(1, 0, 0), location="conv_18-east",
                   width=1, height=40, depth=40, caption="softmax"),
        tk.Connection("conv_18", "softmax"),
        tk.Legend(
            items=[
                (tk.Conv2D("conv"), "Conv2D"),
                (tk.Conv2D("conva", activation="relu"), "Conv2D+ReLU"),
                (tk.ConvTranspose2D("deconv"), "Upsample+Conv"),
                (tk.Pool("maxpool"), "MaxPooling"),
                (tk.Softmax("softmax"), "Softmax"),
                (tk.Ball("concat", logo="||", radius=0.7), "Concat"),
                (tk.Connection((0, 0, 0), (1, 0, 0), color="blue", linestyle="double"), "Copy and Crop"),
            ],
            scale=3.0,
            location="south east",
            offset=(0, 0, 0)
        )
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
