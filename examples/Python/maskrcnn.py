import sys
from plotnn import plotnn
import plotnn.tikzeng as tk


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    arch = [
        # Input
        tk.Box("input", xlabel=3, width=2, height=32, depth=32, caption="Input"),
        tk.Image("image", "./images/dogcat.jpg",
                 location="input-east", offset=(0, 0, 0), width=6, height=6),
        # Convnet Backbone
        tk.Conv2D("backbone", location="input", offset=(3, 0, 0),
                  width=24, height=20, depth=20, caption="Backbone"),
        # RPN
        tk.Box("RPN", location="backbone-east", offset=(3, 4, 0),
               color="\\orange", width=12, height=16, depth=16, caption="RPN"),
        # RoIAlign
        tk.Box("feature", location="backbone-east", offset=(8, 0, 0),
               color="\\olive", width=4, height=20, depth=20),
        tk.Frustum("RoIAlign", location="feature-east",
                   input_offset=(0, -0.8, 1), input_width=8, input_height=10,
                   output_offset=(4, 0.8, -1), output_width=12, output_height=12,
                   caption="RoIAlign"),
        tk.Grid("roi_in", location="RoIAlign-west", width=8, height=10, step=7),
        tk.Box("roi", location="RoIAlign-east", width=4, height=12, depth=12,
               color="\\red", caption="ROI"),
        tk.Grid("roi_out", location="roi-east", width=12, height=12, step=7),
        # Box head
        tk.FC("fc0", location="roi-east", activation="relu", offset=(3, 5, 0), depth=12),
        tk.FC("fc1", location="fc0-east", activation="relu", offset=(1, 0, 0), depth=12, caption="FC"),
        tk.FC("class_head", location="fc1-east", offset=(2, 1, 0), width=8, caption="Class"),
        tk.FC("box_head", location="fc1-east", offset=(2, -1, 0), width=4, caption="BBox"),
        # Mask head
        tk.ConvTranspose2D("deconv0", location="roi-east", offset=(3, 0, 0),
                           height=16, depth=16),
        tk.ConvTranspose2D("deconv1", location="deconv0-east", offset=(0.5, 0, 0),
                           height=16, depth=16, caption="Conv"),
        tk.ConvTranspose2D("deconv2", location="deconv1-east", offset=(0.5, 0, 0),
                           height=16, depth=16),
        tk.Conv2D("mask_head", location="deconv2-east", offset=(2, 0, 0),
                  height=16, depth=16, caption="Mask"),
        tk.Image("mask", "./images/cat_seg.jpg",
                 location="mask_head-east", offset=(0, 0, 0), height=3, width=3),
        # Connections
        tk.Connection("input", "backbone"),
        tk.Connection("backbone", "RPN"),
        tk.Connection("backbone", "feature"),
        tk.Connection("RPN", "feature"),
        tk.Connection("roi", "fc0"),
        tk.Connection("fc0", "fc1"),
        tk.Connection("fc1", "class_head"),
        tk.Connection("fc1", "box_head"),
        tk.Connection("roi", "deconv0"),
        tk.Connection("deconv2", "mask_head"),
    ]
    plotnn.generate([arch], namefile + '.tex')


if __name__ == '__main__':
    main()
