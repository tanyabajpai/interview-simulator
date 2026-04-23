def analyze_typing(timestamps):
    pauses = []

    for i in range(1, len(timestamps)):
        gap = timestamps[i] - timestamps[i-1]
        if gap > 5:
            pauses.append(gap)

    return {
        "pauses": len(pauses),
        "max_pause": max(pauses) if pauses else 0
    }