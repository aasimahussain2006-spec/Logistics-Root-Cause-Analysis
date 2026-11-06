"""
Logistics Root-Cause Analysis - Executive Management Memo PDF Generator
Generates a two-page C-suite operational memo using ReportLab.
Includes executive summary, headline decline, empirical driver tree, rejected hypotheses,
governance action matrix (Owner, Target, Timeline, Review Frequency), and synthetic data disclaimer.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from src.config import MEMO_DIR

NAVY = colors.HexColor("#1B365D")
TEAL = colors.HexColor("#008080")
CHARCOAL = colors.HexColor("#2C3E50")
LIGHT_GRAY = colors.HexColor("#F8F9FA")
BORDER_GRAY = colors.HexColor("#DEE2E6")
CORAL = colors.HexColor("#D9534F")


def build_management_memo_pdf():
    """Generates the two-page management memo PDF."""
    os.makedirs(MEMO_DIR, exist_ok=True)
    pdf_path = MEMO_DIR / "management_memo.pdf"
    print(f"Generating Executive Management Memo PDF at: {pdf_path}")

    # Letter size with 0.5 in margins to ensure crisp two-page layout
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()

    # Custom Typography
    title_style = ParagraphStyle(
        "MemoTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        "MemoSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=TEAL,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        "MemoH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=NAVY,
        spaceBefore=5,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        "MemoBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=10.8,
        textColor=CHARCOAL,
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        "MemoBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.0,
        leading=10.5,
        textColor=CHARCOAL,
        leftIndent=12,
        spaceAfter=2
    )
    tbl_hdr = ParagraphStyle(
        "TblHdr",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=9.5,
        textColor=colors.white
    )
    tbl_cell = ParagraphStyle(
        "TblCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.0,
        textColor=CHARCOAL
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#7F8C8D"),
        spaceBefore=4
    )

    story = []

    # =========================================================================
    # PAGE 1: Executive Summary, Headline Decline & Empirical Drivers
    # =========================================================================
    story.append(Paragraph("KOLKATA FREIGHT & LOGISTICS (KFL) – EXECUTIVE MANAGEMENT MEMORANDUM", title_style))
    story.append(Paragraph("ROOT-CAUSE ANALYSIS & PERFORMANCE INTELLIGENCE INVESTIGATION | FY 2024", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=6, spaceBefore=1))

    # Metadata Header Box
    meta_data = [
        [
            Paragraph("<b>TO:</b> Board of Directors & Chief Operating Officer", tbl_cell),
            Paragraph("<b>DATE:</b> November 6, 2024", tbl_cell)
        ],
        [
            Paragraph("<b>FROM:</b> Senior Analytics & Performance Intelligence Team", tbl_cell),
            Paragraph("<b>SUBJECT:</b> Headline OTD Decline Root-Cause Attribution", tbl_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[310, 230])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5))

    # Executive Summary & Problem
    story.append(Paragraph("1. Executive Summary & Business Problem", h2_style))
    p1_text = (
        "During the second half of FY 2024 (Q3–Q4), Kolkata Freight & Logistics experienced a severe collapse in headline "
        "operational performance. The primary business metric, <b>On-Time Delivery Rate (OTD)</b>, deteriorated from an H1 baseline of "
        "<b>90.26%</b> (exceeding the corporate 85.0% SLA commitment) to <b>64.30%</b> in H2, representing an absolute drop of "
        "<b>-25.96 percentage points</b> (a -28.8% relative contraction). This operational failure resulted in elevated contract SLA penalties, "
        "a surge in enterprise client churn, and severe warehouse sorting congestion."
    )
    story.append(Paragraph(p1_text, body_style))

    # Driver Tree Empirical Attribution Table
    story.append(Paragraph("2. Empirical Driver Tree Decomposition (Target: >= 80% Explained)", h2_style))
    decomp_desc = (
        "Using counterfactual standardization and marginal factor attribution across 349,553 completed consignments and "
        "1.14 million scan events, our model successfully accounts for <b>92.7% of the observed decline</b> without double-counting:"
    )
    story.append(Paragraph(decomp_desc, body_style))

    decomp_rows = [
        [Paragraph("Operational Driver", tbl_hdr), Paragraph("Mechanism", tbl_hdr), Paragraph("Decline Impact", tbl_hdr), Paragraph("Share (%)", tbl_hdr)],
        [Paragraph("<b>Warehouse Sorting Bottlenecks</b>", tbl_cell), Paragraph("Conveyor breakdowns & sorting backlogs at Dhulagarh (DHU) & Taratala (TRT)", tbl_cell), Paragraph("<b>-8.94 pp</b>", tbl_cell), Paragraph("34.4%", tbl_cell)],
        [Paragraph("<b>Corridor Transit Delays</b>", tbl_cell), Paragraph("Bridge repairs & construction congestion on NH16, Kona Exp, and Dankuni bypass", tbl_cell), Paragraph("<b>-7.62 pp</b>", tbl_cell), Paragraph("29.4%", tbl_cell)],
        [Paragraph("<b>Vehicle Breakdowns & Downtime</b>", tbl_cell), Paragraph("Deferred preventative maintenance in 14ft LCV & 32ft multi-axle aging fleet", tbl_cell), Paragraph("<b>-4.38 pp</b>", tbl_cell), Paragraph("16.9%", tbl_cell)],
        [Paragraph("<b>Service Mix Shift</b>", tbl_cell), Paragraph("Expansion of tight-window Express/Same-Day services (8% to 16% volume share)", tbl_cell), Paragraph("<b>-1.85 pp</b>", tbl_cell), Paragraph("7.1%", tbl_cell)],
        [Paragraph("<b>Festive Surge Shock (W39-44)</b>", tbl_cell), Paragraph("Temporary Durga Puja freight spike (+45% volume) causing transient capacity strain", tbl_cell), Paragraph("<b>-1.28 pp</b>", tbl_cell), Paragraph("4.9%", tbl_cell)],
        [Paragraph("<b>Unexplained Residual</b>", tbl_cell), Paragraph("Stochastic transit noise, localized loading dock variances, and adverse weather", tbl_cell), Paragraph("<b>-1.89 pp</b>", tbl_cell), Paragraph("7.3%", tbl_cell)],
        [Paragraph("<b>Total Net Headline Decline</b>", tbl_hdr), Paragraph("Combined cumulative impact across network", tbl_hdr), Paragraph("<b>-25.96 pp</b>", tbl_hdr), Paragraph("<b>100.0%</b>", tbl_hdr)]
    ]
    decomp_table = Table(decomp_rows, colWidths=[130, 240, 90, 80])
    decomp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,-1), (-1,-1), CHARCOAL),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, LIGHT_GRAY])
    ]))
    story.append(decomp_table)
    story.append(Spacer(1, 4))

    # Top Contributing Drivers Deep-Dive
    story.append(Paragraph("3. Deep-Dive Findings on Primary Operational Bottlenecks", h2_style))
    story.append(Paragraph("• <b>Dhulagarh & Taratala Hub Failure (Hypothesis H4 Supported):</b> Facility performance was highly asymmetric. While Salt Lake (HUB_SLK) and Kalyani (HUB_KLY) maintained >82% OTD, Dhulagarh collapsed by 33.2 pp and Taratala by 29.8 pp. Origin sort dwell time at these facilities increased from 36.4 minutes to 118.5 minutes (t=48.2, p<0.001).", bullet_style))
    story.append(Paragraph("• <b>Highway Infrastructure Transit Friction (Hypothesis H1 Supported):</b> Arterial routes passing through the Kona Expressway corridor averaged 2.45 hours of transit delay versus 0.65 hours on peripheral routes (Welch t=31.4, p<0.001), turning planned 2-hour hauls into 5+ hour trips.", bullet_style))
    story.append(Paragraph("• <b>Aging Haulage Fleet Mechanical Risk (Hypothesis H2 Supported):</b> Logistic regression demonstrates that vehicles with >40 hours of downtime increased consignment delay probability by 3.4x (Odds Ratio = 3.42, 95% CI [3.12, 3.75]). Over 72% of breakdowns were concentrated in an identifiable 20% aging vehicle cohort.", bullet_style))

    # End of Page 1
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Rejected Hypotheses, Action Matrix & Implementation Roadmap
    # =========================================================================
    story.append(Paragraph("KOLKATA FREIGHT & LOGISTICS – OPERATIONAL RECOMMENDATIONS & GOVERNANCE", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=6, spaceBefore=1))

    # Refuted Hypotheses
    story.append(Paragraph("4. Analysis of Refuted Hypotheses: The Seasonality Myth", h2_style))
    refuted_text = (
        "<b>Hypothesis H6 (Seasonal Demand as Root Cause) is REJECTED:</b> Management initially suspected that the annual Durga Puja "
        "and Diwali festival surge was the primary culprit behind missed delivery SLAs. However, statistical phase decomposition reveals that "
        "OTD had <b>already dropped to 65.4% during Weeks 27–38</b>, well before the festive volume surge began in Week 39. Furthermore, "
        "when shipment volume returned to normal baseline levels in Weeks 45–52, OTD failed to recover (remaining at 63.8%). "
        "While festival volume added acute short-term strain, it was NOT the structural cause of the multi-quarter performance collapse."
    )
    story.append(Paragraph(refuted_text, body_style))
    story.append(Spacer(1, 3))

    # Evidence-Based Action Matrix
    story.append(Paragraph("5. Targeted Operational Action Matrix", h2_style))
    action_rows = [
        [Paragraph("Focus Area", tbl_hdr), Paragraph("Operational Intervention", tbl_hdr), Paragraph("Responsible Owner", tbl_hdr), Paragraph("Measurable Target", tbl_hdr), Paragraph("Timeline", tbl_hdr), Paragraph("Review Cadence", tbl_hdr)],
        [
            Paragraph("<b>Warehouse Automation</b>", tbl_cell),
            Paragraph("Overhaul sorting lines at Dhulagarh & Taratala; deploy secondary manual sorting bypass", tbl_cell),
            Paragraph("VP Warehouse Operations", tbl_cell),
            Paragraph("Sort dwell time < 45 min; zero backlog", tbl_cell),
            Paragraph("6 Weeks", tbl_cell),
            Paragraph("Weekly", tbl_cell)
        ],
        [
            Paragraph("<b>Dynamic Highway Routing</b>", tbl_cell),
            Paragraph("Implement GPS geofenced routing bypassing Kona Expressway during 08:00-12:00 peak", tbl_cell),
            Paragraph("Head of Fleet Dispatch", tbl_cell),
            Paragraph("Arterial delay < 40 min per trip", tbl_cell),
            Paragraph("3 Weeks", tbl_cell),
            Paragraph("Bi-Weekly", tbl_cell)
        ],
        [
            Paragraph("<b>Fleet Preventative Care</b>", tbl_cell),
            Paragraph("Mandatory 10,000 km overhaul on aging multi-axle fleet; retire 50 highest-downtime LCVs", tbl_cell),
            Paragraph("Fleet Maintenance Director", tbl_cell),
            Paragraph("Fleet breakdown rate < 1.0%", tbl_cell),
            Paragraph("8 Weeks", tbl_cell),
            Paragraph("Monthly", tbl_cell)
        ],
        [
            Paragraph("<b>Express SLA Pricing</b>", tbl_cell),
            Paragraph("Re-calibrate Same Day delivery windows from 6h to 8h in congested zones or apply congestion tariff", tbl_cell),
            Paragraph("Chief Commercial Officer", tbl_cell),
            Paragraph("Same Day OTD >= 85.0%", tbl_cell),
            Paragraph("4 Weeks", tbl_cell),
            Paragraph("Monthly", tbl_cell)
        ],
        [
            Paragraph("<b>Early-Warning Deployment</b>", tbl_cell),
            Paragraph("Operationalize automated weekly composite risk scoring index with 4-week lead alert", tbl_cell),
            Paragraph("Head of Data & BI", tbl_cell),
            Paragraph("Zero undetected bottleneck triggers", tbl_cell),
            Paragraph("2 Weeks", tbl_cell),
            Paragraph("Weekly", tbl_cell)
        ]
    ]
    action_table = Table(action_rows, colWidths=[90, 150, 95, 95, 55, 55])
    action_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GRAY])
    ]))
    story.append(action_table)
    story.append(Spacer(1, 4))

    # Early-Warning & Monitoring System
    story.append(Paragraph("6. Early-Warning Intelligence & Leading Indicators", h2_style))
    ews_text = (
        "Backtesting our multi-factor Early-Warning System over 52 historical weeks demonstrated that leading indicators "
        "(warehouse sort duration creep and arterial transit delays) triggered an <b>Orange Warning at Week 23</b>—a full "
        "<b>4 weeks prior to the public collapse of OTD in Week 27</b>. By tracking composite operational risk rather than lagging OTD, "
        "management can execute localized load-shedding and fleet reassignments before contractual SLAs are breached."
    )
    story.append(Paragraph(ews_text, body_style))

    # Limitations & Notice
    story.append(Paragraph("7. Methodological Limitations & Synthetic Data Disclosure", h2_style))
    disclaimer_text = (
        "<b>DATA NOTICE:</b> This memorandum is part of a portfolio demonstration based on a fictional logistics network in Kolkata. "
        "All 1,546,782 records across shipments, routes, vehicles, and scans were synthetically generated with fixed random seeds for "
        "reproducibility. Operational findings represent modeled scenarios and must never be cited as real-world company records. "
        "Analytical limitations include lack of driver-level telematics and micro-weather precipitation telemetry."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    # Build Document
    doc.build(story)
    print("Executive Management Memo PDF successfully generated!")
    return pdf_path


def export_management_memo_markdown():
    """Also writes a clean Markdown version of the memo for repository inspection."""
    md_path = MEMO_DIR / "management_memo.md"
    content = """# Executive Management Memorandum: Kolkata Freight & Logistics
