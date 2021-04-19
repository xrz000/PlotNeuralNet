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
        tk.Rectangle("hlast", text="$h_{t-1}$", location="bbox", offset=(-7, -3, 0), linewidth=0),
        # Last cell state
        tk.Rectangle("clast", text="$c_{t-1}$", location="bbox", offset=(-7, 3, 0), linewidth=0),
        # Next hidden state
        tk.Rectangle("hnext", text="$h_{t}$", location="bbox", offset=(7, -3, 0), linewidth=0),
        # Next cell state
        tk.Rectangle("cnext", text="$c_{t}$", location="bbox", offset=(7, 3, 0), linewidth=0),

        # Concat input and hidden state
        tk.Concat("concat0", location="input", offset=(0, 2, 0), shade=False),
        tk.Connection("input", "concat0", origin_loc="north", target_loc="south"),
        tk.Connection("hlast", "concat0"),

        # Forget gate
        tk.Rectangle("sigmoid0", location="concat0", offset=(0, 2, 0),
                     width=1, height=1, text="$\\sigma$", color="\\orange"),
        tk.Connection("concat0", "sigmoid0", origin_loc="north", target_loc="south"),
        tk.Multiply("mul0", location="sigmoid0", offset=(0, 4, 0), shade=False),
        tk.Connection("clast", "mul0"),
        tk.Connection("sigmoid0", "mul0", origin_loc="north", target_loc="south", caption="$f_t$"),

        # Input gate
        tk.Rectangle("sigmoid1", location="sigmoid0", offset=(2, 0, 0),
                     width=1, height=1, text="$\\sigma$", color="\\orange"),
        tk.Rectangle("tanh0", location="sigmoid1", offset=(2, 0, 0),
                     width=1, height=1, text="$tanh$", color="\\orange"),
        tk.Multiply("mul1", location="tanh0", offset=(0, 2, 0), shade=False),
        tk.Connection("concat0", "sigmoid1", origin_loc="east", target_loc="south", path="-|"),
        tk.Connection("concat0", "tanh0", origin_loc="east", target_loc="south", path="-|"),
        tk.Connection("sigmoid1", "mul1", origin_loc="north", target_loc="west", path="|-", caption="$i_t$"),
        tk.Connection("tanh0", "mul1", origin_loc="north", target_loc="south", caption="$\\tilde{c}_t$"),
        tk.Sum("sum0", location="mul1", offset=(0, 2, 0), shade=False),
        tk.Connection("mul1", "sum0", origin_loc="north", target_loc="south"),
        tk.Connection("mul0", "sum0", origin_loc="east", target_loc="west"),

        # Output gate
        tk.Rectangle("sigmoid2", location="tanh0", offset=(2, -2, 0),
                     width=1, height=1, text="$\\sigma$", color="\\orange"),
        tk.Multiply("mul2", location="sigmoid2", offset=(2, 0, 0), shade=False),
        tk.Rectangle("tanh1", location="mul2", offset=(0, 2, 0),
                     width=1, height=1, text="$tanh$", color="\\yellow"),
        tk.Connection("concat0", "sigmoid2", origin_loc="east", target_loc="west"),
        tk.Connection("sigmoid2", "mul2", origin_loc="east", target_loc="west", caption="$o_t$"),
        tk.Connection("sum0", "tanh1", origin_loc="east", target_loc="north", path="-|"),
        tk.Connection("tanh1", "mul2", origin_loc="south", target_loc="north"),

        tk.Connection("mul2", "hnext"),
        tk.Connection("mul2", "output", origin_loc="east", target_loc="south", path="-|"),
        tk.Connection("sum0", "cnext"),
        # Legend
        tk.Legend(
            items=[
                (tk.Rectangle("fc", color="\\orange"), "Fully-Connected Layer"),
                (tk.Rectangle("act", color="\\yellow"), "Activation Function"),
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
