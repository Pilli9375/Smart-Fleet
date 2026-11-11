"""
export_reports.py
Autonomous Document Export Engine for FleetPulse AI Project Report
Generates:
  1. FleetPulse_AI_Project_Report.docx (Formatted Microsoft Word Document via python-docx)
  2. FleetPulse_AI_Project_Report.pdf (Academic PDF Document via ReportLab)
Includes Team Members (V Naga Adithya - 23BCE9062, M Karthik - 23BCE9659),
Full 10 Chapters, Mathematical Models, Mamdani Inference Matrix, and Benchmark Tables.
"""

import os
import re
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


REPORT_MD_PATH = os.path.join(os.path.dirname(__file__), "Academic_Project_Report.md")
DOCX_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "FleetPulse_AI_Project_Report.docx")
PDF_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "FleetPulse_AI_Project_Report.pdf")


# =====================================================================
# 1. MARKDOWN PARSER UTILITIES
# =====================================================================
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


def parse_markdown_blocks(md_content):
    """
    Parses Markdown lines into structured blocks:
    headers, paragraphs, bullet lists, numbered lists, blockquotes, tables, and code blocks.
    """
    lines = md_content.splitlines()
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Empty line
        if not stripped:
            i += 1
            continue

        # Horizontal Rule
        if stripped in ["---", "***", "___"]:
            blocks.append({"type": "hr"})
            i += 1
            continue

        # Code block (skip Mermaid diagram blocks in table of content or prose, or render as formatted code)
        if stripped.startswith("```"):
            code_lines = []
            is_mermaid = "mermaid" in stripped
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            blocks.append({
                "type": "code",
                "is_mermaid": is_mermaid,
                "content": "\n".join(code_lines)
            })
            continue

        # Table block
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            # Parse table rows
            rows = []
            for tl in table_lines:
                # Check if separator row like | :--- | :---: |
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
                bullet_text = lines[i].strip()[2:].strip()
                items.append(bullet_text)
                i += 1
            blocks.append({"type": "bullet_list", "items": items})
            continue

        # Numbered List
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                num_text = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(num_text)
                i += 1
            blocks.append({"type": "numbered_list", "items": items})
            continue

        # Blockquote
        if stripped.startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append({"type": "blockquote", "text": " ".join(quote_lines)})
            continue

        # Standard Paragraph or Equation block
        para_lines = []
        while i < n:
            curr_str = lines[i].strip()
            if not curr_str:
                break
            if curr_str.startswith(("#", "```", ">", "---", "***")):
                break
            if curr_str.startswith(("- ", "* ")) or re.match(r"^\d+\.\s+", curr_str):
                break
            if curr_str.startswith("|") and curr_str.endswith("|"):
                break
            para_lines.append(curr_str)
            i += 1

        if para_lines:
            full_p = " ".join(para_lines)
            if full_p.startswith("$$") and full_p.endswith("$$"):
                blocks.append({"type": "equation", "text": clean_latex(full_p[2:-2])})
            else:
                blocks.append({"type": "paragraph", "text": full_p})
        else:
            # Safety: ensure forward progress
            i += 1

    return blocks


