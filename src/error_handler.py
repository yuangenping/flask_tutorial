def handle_bad_request(e):
    return "bad request", 400


def not_found(e):
    return "404", 404


def init(app):
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(404, not_found)
