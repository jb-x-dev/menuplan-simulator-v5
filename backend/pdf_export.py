"""
PDF-Export für Menüpläne mit Allergenen und Zusatzstoffen
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import io


def create_menu_plan_pdf(plan_data, config):
    """Erstellt PDF aus Menüplan-Daten"""
    
    # PDF in Memory erstellen
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Container für PDF-Elemente
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Titel
    elements.append(Paragraph("Menüplan", title_style))
    elements.append(Paragraph(f"Zeitraum: {config['start_date']} bis {config['end_date']}", styles['Normal']))
    elements.append(Paragraph(f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Statistiken
    stats = plan_data['statistics']
    stats_data = [
        ['Durchschnitt BKT:', f"{stats['average_bkt']:.2f}€"],
        ['Gesamtkosten:', f"{stats['total_cost']:.2f}€"],
        ['Anzahl Tage:', str(len(plan_data['days']))],
        ['Budget-Status:', '✓ Im Budget' if stats['within_budget'] else '✗ Außerhalb']
    ]
    
    stats_table = Table(stats_data, colWidths=[8*cm, 8*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0'))
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 1*cm))
    
    # Tage
    for day in plan_data['days']:
        # Tag-Überschrift
        day_date = datetime.fromisoformat(day['date'])
        day_title = f"{day_date.strftime('%A, %d.%m.%Y')} - {day['total_cost']:.2f}€"
        elements.append(Paragraph(day_title, heading_style))
        
        # Rezepte des Tages
        recipes_data = [['Mahlzeit', 'Rezept', 'Portionen', 'Kosten', 'Allergene']]
        
        for menu_line in day['menu_lines']:
            for recipe in menu_line['recipes']:
                allergens_str = ', '.join(recipe.get('allergens', [])) if recipe.get('allergens') else '-'
                # Verwende Fallback für Kosten und Component
                cost = recipe.get('recipe_cost') or recipe.get('cost_per_serving') or recipe.get('cost') or 0
                component = recipe.get('component') or recipe.get('menu_component') or menu_line.get('name', 'Mahlzeit')
                target_count = recipe.get('target_count', 50)
                
                recipes_data.append([
                    component,
                    recipe.get('recipe_name', 'Unbekannt'),
                    str(target_count),
                    f"{cost:.2f}€",
                    allergens_str
                ])
        
        recipes_table = Table(recipes_data, colWidths=[3*cm, 6*cm, 2*cm, 2*cm, 4*cm])
        recipes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        elements.append(recipes_table)
        elements.append(Spacer(1, 0.5*cm))
    
    # Legende
    elements.append(PageBreak())
    elements.append(Paragraph("Allergene-Legende", heading_style))
    
    allergen_legend = [
        ['Allergene nach EU-Verordnung 1169/2011'],
        ['Gluten: Glutenhaltiges Getreide'],
        ['Milch: Milch und Milchprodukte (einschl. Laktose)'],
        ['Eier: Eier und Eierprodukte'],
        ['Fisch: Fisch und Fischprodukte'],
        ['Soja: Sojabohnen und Sojaprodukte'],
        ['Schalenfrüchte: Nüsse und Nussprodukte']
    ]
    
    legend_table = Table(allergen_legend, colWidths=[16*cm])
    legend_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(legend_table)
    
    # PDF generieren
    doc.build(elements)
    
    # Buffer zurücksetzen
    buffer.seek(0)
    return buffer


def export_menu_plan_pdf(plan_data, config, output_path):
    """Exportiert Menüplan als PDF-Datei"""
    pdf_buffer = create_menu_plan_pdf(plan_data, config)
    
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.read())
    
    return output_path

