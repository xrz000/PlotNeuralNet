import sys

from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    v1_arch = [
        tk.Text("V1", location=(0, 0, 0), fontsize="huge"),
        tk.Box("input", zlabel="W", xlabel="C", ylabel="H", location=(0, -4, 0),
               color="white", height=16, depth=16, width=8, caption="Input"),
        tk.Box("mid", zlabel="W", xlabel="C", ylabel="H",
               location="input-east", offset=(6, 0, 0), height=16, depth=16, width=8, color="green", caption=""),
        tk.Conv2D("output", out_depth="W", out_width="N", out_height="H", location="mid-east", offset=(6, 0, 0),
                  height=16, depth=16, width=4, caption="Output"),

        tk.Box("dc", zlabel="K", xlabel="1", ylabel="K", location="input-east", offset=(2, 2, 0),
               height=3, depth=3, width=1, color="green", caption="DepthwiseConv"),
        tk.Text("$\\times$ C", location="dc-east", offset=(0.75, 0, 0)),

        tk.Conv2D("pc", out_channel="C", out_height="1", out_width="1", location="mid-east", offset=(3, 2, 0),
                  height=1, depth=1, width=4, caption="PointwiseConv"),
        tk.Text("$\\times$ N", location="pc-east", offset=(0.75, 0, 0)),

        tk.Connection("input", "mid"),
        tk.Connection("mid", "output"),
        tk.Connection((-2, -4, 0), "input"),
        tk.Connection("output", "output", target_loc=(2, 0, 0)),
    ]
    v2_arch = [
        tk.Text("V2", location=(0, 0, 0), fontsize="huge"),
        tk.Box("input", zlabel="W", xlabel="C", ylabel="H", location=(0, -4, 0),
               color="white", height=16, depth=16, width=8, caption="Input"),
        tk.Conv2D("exp", out_width="W", out_channel="tC", out_height="H",
                  location="input-east", offset=(6, 0, 0), height=16, depth=16, width=16),
        tk.Box("mid", zlabel="W", xlabel="tC", ylabel="H",
               location="exp-east", offset=(6, 0, 0), height=16, depth=16, width=16, color="green", caption=""),
        tk.Conv2D("output", out_depth="W", out_width="N", out_height="H", location="mid-east", offset=(6, 0, 0),
                  height=16, depth=16, width=4, caption="Output"),

        tk.Conv2D("ec", out_width="K", out_channel="C", out_height="K", location="input-east", offset=(2, 2, 0),
                  height=2, depth=2, width=4, caption="Conv"),
        tk.Text("$\\times$ tC", location="ec-east", offset=(0.75, 0, 0)),

        tk.Box("dc", zlabel="K", xlabel="1", ylabel="K", location="exp-east", offset=(2, 2, 0),
               height=3, depth=3, width=1, color="green", caption="DepthwiseConv"),
        tk.Text("$\\times$ tC", location="dc-east", offset=(0.75, 0, 0)),

        tk.Conv2D("pc", out_channel="C", out_height="1", out_width="1", location="mid-east", offset=(3, 2, 0),
                  height=1, depth=1, width=4, caption="PointwiseConv"),
        tk.Text("$\\times$ N", location="pc-east", offset=(0.75, 0, 0)),

        tk.Connection("input", "exp"),
        tk.Connection("exp", "mid"),
        tk.Connection("mid", "output"),
        tk.Connection((-2, -4, 0), "input"),
        tk.Connection("output", "output", target_loc=(2, 0, 0)),
    ]
    plotnn.generate([v1_arch, v2_arch], namefile + '.tex')


if __name__ == '__main__':
    main()
