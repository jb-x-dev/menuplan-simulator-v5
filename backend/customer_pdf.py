"""
Customer PDF Export - Wochenplan für Abnehmer (ohne Preise)
Unterstützt Hochkant und Querformat
"""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime


# Allergene-Mapping: Vollname → Abkürzung
ALLERGEN_ABBREVIATIONS = {
    'Gluten': 'Gl',
    'Krebstiere': 'Kr',
    'Eier': 'Ei',
    'Fisch': 'Fi',
    'Erdnüsse': 'Er',
    'Soja': 'So',
    'Milch': 'Mi',
    'Schalenfrüchte': 'Nü',
    'Sellerie': 'Se',
    'Senf': 'Sf',
    'Sesam': 'Ss',
    'Lupinen': 'Lu',
    'Weichtiere': 'We',
    'Schwefeldioxid': 'Sw'
}


def generate_customer_pdf(plan_data, output_path, orientation='portrait'):
    """
    Generiert ein Kunden-PDF ohne Preise
    
    Args:
        plan_data: Menüplan-Daten
        output_path: Pfad für PDF-Ausgabe
        orientation: 'portrait' (Hochkant) oder 'landscape' (Querformat)
    
    Layouts:
        - portrait: Mahlzeiten als Spalten, Tage als Reihen
        - landscape: Tage als Spalten, Mahlzeiten als Reihen
    """
    # Seitenformat basierend auf Orientierung
    if orientation == 'landscape':
        pagesize = landscape(A4)
    else:
        pagesize = A4
    
    doc = SimpleDocTemplate(output_path, pagesize=pagesize,
                           topMargin=1*cm, bottomMargin=1*cm,
                           leftMargin=1*cm, rightMargin=1*cm)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    # Titel
    story.append(Paragraph("AI-Menüplan", title_style))
    
    # Zeitraum
    days_to_export = plan_data.get('days', [])[:7]
    if days_to_export and len(days_to_export) > 0:
        start_date = days_to_export[0]['date']
        end_date = days_to_export[-1]['date']
        period_text = f"{format_date_german(start_date)} bis {format_date_german(end_date)}"
        story.append(Paragraph(period_text, subtitle_style))
    
    story.append(Spacer(1, 0.3*cm))
    
    # Erstelle Tabelle basierend auf Orientierung
    if orientation == 'landscape':
        table_data, col_widths = create_landscape_table(days_to_export)
    else:
        table_data, col_widths = create_portrait_table(days_to_export)
    
    # Erstelle Tabelle
    menu_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Table Style
    table_style = [
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        
        # Erste Spalte
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor('#667eea')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (0, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('VALIGN', (0, 1), (0, -1), 'TOP'),
        
        # Daten-Zellen
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 1), (-1, -1), 7),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (1, 1), (-1, -1), 'TOP'),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        
        # Padding
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    
    menu_table.setStyle(TableStyle(table_style))
    story.append(menu_table)
    
    # Spacer vor Legende
    story.append(Spacer(1, 0.5*cm))
    
    # Allergene-Legende (kompakt, horizontal)
    legend_style = ParagraphStyle(
        'Legend',
        parent=styles['Normal'],
        fontSize=7,
        leading=9
    )
    
    # Erstelle Legende als Text
    legend_items = []
    for full_name, abbr in ALLERGEN_ABBREVIATIONS.items():
        legend_items.append(f"<b>{abbr}</b>={full_name}")
    
    legend_text = " | ".join(legend_items)
    legend_para = Paragraph(f"<b>Allergene:</b> {legend_text}", legend_style)
    story.append(legend_para)
    
    # Fußzeile
    story.append(Spacer(1, 0.2*cm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer_text = f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    story.append(Paragraph(footer_text, footer_style))
    
    # PDF generieren
    doc.build(story)
    
    return output_path


def create_landscape_table(days_to_export):
    """
    Erstellt Tabelle im Querformat: Tage als Spalten, Mahlzeiten als Reihen
    """
    table_data = []
    
    # Header-Zeile: Mahlzeit | Tag 1 | Tag 2 | ... | Tag 7
    header_row = ['Mahlzeit']
    for day in days_to_export:
        weekday = get_weekday_german(day['date'])
        date_str = format_date_german(day['date'])
        # Kurzer Header: "Mo\n01.11"
        header_row.append(f"{weekday[:2]}\n{date_str[:-5]}")
    table_data.append(header_row)
    
    # Sammle alle Mahlzeiten
    meal_names = []
    if days_to_export:
        for menu_line in days_to_export[0].get('menu_lines', []):
            meal_names.append(menu_line['name'])
    
    # Für jede Mahlzeit eine Zeile
    for meal_name in meal_names:
        row = [meal_name]
        
        for day in days_to_export:
            cell_content = get_recipes_for_meal(day, meal_name)
            row.append(cell_content if cell_content else "-")
        
        table_data.append(row)
    
    # Spaltenbreiten
    num_days = len(days_to_export)
    available_width = 27.7 * cm - 2.5*cm
    day_col_width = available_width / num_days
    col_widths = [2.5*cm] + [day_col_width] * num_days
    
    return table_data, col_widths


def create_portrait_table(days_to_export):
    """
    Erstellt Tabelle im Hochformat: Mahlzeiten als Spalten, Tage als Reihen
    """
    table_data = []
    
    # Sammle alle Mahlzeiten
    meal_names = []
    if days_to_export:
        for menu_line in days_to_export[0].get('menu_lines', []):
            meal_names.append(menu_line['name'])
    
    # Header-Zeile: Tag | Mahlzeit 1 | Mahlzeit 2 | ... | Mahlzeit N
    header_row = ['Tag'] + meal_names
    table_data.append(header_row)
    
    # Für jeden Tag eine Zeile
    for day in days_to_export:
        weekday = get_weekday_german(day['date'])
        date_str = format_date_german(day['date'])
        row = [f"{weekday}\n{date_str}"]
        
        for meal_name in meal_names:
            cell_content = get_recipes_for_meal(day, meal_name)
            row.append(cell_content if cell_content else "-")
        
        table_data.append(row)
    
    # Spaltenbreiten
    num_meals = len(meal_names)
    available_width = 19 * cm - 3*cm  # A4 Hochformat - Tag-Spalte
    meal_col_width = available_width / num_meals
    col_widths = [3*cm] + [meal_col_width] * num_meals
    
    return table_data, col_widths


def get_recipes_for_meal(day, meal_name):
    """
    Holt alle Rezepte für eine bestimmte Mahlzeit an einem Tag
    Gibt formatierten String mit Rezeptnamen und Allergenen zurück
    """
    for menu_line in day.get('menu_lines', []):
        if menu_line['name'] == meal_name:
            recipes_text = []
            for recipe in menu_line.get('recipes', []):
                recipe_name = recipe.get('recipe_name', 'Unbekannt')
                
                # Allergene als Abkürzungen
                allergens = recipe.get('allergens', [])
                allergen_abbr = []
                for allergen in allergens:
                    abbr = ALLERGEN_ABBREVIATIONS.get(allergen, allergen[:2])
                    allergen_abbr.append(abbr)
                
                if allergen_abbr:
                    allergen_str = f" ({', '.join(allergen_abbr)})"
                else:
                    allergen_str = ""
                
                recipes_text.append(f"{recipe_name}{allergen_str}")
            
            return "\n\n".join(recipes_text)
    
    return ""


def format_date_german(date_str):
    """Formatiert Datum im deutschen Format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d.%m.%Y')
    except:
        return date_str


def get_weekday_german(date_str):
    """Gibt deutschen Wochentag zurück"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        return weekdays[date_obj.weekday()]
    except:
        return ''

