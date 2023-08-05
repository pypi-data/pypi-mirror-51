API_URL = "https://statsapi.web.nhl.com/{endpoint}"

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    ),
    "Dnt": ("1"),
    "Accept-Language": ("en"),
    "origin": ("https://statsapi.web.nhl.com"),
    "referer": ("https://www.nhl.com/"),
}

SCHEDULE_PARAMS = "schedule.teams,schedule.linescore,schedule.decisions,schedule.scoringplays"
