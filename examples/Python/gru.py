import sys
from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = [
        # Background
        tk.Rectangle("bbox", color="\\gray", width=11, height=8, opacity=0.4,
                     linewidth="1.1pt", curve_corner=True),
        # Input
        tk.Ball("input", text="$x_t$", location="bbox", offset=(-4, -5, 0),
                color="\\blue", shade=False),
        # Output
        tk.Ball("output", text="$h_t$", location="bbox", offset=(5, 5, 0),
                color="\\red", shade=False),
        # Last hidden state
        tk.Rectangle("hlast", text="$h_{t-1}$", location="bbox", offset=(-7, 3, 0), linewidth=0),
        # Next hidden state
        tk.Rectangle("hnext", text="$h_{t}$", location="bbox", offset=(7, 3, 0), linewidth=0),

        # Concat input and hidden state
        tk.Concat("concat0", location="input", offset=(0, 2, 0), shade=False),
        tk.Connection("input", "concat0", origin_loc="north", target_loc="south"),
        tk.Connection("hlast", "concat0", origin_loc="east", target_loc="west", target_pos=2, path="-|-"),

        # # Reset gate
        tk.Rectangle("sigmoid0", location="concat0", offset=(1, 2, 0),
                     width=1, height=1, text="$\\sigma$", color="\\orange"),
        tk.Connection("concat0", "sigmoid0", origin_loc="north", target_loc="west", path="|-"),
        tk.Multiply("mul0", location="sigmoid0", offset=(2, 0, 0), shade=False),
        tk.Connection("sigmoid0", "mul0", caption="$r_t$"),
        tk.Connection("hlast", "mul0", target_loc="north", path="-|"),

        # Update gate
        tk.Rectangle("sigmoid1", location="concat0", offset=(5, 3, 0),
                     width=1, height=1, text="$\\sigma$", color="\\orange"),
        tk.Ball("minus", text="$1-$", location="sigmoid1", offset=(0, 1.5, 0), shade=False),
        tk.Multiply("mul1", location="minus", offset=(0, 1.5, 0), shade=False),
        tk.Connection("concat0", "sigmoid1", origin_loc="north", path="|-"),
        tk.Connection("sigmoid1", "minus", origin_loc="north", target_loc="south", caption="$z_t$"),
        tk.Connection("minus", "mul1", origin_loc="north", target_loc="south"),
        tk.Connection("hlast", "mul1"),

        # Output gate
        tk.Concat("concat1", location="concat0", offset=(3, 0, 0), shade=False),
        tk.Rectangle("tanh", location="concat1", offset=(4, 0, 0),
                     width=1, height=1, text="$tanh$", color="\\orange"),
        tk.Multiply("mul2", location="tanh", offset=(0, 3, 0), shade=False),
        tk.Sum("sum", location="mul2", offset=(0, 3, 0), shade=False),
        tk.Connection("concat0", "concat1"),
        tk.Connection("mul0", "concat1", origin_loc="south", target_loc="north"),
        tk.Connection("concat1", "tanh"),
        tk.Connection("sigmoid1", "mul2"),
        tk.Connection("tanh", "mul2", origin_loc="north", target_loc="south"),
        tk.Connection("mul1", "sum"),
        tk.Connection("mul2", "sum", origin_loc="north", target_loc="south"),
        tk.Connection("sum", "hnext"),
        tk.Connection("sum", "output", target_loc="south", path="-|"),
        # Legend
        tk.Legend(
            items=[
                (tk.Rectangle("fc", color="\\orange"), "Fully-Connected Layer"),
                (tk.Ball("not", text="1-", shade=False), "1 - inputs"),
                (tk.Multiply("mul", shade=False), "Element-wise Product"),
                (tk.Sum("sum", shade=False), "Element-wise Sum"),
                (tk.Concat("concat", shade=False), "Concatenation"),
            ],
            scale=1.0,
            offset=(5, 0, 0)
        )
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