# =====================================================================
# 2. WORD DOCUMENT GENERATION (.DOCX)
# =====================================================================
def set_cell_background(cell, hex_color):
    """Sets background shading of a Word table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding of a Word table cell in dxa units."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def add_formatted_text(paragraph, text, base_font="Calibri", base_size=11, color_rgb=(24, 30, 42)):
    """Parses markdown bold, italic, code spans, and LaTeX in a paragraph."""
    # Split tokens by markdown bold/italic/code/latex
    tokens = re.split(r"(\*\*.*?\*\*|\*.*?\*|`.*?`|\$\$.*?\$\$|\$.*?\$)", text)
    for token in tokens:
        if not token:
            continue
        run = paragraph.add_run()
        run.font.name = base_font
        run.font.size = Pt(base_size)
        run.font.color.rgb = RGBColor(*color_rgb)

        if token.startswith("**") and token.endswith("**") and len(token) >= 4:
            run.text = clean_latex(token[2:-2])
            run.bold = True
        elif token.startswith("*") and token.endswith("*") and len(token) >= 2:
            run.text = clean_latex(token[1:-1])
            run.italic = True
        elif token.startswith("`") and token.endswith("`") and len(token) >= 2:
            run.text = token[1:-1]
            run.font.name = "Consolas"
            run.font.size = Pt(base_size - 0.5)
            run.font.color.rgb = RGBColor(12, 74, 110)
        elif (token.startswith("$$") and token.endswith("$$")) or (token.startswith("$") and token.endswith("$")):
            clean_math = clean_latex(token)
            run.text = clean_math
            run.italic = True
            run.font.name = "Cambria Math"
            run.font.color.rgb = RGBColor(14, 116, 144)
        else:
            run.text = clean_latex(token)


def generate_docx(blocks, output_path):
    doc = Document()

    # Page Margins: Standard 1 inch (72 pt)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # ACADEMIC TITLE PAGE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    run_title = title_p.add_run("Hybrid Fuzzy-NSGA-II Intelligent Fleet Dispatcher")
    run_title.bold = True
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(28)
    run_sub = sub_p.add_run("Multi-Objective Vehicle Routing with Fuzzy Time Windows, Mamdani Traffic Inference & 5-Algorithm Benchmarking")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(56, 189, 248)
    run_sub.bold = True

    # Decorative Divider
    div_p = doc.add_paragraph()
    div_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    div_p.paragraph_format.space_after = Pt(36)
    r_div = div_p.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    r_div.font.color.rgb = RGBColor(14, 116, 144)
    r_div.bold = True

    # Metadata Card (Table)
    meta_table = doc.add_table(rows=7, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    meta_items = [
        ("Project Domain:", "Soft Computing & Artificial Intelligence (Fuzzy Logic + Evolutionary Computation)"),
        ("Course & Project Type:", "Soft Computing (Undergraduate Mini-Project / Capstone Report)"),
        ("Faculty Guide / Evaluator:", "Dr. Seetha Hari, Associate Professor, SCOPE, VIT-AP University"),
        ("Institution:", "School of Computer Science & Engineering (SCOPE), VIT-AP University, Amaravati"),
        ("Team Member 1:", "V Naga Adithya  |  Registration No: 23BCE9062"),
        ("Team Member 2:", "M Karthik       |  Registration No: 23BCE9659"),
        ("Submission Date:", "November 2026  (Academic Year: 2026–2027)")
    ]

    for idx, (label, val) in enumerate(meta_items):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.3)

        p_lbl = cell_lbl.paragraphs[0]
        p_lbl.paragraph_format.space_before = Pt(4)
        p_lbl.paragraph_format.space_after = Pt(4)
        r_l = p_lbl.add_run(label)
        r_l.bold = True
        r_l.font.size = Pt(10)
        r_l.font.color.rgb = RGBColor(30, 41, 59)

        p_val = cell_val.paragraphs[0]
        p_val.paragraph_format.space_before = Pt(4)
        p_val.paragraph_format.space_after = Pt(4)
        r_v = p_val.add_run(val)
        if "V Naga Adithya" in val or "M Karthik" in val:
            r_v.bold = True
            r_v.font.color.rgb = RGBColor(14, 116, 144)
            r_v.font.size = Pt(10.5)
        else:
            r_v.font.size = Pt(10)
            r_v.font.color.rgb = RGBColor(51, 65, 85)

        set_cell_margins(cell_lbl, 80, 80, 120, 120)
        set_cell_margins(cell_val, 80, 80, 120, 120)
        bg = "F1F5F9" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(cell_lbl, bg)
        set_cell_background(cell_val, bg)

    doc.add_page_break()

    # -------------------------------------------------------------
    # DOCUMENT BODY (PARSED MARKDOWN BLOCKS)
    # -------------------------------------------------------------
    skip_preamble = True
    for block in blocks:
        btype = block["type"]

        if skip_preamble:
            if btype == "header" and block["text"] == "Abstract":
                skip_preamble = False
            else:
                continue

        if btype == "header":
            level = block["level"]
            text = block["text"]

            if level == 2 and (text in ["Table of Contents"] or re.match(r"^\d+\.", text)):
                doc.add_page_break()

            hp = doc.add_paragraph()
            hp.paragraph_format.keep_with_next = True
            if level == 1:
                hp.paragraph_format.space_before = Pt(20)
                hp.paragraph_format.space_after = Pt(8)
                run = hp.add_run(text)
                run.font.name = "Arial"
                run.font.size = Pt(16)
                run.bold = True
                run.font.color.rgb = RGBColor(12, 74, 110)
            elif level == 2:
                hp.paragraph_format.space_before = Pt(16)
                hp.paragraph_format.space_after = Pt(6)
                run = hp.add_run(text)
                run.font.name = "Arial"
                run.font.size = Pt(13.5)
                run.bold = True
                run.font.color.rgb = RGBColor(15, 23, 42)
            elif level == 3:
                hp.paragraph_format.space_before = Pt(12)
                hp.paragraph_format.space_after = Pt(4)
                run = hp.add_run(text)
                run.font.name = "Calibri"
                run.font.size = Pt(12)
                run.bold = True
                run.font.color.rgb = RGBColor(30, 41, 59)
            else:
                hp.paragraph_format.space_before = Pt(8)
                hp.paragraph_format.space_after = Pt(3)
                run = hp.add_run(text)
                run.font.name = "Calibri"
                run.font.size = Pt(11)
                run.bold = True
                run.font.color.rgb = RGBColor(71, 85, 105)

        elif btype == "paragraph":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_text(p, block["text"])

        elif btype == "equation":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(block["text"])
            run.bold = True
            run.italic = True
            run.font.name = "Cambria Math"
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(14, 116, 144)

        elif btype == "bullet_list":
            for it in block["items"]:
                bp = doc.add_paragraph(style='List Bullet')
                bp.paragraph_format.space_before = Pt(1)
                bp.paragraph_format.space_after = Pt(3)
                bp.paragraph_format.line_spacing = 1.12
                add_formatted_text(bp, it)

        elif btype == "numbered_list":
            for it in block["items"]:
                np = doc.add_paragraph(style='List Number')
                np.paragraph_format.space_before = Pt(1)
                np.paragraph_format.space_after = Pt(3)
                np.paragraph_format.line_spacing = 1.12
                add_formatted_text(np, it)

        elif btype == "blockquote":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            add_formatted_text(p, block["text"], color_rgb=(71, 85, 105))

        elif btype == "table":
            rows_data = block["rows"]
            if not rows_data:
                continue
            num_rows = len(rows_data)
            num_cols = len(rows_data[0])
            tbl = doc.add_table(rows=num_rows, cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl.autofit = True

            for r_idx, r_data in enumerate(rows_data):
                is_header = (r_idx == 0)
                row_elem = tbl.rows[r_idx]
                for c_idx, cell_text in enumerate(r_data):
                    if c_idx >= len(row_elem.cells):
                        continue
                    cell = row_elem.cells[c_idx]
                    cp = cell.paragraphs[0]
                    cp.paragraph_format.space_before = Pt(3)
                    cp.paragraph_format.space_after = Pt(3)
                    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_header or any(ch.isdigit() for ch in cell_text) else WD_ALIGN_PARAGRAPH.LEFT

                    if is_header:
                        run = cp.add_run(clean_latex(cell_text))
                        run.bold = True
                        run.font.name = "Arial"
                        run.font.size = Pt(9.5)
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        set_cell_background(cell, "0F172A")
                    else:
                        add_formatted_text(cp, cell_text, base_size=9)
                        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                        if "Hybrid Fuzzy-NSGA-II" in cell_text or "Rank #1" in cell_text:
                            bg = "E0F2FE"
                        set_cell_background(cell, bg)

                    set_cell_margins(cell, 70, 70, 100, 100)

            # Space after table
            post_sp = doc.add_paragraph()
            post_sp.paragraph_format.space_after = Pt(8)

        elif btype == "code":
            if block["is_mermaid"]:
                # Render diagram as a clean text card
                cp = doc.add_paragraph()
                cp.paragraph_format.space_before = Pt(4)
                cp.paragraph_format.space_after = Pt(6)
                cp.paragraph_format.left_indent = Inches(0.2)
                run_tag = cp.add_run("[System Architecture Diagram Flow]\n")
                run_tag.bold = True
                run_tag.font.size = Pt(9)
                run_tag.font.color.rgb = RGBColor(14, 116, 144)

                run_diag = cp.add_run(block["content"])
                run_diag.font.name = "Consolas"
                run_diag.font.size = Pt(8.5)
                run_diag.font.color.rgb = RGBColor(71, 85, 105)

        elif btype == "hr":
            doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path} ({os.path.getsize(output_path):,} bytes)")


# =====================================================================
# 3. ACADEMIC PDF DOCUMENT GENERATION (REPORTLAB)
# =====================================================================
class NumberedCanvas(canvas.Canvas):
    """Adds running headers and 'Page X of Y' footers to ReportLab PDFs."""
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
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))

            # Running Header
            self.drawString(54, 750, "FleetPulse AI — Hybrid Fuzzy-NSGA-II Autonomous Fleet Dispatcher Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

            # Running Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 38, page_text)
            self.drawString(54, 38, "V Naga Adithya (23BCE9062) & M Karthik (23BCE9659) | Faculty Guide: Dr. Seetha Hari")
            self.line(54, 48, 558, 48)
            self.restoreState()


def generate_pdf(blocks, output_path):
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Academic Styles
    styles.add(ParagraphStyle(
        name="AcademicTitle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name="AcademicSubtitle",
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name="SectionH1",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0c4a6e"),
        spaceBefore=16,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="SectionH2",
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="SectionH3",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="AcademicBody",
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.2,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="AcademicBullet",
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="AcademicEquation",
        fontName="Courier-Bold",
        fontSize=9,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#0e7490"),
        spaceBefore=5,
        spaceAfter=7
    ))
    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#1e293b")
    ))
    styles.add(ParagraphStyle(
        name="TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    ))

    story = []

    # -------------------------------------------------------------
    # TITLE PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("Hybrid Fuzzy-NSGA-II Intelligent Fleet Dispatcher", styles["AcademicTitle"]))
    story.append(Paragraph(
        "Multi-Objective Vehicle Routing with Fuzzy Time Windows, Mamdani Traffic Inference & 5-Algorithm Benchmarking",
        styles["AcademicSubtitle"]
    ))
    story.append(HRFlowable(width="90%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=30))

    meta_rows = [
        [
            Paragraph("<b>Project Domain:</b>", styles["TableCellBold"]),
            Paragraph("Soft Computing & Artificial Intelligence (Fuzzy Logic + Evolutionary Computation)", styles["TableCell"])
        ],
        [
            Paragraph("<b>Course & Category:</b>", styles["TableCellBold"]),
            Paragraph("Soft Computing (CSE Undergraduate Mini-Project / Capstone Report)", styles["TableCell"])
        ],
        [
            Paragraph("<b>Faculty Guide / Evaluator:</b>", styles["TableCellBold"]),
            Paragraph("<b>Dr. Seetha Hari</b>, Associate Professor, SCOPE, VIT-AP University", styles["TableCell"])
        ],
        [
            Paragraph("<b>Institution:</b>", styles["TableCellBold"]),
            Paragraph("School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati", styles["TableCell"])
        ],
        [
            Paragraph("<b>Research Team:</b>", styles["TableCellBold"]),
            Paragraph("<b>V Naga Adithya</b> (23BCE9062)<br/><b>M Karthik</b> (23BCE9659)", styles["TableCell"])
        ],
        [
            Paragraph("<b>Submission Date:</b>", styles["TableCellBold"]),
            Paragraph("November 2026 (Academic Year 2026–2027)", styles["TableCell"])
        ]
    ]
    t_meta = Table(meta_rows, colWidths=[1.8 * inch, 4.8 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # REPORT BODY
    # -------------------------------------------------------------
    skip_preamble = True
    for block in blocks:
        btype = block["type"]

        if skip_preamble:
            if btype == "header" and block["text"] == "Abstract":
                skip_preamble = False
            else:
                continue

        if btype == "header":
            level = block["level"]
            text = block["text"]

            # Strip markdown formatting inside header
            clean_head = re.sub(r"[*`$]", "", text)
            if level == 2 and (clean_head in ["Abstract", "Table of Contents"] or re.match(r"^\d+\.", clean_head)):
                if clean_head != "Abstract":
                    story.append(PageBreak())

            if level == 1:
                story.append(Paragraph(clean_head, styles["SectionH1"]))
            elif level == 2:
                story.append(Paragraph(clean_head, styles["SectionH2"]))
            else:
                story.append(Paragraph(clean_head, styles["SectionH3"]))

        elif btype == "paragraph":
            txt = block["text"]
            # Convert markdown formatting to ReportLab XML tags
            txt = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", txt)
            txt = re.sub(r"\*(.*?)\*", r"<i>\1</i>", txt)
            txt = clean_latex(txt)
            story.append(Paragraph(txt, styles["AcademicBody"]))

        elif btype == "equation":
            eq = clean_latex(block["text"])
            story.append(Paragraph(f"<b>[Equation]</b> {eq}", styles["AcademicEquation"]))

        elif btype == "bullet_list":
            for it in block["items"]:
                it_clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", it)
                it_clean = re.sub(r"\*(.*?)\*", r"<i>\1</i>", it_clean)
                it_clean = clean_latex(it_clean)
                story.append(Paragraph(f"&bull; {it_clean}", styles["AcademicBullet"]))

        elif btype == "numbered_list":
            for idx, it in enumerate(block["items"], start=1):
                it_clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", it)
                it_clean = re.sub(r"\*(.*?)\*", r"<i>\1</i>", it_clean)
                it_clean = clean_latex(it_clean)
                story.append(Paragraph(f"{idx}. {it_clean}", styles["AcademicBullet"]))

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
                    c_clean = clean_latex(c_clean)
                    if is_h:
                        row_cells.append(Paragraph(f"<b>{c_clean}</b>", styles["TableHeader"]))
                    else:
                        row_cells.append(Paragraph(c_clean, styles["TableCell"]))
                table_flow_data.append(row_cells)

            col_count = len(rows_data[0])
            avail_width = 504.0  # 8.5 * 72 - 108 margin
            col_width = avail_width / max(1, col_count)
            t = Table(table_flow_data, colWidths=[col_width] * col_count)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
            ]))
            story.append(Spacer(1, 4))
            story.append(t)
            story.append(Spacer(1, 6))

        elif btype == "hr":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=6, spaceAfter=8))

    pdf.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF:  {output_path} ({os.path.getsize(output_path):,} bytes)")


# =====================================================================
# 4. SCRIPT ENTRY POINT & RUNNER
# =====================================================================
def main():
    print("=" * 76)
    print(" FLEETPULSE AI — ACADEMIC PROJECT REPORT EXPORT ENGINE")
    print("=" * 76)

    if not os.path.exists(REPORT_MD_PATH):
        print(f"Error: {REPORT_MD_PATH} not found!")
        sys.exit(1)

    with open(REPORT_MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    print(f"Read markdown report: {len(md_text):,} characters from {REPORT_MD_PATH}")
    blocks = parse_markdown_blocks(md_text)
    print(f"Parsed {len(blocks)} document blocks (headers, paragraphs, tables, equations).")

    print("\n--- Generating Word Document (.docx) ---")
    generate_docx(blocks, DOCX_OUTPUT_PATH)

    print("\n--- Generating Academic PDF Document (.pdf) ---")
    generate_pdf(blocks, PDF_OUTPUT_PATH)

    print("\n" + "=" * 76)
    print(" VERIFICATION & INTEGRITY CHECK")
    print("=" * 76)
    for p in [DOCX_OUTPUT_PATH, PDF_OUTPUT_PATH]:
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            print(f" [PASS] File: {os.path.basename(p):32s} | Size: {os.path.getsize(p):,} bytes | Status: Valid")
        else:
            print(f" [FAIL] File: {os.path.basename(p):32s} | Status: Missing or empty!")
    print("=" * 76)


if __name__ == "__main__":
    main()
