from http import HTTPStatus
from injector import Injector
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from twijournal.adapters.endpoints.rest_fastapi.fastapi_injector import EUserNotFoundOnToken, attach_injector
from twijournal.adapters.endpoints.rest_fastapi.controllers import user_controller
from twijournal.adapters.endpoints.rest_fastapi.controllers import post_controller
from twijournal.adapters.endpoints.rest_fastapi.controllers import feed_controller
from twijournal.adapters.endpoints.rest_fastapi.controllers import seed_controller


def build(injector: Injector):
    app = FastAPI(
        redoc_url="/",
        title="TwiJournal Microblog",
        description="TwiJournal is very similar to Twitter, but it has far fewer features.",
        version="0.1.0",
        terms_of_service="https://github.com/paulorodriguesxv/",
        contact={
            "name": "Paulo Rodrigues",
            "url": "https://github.com/paulorodriguesxv/",
        },
        license_info={
            "name": "MIT",
            "url": "https://en.wikipedia.org/wiki/MIT_License",
        },
    )

    app.include_router(user_controller.router,
                        prefix='/users',
                        tags=['users'])

    app.include_router(post_controller.router,
                        prefix='/posts',
                        tags=['posts'])

    app.include_router(feed_controller.router,
                        prefix='/feeds',
                        tags=['feeds'])

    app.include_router(seed_controller.router,
                        prefix='/seeds',
                        tags=['seeds'])

    attach_injector(app, injector)
    
    
    @app.exception_handler(EUserNotFoundOnToken)
    async def unicorn_exception_handler(request: Request, exc: EUserNotFoundOnToken):
        return JSONResponse(
            status_code=HTTPStatus.IM_A_TEAPOT,
            content={"message": f"Oops! JWT Token not found..."},
        )

    return app