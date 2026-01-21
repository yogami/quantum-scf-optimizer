"""PDF Report Generator - Creates QR-shareable benchmark reports."""
import io
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode
from reportlab.lib.utils import ImageReader

from domain.entities import OptimizationResult


class PDFReportGenerator:
    """Generates PDF benchmark reports with QR codes."""
    
    def __init__(self, base_url: str = "https://quantum-scf-optimizer.up.railway.app"):
        self.base_url = base_url
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='QuantumTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a1a2e'),
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='QuantumMetric',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=HexColor('#16213e'),
            spaceBefore=10
        ))
    
    def _generate_qr(self, job_id: str) -> ImageReader:
        """Generate QR code for report sharing."""
        url = f"{self.base_url}/report/{job_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return ImageReader(buffer)
    
    def generate(
        self,
        classical_result: OptimizationResult,
        quantum_result: OptimizationResult,
        job_id: str
    ) -> bytes:
        """Generate PDF comparing classical vs quantum results."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Title
        story.append(Paragraph("Quantum SCF Optimization Report", self.styles['QuantumTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        # Summary metrics
        yield_improvement = ((quantum_result.total_yield - classical_result.total_yield) 
                            / classical_result.total_yield * 100) if classical_result.total_yield > 0 else 0
        risk_improvement = ((classical_result.total_risk - quantum_result.total_risk)
                           / classical_result.total_risk * 100) if classical_result.total_risk > 0 else 0
        speedup = classical_result.solve_time_ms / quantum_result.solve_time_ms if quantum_result.solve_time_ms > 0 else 1
        
        story.append(Paragraph(f"<b>Yield Improvement:</b> {yield_improvement:+.1f}%", self.styles['QuantumMetric']))
        story.append(Paragraph(f"<b>Risk Reduction:</b> {risk_improvement:+.1f}%", self.styles['QuantumMetric']))
        story.append(Paragraph(f"<b>Speedup Factor:</b> {speedup:.2f}x", self.styles['QuantumMetric']))
        story.append(Spacer(1, 1*cm))
        
        # Comparison table
        table_data = [
            ["Metric", "Classical", "Quantum", "Δ"],
            ["Total Yield (€)", f"{classical_result.total_yield:,.0f}", f"{quantum_result.total_yield:,.0f}", f"{yield_improvement:+.1f}%"],
            ["Total Risk", f"{classical_result.total_risk:.1f}", f"{quantum_result.total_risk:.1f}", f"{risk_improvement:+.1f}%"],
            ["Solve Time (ms)", f"{classical_result.solve_time_ms:.0f}", f"{quantum_result.solve_time_ms:.0f}", f"{speedup:.2f}x"],
        ]
        
        table = Table(table_data, colWidths=[4*cm, 4*cm, 4*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1a2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6'))
        ]))
        story.append(table)
        story.append(Spacer(1, 1*cm))
        
        # Solver logs
        story.append(Paragraph("<b>Quantum Solver Logs:</b>", self.styles['QuantumMetric']))
        if quantum_result.solver_logs:
            story.append(Paragraph(quantum_result.solver_logs.replace('\n', '<br/>'), self.styles['Normal']))
        
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(f"<b>Job ID:</b> {job_id}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Scan QR to share this report</b>", self.styles['Normal']))
        
        doc.build(story)
        return buffer.getvalue()
