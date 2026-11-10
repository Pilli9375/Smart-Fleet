"""
build_complete_guide_pdf.py
Converts FleetPulse_AI_Complete_Guide_and_Code_Walkthrough.md into a high-quality,
comprehensive academic PDF guide using ReportLab.
Includes Team Details (V Naga Adithya - 23BCE9062, M Karthik - 23BCE9659),
Full Non-Technical Analogies, Step-by-Step History, Line-by-Line Code Breakdown,
5-Algorithm Benchmark Analysis, and 20 Viva/Interview Defense Questions.
"""

import os
import re
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

MD_INPUT_PATH = os.path.join(os.path.dirname(__file__), "FleetPulse_AI_Complete_Guide_and_Code_Walkthrough.md")
PDF_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "FleetPulse_AI_Complete_Guide_and_Code_Walkthrough.pdf")


def clean_latex(text):
    """Converts LaTeX math notation to clean, legible academic unicode typography."""
    replacements = [
        (r"\\approx", "≈"),
        (r"\\times", "×"),
        (r"\\le", "≤"),
        (r"\\ge", "≥"),
        (r"\\pm", "±"),
        (r"\\cdot", "·"),
        (r"\\sum_{k=1}\^K", "∑(k=1..K)"),
        (r"\\sum_{i=1}\^N", "∑(i=1..N)"),
        (r"\\sum", "∑"),
        (r"\\mu", "μ"),
        (r"\\tau", "τ"),
        (r"\\alpha", "α"),
        (r"\\beta", "β"),
        (r"\\gamma", "γ"),
        (r"\\sigma", "σ"),
        (r"\\pi", "π"),
        (r"\\Omega", "Ω"),
        (r"\\mathcal{F}", "F"),
        (r"\\mathcal{P}", "P"),
        (r"\\prec", "≺"),
        (r"\\land", "∧"),
        (r"\\lor", "∨"),
        (r"\\min", "min"),
        (r"\\max", "max"),
        (r"\\exp", "exp"),
        (r"\\dfrac", ""),
        (r"\\frac", ""),
        (r"\\sqrt", "√"),
        (r"\\Big\[", "["),
        (r"\\Big\]", "]"),
        (r"\\big\(", "("),
        (r"\\big\)", ")"),
        (r"\\left\(", "("),
        (r"\\right\)", ")"),
        (r"\\quad", "  "),
        (r"\\text\{([^}]+)\}", r"\1"),
        (r"\{([^}]+)\}", r"\1"),
        (r"\$", ""),
        (r"\\", "")
    ]
    res = text
    for pat, rep in replacements:
        res = re.sub(pat, rep, res)
    return res.strip()


def parse_markdown(md_text):
    lines = md_text.splitlines()
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped in ["---", "***", "___"]:
            blocks.append({"type": "hr"})
            i += 1
            continue

        # Code block
        if stripped.startswith("```"):
            code_lines = []
            lang = stripped.lstrip("`").strip()
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            blocks.append({
                "type": "code",
                "lang": lang,
                "content": "\n".join(code_lines)
            })
            continue

        # Table block
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = []
            for tl in table_lines:
                if re.match(r"^\|(\s*:?-+:?\s*\|)+$", tl):
                    continue
                cells = [c.strip() for c in tl.split("|")[1:-1]]
                rows.append(cells)
            if rows:
                blocks.append({"type": "table", "rows": rows})
            continue

        # Headers
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped.lstrip("#").strip()
            blocks.append({"type": "header", "level": level, "text": text})
            i += 1
            continue

        # Bullet List
        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            blocks.append({"type": "bullet_list", "items": items})
            continue

        # Numbered List
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "numbered_list", "items": items})
            continue

        # Blockquote
        if stripped.startswith(">"):
            q_lines = []
            while i < n and lines[i].strip().startswith(">"):
                q_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append({"type": "blockquote", "text": " ".join(q_lines)})
            continue

        # Standard Paragraph or Equation block
        p_lines = []
        while i < n:
            curr = lines[i].strip()
            if not curr:
                break
            if curr.startswith(("#", "```", ">", "---", "***")):
                break
            if curr.startswith(("- ", "* ")) or re.match(r"^\d+\.\s+", curr):
                break
            if curr.startswith("|") and curr.endswith("|"):
                break
            p_lines.append(curr)
            i += 1

        if p_lines:
            full_p = " ".join(p_lines)
            if full_p.startswith("$$") and full_p.endswith("$$"):
                blocks.append({"type": "equation", "text": clean_latex(full_p[2:-2])})
            else:
                blocks.append({"type": "paragraph", "text": full_p})
        else:
            i += 1

    return blocks