**To:** Board of Directors & Chief Operating Officer  
**From:** Senior Analytics & Performance Intelligence Team  
**Date:** November 6, 2024  
**Subject:** Root-Cause Attribution & Corrective Action Plan for Headline OTD Decline  

---

## 1. Executive Summary
During H2 FY 2024 (Q3–Q4), Kolkata Freight & Logistics experienced a severe operational decline. The headline **On-Time Delivery Rate (OTD)** collapsed from a baseline of **90.26%** to **64.30%**, representing an absolute loss of **-25.96 percentage points**.

## 2. Empirical Driver Tree Decomposition
Using counterfactual standardization across 349,553 consignments, **92.7% of the decline** is explained:
1. **Warehouse Sorting Bottlenecks (Dhulagarh & Taratala):** -8.94 pp (34.4% of drop)
2. **Highway Corridor Congestion (NH16 / Kona Expressway):** -7.62 pp (29.4% of drop)
3. **Fleet Mechanical Breakdowns & Downtime (Aging Fleet):** -4.38 pp (16.9% of drop)
4. **Commercial Service Mix Shift (Tight-SLA Expansion):** -1.85 pp (7.1% of drop)
5. **Festive Season Demand Surge (Durga Puja Peak):** -1.28 pp (4.9% of drop)
6. **Unexplained Residual Variance:** -1.89 pp (7.3% of drop)

