import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ..services.llm_service import llm_service

class SummaryAgent:
    def generate_text_summary(self, filename: str, risk_score: int, clauses: List[Dict[str, Any]], risks: List[Dict[str, Any]]) -> str:
        """
        Uses the LLM to write an executive summary report (2-3 pages equivalence).
        """
        clauses_str = json.dumps(clauses[:10], indent=2)  # limit to top 10
        risks_str = json.dumps(risks, indent=2)
        
        prompt = (
            f"You are a professional legal auditor. Write a comprehensive 2-3 page executive summary report for the contract '{filename}'.\n"
            f"Risk Score: {risk_score}/100\n"
            f"Key Clauses Found:\n{clauses_str}\n\n"
            f"Identified Risks:\n{risks_str}\n\n"
            f"Structure the report with the following headers:\n"
            f"1. EXECUTIVE SUMMARY\n"
            f"2. RISK ASSESSMENT & METRIC EXPLANATION (Explain why the score is {risk_score}/100)\n"
            f"3. DETAILED CLAUSE ANALYSIS (Grouped by risk level)\n"
            f"4. RECOMMENDATIONS & NEGOTIATION STRATEGY\n\n"
            f"Write in a highly professional, clear, and actionable tone."
        )
        
        return llm_service.generate_content(prompt)

    def generate_pdf_report(self, filename: str, risk_score: int, summary_text: str, clauses: List[Dict[str, Any]], risks: List[Dict[str, Any]]) -> bytes:
        """
        Generates a PDF bytes representation of the report using ReportLab.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            name='DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor('#1A2B4C'),
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            name='DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=24
        )
        
        h2_style = ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1A2B4C'),
            spaceBefore=16,
            spaceAfter=10,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            name='ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10
        )
        
        score_style = ParagraphStyle(
            name='RiskScoreStyle',
            fontName='Helvetica-Bold',
            fontSize=28,
            leading=32,
            textColor=colors.HexColor('#B22222') if risk_score > 50 else colors.HexColor('#2E8B57'),
            alignment=1, # Center
            spaceAfter=4
        )

        score_label_style = ParagraphStyle(
            name='RiskScoreLabel',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#666666'),
            alignment=1,
            spaceAfter=20
        )

        story = []
        
        # Title
        story.append(Paragraph("LEGALRAG AUDIT REPORT", title_style))
        story.append(Paragraph(f"Document: {filename} | Generated dynamically via Agentic RAG", subtitle_style))
        story.append(Spacer(1, 10))
        
        # Risk Score Callout
        story.append(Paragraph(f"{risk_score} / 100", score_style))
        story.append(Paragraph("Normalized Risk Score", score_label_style))
        
        # Split LLM summary text into sections based on headers/newlines
        paragraphs = summary_text.split('\n')
        for p in paragraphs:
            p_strip = p.strip()
            if not p_strip:
                continue
            if p_strip.startswith('#') or any(p_strip.startswith(h) for h in ["1.", "2.", "3.", "4.", "EXECUTIVE SUMMARY", "RISK ASSESSMENT", "DETAILED CLAUSE", "RECOMMENDATIONS"]):
                story.append(Paragraph(p_strip.lstrip('#').strip(), h2_style))
            else:
                story.append(Paragraph(p_strip, body_style))
                
        story.append(PageBreak())
        
        # Table of Clauses
        story.append(Paragraph("Extracted Key Clauses", h2_style))
        story.append(Spacer(1, 10))
        
        table_data = [["Type", "Risk Level", "Clause Excerpt"]]
        for cl in clauses[:15]:  # limit to top 15 in pdf table
            content_excerpt = cl.get("content", "")
            if len(content_excerpt) > 100:
                content_excerpt = content_excerpt[:97] + "..."
            
            table_data.append([
                cl.get("type", "Other"),
                cl.get("risk_level", "Low"),
                content_excerpt
            ])
            
        col_widths = [110, 70, 320]
        clause_table = Table(table_data, colWidths=col_widths)
        clause_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A2B4C')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F7FA')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
        ]))
        story.append(clause_table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_csv_summary(self, clauses: List[Dict[str, Any]], risks: List[Dict[str, Any]]) -> str:
        """
        Generates a CSV string summarizing extracted clauses and identified risks.
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["--- EXTRACTED CLAUSES ---"])
        writer.writerow(["Type", "Risk Level", "Content"])
        for cl in clauses:
            writer.writerow([cl.get("type"), cl.get("risk_level"), cl.get("content")])
            
        writer.writerow([])
        writer.writerow(["--- IDENTIFIED RISKS ---"])
        writer.writerow(["Clause Type", "Severity", "Risk Explanation"])
        for r in risks:
            writer.writerow([r.get("clause_type"), r.get("severity"), r.get("risk_explanation")])
            
        return output.getvalue()

summary_agent = SummaryAgent()
