import sys

from plotnn import plotnn
import plotnn.tikzeng as tk


def conv_block(block_prefix, input_name, input_offset, output_width, output_channels, width, height, depth):
    layers = []
    for i, channel in enumerate(output_channels):
        if i == 0:
            layer = tk.Conv2D(name='conv_0', out_channel=channel, activation="relu",
                              location=input_name, offset=input_offset, width=width, height=height, depth=depth)
        elif i == len(output_channels) - 1:
            layer = tk.Conv2D(name='conv_{}'.format(i), out_width=output_width, out_channel=channel,
                              activation="relu", location="conv_{}-east".format(i-1), offset=(0, 0, 0),
                              width=width, height=height, depth=height, caption="ConvReLU")
        else:
            layer = tk.Conv2D(name='conv_{}'.format(i), out_channel=channel,
                              activation="relu", location="conv_{}-east".format(i-1), offset=(0, 0, 0),
                              width=width, height=height, depth=height)
        layers.append(layer)
    layers.append(tk.Pool(name="pool", location="conv_{}-east".format(len(output_channels)-1), offset=(0, 0, 0),
                          width=width, height=height//2, depth=depth//2, opacity=0.5, caption="MaxPool"))
    block = tk.Block(block_prefix, layers)
    return block


def main():
    namefile = str(sys.argv[0]).split('.')[0]

    block0 = conv_block("block0", "input-east", (4, 0, 0), 224, (64, 64), 3, 48, 48)
    block1 = conv_block("block1", block0.output_name+"-east", (2, 0, 0), 112, (128, 128), 4, 24, 24)
    block2 = conv_block("block2", block1.output_name+"-east", (1, 0, 0), 56, (256, 256, 256), 6, 12, 12)
    block3 = conv_block("block3", block2.output_name+"-east", (1, 0, 0), 28, (512, 512, 512), 8, 6, 6)
    block4 = conv_block("block4", block3.output_name+"-east", (1, 0, 0), 14, (512, 512, 512), 8, 3, 3)

    arch = [
        tk.Box("input", xlabel=3, ylabel=224, zlabel=224, width=2, height=48, depth=48, caption="Input"),
        tk.Image("image", "../LaTex/fcn8s/cats.jpg", location="input-east", offset=(0, 0, 0), width=8, height=8),
        block0,
        block1,
        block2,
        block3,
        block4,
        tk.Box("flatten", xlabel="7x7x512", location=block4.output_name+"-east", offset=(2, 0, 0), width=1, height=1, depth=48, caption="Flatten"),
        tk.FC("fc0", out_channel=4096, activation="relu", location="flatten-east", offset=(1, 0, 0), width=1, depth=24, caption="FC"),
        tk.FC("fc1", out_channel=4096, activation="relu", location="fc0-east", offset=(1, 0, 0), width=1, depth=24, caption="FC"),
        tk.FC("fc2", out_channel=1000, location="fc1-east", offset=(1, 0, 0), width=1, depth=12, caption="FC"),
        tk.Softmax("softmax", out_channel=1000, location="fc2-east", offset=(1, 0, 0), width=1, height=1, depth=12, caption="Softmax"),
        tk.Connection("input", block0.input_name),
        tk.Connection(block0.output_name, block1.input_name),
        tk.Connection(block1.output_name, block2.input_name),
        tk.Connection(block2.output_name, block3.input_name),
        tk.Connection(block3.output_name, block4.input_name),
        tk.Connection(block4.output_name, "flatten"),
        tk.Connection("flatten", "fc0"),
        tk.Connection("fc0", "fc1"),
        tk.Connection("fc1", "fc2"),
        tk.Connection("fc2", "softmax"),
        tk.Anchor("out", "softmax-east", (2, 0, 0)),
        tk.Connection("softmax", "out"),
        tk.Text("Output", location="out-east", offset=(0, -0.25, 0), bold=True, fontsize="small"),
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
