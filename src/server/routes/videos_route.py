from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse, StreamingResponse

from src.factories.video_stream_factory import video_reader
from src.utils.routes_utils import normalize_range

video_router = APIRouter(prefix="/api")

reader = video_reader()


@video_router.get("/videos", status_code=status.HTTP_200_OK)
async def list_videos() -> JSONResponse:
    video_names = reader.path.get_video_names()
    return JSONResponse(content=video_names, status_code=status.HTTP_200_OK)


@video_router.get("/stream/{video_name}", status_code=status.HTTP_200_OK)
async def stream_video(video_name: str, request: Request) -> StreamingResponse:
    if not reader.path.video_exists(video_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Video '{video_name}' not found"
        )

    try:
        raw_range = request.headers.get("Range", None)
        video_size = reader.path.get_video_size(video_name)

        if not raw_range:
            chunks = reader.read_chunks(video_name)
            return StreamingResponse(
                chunks,
                media_type="video/mp4",
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(video_size),
                },
            )

        start, end = normalize_range(raw_range, video_size)

        content_range = f"bytes {start}-{end}/{video_size}"
        chunks_range = reader.read_range(video_name, start, end)

        return StreamingResponse(
            chunks_range,
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(end - start + 1),
                "Content-Range": str(content_range),
            },
            status_code=206,
        )

    except Exception as err:
        print(f"Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server error: {err}",
        ) from err


@video_router.get("/metrics", status_code=status.HTTP_200_OK)
def metrics() -> JSONResponse:
    return JSONResponse(content=reader.metrics.get_metrics())
