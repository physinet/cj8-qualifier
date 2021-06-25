import math
from itertools import zip_longest
from typing import Any, List, Optional

BORDER = {
    "top": ["┌", "┬", "┐"],
    "header": ["├", "┼", "┤"],
    "bottom": ["└", "┴", "┘"],
}
VERTICAL = "│"
HORIZONTAL = "─"


def make_horizontal_rule(column_widths: List[int], which: str):
    """Makes a horizontal rule with the set of left, column, and right borders labeled by `which`"""
    borders = BORDER[which]
    return (
        borders[0]
        + borders[1].join(HORIZONTAL * column_width for column_width in column_widths)
        + borders[2]
    )


def make_table(
    rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False
) -> str:
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """
    assert len(set(n_cols := len(row) for row in rows)) == 1

    if labels := labels or []:
        assert n_cols == len(labels)

    column_widths = [0] * n_cols
    for i, cols in enumerate(zip_longest(labels, *rows)):
        # each column will be as wide as the longest string, plus two spaces on either side
        column_widths[i] = max(len(str(col)) for col in cols) + 2


    # final table: top rule, header row (if labels given), header rule (if labels given), rows, bottom rule
    return "\n".join(
        [make_horizontal_rule(column_widths, "top")]
        + ([process_row(labels, column_widths, centered)] if labels else [])
        + ([make_horizontal_rule(column_widths, "header")] if labels else [])
        + [process_row(row, column_widths, centered) for row in rows]
        + [make_horizontal_rule(column_widths, "bottom")]
    )


def pad_column(column_object: Any, column_width: int, centered: bool) -> str:
    """Pads the string representation of column_object up to `column_width` using the given formatting
    rule (centered or not centered). Extra spaces for unevenly centered columns pad to the right.
    """
    column_text = f" {column_object} "  # padded by at least one space on either side
    pad = column_width - len(column_text)
    if not centered:  # left justified, pad to the right
        return column_text + " " * pad
    if centered:  # centered, pad evenly on both sides, extra spaces on the right
        left_pad, right_pad = pad // 2, math.ceil(pad / 2)
        return " " * left_pad + column_text + " " * right_pad


def process_row(row: List[Any], column_widths: List[int], centered: bool) -> List[str]:
    """Returns the string representation of each row. Each column is separated by vertical bars"""
    return (
        VERTICAL
        + VERTICAL.join(
            pad_column(col, column_width, centered)
            for col, column_width in zip(row, column_widths)
        )
        + VERTICAL
    )


if __name__ == "__main__":
    table = make_table(
        rows=[["Lemon"], ["Sebastiaan"], ["KutieKatj9"], ["Jake"], ["Not Joe"]]
    )
    print(table)

    table = make_table(
        rows=[
            ["Lemon", 18_3285, "Owner"],
            ["Sebastiaan", 18_3285.1, "Owner"],
            ["KutieKatj", 15_000, "Admin"],
            ["Jake", "MoreThanU", "Helper"],
            ["Joe", -12, "Idk Tbh"],
        ],
        labels=["User", "Messages", "Role"],
    )
    print(table)

    table = make_table(
        rows=[
            ["Ducky Yellow", 3],
            ["Ducky Dave", 12],
            ["Ducky Tube", 7],
            ["Ducky Lemon", 1],
        ],
        labels=["Name", "Duckiness"],
        centered=True,
    )
    print(table)
