def say_hello2(value):
    print(f" say hello -> {value}")
    return "hhhhhh"


def init(app):
    app.add_template_filter(say_hello2, "say_hello2")
