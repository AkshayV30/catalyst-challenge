from loguru import logger
import sys

logger.remove()

# ---------------- FORMATTER ----------------
def format_record(record):
    stage = record["extra"].get("stage", "general")

    return (
        f"{record['time']} | {record['level'].name} | {stage} | "
        f"{record['file'].name}:{record['line']}\n"
        f"{record['message']}\n"
    )


# ---------------- HELPERS ----------------
def stage_filter(stage):
    return lambda r: r["extra"].get("stage") == stage


def multi_stage_filter(stages):
    return lambda r: r["extra"].get("stage") in stages


# ---------------- CORE OUTPUTS ----------------
logger.add(sys.stdout, format=format_record, level="INFO")

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG"
)


# ---------------- GENERIC LOGS ----------------
logger.add("logs/errors.log", rotation="5 MB", level="ERROR")

logger.add("logs/warnings.log", rotation="5 MB", level="WARNING")

logger.add(
    "logs/performance.log",
    rotation="5 MB",
    filter=lambda r: "latency" in str(r["message"]).lower()
)

logger.add(
    "logs/unknown_stage.log",
    rotation="5 MB",
    filter=lambda r: "stage" not in r["extra"]
)


# ---------------- LLM RAW ----------------
logger.add(
    "logs/llm_raw.log",
    rotation="20 MB",
    level="DEBUG",
    filter=multi_stage_filter(["jd_parser", "matcher", "engagement"])
)


logger.add(
    "logs/json_parser.log",
    rotation="5 MB",
    filter=stage_filter("json_parser")
)

# ---------------- STAGE-SPECIFIC ----------------
STAGE_LOGS = {
    "jd_parser": ("logs/jd_parser.log", "5 MB"),
    "candidate": ("logs/candidates.log", "10 MB"),
    "matcher": ("logs/matcher.log", "5 MB"),
    "engagement": ("logs/engagement.log", "5 MB"),
    "pipeline": ("logs/pipeline.log", "5 MB"),
    "ranking": ("logs/ranking.log", "5 MB"),
    "shortlist": ("logs/shortlist.log", "5 MB"),
    "api": ("logs/api.log", "5 MB"),
}

for stage, (path, rotation) in STAGE_LOGS.items():
    logger.add(
        path,
        rotation=rotation,
        filter=stage_filter(stage)
    )