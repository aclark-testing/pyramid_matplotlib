# Pyramid/matplotlib demo
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
try:  # Python 3
    from urllib.parse import parse_qs
except:  # Python 2
    from urlparse import parse_qs


def plot(request):
    """
    http://stackoverflow.com/a/5515994/185820
    """

    import cStringIO
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    x, y = 4, 4
    qs = parse_qs(request.query_string)
    if 'x' in qs:
        x = int(qs['x'][0])
    if 'y' in qs:
        y = int(qs['y'][0])
    fig = Figure(figsize=[x, y])
    ax = fig.add_axes([.1, .1, .8, .8])
    ax.scatter([1, 2], [3, 4])
    canvas = FigureCanvasAgg(fig)

    # write image data to a string buffer and get the PNG image bytes
    buf = cStringIO.StringIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    # write image bytes back to the browser
    response = Response(data)
    response.content_type = 'image/png'
    response.content_length = len(data)
    return response


if __name__ == '__main__':
    config = Configurator()
    config.add_route('plot', '/')
    config.add_view(plot, route_name='plot')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    print(
        "Pyramid/matplotlib demo running on: http://0.0.0.0:8080. "
        "Try changing the fig size with: http://0.0.0.0:8080/?x=8&y=8."
    )
    server.serve_forever()
