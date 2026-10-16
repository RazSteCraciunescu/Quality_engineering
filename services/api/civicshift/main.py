from __future__ import annotations

import json
import logging
import time
from collections import Counter
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Header, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from .database import BusinessRuleError, ConflictError, NotFoundError, Store
from .quality_assistant import generate_scenarios
from .rate_limit import SlidingWindowRateLimiter
from .schemas import (
    EventResponse,
    RegistrationCreate,
    RegistrationResponse,
    ScenarioRequest,
    ScenarioResponse,
)
from .settings import Settings

LOGGER = logging.getLogger("civicshift")
logging.basicConfig(level=logging.INFO, format="%(message)s")


def problem(
    status: int,
    title: str,
    detail: str,
    request_id: str,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        headers=headers,
        content={
            "type": "about:blank",
            "title": title,
            "status": status,
            "detail": detail,
            "request_id": request_id,
        },
    )


def create_app(database_path: str | Path | None = None) -> FastAPI:
    settings = Settings.from_env(database_path)
    store = Store(settings.database_path)
    limiter = SlidingWindowRateLimiter(settings.rate_limit_per_minute)
    counters: Counter[str] = Counter()

    app = FastAPI(
        title="CivicShift API",
        version="1.0.0",
        description="Volunteer-event booking API used by the Quality Engineering Capstone.",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
    )
    app.state.settings = settings
    app.state.store = store
    app.state.counters = counters
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Idempotency-Key", "X-Request-ID"],
    )

    @app.middleware("http")
    async def quality_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))[:80]
        request.state.request_id = request_id
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        counters[f"http_{response.status_code}"] += 1
        counters["http_requests_total"] += 1
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = str(elapsed_ms)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if request.url.path == "/api/docs":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "connect-src 'self'; font-src 'self'; object-src 'none'; "
                "base-uri 'self'; frame-ancestors 'none'"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; connect-src 'self'; "
                "font-src 'self'; object-src 'none'; base-uri 'self'; "
                "frame-ancestors 'none'"
            )
        LOGGER.info(
            json.dumps(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "elapsed_ms": elapsed_ms,
                }
            )
        )
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        fields = [".".join(str(part) for part in error["loc"]) for error in exc.errors()]
        return problem(
            422,
            "Validation failed",
            f"Invalid fields: {', '.join(fields)}",
            request.state.request_id,
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return problem(404, "Not found", str(exc), request.state.request_id)

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
        return problem(409, "Conflict", str(exc), request.state.request_id)

    @app.exception_handler(BusinessRuleError)
    async def rule_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
        return problem(
            422,
            "Business rule rejected the request",
            str(exc),
            request.state.request_id,
        )

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        snapshot = store.quality_snapshot()
        return {
            "status": "ok",
            "service": "civicshift-api",
            "version": "1.0.0",
            "database": "ready" if snapshot["events"] > 0 else "empty",
        }

    @app.get("/api/events", response_model=list[EventResponse])
    def list_events() -> list[dict[str, Any]]:
        return store.list_events()

    @app.get("/api/events/{event_id}", response_model=EventResponse)
    def get_event(event_id: str) -> dict[str, Any]:
        return store.get_event(event_id)

    @app.post("/api/registrations", response_model=RegistrationResponse, status_code=201)
    def register(
        payload: RegistrationCreate,
        request: Request,
        response: Response,
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    ) -> dict[str, Any]:
        client_key = request.client.host if request.client else "unknown"
        if not limiter.allow(f"registration:{client_key}"):
            return problem(
                429,
                "Too many requests",
                "Registration rate limit exceeded",
                request.state.request_id,
                headers={"Retry-After": "60"},
            )
        if idempotency_key is not None and not 8 <= len(idempotency_key) <= 80:
            return problem(
                400,
                "Invalid idempotency key",
                "Idempotency-Key must contain 8 to 80 characters",
                request.state.request_id,
            )
        created, replayed = store.create_registration(
            event_id=payload.event_id,
            attendee_name=payload.attendee_name,
            attendee_email=payload.attendee_email,
            attendee_age=payload.attendee_age,
            consent=payload.consent,
            idempotency_key=idempotency_key,
        )
        created["replayed"] = replayed
        if replayed:
            response.status_code = 200
            response.headers["Idempotent-Replayed"] = "true"
        return created

    @app.get("/api/registrations/{registration_id}", response_model=RegistrationResponse)
    def get_registration(registration_id: str) -> dict[str, Any]:
        return store.get_registration(registration_id)

    @app.post(
        "/api/registrations/{registration_id}/cancel",
        response_model=RegistrationResponse,
    )
    def cancel_registration(registration_id: str) -> dict[str, Any]:
        return store.cancel_registration(registration_id)

    @app.post("/api/quality/generate-scenarios", response_model=ScenarioResponse)
    def quality_scenarios(payload: ScenarioRequest, request: Request) -> dict[str, Any] | JSONResponse:
        client_key = request.client.host if request.client else "unknown"
        if not limiter.allow(f"quality:{client_key}"):
            return problem(
                429,
                "Too many requests",
                "Quality-assistant rate limit exceeded",
                request.state.request_id,
                headers={"Retry-After": "60"},
            )
        counters["quality_scenarios_total"] += 1
        return generate_scenarios(settings, payload.requirement, payload.risk)

    @app.get("/api/quality/snapshot")
    def quality_snapshot() -> dict[str, Any]:
        return store.quality_snapshot()

    @app.get("/metrics", response_class=PlainTextResponse)
    def metrics() -> str:
        snapshot = store.quality_snapshot()
        lines = [
            "# HELP civicshift_http_requests_total Total HTTP requests processed.",
            "# TYPE civicshift_http_requests_total counter",
            f"civicshift_http_requests_total {counters['http_requests_total']}",
            "# HELP civicshift_registrations_total Total persisted registrations.",
            "# TYPE civicshift_registrations_total gauge",
            f"civicshift_registrations_total {snapshot['registrations']}",
            "# HELP civicshift_data_quality_violations Current critical data-quality violations.",
            "# TYPE civicshift_data_quality_violations gauge",
            "civicshift_data_quality_violations "
            f"{snapshot['active_duplicates'] + snapshot['overbooked_events']}",
        ]
        return "\n".join(lines) + "\n"

    repository_root = Path(__file__).resolve().parents[3]
    web_dist = repository_root / "apps" / "web" / "dist"
    if web_dist.exists():
        assets = web_dist / "assets"
        if assets.exists():
            app.mount("/assets", StaticFiles(directory=assets), name="assets")

        @app.get("/robots.txt", include_in_schema=False)
        def robots() -> FileResponse:
            return FileResponse(web_dist / "robots.txt")

        @app.get("/sitemap.xml", include_in_schema=False)
        def sitemap() -> FileResponse:
            return FileResponse(web_dist / "sitemap.xml")

        web_root = web_dist.resolve()

        @app.get("/{path:path}", include_in_schema=False)
        def spa(path: str) -> FileResponse:
            candidate = (web_root / path).resolve()
            if path and candidate.is_relative_to(web_root) and candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(web_root / "index.html")

    return app


app = create_app()
