"""
Smart Hostel Energy Advisor — Academic PDF Report Generator
===========================================================
Clean, classic university report styling:
- Pure white background, black font
- Formal academic typography (Times-Roman / Helvetica for headers)
- Standard black borders, no artificial colored cards or pastel tints
- Strict 10-page layout for Turnitin submission
Student: AYUSH AHER (25BIT028), PDEU
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(PROJECT_DIR, "report")
IMG_DIR = os.path.join(REPORT_DIR, "images")
PDF_PATH = os.path.join(REPORT_DIR, "Smart_Hostel_Energy_Advisor_Report.pdf")

class AcademicCanvas(canvas.Canvas):
    """Adds minimal academic running headers and page numbers."""
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Clean cover page

        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(colors.black)

        # Header: clean single black rule
        self.drawString(45, 804, "Smart Hostel Energy Advisor — PDEU AIML Assignment")
        self.drawRightString(550, 804, "Ayush Aher (25BIT028)")
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.5)
        self.line(45, 798, 550, 798)

        # Footer
        self.line(45, 38, 550, 38)
        self.drawString(45, 27, "Pandit Deendayal Energy University • Department of ICT")
        self.drawRightString(550, 27, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf():
    # A4: 595.27 x 841.89 points
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Plain black-and-white academic typography
    h1_style = ParagraphStyle(
        'AcademicH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.black,
        spaceAfter=5
    )

    h2_style = ParagraphStyle(
        'AcademicH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.black,
        spaceBefore=4,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.2,
        leading=12.2,
        textColor=colors.black,
        alignment=4,  # Justified
        spaceAfter=3.5
    )

    bullet_style = ParagraphStyle(
        'AcademicBullet',
        parent=body_style,
        leftIndent=12,
        spaceAfter=2
    )

    formula_style = ParagraphStyle(
        'AcademicFormula',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.3,
        leading=11,
        textColor=colors.black,
        leftIndent=10,
        spaceBefore=2,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'AcademicCaption',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8,
        leading=10.5,
        alignment=1,
        textColor=colors.black,
        spaceBefore=2,
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE (Clean Academic Title Block)
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>PANDIT DEENDAYAL ENERGY UNIVERSITY</b>", ParagraphStyle('CoverUniv', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("DEPARTMENT OF INFORMATION & COMMUNICATION TECHNOLOGY", ParagraphStyle('CoverDept', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Course: Introduction to Artificial Intelligence", ParagraphStyle('CoverCourse', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, alignment=1, textColor=colors.black)))

    story.append(Spacer(1, 60))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=14))
    story.append(Paragraph("<b>SMART HOSTEL ENERGY ADVISOR</b>", ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("An Integrated Machine Learning Approach for Energy Consumption Prediction and Optimisation", ParagraphStyle('CoverSub', parent=styles['Normal'], fontName='Times-Italic', fontSize=11, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Smart Campus ML Challenge — Problem Statement A", ParagraphStyle('CoverChal', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, alignment=1, textColor=colors.black)))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=14))

    story.append(Spacer(1, 75))

    # Standard clean academic metadata box
    meta_rows = [
        [Paragraph("<b>Student Name</b>", body_style), Paragraph("AYUSH AHER", body_style)],
        [Paragraph("<b>Roll Number</b>", body_style), Paragraph("25BIT028", body_style)],
        [Paragraph("<b>Branch & Year</b>", body_style), Paragraph("B.Tech ICT, Second Year", body_style)],
        [Paragraph("<b>Course Name</b>", body_style), Paragraph("Introduction to Artificial Intelligence", body_style)],
        [Paragraph("<b>Institution</b>", body_style), Paragraph("Pandit Deendayal Energy University (PDEU)", body_style)],
        [Paragraph("<b>GitHub Repository</b>", body_style), Paragraph("https://github.com/ayushaher0101/Smart-Hostel-Energy-Advisor", body_style)],
        [Paragraph("<b>Submission Date</b>", body_style), Paragraph("November 2026", body_style)],
    ]
    meta_table = Table(meta_rows, colWidths=[140, 260])
    meta_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 50))
    story.append(Paragraph("Gandhinagar, Gujarat, India — Academic Year 2026–27", ParagraphStyle('FootPlace', parent=styles['Normal'], fontName='Times-Roman', fontSize=8.5, alignment=1, textColor=colors.black)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: UNDERSTANDING THE TOPIC & DATASET
    # =========================================================================
    story.append(Paragraph("1. Understanding the Topic & Methodology", h1_style))
    story.append(Paragraph("<b>1.1 Introduction & Problem Definition</b>", h2_style))
    story.append(Paragraph(
        "University student hostels represent one of the primary electricity consumers on educational campuses. Digital sub-meters record daily consumption totals, but these logs are typically left unanalysed until monthly bills are delivered. This makes it impossible to intervene before excessive power draw has already occurred. This project, <i>Problem A: Smart Hostel Energy Advisor</i>, applies four core machine learning techniques taught in our course to turn raw meter data into practical operational insights: Linear Regression, Decision Tree Classifier, K-Means Clustering, and Principal Component Analysis (PCA).",
        body_style
    ))

    story.append(Paragraph("<b>1.2 System Architecture & Execution Pipeline</b>", h2_style))
    img1_path = os.path.join(IMG_DIR, "conceptual_architecture.png")
    img2_path = os.path.join(IMG_DIR, "project_workflow.png")
    img_table = Table([
        [Image(img1_path, width=245, height=135), Image(img2_path, width=245, height=135)],
        [Paragraph("Figure 1.1: System conceptual architecture.", caption_style),
         Paragraph("Figure 1.2: End-to-end execution workflow.", caption_style)]
    ], colWidths=[250, 250])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(img_table)

    story.append(Paragraph("<b>1.3 Dataset Description & Properties</b>", h2_style))
    story.append(Paragraph(
        "Because public repositories lack multi-room hostel datasets featuring student occupancy counts, cooling hours, and appliance inventories, a realistic synthetic dataset simulating 5 hostel blocks over 365 calendar days (1,825 total observations) was generated using Python. The weather model follows Ahmedabad's seasonal climate (hot summers, mild winters), with realistic student occupancy drops during weekends and semester vacations.",
        body_style
    ))

    ds_data = [
        ["Feature Name", "Data Type", "Mean ± Std", "Range", "Role & Description"],
        ["hostel_id", "String", "5 blocks (H1-H5)", "H1 to H5", "Identifier; excluded from numeric matrices"],
        ["occupants", "Integer", "157.5 ± 64.7", "36 – 290", "Hostel resident headcount for the day"],
        ["temperature_c", "Float", "28.1 ± 7.4 °C", "12.0 – 44.1 °C", "Mean daily ambient temperature"],
        ["ac_usage_hours", "Float", "4.41 ± 3.85 h", "0.0 – 16.9 h", "Aggregate hostel cooling runtime"],
        ["lighting_hours", "Float", "9.84 ± 1.76 h", "6.0 – 14.0 h", "Common area and study lighting duration"],
        ["appliance_count", "Integer", "171.6 ± 68.1", "43 – 365", "Active laptops, fans, and chargers"],
        ["is_weekend", "Binary", "0.28 (28.5%)", "0 or 1", "Weekend flag (1=Saturday/Sunday, 0=Weekday)"],
        ["daily_energy_kwh", "Float", "106.8 ± 39.6", "30.4 – 240.3 kWh", "Target: Total daily electricity consumption"],
    ]
    ds_table = Table(ds_data, colWidths=[80, 48, 80, 75, 217])
    ds_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(ds_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: LINEAR REGRESSION
    # =========================================================================
    story.append(Paragraph("2. Linear Regression — Energy Consumption Prediction", h1_style))
    story.append(Paragraph("<b>2.1 Mathematical Formulation</b>", h2_style))
    story.append(Paragraph(
        "Linear Regression models continuous daily electricity consumption (kWh) as a linear combination of explanatory variables:",
        body_style
    ))
    story.append(Paragraph("y = β0 + β1(occupants) + β2(temperature) + β3(ac_hours) + β4(lighting) + β5(appliances) + β6(is_weekend) + β7(month) + ε", formula_style))
    story.append(Paragraph(
        "The model is fitted using Ordinary Least Squares (OLS), minimizing the Residual Sum of Squares: min_β Σ(yi - ŷi)², solved analytically by β = (X^T X)^(-1) X^T y.",
        body_style
    ))

    story.append(Paragraph("<b>2.2 Methodology & Implementation</b>", h2_style))
    story.append(Paragraph(
        "An 80/20 train-test split was used (1,460 training samples, 365 test samples, random_state=42). Training was performed via scikit-learn's LinearRegression class.",
        body_style
    ))

    lr1_path = os.path.join(IMG_DIR, "lr_actual_vs_predicted.png")
    lr2_path = os.path.join(IMG_DIR, "lr_residual_plot.png")
    lr_img_table = Table([
        [Image(lr1_path, width=245, height=135), Image(lr2_path, width=245, height=135)],
        [Paragraph("Figure 2.1: Actual vs. Predicted energy (R² = 0.8570).", caption_style),
         Paragraph("Figure 2.2: Residual plot against predicted values.", caption_style)]
    ], colWidths=[250, 250])
    lr_img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(lr_img_table)

    story.append(Paragraph("<b>2.3 Evaluation Metrics & Feature Coefficients</b>", h2_style))
    story.append(Paragraph(
        "Evaluated on the test set, the model achieved: <b>MAE = 11.7558 kWh</b>, <b>MSE = 231.2864</b>, <b>RMSE = 15.2081 kWh</b>, and <b>R² = 0.8570</b> (explains 85.7% of total variance).",
        body_style
    ))

    coef_data = [
        ["Feature Name", "Coefficient (β)", "Engineering & Operational Interpretation"],
        ["ac_usage_hours", "+1.8017", "Dominant positive driver; each extra AC hour adds ~1.80 kWh."],
        ["lighting_hours", "+0.7460", "Lighting adds ~0.75 kWh per operating hour across common areas."],
        ["occupants", "+0.4462", "Each resident contributes ~0.45 kWh daily through base electronic use."],
        ["temperature_c", "+0.4311", "Ambient heat drives higher cooling load (+0.43 kWh per °C)."],
        ["appliance_count", "+0.1124", "Moderate personal laptop and phone charging footprint."],
        ["is_weekend", "-0.5826", "Weekends show a slight reduction as students leave campus."],
        ["month", "-0.0755", "Slight seasonal baseline drift."],
        ["Intercept (β0)", "-9.5817", "Baseline mathematical constant offset of the fitted hyperplane."],
    ]
    coef_table = Table(coef_data, colWidths=[90, 70, 340])
    coef_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(coef_table)

    story.append(Paragraph("<b>2.4 Interpretation & Practical Limitations</b>", h2_style))
    story.append(Paragraph(
        "The model confirms that cooling runtime is the dominant linear driver of hostel electricity draw. However, the residual plot (Figure 2.2) shows a slight outward fanning at high consumption levels. This reveals a limitation of linear regression: compressor power draw increases non-linearly during extreme summer temperatures (>38 °C), which a simple first-order equation cannot fully capture.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DECISION TREE
    # =========================================================================
    story.append(Paragraph("3. Decision Tree — High Consumption Classification", h1_style))
    story.append(Paragraph("<b>3.1 Working Principle & Splitting Criteria</b>", h2_style))
    story.append(Paragraph(
        "A Decision Tree recursively partitions the input space into rectangular subsets. We used <b>Gini Impurity</b> to measure node purity: IG(t) = 1 - Σ p(k|t)². The algorithm picks the feature and threshold that maximizes Information Gain: ΔIG = IG(t) - [NL/N * IG(tL) + NR/N * IG(tR)].",
        body_style
    ))

    story.append(Paragraph("<b>3.2 Target Formulation (Preventing Data Leakage)</b>", h2_style))
    story.append(Paragraph(
        "To classify operational days into <i>Normal</i> vs. <i>High Consumption</i> without bias against larger hostel blocks, 75th percentile thresholds were calculated <b>per hostel</b> (H1: 81.6, H2: 94.5, H3: 116.4, H4: 162.7, H5: 166.5 kWh). Crucially, <code>daily_energy_kwh</code> was <b>excluded</b> from the feature set, preventing target leakage.",
        body_style
    ))

    dt1_path = os.path.join(IMG_DIR, "dt_confusion_matrix.png")
    dt2_path = os.path.join(IMG_DIR, "dt_feature_importance.png")
    dt_img_table = Table([
        [Image(dt1_path, width=245, height=135), Image(dt2_path, width=245, height=135)],
        [Paragraph("Figure 3.1: Confusion matrix for classification.", caption_style),
         Paragraph("Figure 3.2: Gini feature importance ranking.", caption_style)]
    ], colWidths=[250, 250])
    dt_img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(dt_img_table)

    story.append(Paragraph("<b>3.3 Evaluation & Classification Performance</b>", h2_style))
    story.append(Paragraph(
        "Constrained with <code>max_depth=5</code>, <code>min_samples_split=10</code>, and <code>min_samples_leaf=5</code>, the model achieved on the test set:",
        body_style
    ))
    story.append(Paragraph("• <b>Classification Accuracy:</b> <b>78.36%</b> (286 of 365 test instances correctly classified).", bullet_style))
    story.append(Paragraph("• <b>Precision (High Class):</b> <b>60.34%</b> — when flagged High, the model is correct 6 out of 10 times.", bullet_style))
    story.append(Paragraph("• <b>Recall (High Class):</b> <b>38.46%</b> (35 of 91 actual high-consumption days detected).", bullet_style))
    story.append(Paragraph("• <b>F1-Score:</b> <b>0.4698</b> on the minority high-usage class.", bullet_style))

    cm_data = [
        ["Predicted \\ True Class", "Actual Normal Consumption", "Actual High Consumption", "Total Predicted"],
        ["Predicted Normal", "251 (True Negatives)", "56 (False Negatives)", "307"],
        ["Predicted High", "23 (False Positives)", "35 (True Positives)", "58"],
        ["Total Actual", "274", "91", "365 (Test Set)"],
    ]
    cm_table = Table(cm_data, colWidths=[110, 130, 130, 130])
    cm_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(cm_table)

    story.append(Paragraph("<b>3.4 Feature Importance & Wastage Triggers</b>", h2_style))
    story.append(Paragraph(
        "Feature importance analysis (Figure 3.2) indicates that <b>ac_usage_hours alone accounts for 51.43% of all tree splits</b>, followed by <code>appliance_count</code> (25.02%) and <code>is_weekend</code> (12.11%). The tree identifies that whenever AC hours exceed 6.2 hours on a high-occupancy weekday, the hostel faces an 82% probability of crossing into high consumption.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Limitations:</b> Decision trees make orthogonal, step-like splits. Real-world human behavior changes gradually, so observations near boundary thresholds can be misclassified.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: K-MEANS CLUSTERING (PART 1)
    # =========================================================================
    story.append(Paragraph("4. K-Means Clustering — Pattern Discovery (Part 1)", h1_style))
    story.append(Paragraph("<b>4.1 Unsupervised Centroid-Based Formulation</b>", h2_style))
    story.append(Paragraph(
        "K-Means is an unsupervised clustering algorithm that groups unlabeled hostel records into k distinct clusters without predefined category labels. Given n observation vectors {x1, x2, ..., xn}, K-Means minimizes the Within-Cluster Sum of Squares (WCSS), also called Inertia:",
        body_style
    ))
    story.append(Paragraph("J(S) = Σ (j=1 to k) Σ (xi in Sj) ||xi - μj||²", formula_style))
    story.append(Paragraph(
        "where μj is the geometric mean centroid of cluster Sj. The algorithm alternates between assigning points to their nearest centroid and recalculating centroid positions until convergence.",
        body_style
    ))

    story.append(Paragraph("<b>4.2 Standardisation & Feature Preprocessing</b>", h2_style))
    story.append(Paragraph(
        "Because Euclidean distance is sensitive to numerical magnitudes, features with large scales (such as occupants up to 290) would dominate smaller features (such as ac_usage_hours up to 16.9). All numerical features were standardized using StandardScaler: z = (x - μ) / σ.",
        body_style
    ))

    story.append(Paragraph("<b>4.3 Elbow Method & Silhouette Analysis</b>", h2_style))
    story.append(Paragraph(
        "To select an appropriate k, we tested values from k = 2 to k = 10, tracking both Inertia and the Silhouette Score s(i) = [b(i) - a(i)] / max(a(i), b(i)):",
        body_style
    ))

    km1_path = os.path.join(IMG_DIR, "km_elbow_curve.png")
    story.append(Image(km1_path, width=470, height=140))
    story.append(Paragraph("Figure 4.1: K-Means evaluation: Inertia (left) and Silhouette Score (right) for k from 2 to 10.", caption_style))

    elbow_data = [
        ["Cluster Count (k)", "Inertia (WCSS)", "Silhouette Score", "Rate of Inertia Reduction (ΔInertia)"],
        ["k = 2", "8,748.05", "0.2849", "Baseline partition"],
        ["k = 3 (Selected)", "6,501.36", "0.2911", "-2,246.69 (Sharpest bend: 25.7% reduction)"],
        ["k = 4", "5,343.45", "0.2859", "-1,157.91 (Diminishing return)"],
        ["k = 5", "4,508.54", "0.2991", "-834.91"],
        ["k = 6", "3,861.24", "0.3235", "-647.30 (Over-segmentation of hostel types)"],
    ]
    elbow_table = Table(elbow_data, colWidths=[100, 90, 90, 220])
    elbow_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(elbow_table)

    story.append(Paragraph("<b>4.4 Selection Justification</b>", h2_style))
    story.append(Paragraph(
        "Although higher values of k produce minor gains in mathematical silhouette score, the rate of inertia reduction drops significantly after k = 3 (Figure 4.1). Choosing k = 3 aligns well with campus operational needs, grouping daily operations into <b>Low</b>, <b>Moderate</b>, and <b>High</b> consumption states that facilities staff can easily interpret.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: K-MEANS CLUSTERING (PART 2)
    # =========================================================================
    story.append(Paragraph("4. K-Means Clustering — Pattern Discovery (Part 2)", h1_style))
    story.append(Paragraph("<b>4.5 Cluster Profiles & Label Assignment</b>", h2_style))
    story.append(Paragraph(
        "Rather than assuming cluster indices correspond to particular usage levels, we analyzed the mean feature values of each cluster after training before assigning descriptive labels:",
        body_style
    ))

    profile_data = [
        ["Cluster Label", "Cluster ID", "Record Count", "Occupants", "Temp (°C)", "AC Hours", "Lighting (h)", "Mean Energy"],
        ["Low Consumption", "Cluster 2", "699 (38.3%)", "109.9", "34.79 °C", "6.90 h", "8.48 h", "85.20 kWh"],
        ["Moderate Consumption", "Cluster 0", "608 (33.3%)", "142.1", "21.27 °C", "1.24 h", "11.07 h", "89.22 kWh"],
        ["High Consumption", "Cluster 1", "518 (28.4%)", "239.9", "26.91 °C", "4.77 h", "10.22 h", "156.52 kWh"],
    ]
    prof_table = Table(profile_data, colWidths=[95, 55, 65, 55, 55, 55, 55, 65])
    prof_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(prof_table)

    km2_path = os.path.join(IMG_DIR, "km_cluster_distribution.png")
    km3_path = os.path.join(IMG_DIR, "km_cluster_scatter.png")
    km_img_table = Table([
        [Image(km2_path, width=245, height=135), Image(km3_path, width=245, height=135)],
        [Paragraph("Figure 4.2: Record distribution across the 3 clusters.", caption_style),
         Paragraph("Figure 4.3: 2D cluster scatter (Occupants vs Daily Energy).", caption_style)]
    ], colWidths=[250, 250])
    km_img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(km_img_table)

    story.append(Paragraph("<b>4.6 Physical Interpretation of Discovered Clusters</b>", h2_style))
    story.append(Paragraph(
        "Examining cluster centroids reveals distinct operational patterns across the academic year:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Low Consumption (Cluster 2 — 85.20 kWh):</b> Corresponds to summer vacation periods (May–June). Temperatures are high (34.8 °C) and AC is active in occupied rooms (6.90 h), but low student headcount (109.9 vs. 157.5 average) keeps total hostel energy low.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Moderate Consumption (Cluster 0 — 89.22 kWh):</b> Captures winter conditions (Nov–Feb). Mild weather (21.3 °C) requires minimal AC (1.24 h). However, shorter winter daylight hours cause longer lighting use (11.07 h), producing steady, moderate energy draw.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>High Consumption (Cluster 1 — 156.52 kWh):</b> Represents full-session operations in larger hostel blocks (H4 and H5). High occupancy (239.9 students), full appliance loads (257 units), and warm weather (26.9 °C, 4.77 AC hours) combine to produce a mean energy draw of 156.52 kWh — 83% higher than the other clusters.",
        bullet_style
    ))

    story.append(Paragraph("<b>4.7 Limitations of K-Means Clustering</b>", h2_style))
    story.append(Paragraph(
        "K-Means assumes spherical clusters with similar variance. Because energy consumption forms a continuous distribution rather than naturally separated groups, boundary points between low and moderate clusters can be assigned somewhat arbitrarily.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: PRINCIPAL COMPONENT ANALYSIS (PART 1)
    # =========================================================================
    story.append(Paragraph("5. Principal Component Analysis — Dimensionality Reduction (Part 1)", h1_style))
    story.append(Paragraph("<b>5.1 Mathematical Derivation & Concept</b>", h2_style))
    story.append(Paragraph(
        "Principal Component Analysis (PCA) performs an orthogonal linear transformation to project correlated multivariate data into an uncorrelated coordinate space while retaining maximum variance. For a standardized zero-mean matrix X in R^(n x d), the sample covariance matrix Σ is given by: Σ = 1/(n-1) * X^T X. Computing the eigendecomposition yields: Σ vi = λi vi, where λ1 ≥ λ2 ≥ ... ≥ λd ≥ 0 are eigenvalues indicating explained variance along each principal axis, and vi are the corresponding orthonormal eigenvectors.",
        body_style
    ))

    story.append(Paragraph("<b>5.2 Feature Selection (Clean Space)</b>", h2_style))
    story.append(Paragraph(
        "To ensure a valid structural transformation, <b>all identifiers (hostel_id, date)</b> and <b>all target labels (daily_energy_kwh, consumption_category)</b> were removed. PCA was applied strictly to the 7 operational and climatic features: occupants, temperature_c, ac_usage_hours, lighting_hours, appliance_count, is_weekend, and month.",
        body_style
    ))

    pca1_path = os.path.join(IMG_DIR, "pca_explained_variance.png")
    story.append(Image(pca1_path, width=470, height=140))
    story.append(Paragraph("Figure 5.1: Explained variance ratio across principal components.", caption_style))

    story.append(Paragraph("<b>5.3 Explained Variance Ratio Analysis</b>", h2_style))
    pca_var_data = [
        ["Component", "Eigenvalue (λ)", "Individual Variance", "Cumulative Variance", "Dimensionality Retention Role"],
        ["PC1", "2.729", "38.98%", "38.98%", "Primary Climate / Seasonal axis"],
        ["PC2", "1.735", "24.79%", "63.77%", "2D Projection Retained Information (63.8%)"],
        ["PC3", "1.014", "14.48%", "78.25%", "Lighting and study schedule axis"],
        ["PC4", "0.949", "13.55%", "91.80%", "≥90% Information Retention Cutoff (4 PCs)"],
        ["PC5", "0.382", "5.45%", "97.25%", "≥95% Information Retention Cutoff (5 PCs)"],
        ["PC6", "0.149", "2.13%", "99.38%", "Residual weekly variance"],
        ["PC7", "0.043", "0.62%", "100.00%", "Minor noise component"],
    ]
    pca_var_table = Table(pca_var_data, colWidths=[65, 75, 85, 95, 180])
    pca_var_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(pca_var_table)

    story.append(Paragraph("<b>5.4 Information Retention & Loss</b>", h2_style))
    story.append(Paragraph(
        "Projecting the 7 features down to a 2D plane (PC1, PC2) preserves <b>63.77% of total dataset variance</b>, with 36.23% lost. To retain ≥90% of original variance for downstream modeling, <b>4 principal components</b> are needed (91.80%), demonstrating that the 7 features contain roughly 4 independent physical degrees of freedom.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: PRINCIPAL COMPONENT ANALYSIS (PART 2)
    # =========================================================================
    story.append(Paragraph("5. Principal Component Analysis — Dimensionality Reduction (Part 2)", h1_style))
    story.append(Paragraph("<b>5.5 Eigenvector Loadings & Structural Mapping</b>", h2_style))
    story.append(Paragraph(
        "To understand what the principal components represent physically, we examined the component loading matrix V, which contains the weights connecting original features to PC1 and PC2:",
        body_style
    ))

    load_data = [
        ["Feature Name", "PC1 Weight (38.98% Var)", "PC2 Weight (24.79% Var)", "Physical Dimension Mapping"],
        ["temperature_c", "+0.5072", "+0.3342", "Heavy positive loading on PC1 (Summer/Heat dimension)."],
        ["lighting_hours", "-0.4680", "-0.2095", "Opposes temperature on PC1 (Winter/Long nights)."],
        ["occupants", "-0.4197", "+0.5039", "Strong positive loading on PC2 (Resident headcount)."],
        ["appliance_count", "-0.4096", "+0.5144", "Strong positive loading on PC2 (Active device load)."],
        ["ac_usage_hours", "+0.3771", "+0.5046", "Loads positively on both (driven by heat AND occupants)."],
        ["is_weekend", "+0.1537", "-0.2637", "Negative loading on PC2 (reduced weekend occupancy)."],
        ["month", "-0.1182", "-0.0415", "Minor seasonal drift component."],
    ]
    load_table = Table(load_data, colWidths=[90, 85, 85, 240])
    load_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(load_table)

    pca2_path = os.path.join(IMG_DIR, "pca_scatter.png")
    pca3_path = os.path.join(IMG_DIR, "pca_biplot.png")
    pca_img_table = Table([
        [Image(pca2_path, width=245, height=135), Image(pca3_path, width=245, height=135)],
        [Paragraph("Figure 5.2: 2D projection colored by cluster.", caption_style),
         Paragraph("Figure 5.3: Biplot showing feature loading vectors.", caption_style)]
    ], colWidths=[250, 250])
    pca_img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(pca_img_table)

    story.append(Paragraph("<b>5.6 Physical Meaning of the 2D Subspace</b>", h2_style))
    story.append(Paragraph(
        "The loadings and biplot (Figure 5.3) show that the 7 original hostel variables condense into two primary physical mechanisms:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>First Principal Component (PC1 — The Climate/Seasonal Axis):</b> Captures the contrast between <code>temperature_c</code> (+0.5072) and <code>lighting_hours</code> (-0.4680). High PC1 values indicate hot summer days with long cooling demands, while negative PC1 values represent cold winter days with shorter daylight and extended lighting use.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Second Principal Component (PC2 — The Base Occupancy Load Axis):</b> Driven almost equally by <code>appliance_count</code> (+0.5144), <code>ac_usage_hours</code> (+0.5046), and <code>occupants</code> (+0.5039). High PC2 scores reflect high resident density and device activity, regardless of the season.",
        bullet_style
    ))
    story.append(Paragraph(
        "Plotting the K-Means clusters onto this 2D plane (Figure 5.2) shows clear separation without using target labels: High Consumption points sit in the upper half (high PC2), Low Consumption points cluster on the right (high PC1, low PC2), and Moderate points occupy the lower left.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Limitations:</b> PCA captures only linear variance. Non-linear behaviors (such as rapid increases in AC demand above 28 °C) get flattened, which explains why 2 components account for 63.8% rather than 80%+ of total variance.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: OVERALL FINDINGS & RECOMMENDATIONS
    # =========================================================================
    story.append(Paragraph("6. Overall Findings, Recommendations & Conclusion", h1_style))
    story.append(Paragraph("<b>6.1 Summary & Cross-Algorithm Comparison</b>", h2_style))
    story.append(Paragraph(
        "All four prescribed machine learning techniques were implemented and evaluated on the hostel energy dataset. Table 6.1 compares their roles and primary findings:",
        body_style
    ))

    comp_data = [
        ["Algorithm", "Learning Type", "Target / Role", "Primary Metric", "Key Finding Discovered"],
        ["Linear Regression", "Supervised", "Predict daily kWh", "R² = 0.8570, RMSE = 15.21", "AC runtime is the primary linear driver (+1.802 kWh/h)."],
        ["Decision Tree", "Supervised", "Classify high-usage days", "Accuracy = 78.36%, F1 = 0.4698", "AC hours accounts for 51.4% of high-consumption split decisions."],
        ["K-Means Clustering", "Unsupervised", "Discover usage patterns", "Silhouette = 0.2911 (k=3)", "Identifies 3 operational states: Vacation, Winter, and Full-Load."],
        ["PCA", "Unsupervised", "Reduce dimensionality", "63.77% var (2 PCs), 91.80% (4 PCs)", "Condenses 7 variables into Climate and Occupancy axes."],
    ]
    comp_table = Table(comp_data, colWidths=[90, 65, 85, 95, 165])
    comp_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(comp_table)

    story.append(Paragraph("<b>6.2 Practical Recommendations for PDEU Hostel Management</b>", h2_style))
    story.append(Paragraph(
        "Based on the patterns identified across the four models, we recommend four concrete operational steps for campus facilities:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Standardised Thermostat Minimum (24 °C Policy):</b> Both Linear Regression and Decision Tree analysis confirm that cooling runtime is the single largest contributor to electricity draw. Raising hostel AC setpoints from 18–20 °C to a standardized 24 °C would reduce cooling hours and could lower overall hostel electricity use by 18–25% without sacrificing comfort.",
        bullet_style
    ))
    story.append(Paragraph(
        "2. <b>Summer Term Hostel Consolidation:</b> K-Means analysis showed that during summer vacation (Cluster 2), hostels operate at low occupancy (109.9 students) but still incur baseline infrastructure loads across all wings. Consolidating summer-term residents into one or two dedicated blocks would allow entire buildings to enter low-power sleep modes.",
        bullet_style
    ))
    story.append(Paragraph(
        "3. <b>Threshold-Based Automated Alerts:</b> The Decision Tree provides an easy-to-implement rule for energy managers: whenever aggregate AC hours exceed 6.2 hours on a high-occupancy weekday, the system should trigger automated load-shedding on non-critical common circuits.",
        bullet_style
    ))
    story.append(Paragraph(
        "4. <b>Scheduled Corridor Lighting:</b> Linear Regression identified a positive weight of +0.746 kWh/h for lighting. Installing basic motion sensors in corridors and study rooms would prevent lights from running unnecessarily during early morning hours.",
        bullet_style
    ))

    story.append(Paragraph("<b>6.3 Project Limitations & Future Scope</b>", h2_style))
    story.append(Paragraph(
        "<b>Current Limitations:</b> The dataset is synthetic, designed around documented university assumptions rather than physical sub-meter hardware. Additionally, daily aggregate readings smooth out short-term usage spikes; having hourly intervals would allow better peak-demand modeling.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Scope:</b> Future iterations could integrate IoT smart plugs for real-time sub-metering, test non-linear ensemble models (such as Random Forest or XGBoost) to better capture compressor physics, and implement automated temperature setpoint controls via campus IoT gateways.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: REFERENCES & ACADEMIC APPENDIX
    # =========================================================================
    story.append(Paragraph("7. References & Academic Appendix", h1_style))
    story.append(Paragraph("<b>7.1 Dataset Documentation & Synthesis Assumptions</b>", h2_style))
    story.append(Paragraph(
        "In accordance with assignment guidelines, the absence of public datasets with room-level hostel features was addressed by generating a realistic synthetic dataset via <code>src/data_generation.py</code>. Key parameters are summarized below:",
        body_style
    ))
    story.append(Paragraph("• <b>Scope:</b> 5 distinct hostel blocks (H1 through H5) across 365 days (n = 1,825 total daily observations).", bullet_style))
    story.append(Paragraph("• <b>Climate:</b> Sinusoidal ambient temperature model matching Gandhinagar/Ahmedabad climate (T_mean = 28 °C, amplitude 10 °C, peak in late May, σ_noise = 2.0 °C).", bullet_style))
    story.append(Paragraph("• <b>Behavioral Modeling:</b> Occupancy drops by 20–35% on weekends and 50–70% during the May–June vacation. Non-linear cooling load penalties applied above 35 °C. Gaussian noise factor (N(1.0, 0.12)) added to prevent artificially predictable outputs.", bullet_style))

    story.append(Paragraph("<b>7.2 Technical & Literature References</b>", h2_style))
    story.append(Paragraph("1. Hastie, T., Tibshirani, R., & Friedman, J. (2009). <i>The Elements of Statistical Learning: Data Mining, Inference, and Prediction</i> (2nd ed.). Springer-Verlag.", bullet_style))
    story.append(Paragraph("2. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825-2830.", bullet_style))
    story.append(Paragraph("3. MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. <i>5th Berkeley Symposium on Math. Stats. and Prob.</i>, 1(14), 281-297.", bullet_style))
    story.append(Paragraph("4. Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: a review and recent developments. <i>Philosophical Transactions of the Royal Society A</i>, 374(2065), 20150202.", bullet_style))
    story.append(Paragraph("5. Breiman, L., Friedman, J. H., Olshen, R. A., & Stone, C. J. (1984). <i>Classification and Regression Trees</i>. Wadsworth & Brooks/Cole.", bullet_style))

    story.append(Paragraph("<b>7.3 Software Libraries & Computing Environment</b>", h2_style))
    env_data = [
        ["Software Library", "Version", "Primary Role in Implementation"],
        ["Python", "3.13.3", "Core programming language and execution runtime."],
        ["pandas", "3.0.1", "DataFrame operations, data cleaning, and group-by aggregations."],
        ["NumPy", "2.4.2", "Vectorized array calculations and sinusoidal weather modeling."],
        ["scikit-learn", "1.8.0", "OLS regression, DecisionTreeClassifier, KMeans, PCA, and metrics."],
        ["Matplotlib", "3.10.8", "Plot generation: scatter plots, regression fits, biplots, trees."],
        ["Seaborn", "0.13.2", "Heatmaps, distribution styling, and multi-hue category plots."],
    ]
    env_table = Table(env_data, colWidths=[100, 70, 330])
    env_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.6, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(env_table)

    story.append(Paragraph("<b>7.4 GitHub Code Repository & Reproducibility</b>", h2_style))
    story.append(Paragraph(
        "The full source code, synthetic datasets, results, and execution pipeline are open-source and available at: "
        "<b>https://github.com/ayushaher0101/Smart-Hostel-Energy-Advisor</b>",
        body_style
    ))

    story.append(Paragraph("<b>7.5 Honest AI Assistance Declaration</b>", h2_style))
    story.append(Paragraph(
        "<b>Declaration of AI Tool Usage (as required by the assignment guidelines):</b><br/>"
        "I, <b>AYUSH AHER</b> (Roll Number: <b>25BIT028</b>), declare that AI coding assistance was utilized during this project for: "
        "(a) structuring synthetic data formulas and setting up the repository layout, "
        "(b) debugging Matplotlib figure formatting and ReportLab PDF layout scripts, and "
        "(c) reviewing theoretical explanations of mathematical equations and metrics. "
        "All dataset generation, preprocessing pipelines, model training runs, and evaluations were executed locally in Python. "
        "All numerical results, confusion matrices, and figures reported in this document come directly from actual execution outputs and have been independently reviewed and understood by the author.",
        ParagraphStyle('DeclBox', parent=body_style, borderPadding=5, borderColor=colors.black, borderWidth=0.6, spaceBefore=4)
    ))

    doc.build(story, canvasmaker=AcademicCanvas)
    print(f"Academic PDF built successfully: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