## 3. Rejected Hypotheses: Seasonality Refuted
**Hypothesis H6 (Seasonal Volume as Root Cause) is REJECTED:** Performance had already collapsed to 65.4% in Weeks 27–38 before the festival, and did not recover post-festival (63.8%). The root causes are structural equipment failures and route bottlenecks, not seasonal volume.

## 4. Targeted Operational Action Matrix
| Focus Area | Operational Action | Owner | Target | Timeline | Cadence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Warehouse Automation** | Overhaul sorting lines at Dhulagarh & Taratala; deploy bypass lane | VP Warehouse Operations | Sort dwell < 45 min | 6 Weeks | Weekly |
| **Dynamic Highway Routing** | GPS rerouting avoiding Kona Expressway during 08:00-12:00 peak | Head of Fleet Dispatch | Arterial delay < 40 min | 3 Weeks | Bi-Weekly |
| **Fleet Preventative Care** | 10k km overhaul on aging multi-axle fleet; retire 50 bad LCVs | Fleet Maintenance Director | Breakdown rate < 1.0% | 8 Weeks | Monthly |
| **Express SLA Pricing** | Adjust Same-Day window from 6h to 8h in congested zones | Chief Commercial Officer | Same Day OTD >= 85% | 4 Weeks | Monthly |
| **Early-Warning System** | Deploy composite risk index monitoring leading indicators | Head of Data & BI | Zero unflagged bottlenecks | 2 Weeks | Weekly |

---
*Notice: Synthetic demonstration project. All data, findings, and figures are synthetically generated.*
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Executive memo markdown exported to: {md_path}")


if __name__ == "__main__":
    build_management_memo_pdf()
    export_management_memo_markdown()

