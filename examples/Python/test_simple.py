import sys
import plotnn.tikzeng as tk


# defined your arch
arch = [
    tk.to_head(),
    tk.to_cor(),
    tk.to_begin(),
    tk.to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
    tk.to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    tk.to_Conv("conv2", 128, 64, offset="(1,0,0)", to="(pool1-east)", height=32, depth=32, width=2 ),
    tk.to_connection( "pool1", "conv2"),
    tk.to_Pool("pool2", offset="(0,0,0)", to="(conv2-east)", height=28, depth=28, width=1),
    tk.to_SoftMax("soft1", 10 ,"(3,0,0)", "(pool1-east)", caption="SOFT"  ),
    tk.to_connection("pool2", "soft1"),
    tk.to_Sum("sum1", offset="(1.5,0,0)", to="(soft1-east)", radius=2.5, opacity=0.6),
    tk.to_connection("soft1", "sum1"),
    tk.to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    tk.to_generate(arch, namefile + '.tex' )


if __name__ == '__main__':
    main()
