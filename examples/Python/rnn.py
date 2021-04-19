import sys
from plotnn import plotnn
import plotnn.tikzeng as tk


def rnn_block(block_prefix, k, input_location, input_offset):
    layers = [
        tk.Rectangle("hidden", location=input_location, offset=input_offset, height=2, width=1,
                     color="\\aqua", curve_corner=True, text="$h_{{ {} }}$".format(k)),
        tk.Ball("input", location="hidden-south", offset=(0, -2, 0),
                shade=False, color="\\green", text="$x_{{ {} }}$".format(k)),
        tk.Ball("output", location="hidden-north", offset=(0, 2, 0),
                shade=False, color="\\red", text="$y_{{ {} }}$".format(k)),
        tk.Connection("input", "hidden", origin_loc="north", target_loc="south"),
        tk.Connection("hidden", "output", origin_loc="north", target_loc="south"),
    ]
    block = tk.Block(block_prefix, layers, "hidden", "hidden")
    return block


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    block = rnn_block("block", "0", input_location=(0, 0, 0), input_offset=(0, 0, 0))
    block0 = rnn_block("block0", "t-1", input_location="dot-east", input_offset=(2, 0, 0))
    block1 = rnn_block("block1", "t", input_location="block0_hidden-east", input_offset=(2, 0, 0))
    block2 = rnn_block("block2", "t+1", input_location="block1_hidden-east", input_offset=(2, 0, 0))
    arch = [
        block,
        tk.Rectangle("dot", text="...", location=block.output_name, offset=(2, 0, 0), linewidth=0),
        block0,
        block1,
        block2,
        tk.Anchor("output", location=block2.output_name, offset=(2, 0, 0)),
        tk.Connection(block.output_name, "dot"),
        tk.Connection("dot", block0.input_name),
        tk.Connection(block0.output_name, block1.input_name),
        tk.Connection(block1.output_name, block2.input_name),
        tk.Connection(block2.output_name, "output")
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
