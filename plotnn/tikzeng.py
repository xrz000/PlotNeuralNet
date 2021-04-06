import os
import jinja2


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates", "objects")


def iter_to_string(t):
    return "({})".format(",".join([str(x) for x in t]))


def parse_location(location, offset=None):
    if isinstance(offset, str) and isinstance(location, str):
        return "({}-{})".format(location, offset)

    if isinstance(location, (tuple, list)):
        tmp = iter_to_string(location)
    elif isinstance(location, str):
        tmp = "({})".format(location)
    else:
        raise NotImplementedError
    if isinstance(offset, (tuple, list)):
        return "{} -- +{}".format(tmp, iter_to_string(offset))
    else:
        return tmp


def parse_color(color):
    if isinstance(color, tuple) and all(isinstance(x, int) for x in color):
        if len(color) != 3 or not all(0 <= x <= 255 for x in color):
            raise ValueError("Invalid RGB color")
        color = "{rgb,255:" + "red,{0};green,{1};blue,{2}".format(*color) + "}"
    return color


class Base(object):
    def __init__(self, name="", *args, **kwargs):
        self.attributes = kwargs
        self.attributes['name'] = name

    def to_tex(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
        template = env.get_template(self.template_name)

        return template.render(self.attributes)

    def update(self, data):
        self.attributes.update(data)

    @property
    def name(self):
        return self.attributes['name']


class Custom(Base):
    def __init__(self, name, template_name, **kwargs):
        self.template_name = template_name
        super(Custom, self).__init__(name=name, **kwargs)


class Image(Base):
    def __init__(self, name, image_path, location=(0, 0, 0), offset=(0, 0, 0),
                 width=8, height=8):
        self.template_name = "image.tex"
        super(Image, self).__init__(
            name=name, image_path=image_path,
            raw_location=location, offset=offset,
            width=width, height=height
        )

    def to_tex(self):
        self.attributes['location'] = parse_location(self.attributes['raw_location'])
        return super(Image, self).to_tex()


class Box(Base):
    def __init__(self, name,
                 location=(0, 0, 0), offset=(0, 0, 0),
                 xlabel="", ylabel="", zlabel="",
                 width=1, height=1, depth=1,
                 right_band=False, color="white",
                 bandcolor='white', caption="", **args):
        if right_band:
            self.template_name = "right_band_box.tex"
        else:
            self.template_name = "box.tex"
        super(Box, self).__init__(
            name=name, raw_location=location, offset=offset,
            xlabel=xlabel, ylabel=ylabel, zlabel=zlabel,
            width=width, height=height, depth=depth,
            color=color, bandcolor=bandcolor, caption=caption, **args
        )

    def to_tex(self):
        self.attributes['location'] = parse_location(self.attributes['raw_location'])
        self.attributes['color'] = parse_color(self.attributes['color'])
        self.attributes['bandcolor'] = parse_color(self.attributes['bandcolor'])
        xlabel = self.attributes['xlabel']
        if isinstance(xlabel, (int, str)):
            xlabel = str(xlabel).split(',')
        xlabel = ['"{}"'.format(x) for x in xlabel]
        xlabel = "{{" + ",".join(xlabel) + ",}}"
        self.attributes['xlabel'] = xlabel
        return super(Box, self).to_tex()


class Conv2D(Box):
    def __init__(self, name, out_channel="", out_height="", out_width="",
                 activation=None, color="\\ConvColor", bandcolor="\\ActColor", **args):
        right_band = activation is not None
        super(Conv2D, self).__init__(
            name=name, xlabel=out_channel, ylabel=out_height, zlabel=out_width,
            right_band=right_band, color=color, bandcolor=bandcolor, **args
        )


class ConvTranspose2D(Conv2D):
    def __init__(self, name, color="\\UnpoolColor", **args):
        super(ConvTranspose2D, self).__init__(name=name, color=color, **args)


class FC(Box):
    def __init__(self, name, out_channel="", activation=None, color="\\FcColor", **args):
        right_band = activation is not None
        super(FC, self).__init__(name=name, xlabel=out_channel, right_band=right_band, color=color, **args)


class Softmax(Box):
    def __init__(self, name, out_channel="", color="\\SoftmaxColor", **args):
        super(Softmax, self).__init__(name=name, zlabel=out_channel, color=color, **args)


class Pool(Box):
    def __init__(self, name, color="\\PoolColor", opacity=0.5, **args):
        super(Pool, self).__init__(name=name, color=color, opacity=opacity, **args)


class Anchor(Base):
    def __init__(self, name, location, offset):
        self.template_name = "anchor.tex"
        super(Anchor, self).__init__(name=name, raw_location=location, offset=offset)

    def to_tex(self):
        self.attributes['location'] = parse_location(self.attributes['raw_location'])
        return super(Anchor, self).to_tex()


class Connection(Base):
    def __init__(self, origin="", target="", origin_loc="east", target_loc="west",
                 origin_pos=1.5, target_pos=1.5, path="--", arrow="-Stealth",
                 color="black", linestyle="solid", linewidth="1.2pt", opacity=0.6):
        self.template_name = "connection.tex"
        super(Connection, self).__init__(
            origin=origin, target=target,
            origin_loc=origin_loc, target_loc=target_loc,
            origin_pos=origin_pos, target_pos=target_pos,
            path=path, arrow=arrow, color=color,
            linestyle=linestyle, linewidth=linewidth, opacity=opacity,
        )

    def to_tex(self):
        self.attributes['color'] = parse_color(self.attributes['color'])
        self.attributes['style'] = "{}, arrows={}, line width={}, draw={}, opacity={}".format(
            self.attributes['linestyle'], self.attributes['arrow'], self.attributes['linewidth'],
            self.attributes['color'], str(self.attributes['opacity'])
        )

        if self.attributes['path'] in ["--", "|-", "-|"]:
            self.attributes['origin'] = parse_location(
                self.attributes['origin'], self.attributes['origin_loc']
            )
            self.attributes['target'] = parse_location(
                self.attributes['target'], self.attributes['target_loc']
            )
        return super(Connection, self).to_tex()


class Ball(Base):
    def __init__(self, name, location=(0, 0, 0), offset=(0, 0, 0),
                 color="white", logo="",
                 radius=2.5, opacity=0.6, **args):
        self.template_name = "node.tex"
        super(Ball, self).__init__(
            name=name, raw_location=location, offset=offset,
            opacity=opacity, radius=radius, color=color,
            logo=logo, **args
        )

    def to_tex(self):
        self.attributes['location'] = parse_location(self.attributes['raw_location'])
        self.attributes['color'] = parse_color(self.attributes['color'])
        return super(Ball, self).to_tex()


class Sum(Ball):
    def __init__(self, name, color="\\SumColor", logo="+", **args):
        super(Sum, self).__init__(name=name, color=color, logo=logo, **args)


class Multiply(Ball):
    def __init__(self, name, color="\\SumColor", logo="\\times", **args):
        super(Multiply, self).__init__(name=name, color=color, logo=logo, **args)


class Concat(Ball):
    def __init__(self, name, color="\\SumColor", logo="||", **args):
        super(Concat, self).__init__(name=name, color=color, logo=logo, **args)


class Text(Base):
    def __init__(self, text="", location=(0, 0, 0), offset=(0, 0, 0),
                 color="black", bold=True, fontsize="small"):
        self.template_name = "text.tex"
        super(Text, self).__init__(
            name="", raw_location=location, offset=offset,
            text=text, color=color, bold=bold, fontsize=fontsize,
        )

    def to_tex(self):
        self.attributes['location'] = parse_location(self.attributes['raw_location'])
        self.attributes['color'] = parse_color(self.attributes['color'])
        return super(Text, self).to_tex()


class Block(object):
    def __init__(self, name, layers):
        self.layers = layers
        old_names = set([x.name for x in self.layers])
        for layer in self.layers:
            new_name = "{}_{}".format(name, layer.attributes["name"])
            update_dict = {"name": new_name}
            for aname in ['raw_location', 'raw_origin', 'raw_target']:
                if aname in layer.attributes:
                    loc = layer.attributes[aname]
                    if self.raw_name(loc) in old_names:
                        update_dict[aname] = self.add_prefix(loc, name)
            layer.update(update_dict)

    @staticmethod
    def add_prefix(name, prefix):
        if name.startswith('('):
            return name
        else:
            return prefix + '_' + name

    @staticmethod
    def raw_name(name):
        return name.split('-')[0]

    @property
    def output_name(self):
        return self.layers[-1].name

    @property
    def input_name(self):
        return self.layers[0].name


class Legend(Base):
    def __init__(self, items=[], location="south east", offset=(0, 0, 0),
                 scale=1.0, fontsize="tiny"):
        self.template_name = "legend.tex"
        self.items = items
        if location in ["north west", "south west", "north east", "south east"]:
            anchor = location
            location = "(current bounding box.{})".format(location)
        else:
            anchor = "center"
            location = parse_location(location)
        super(Legend, self).__init__(
            name="legend", location=location, offset=offset,
            anchor=anchor, scale=scale, fontsize=fontsize)

    def to_tex(self):
        self.attributes["items"] = [
            (x[0].to_tex(), x[1]) for x in self.items
        ]
        return super(Legend, self).to_tex()
