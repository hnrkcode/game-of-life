from gameoflife.settings import PATTERN_LIST


def get_patterns():
    patterns = {}
    with open(PATTERN_LIST) as patterns_file:
        name, layout = None, []
        for line in patterns_file:
            if line[0] == "#":
                continue
            if line[0].isalpha():
                name, layout = f"{len(patterns) + 1}. {line.strip()}", []
            elif line.strip():
                layout.append(list(map(int, line.strip())))
            if name and layout:
                patterns[name] = layout
    return patterns
