from faststream.asgi import AsgiFastStream, AsgiResponse, get


@get
async def liveness_ping(scope):
    return AsgiResponse(b"Service is alive", status_code=200)



def create_app_with_health_check() -> AsgiFastStream:
    application = AsgiFastStream(
        asgi_routes=[("/health", liveness_ping)]
    )
    return application
