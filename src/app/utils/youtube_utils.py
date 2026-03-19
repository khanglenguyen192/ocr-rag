import re


def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from common URL formats.
    Supports:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://youtube.com/shorts/VIDEO_ID
    Returns None if URL is not a valid YouTube URL.
    """
    patterns = [
        r"(?:youtube\.com/watch\?(?:.*&)?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_transcript_to_markdown(transcript_entries: list, video_id: str) -> str:
    """Format a list of transcript entries into Markdown with timestamps."""
    lines = [
        f"# YouTube Transcript\n",
        f"**Video ID:** `{video_id}`\n",
        f"**Source:** https://www.youtube.com/watch?v={video_id}\n",
        "---\n",
    ]
    for entry in transcript_entries:
        start = entry.start
        minutes = int(start // 60)
        seconds = int(start % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        lines.append(f"**[{timestamp}]** {entry.text}")

    return "\n".join(lines)