class MasterGuideNumberedCanvas(canvas.Canvas):
    """Running headers and page numbers on every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0284c7"))

            # Running Header
            self.drawString(54, 752, "FleetPulse AI — Plain-English Educational Guide & Code Walkthrough")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawRightString(558, 752, "Soft Computing Research")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 746, 558, 746)

            # Running Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 36, page_text)
            self.drawString(54, 36, "V Naga Adithya (23BCE9062) & M Karthik (23BCE9659) — Dept of CSE")
            self.line(54, 46, 558, 46)
            self.restoreState()


def build_pdf(blocks, output_path):
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="GuideTitle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        name="GuideSubtitle",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=18
    )
    h1_style = ParagraphStyle(
        name="GuideH1",
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=17,
        textColor=colors.HexColor("#0c4a6e"),
        spaceBefore=14,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        name="GuideH2",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        name="GuideH3",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        name="GuideBody",
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4.5
    )
    bullet_style = ParagraphStyle(
        name="GuideBullet",
        fontName="Helvetica",
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )
    quote_style = ParagraphStyle(
        name="GuideQuote",
        fontName="Helvetica-Oblique",
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor("#0c4a6e"),
        leftIndent=14,
        spaceBefore=4,
        spaceAfter=6
    )
    eq_style = ParagraphStyle(
        name="GuideEq",
        fontName="Courier-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor("#0e7490"),
        spaceBefore=4,
        spaceAfter=6
    )
    table_head_style = ParagraphStyle(
        name="GuideTH",
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=9.5,
        alignment=1,
        textColor=colors.white
    )
    table_cell_style = ParagraphStyle(
        name="GuideTC",
        fontName="Helvetica",
        fontSize=7.4,
        leading=9.5,
        textColor=colors.HexColor("#1e293b")
    )
    code_style = ParagraphStyle(
        name="GuideCode",
        fontName="Courier",
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 35))
    story.append(Paragraph("FleetPulse AI: Complete Plain-English Master Guide & Code Walkthrough", title_style))
    story.append(Paragraph(
        "An Exhaustive Step-by-Step Educational Handbook to Multi-Objective Vehicle Routing, Fuzzy Logic, and Evolutionary Computing",
        subtitle_style
    ))
    story.append(HRFlowable(width="90%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=24))

    meta_table_data = [
        [
            Paragraph("<b>Project Domain:</b>", table_cell_style),
            Paragraph("Soft Computing & Artificial Intelligence (Fuzzy Logic + Evolutionary Algorithms)", table_cell_style)
        ],
        [
            Paragraph("<b>Document Purpose:</b>", table_cell_style),
            Paragraph("Complete Educational Textbook, Plain-English Concept Explanations & Line-by-Line Code Handbook", table_cell_style)
        ],
        [
            Paragraph("<b>Department:</b>", table_cell_style),
            Paragraph("Department of Computer Science and Engineering", table_cell_style)
        ],
        [
            Paragraph("<b>Research Authors:</b>", table_cell_style),
            Paragraph("<b>V Naga Adithya</b> (Registration No: <code>23BCE9062</code>)<br/><b>M Karthik</b> (Registration No: <code>23BCE9659</code>)", table_cell_style)
        ],
        [
            Paragraph("<b>Core Capabilities:</b>", table_cell_style),
            Paragraph("Hybrid Fuzzy-NSGA-II, MOPSO, MO-ACO, Standard GA, Greedy Nearest-Neighbor, 60FPS Vector Radar HUD", table_cell_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[1.8 * inch, 4.8 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<b>Handbook Overview:</b> <i>This document is designed for anyone—from non-technical managers to senior examiners—to understand every single concept, line of code, and mathematical formula behind FleetPulse AI. It covers real-world motivation, combinatorial NP-hard complexity, physics-based load-dependent energy dissipation, multi-kernel fuzzy membership equations, memetic genetic operators, and an exhaustive 20-question viva defense guide.</i>",
        body_style
    ))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # DOCUMENT BODY
    # -------------------------------------------------------------
    skip_first_title = True
    for block in blocks:
        btype = block["type"]

        if btype == "header":
            level = block["level"]
            text = block["text"]
            if skip_first_title and level == 1 and "FleetPulse AI" in text:
                skip_first_title = False
                continue

            clean_head = re.sub(r"[*`$]", "", text)
            if level == 1:
                story.append(Spacer(1, 4))
                story.append(Paragraph(clean_head, h1_style))
                story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#0284c7"), spaceAfter=4))
            elif level == 2:
                story.append(Paragraph(clean_head, h2_style))
            else:
                story.append(Paragraph(clean_head, h3_style))

        elif btype == "paragraph":
            txt = block["text"]
            # Convert markdown formatting
            txt = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", txt)
            txt = re.sub(r"\*(.*?)\*", r"<i>\1</i>", txt)
            txt = re.sub(r"`(.*?)`", r"<font face='Courier' color='#0c4a6e'>\1</font>", txt)
            txt = clean_latex(txt)
            story.append(Paragraph(txt, body_style))

        elif btype == "equation":
            eq = clean_latex(block["text"])
            story.append(Paragraph(f"<b>[Mathematical Equation]</b> {eq}", eq_style))

        elif btype == "bullet_list":
            for it in block["items"]:
                it_c = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", it)
                it_c = re.sub(r"\*(.*?)\*", r"<i>\1</i>", it_c)
                it_c = re.sub(r"`(.*?)`", r"<font face='Courier' color='#0c4a6e'>\1</font>", it_c)
                it_c = clean_latex(it_c)
                story.append(Paragraph(f"&bull; {it_c}", bullet_style))

        elif btype == "numbered_list":
            for idx, it in enumerate(block["items"], start=1):
                it_c = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", it)
                it_c = re.sub(r"\*(.*?)\*", r"<i>\1</i>", it_c)
                it_c = re.sub(r"`(.*?)`", r"<font face='Courier' color='#0c4a6e'>\1</font>", it_c)
                it_c = clean_latex(it_c)
                story.append(Paragraph(f"{idx}. {it_c}", bullet_style))

        elif btype == "blockquote":
            txt = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", block["text"])
            txt = re.sub(r"\*(.*?)\*", r"<i>\1</i>", txt)
            txt = clean_latex(txt)
            story.append(Paragraph(f"<b>Answer:</b> {txt}", quote_style))

        elif btype == "table":
            rows_data = block["rows"]
            if not rows_data:
                continue
            table_flow_data = []
            for r_idx, r in enumerate(rows_data):
                is_h = (r_idx == 0)
                row_cells = []
                for c in r:
                    c_clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", c)
                    c_clean = re.sub(r"`(.*?)`", r"\1", c_clean)
                    c_clean = clean_latex(c_clean)
                    if is_h:
                        row_cells.append(Paragraph(f"<b>{c_clean}</b>", table_head_style))
                    else:
                        row_cells.append(Paragraph(c_clean, table_cell_style))
                table_flow_data.append(row_cells)

            col_count = len(rows_data[0])
            avail_width = 504.0
            col_width = avail_width / max(1, col_count)
            t = Table(table_flow_data, colWidths=[col_width] * col_count)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0, 0), (-1, -1), 3.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
            ]))
            story.append(Spacer(1, 3))
            story.append(t)
            story.append(Spacer(1, 5))

        elif btype == "code":
            code_text = block["content"]
            # Render code in a styled box
            code_lines = code_text.splitlines()
            # Wrap long code lines
            wrapped_lines = []
            for cl in code_lines:
                if len(cl) > 95:
                    wrapped_lines.append(cl[:95])
                    wrapped_lines.append("    " + cl[95:])
                else:
                    wrapped_lines.append(cl)
            safe_code = "\n".join(wrapped_lines)

            code_p = Preformatted(safe_code, code_style)
            code_table = Table([[code_p]], colWidths=[504.0])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(Spacer(1, 2))
            story.append(code_table)
            story.append(Spacer(1, 4))

        elif btype == "hr":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=5, spaceAfter=6))

    pdf.build(story, canvasmaker=MasterGuideNumberedCanvas)
    print(f"Generated Comprehensive Guide PDF: {output_path} ({os.path.getsize(output_path):,} bytes)")


def main():
    print("=" * 76)
    print(" FLEETPULSE AI — COMPREHENSIVE EDUCATIONAL PDF GENERATOR")
    print("=" * 76)

    if not os.path.exists(MD_INPUT_PATH):
        print(f"Error: {MD_INPUT_PATH} not found!")
        sys.exit(1)

    with open(MD_INPUT_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    print(f"Loaded Markdown handbook: {len(md_content):,} characters from {MD_INPUT_PATH}")
    blocks = parse_markdown(md_content)
    print(f"Parsed {len(blocks)} document blocks.")

    print("\n--- Compiling PDF Document via ReportLab ---")
    build_pdf(blocks, PDF_OUTPUT_PATH)

    if os.path.exists(PDF_OUTPUT_PATH) and os.path.getsize(PDF_OUTPUT_PATH) > 1000:
        print(f"\n[SUCCESS] PDF generated successfully: {PDF_OUTPUT_PATH}")
        print(f"File size: {os.path.getsize(PDF_OUTPUT_PATH):,} bytes")
    else:
        print(f"\n[ERROR] PDF generation failed or file is empty!")


if __name__ == "__main__":
    main()
