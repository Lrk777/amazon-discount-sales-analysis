#!/usr/bin/env python3
"""Regenerate final_report.pdf from final_report.md (requires: pip install fpdf2 markdown)."""
from pathlib import Path

import markdown
from fpdf import FPDF

try:
    import matplotlib
    _mpl = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    FONT = str(_mpl / "DejaVuSans.ttf")
    FONT_BOLD = str(_mpl / "DejaVuSans-Bold.ttf")
    FONT_ITALIC = str(_mpl / "DejaVuSans-Oblique.ttf")
except Exception:
    FONT = FONT_BOLD = FONT_ITALIC = None


def main() -> None:
    if not FONT or not Path(FONT).is_file():
        raise SystemExit("Matplotlib DejaVu fonts not found; install matplotlib or set FONT paths.")

    root = Path(__file__).resolve().parent
    md_path = root / "final_report.md"
    out_path = root / "final_report.pdf"

    md_text = md_path.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=["extra", "sane_lists"])

    class PDF(FPDF):
        def footer(self) -> None:
            self.set_y(-12)
            self.set_font("DejaVu", "", 8)
            self.set_text_color(80, 80, 80)
            self.cell(0, 8, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("DejaVu", "", FONT)
    pdf.add_font("DejaVu", "B", FONT_BOLD)
    pdf.add_font("DejaVu", "I", FONT_ITALIC)
    pdf.add_page()
    pdf.set_font("DejaVu", "", 10)
    pdf.set_margins(18, 18, 18)
    pdf.write_html(html)
    pdf.output(str(out_path))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
