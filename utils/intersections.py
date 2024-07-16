def segments_do_not_intersect(segments):
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            if (
                segments[j][0] < segments[i][1]
                and segments[i][0] < segments[j][1]
            ):
                return False
    return True
