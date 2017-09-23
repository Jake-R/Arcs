import cairocffi as cairo
from matplotlib import colors
import math

pi = math.pi
DEFAULT_ANGLE=.5*pi


class Arc(object):
    def __init__(self, radius, angle=None, color=None):
        self.radius = radius
        self.angle = angle
        self.color = color

    def center(self, x, y, angle):
        return (math.cos(angle + pi) * self.radius + x,
                math.sin(angle + pi) * self.radius + y)


class Sequence(object):
    def __init__(self, arcs=None, angle=DEFAULT_ANGLE, color_list=None):
        if not arcs:
            self.arcs = []
        else:
            self.arcs = arcs.copy()
        self.angle = angle
        if not color_list:
            self.color_list = list(colors.BASE_COLORS.values())

    def draw(self, context, x, y, repetitions=50, starting_angle=0, line_width=1):
        i = 0
        for arc in self.arcs:
            if arc.color is None:
                if(len(self.color_list) <= i):
                    i = 0
                arc.color = self.color_list[i]
                i += 1
        degree_from = starting_angle
        degree_to = None
        context.move_to(x, y)
        for i in range(repetitions):
            for arc in self.arcs:
                degree_to = degree_from + (arc.angle if arc.angle else self.angle)
                loc = context.get_current_point()
                center = arc.center(*loc, degree_from)
                context.set_source_rgb(*arc.color)
                context.set_line_width(line_width)
                context.set_antialias(cairo.ANTIALIAS_BEST)
                context.arc(*center, arc.radius, degree_from, degree_to)
                stash_loc = context.get_current_point()
                context.stroke()
                context.move_to(*stash_loc)
                degree_from = degree_to

if __name__ == "__main__":
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640, 480)
    context = cairo.Context(surface)
    with context:
        context.set_source_rgb(1, 1, 1)
        context.paint()
    s = Sequence([Arc(20), Arc(40), Arc(60)])
    s.draw(context, 200, 200)
    surface.write_to_png('test.png')

