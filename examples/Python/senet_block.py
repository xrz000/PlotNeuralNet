import sys

from plotnn import plotnn
import plotnn.tikzeng as tk


arch = [
    tk.Box("input", zlabel="W", xlabel="C'", location=(0, 0, 0), offset=(0, 0, 0),
           color="white", height=16, depth=16, width=8, caption="Input"),
    tk.Conv2D("conv0", out_width="W", out_channel="C", location="input-east", offset=(2, 0, 0),
              height=16, depth=16, width=4, caption="Conv"),
    tk.Box("gap", zlabel=1, xlabel="C", location="conv0-east", offset=(2, 2, 0),
           height=1, depth=1, width=4, caption="GAP"),
    tk.FC("fc0", out_channel="C/r", offset=(2, 0, 0), location="gap-east",
          activation="relu", width=3, caption="FC+ReLU"),
    tk.FC("fc1", out_channel="C", offset=(2, 0, 0), location="fc0-east",
          activation="sigmoid", width=4, caption="FC+Sigmoid"),
    tk.Multiply("mul", offset=(10, 0, 0), location="conv0-east"),
    tk.Box("output", zlabel="W", xlabel="C", offset=(2, 0, 0), location="mul-east",
           color="white", height=16, depth=16, width=4, caption="Output"),

    tk.Connection("input", "conv0"),
    tk.Connection("conv0", "gap"),
    tk.Connection("gap", "fc0"),
    tk.Connection("fc0", "fc1"),
    tk.Connection("fc1", "mul", target_loc="north"),
    tk.Connection("conv0", "mul"),
    tk.Connection("mul", "output"),
    tk.Connection((-2, 0, 0), "input"),
    tk.Connection("output", "output", target_loc=(2, 0, 0)),
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
