from typing import Any, Dict, Optional


class Location:
    def __init__(
        self,
        line: int,
        column: int,
        line_end: Optional[int] = None,
        column_end: Optional[int] = None,
        context: Optional[str] = None,
    ) -> None:
        self.line = line
        self.column = column
        self.line_end = line_end
        self.column_end = column_end
        self.context = context or ""

    def __repr__(self) -> str:
        return (
            "{}(line={!r}, column={!r}, "
            "line_end={!r}, column_end={!r}, context={!r})".format(
                self.__class__.__name__,
                self.line,
                self.column,
                self.line_end,
                self.column_end,
                self.context,
            )
        )

    def __str__(self) -> str:
        ret = "at line {} col {}".format(self.line, self.column)
        if self.line_end:
            ret += ", ending at line {}".format(self.line_end)
            if self.column_end:
                ret += " col {}".format(self.column_end)
        return ret

    def __eq__(self, other: Any) -> bool:
        return type(other) is type(self) and (
            self.line == other.line
            and self.column == other.column
            and self.line_end == other.line_end
            and self.column_end == other.column_end
            and self.context == other.context
        )

    def collect_value(self) -> Dict[str, int]:
        return {"line": self.line, "column": self.column}
