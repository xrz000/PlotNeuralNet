import sys
from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = [
        tk.Conv2D("conv1", out_width=512, out_channel=64, location=(0, 0, 0), offset=(0, 0, 0),
                  height=64, depth=64, width=2, caption="Conv"),
        tk.Pool("pool1", location="conv1-east", offset=(1, 0, 0), height=32, depth=32, width=2, caption="MaxPool"),
        tk.Connection("conv1", "pool1"),

        tk.Conv2D("conv2", out_width=128, out_channel=64, location="pool1-east", offset=(2, 0, 0),
                  height=32, depth=32, width=2, caption="Conv"),
        tk.Connection("pool1", "conv2"),

        tk.Pool("pool2", location="conv2-east", offset=(1, 0, 0), height=16, depth=16, width=2, caption="MaxPool"),
        tk.Connection("conv2", "pool2"),

        tk.Softmax("soft1", out_channel=10, location="pool2-east", offset=(3, 0, 0), height=16, depth=16, width=2, caption="Softmax"),
        tk.Connection("pool2", "soft1"),

        tk.Sum("sum1", location="soft1-east", offset=(1.5, 0, 0), radius=2.5, opacity=0.6),
        tk.Connection("soft1", "sum1"),
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
