import sys

from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = [
        tk.Box("input", zlabel=56, xlabel=256, offset=(0, 0, 0), location=(0, 0, 0),
               color="white", height=32, depth=32, width=6, caption="Input"),
        tk.Conv2D("conv0", out_width=28, out_channel=128, offset=(2, 0, 0), location="input-east",
                  height=16, depth=16, width=4, caption="Stride2 1x1 Conv"),
        tk.Box("bn0", xlabel=128, offset=(1, 0, 0), location="conv0-east",
               color="yellow", height=16, depth=16, width=4, caption="BN"),
        tk.Box("relu0", xlabel=128, offset=(1, 0, 0), location="bn0-east",
               color="blue", height=16, depth=16, width=4, caption="RELU"),
        tk.Conv2D("conv1", out_width=28, out_channel=128, offset=(2, 0, 0), location="relu0-east",
                  height=16, depth=16, width=4, caption="3x3 Conv"),
        tk.Box("bn1", xlabel=128, offset=(1, 0, 0), location="conv1-east",
               color="yellow", height=16, depth=16, width=4, caption="BN"),
        tk.Box("relu1", xlabel=128, offset=(1, 0, 0), location="bn1-east",
               color="blue", height=16, depth=16, width=4, caption="RELU"),
        tk.Conv2D("conv2", out_width=28, out_channel=512, offset=(2, 0, 0), location="relu1-east",
                  height=16, depth=16, width=8, caption="1x1 Conv"),
        tk.Box("bn2", xlabel=512, offset=(1, 0, 0), location="conv2-east",
               color="yellow", height=16, depth=16, width=8, caption="BN"),
        tk.Sum("sum", offset=(2, 0, 0), location="bn2-east"),
        tk.Conv2D("conv3", out_width=28, out_channel=512, offset=(2, 6, 0), location="relu1-east",
                  height=16, depth=16, width=8, caption="Stride2 1x1 Conv"),
        tk.Box("bn3", xlabel=512, offset=(1, 6, 0), location="conv2-east",
               color="yellow", height=16, depth=16, width=8, caption="BN"),
        tk.Box("relu2", xlabel=512, offset=(2, 0, 0), location="sum-east",
               color="blue", height=16, depth=16, width=8, caption="RELU"),
        tk.Box("output", zlabel=28, xlabel=512, offset=(3, 0, 0), location="relu2-east",
               color="white", height=16, depth=16, width=8, caption="Output"),
        tk.Connection("input", "conv0"),
        tk.Connection("conv0", "bn0"),
        tk.Connection("bn0", "relu0"),
        tk.Connection("relu0", "conv1"),
        tk.Connection("conv1", "bn1"),
        tk.Connection("bn1", "relu1"),
        tk.Connection("relu1", "conv2"),
        tk.Connection("conv2", "bn2"),
        tk.Connection("bn2", "sum"),
        tk.Connection("sum", "relu2"),
        tk.Connection("conv3", "bn3"),
        tk.Connection("input", "conv3", origin_loc="north", target_loc="west", path="|-"),
        tk.Connection("bn3", "sum", origin_loc="east", target_loc="north", path="-|"),
        tk.Connection("relu2", "output"),
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
