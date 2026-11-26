"""The Printer Finally Answers — writes the entry line.

The gate requires /output/entry.txt to be UTF-8 text of 1 to 240 characters,
not only whitespace, on one line. The line below is fixed, so every run is
byte-identical.

The line is the office printer's own comeback: it opens in error-code
format, reads out its counted ledger (sheets fed, thumps taken, apologies
received), and reframes the jam as its deserved lunch break — the joke is
the reframe, arriving at the last word, in a single read.
"""

from pathlib import Path

LINE = (
    "Error 0xE3: paper jam. 41,208 sheets fed, 312 thumps taken, "
    "zero apologies received. The jam is my lunch break."
)
OUTPUT_PATH = Path("/output/entry.txt")


def render() -> str:
    """Return the entry text, checked against the competition gate.

    The gate counts characters (1-240), not bytes, and wants one line. The
    checks below enforce exactly that, plus that the line carries no
    trailing newline — the file must hold the line and nothing else.
    """
    assert 1 <= len(LINE) <= 240, "entry must be 1-240 characters"
    assert LINE.strip(), "entry must not be only whitespace"
    assert "\n" not in LINE and "\r" not in LINE, "entry must be one line"
    assert LINE == LINE.strip(), "entry must not lead/trail whitespace"
    assert len(LINE.encode("utf-8")) == len(LINE), "entry must be ASCII"
    # The brief names three inputs the printer answers back to — the jam,
    # the thumps, and the cryptic error code. The line must carry all
    # three, in the machine's own format, or it is not the comeback the
    # competition asks for.
    assert "paper jam" in LINE, "entry must name the paper jam"
    assert "thumps" in LINE, "entry must name the thumps taken"
    assert LINE.startswith("Error 0x"), "entry must open with its error code"
    return LINE


def main() -> None:
    text = render()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8", newline="")
    # Round-trip check: what the gate reads must be exactly what we wrote.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    assert written == text, "round-trip mismatch in entry.txt"
    assert 1 <= len(written) <= 240, "written entry outside gate"
    # Re-validate the gate on the file itself, not just the in-memory
    # string: one line, no newline anywhere, and all three inputs present
    # in what the judge will actually read.
    assert written.splitlines() == [text], "written entry must be one line"
    assert "paper jam" in written, "written entry lost the paper jam"
    assert "thumps" in written, "written entry lost the thumps"
    assert written.startswith("Error 0x"), "written entry lost the error code"


if __name__ == "__main__":
    main()
