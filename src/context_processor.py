def format_hello3(value):
    return f"hlo: {value}"


def init(app):
    app.context_processor(lambda: {format_hello3.__name__: format_hello3})
