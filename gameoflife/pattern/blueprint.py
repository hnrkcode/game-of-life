import os.path
import string

from gameoflife import settings


def get_patterns():
    """Read patterns from text file."""

    patterns = {}
    patterns_list = os.path.join(settings.TEXT_DIR, "patterns.txt")

    with open(patterns_list, "r") as patterns_file:

        name = None
        layout = []

        for line in patterns_file:
            # Ignore lines that start with '#'.
            if line[0] == "#":
                continue

            # Line is a pattern name if it contains letters.
            is_name = "".join(
                [i for i in line if not i.isdigit() and i.isalpha()]
            ).isalpha()

            # Use name as dictionary key.
            if is_name:
                name = line.strip("\n")
                patterns[name] = []
                continue

            # All other lines that isn't empty are part of the pattern.
            if line[0] != "\n":
                result = list(map(int, list(line.strip("\n"))))
                layout.append(result)
                continue

            # Add pattern to the key with it's name and reset pattern list.
            patterns[name] = layout
            layout = []

        # Add the last pattern to the dictionary.
        patterns[name] = layout

    return patterns
