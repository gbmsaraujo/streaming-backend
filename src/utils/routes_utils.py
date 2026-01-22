def normalize_range(raw_range: str, video_size: int):
    range_value = raw_range.replace("bytes=", "").strip()
    parts = range_value.split("-")

    match parts:
        case [start_str, ""]:
            start = int(start_str)
            end = video_size - 1

        case [start_str, end_str]:
            start = int(start_str)
            end = int(end_str)

        case ["", end_str]:
            start = max(0, video_size - int(end_str))
            end = video_size - 1

        case _:  # Formato inválido
            raise ValueError("Invalid Range format")

    return start, end

    # if range.startswith("bytes=-"):
    #     # bytes=-N (sufixo)
    #     suffix = int(parts[1]) if parts[1] else 0
    #     start = max(0, video_size - suffix)
    #     end = video_size - 1
    # elif len(parts[1]):
    #     start = int(parts[0]) if len(parts[0]) else 0
    #     end = int(parts[1])
    # else:
    #     # bytes=start- (do start até o fim)
    #     start = int(parts[0]) if len(parts[0]) else 0
    #     end = video_size - 1

    # # Validar SEMPRE (não só no sufixo)
    # if start < 0 or end >= video_size or start > end:
    #     raise HTTPException(status_code=416, detail="Range Not Satisfiable")


# 2-100
# 19238298219-
# -12082918
