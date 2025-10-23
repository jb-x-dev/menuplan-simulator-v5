# Tagesauswahl und Bestellvorschlag - Implementierungsdokumentation

## Datum: 22. Oktober 2025

## Übersicht

Diese Dokumentation beschreibt die Implementierung von zwei neuen Features:

1. **Tagesauswahl:** Ermöglicht die Auswahl einzelner Tage oder aller Tage im Menüplan
2. **Bestellvorschlag auf Komponentenebene:** Aggregiert Zutaten aus ausgewählten Tagen und gruppiert sie nach Komponenten

---

## Feature 1: Tagesauswahl

### Funktionalität

**Zweck:** Benutzer können gezielt auswählen, welche Tage für den Bestellvorschlag berücksichtigt werden sollen.

**Anwendungsfälle:**
- Bestellung nur für bestimmte Wochentage (z.B. Mo-Fr, ohne Wochenende)
- Teilbestellungen für Lieferengpässe
- Separate Bestellungen für verschiedene Lieferanten
- Flexibilität bei kurzfristigen Planänderungen

### UI-Komponenten

#### 1. Tages-Checkbox

**Position:** In jedem Day-Card Header, links neben dem Datum

**HTML-Struktur:**
```html
<div class="day-header">
    <div style="display: flex; align-items: center; gap: 10px;">
        <input type="checkbox" 
               id="daySelect-${dayIdx}" 
               class="day-select-checkbox" 
               checked 
               onchange="toggleDaySelection(${dayIdx}, this.checked)" 
               style="width: 20px; height: 20px; cursor: pointer;">
        <label for="daySelect-${dayIdx}" style="cursor: pointer; font-weight: 600;">
            <div class="day-date">${formatDate(day.date)}</div>
        </label>
    </div>
    <div class="day-cost">${day.total_cost.toFixed(2)}€</div>
</div>
```

**Features:**
- Standardmäßig aktiviert (checked)
- 20x20px Größe für bessere Klickbarkeit
- Label ist klickbar (gesamter Datumsbereich)
- Visuelles Feedback beim An-/Abwählen

#### 2. Tagesauswahl-Steuerung

**Position:** Unter den Export-Buttons, über dem Menüplan

**HTML-Struktur:**
```html
<div id="daySelectionControls" style="display: none; ...">
    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <span style="font-weight: 600; color: #667eea;">📅 Tagesauswahl:</span>
        <button onclick="selectAllDays()">✔️ Alle auswählen</button>
        <button onclick="deselectAllDays()">❌ Alle abwählen</button>
        <button onclick="generateOrderSuggestion()">📋 Bestellvorschlag generieren</button>
    </div>
</div>
```

**Buttons:**
- **Alle auswählen:** Aktiviert alle Tages-Checkboxen
- **Alle abwählen:** Deaktiviert alle Tages-Checkboxen
- **Bestellvorschlag generieren:** Öffnet Modal mit aggregierten Zutaten

### JavaScript-Funktionen

#### 1. `toggleDaySelection(dayIdx, isChecked)`

**Zweck:** Verwaltet die Auswahl/Abwahl einzelner Tage

**Parameter:**
- `dayIdx` (number): Index des Tages im Plan
- `isChecked` (boolean): Checkbox-Status

**Funktionsweise:**
```javascript
function toggleDaySelection(dayIdx, isChecked) {
    if (isChecked) {
        if (!selectedDays.includes(dayIdx)) {
            selectedDays.push(dayIdx);
        }
        // Visuelles Feedback: volle Opacity, blaue Border
        const dayCard = document.getElementById(`day-${dayIdx}`);
        if (dayCard) {
            dayCard.style.opacity = '1';
            dayCard.style.border = '2px solid #667eea';
        }
    } else {
        selectedDays = selectedDays.filter(d => d !== dayIdx);
        // Visuelles Feedback: reduzierte Opacity, graue Border
        const dayCard = document.getElementById(`day-${dayIdx}`);
        if (dayCard) {
            dayCard.style.opacity = '0.5';
            dayCard.style.border = '2px solid #e0e0e0';
        }
    }
}
```

**Visuelles Feedback:**
- **Ausgewählt:** Opacity 1.0, Border #667eea (blau)
- **Nicht ausgewählt:** Opacity 0.5, Border #e0e0e0 (grau)

#### 2. `selectAllDays()`

**Zweck:** Wählt alle Tage aus

**Funktionsweise:**
```javascript
function selectAllDays() {
    if (!currentPlan) return;
    
    selectedDays = currentPlan.days.map((_, idx) => idx);
    
    // Update all checkboxes and visual feedback
    currentPlan.days.forEach((_, idx) => {
        const checkbox = document.getElementById(`daySelect-${idx}`);
        if (checkbox) checkbox.checked = true;
        
        const dayCard = document.getElementById(`day-${idx}`);
        if (dayCard) {
            dayCard.style.opacity = '1';
            dayCard.style.border = '2px solid #667eea';
        }
    });
}
```

#### 3. `deselectAllDays()`

**Zweck:** Wählt alle Tage ab

**Funktionsweise:**
```javascript
function deselectAllDays() {
    if (!currentPlan) return;
    
    selectedDays = [];
    
    // Update all checkboxes and visual feedback
    currentPlan.days.forEach((_, idx) => {
        const checkbox = document.getElementById(`daySelect-${idx}`);
        if (checkbox) checkbox.checked = false;
        
        const dayCard = document.getElementById(`day-${idx}`);
        if (dayCard) {
            dayCard.style.opacity = '0.5';
            dayCard.style.border = '2px solid #e0e0e0';
        }
    });
}
```

### Datenstruktur

**Variable:** `selectedDays`

**Typ:** `Array<number>`

**Beschreibung:** Array von Tages-Indizes, die ausgewählt sind

**Beispiel:**
```javascript
// Alle Tage ausgewählt (14-Tage-Plan)
selectedDays = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

// Nur Montag bis Freitag (erste Woche)
selectedDays = [0, 1, 2, 3, 4];

// Nur Wochenenden
selectedDays = [5, 6, 12, 13];
```

**Initialisierung:**
```javascript
// In displayPlan() function
selectedDays = plan.days.map((_, idx) => idx);  // All days selected by default
```

---

## Feature 2: Bestellvorschlag auf Komponentenebene

### Funktionalität

**Zweck:** Aggregiert alle Zutaten aus ausgewählten Tagen und gruppiert sie nach Komponenten (z.B. Gemüse, Fleisch, Milchprodukte)

**Vorteile:**
- Übersichtliche Bestellliste nach Warengruppen
- Automatische Mengenberechnung
- Vermeidung von Doppelbestellungen
- Export-Funktionen für Lieferanten

### UI-Komponenten

#### 1. Bestellvorschlag-Modal

**HTML-Struktur:**
```html
<div id="orderSuggestionModal" class="modal">
    <div class="modal-content" style="max-width: 1200px; max-height: 90vh; overflow-y: auto;">
        <div class="modal-header">
            <h2 class="modal-title">📋 Bestellvorschlag auf Komponentenebene</h2>
            <button class="modal-close" onclick="closeOrderSuggestionModal()">&times;</button>
        </div>
        <div id="orderSuggestionContent" style="padding: 20px;">
            <!-- Content will be dynamically generated -->
        </div>
        <div style="padding: 20px; border-top: 2px solid #e0e0e0; display: flex; gap: 10px; justify-content: flex-end;">
            <button onclick="exportOrderSuggestionCSV()">📊 CSV exportieren</button>
            <button onclick="exportOrderSuggestionPDF()">📝 PDF exportieren</button>
            <button onclick="closeOrderSuggestionModal()">Schließen</button>
        </div>
    </div>
</div>
```

**Features:**
- Maximale Breite: 1200px (für große Tabellen)
- Scrollbar bei viel Inhalt
- Export-Buttons für CSV und PDF
- Schließen-Button

#### 2. Zusammenfassung

**Anzeige:**
- Anzahl ausgewählter Tage
- Anzahl Komponenten
- Zeitraum (von-bis)

**Beispiel:**
```
📊 Zusammenfassung
Ausgewählte Tage: 7 von 14
Komponenten: 8
Zeitraum: 03.11.2025 - 09.11.2025
```

#### 3. Komponenten-Tabellen

**Struktur pro Komponente:**
- Header mit Komponentenname und Anzahl Zutaten
- Tabelle mit Spalten:
  - Zutat
  - Menge (numerisch, 2 Dezimalstellen)
  - Einheit
  - Verwendet in (Anzahl Rezepte)

**Beispiel:**

| Zutat | Menge | Einheit | Verwendet in |
|-------|-------|---------|--------------|
| Karotten | 1250.00 | g | 3 Rezept(e) |
| Zwiebeln | 850.50 | g | 5 Rezept(e) |
| Paprika | 600.00 | g | 2 Rezept(e) |

### JavaScript-Funktionen

#### 1. `generateOrderSuggestion()`

**Zweck:** Generiert den Bestellvorschlag aus ausgewählten Tagen

**Validierung:**
```javascript
if (!currentPlan) {
    alert('Bitte erstellen Sie zuerst einen Menüplan.');
    return;
}

if (selectedDays.length === 0) {
    alert('Bitte wählen Sie mindestens einen Tag aus.');
    return;
}
```

**Algorithmus:**

1. **Initialisierung:**
   ```javascript
   const componentMap = {};  // { component: { ingredientName: { ... } } }
   ```

2. **Iteration über ausgewählte Tage:**
   ```javascript
   selectedDays.forEach(dayIdx => {
       const day = currentPlan.days[dayIdx];
       // ...
   });
   ```

3. **Iteration über Menülinien und Rezepte:**
   ```javascript
   day.menu_lines.forEach(menuLine => {
       menuLine.recipes.forEach(recipeSlot => {
           // Extract recipe and portions
           // ...
       });
   });
   ```

4. **Rezept-Format-Handling:**
   ```javascript
   // Handle both old and new format
   if (recipeSlot.options && recipeSlot.options.length > 0) {
       // New format: MealSlot with options
       const selectedOption = recipeSlot.options[recipeSlot.selected_index || 0];
       recipe = selectedOption.recipe;
       portions = selectedOption.portions || 0;
   } else if (recipeSlot.recipe) {
       // Old format: direct recipe
       recipe = recipeSlot.recipe;
       portions = recipeSlot.portions || 0;
   }
   ```

5. **Zutaten-Aggregation:**
   ```javascript
   recipe.ingredients.forEach(ingredient => {
       const component = ingredient.component || 'Sonstiges';
       const ingredientName = ingredient.name;
       
       // Initialize component and ingredient if not exists
       if (!componentMap[component]) {
           componentMap[component] = {};
       }
       
       if (!componentMap[component][ingredientName]) {
           componentMap[component][ingredientName] = {
               name: ingredientName,
               quantity: 0,
               unit: ingredient.unit || 'Stück',
               recipes: []
           };
       }
       
       // Calculate total quantity (ingredient quantity * portions)
       const totalQuantity = (ingredient.quantity || 0) * portions;
       componentMap[component][ingredientName].quantity += totalQuantity;
       
       // Track which recipes use this ingredient
       if (!componentMap[component][ingredientName].recipes.includes(recipe.name)) {
           componentMap[component][ingredientName].recipes.push(recipe.name);
       }
   });
   ```

6. **Anzeige:**
   ```javascript
   orderSuggestionData = componentMap;
   displayOrderSuggestion(componentMap);
   ```

#### 2. `displayOrderSuggestion(componentMap)`

**Zweck:** Rendert den Bestellvorschlag im Modal

**HTML-Generierung:**

1. **Zusammenfassung:**
   ```javascript
   html += `
       <div style="background: #f0f4ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 2px solid #667eea;">
           <h3 style="margin: 0 0 10px 0; color: #667eea;">📊 Zusammenfassung</h3>
           <p><strong>Ausgewählte Tage:</strong> ${selectedDays.length} von ${currentPlan.days.length}</p>
           <p><strong>Komponenten:</strong> ${Object.keys(componentMap).length}</p>
           <p><strong>Zeitraum:</strong> ${formatDate(...)} - ${formatDate(...)}</p>
       </div>
   `;
   ```

2. **Komponenten-Tabellen:**
   ```javascript
   const sortedComponents = Object.keys(componentMap).sort();
   
   sortedComponents.forEach(component => {
       const ingredients = componentMap[component];
       const ingredientList = Object.values(ingredients).sort((a, b) => a.name.localeCompare(b.name));
       
       html += `
           <div style="margin-bottom: 25px; border: 2px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
               <div style="background: #667eea; color: white; padding: 12px 15px; font-weight: 600; font-size: 16px;">
                   ${component} (${ingredientList.length} Zutaten)
               </div>
               <table style="width: 100%; border-collapse: collapse;">
                   <thead>
                       <tr style="background: #f8f9fa;">
                           <th>Zutat</th>
                           <th>Menge</th>
                           <th>Einheit</th>
                           <th>Verwendet in</th>
                       </tr>
                   </thead>
                   <tbody>
                       ${ingredientList.map((ingredient, idx) => `
                           <tr style="background: ${idx % 2 === 0 ? 'white' : '#f8f9fa'};">
                               <td>${ingredient.name}</td>
                               <td style="text-align: right; font-weight: 600;">${ingredient.quantity.toFixed(2)}</td>
                               <td>${ingredient.unit}</td>
                               <td style="font-size: 12px; color: #666;">${ingredient.recipes.length} Rezept(e)</td>
                           </tr>
                       `).join('')}
                   </tbody>
               </table>
           </div>
       `;
   });
   ```

3. **Modal öffnen:**
   ```javascript
   container.innerHTML = html;
   document.getElementById('orderSuggestionModal').classList.add('active');
   ```

#### 3. `closeOrderSuggestionModal()`

**Zweck:** Schließt das Modal

```javascript
function closeOrderSuggestionModal() {
    document.getElementById('orderSuggestionModal').classList.remove('active');
}
```

#### 4. `exportOrderSuggestionCSV()`

**Zweck:** Exportiert den Bestellvorschlag als CSV-Datei

**CSV-Format:**
```csv
Komponente,Zutat,Menge,Einheit,Anzahl Rezepte
"Gemüse","Karotten",1250.00,"g",3
"Gemüse","Zwiebeln",850.50,"g",5
"Fleisch","Hähnchenbrust",2500.00,"g",2
...
```

**Implementierung:**
```javascript
function exportOrderSuggestionCSV() {
    if (!orderSuggestionData) return;
    
    let csv = 'Komponente,Zutat,Menge,Einheit,Anzahl Rezepte\n';
    
    Object.keys(orderSuggestionData).sort().forEach(component => {
        const ingredients = orderSuggestionData[component];
        Object.values(ingredients).sort((a, b) => a.name.localeCompare(b.name)).forEach(ingredient => {
            csv += `"${component}","${ingredient.name}",${ingredient.quantity.toFixed(2)},"${ingredient.unit}",${ingredient.recipes.length}\n`;
        });
    });
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `bestellvorschlag_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
}
```

**Dateiname:** `bestellvorschlag_YYYY-MM-DD.csv`

#### 5. `exportOrderSuggestionPDF()`

**Zweck:** Exportiert den Bestellvorschlag als PDF-Datei

**Status:** Placeholder (TODO)

```javascript
async function exportOrderSuggestionPDF() {
    if (!orderSuggestionData) return;
    
    alert('PDF-Export wird implementiert...');
    // TODO: Implement PDF export using backend endpoint
}
```

### Datenstruktur

**Variable:** `orderSuggestionData`

**Typ:** `Object<string, Object<string, IngredientData>>`

**Struktur:**
```typescript
type IngredientData = {
    name: string;           // Name der Zutat
    quantity: number;       // Gesamtmenge (aggregiert)
    unit: string;           // Einheit (g, kg, l, Stück, etc.)
    recipes: string[];      // Liste der Rezeptnamen, die diese Zutat verwenden
};

type ComponentMap = {
    [component: string]: {
        [ingredientName: string]: IngredientData
    }
};
```

**Beispiel:**
```javascript
{
    "Gemüse": {
        "Karotten": {
            name: "Karotten",
            quantity: 1250.00,
            unit: "g",
            recipes: ["Gemüsesuppe", "Ratatouille", "Karotten-Ingwer-Suppe"]
        },
        "Zwiebeln": {
            name: "Zwiebeln",
            quantity: 850.50,
            unit: "g",
            recipes: ["Gemüsesuppe", "Ratatouille", "Zwiebelkuchen", "Gulasch", "Bolognese"]
        }
    },
    "Fleisch": {
        "Hähnchenbrust": {
            name: "Hähnchenbrust",
            quantity: 2500.00,
            unit: "g",
            recipes: ["Hähnchen mit Reis", "Hähnchencurry"]
        }
    }
}
```

---

## Integration mit bestehendem Code

### Änderungen in `displayPlan()`

**Zeilen 1564-1568:**
```javascript
// Initialize selectedDays array (all days selected by default)
selectedDays = plan.days.map((_, idx) => idx);

// Show day selection controls
document.getElementById('daySelectionControls').style.display = 'block';
```

**Zweck:**
- Initialisiert `selectedDays` mit allen Tages-Indizes
- Zeigt die Tagesauswahl-Steuerung an

### Änderungen in Day-Card HTML

**Zeilen 1392-1403:**
```javascript
html += `
    <div class="day-card" id="day-${dayIdx}" data-day-index="${dayIdx}">
        <div class="day-header">
            <div style="display: flex; align-items: center; gap: 10px;">
                <input type="checkbox" id="daySelect-${dayIdx}" class="day-select-checkbox" checked onchange="toggleDaySelection(${dayIdx}, this.checked)" style="width: 20px; height: 20px; cursor: pointer;">
                <label for="daySelect-${dayIdx}" style="cursor: pointer; font-weight: 600;">
                    <div class="day-date">${formatDate(day.date)}</div>
                </label>
            </div>
            <div class="day-cost">${day.total_cost.toFixed(2)}€</div>
        </div>
        <div class="meals-grid">
`;
```

**Änderungen:**
- `id="day-${dayIdx}"` hinzugefügt für visuelles Feedback
- `data-day-index="${dayIdx}"` hinzugefügt für Daten-Tracking
- Checkbox mit Label um Datum hinzugefügt

---

## Benutzer-Workflow

### Szenario 1: Vollständige Wochenbestellung

1. **Menüplan generieren** (z.B. 14 Tage)
2. **Alle Tage sind bereits ausgewählt** (Standard)
3. **Klick auf "📋 Bestellvorschlag generieren"**
4. **Modal öffnet sich** mit aggregierten Zutaten
5. **CSV exportieren** für Lieferant
6. **Modal schließen**

### Szenario 2: Teilbestellung (nur Werktage)

1. **Menüplan generieren** (z.B. 14 Tage)
2. **Klick auf "❌ Alle abwählen"**
3. **Manuell Montag bis Freitag auswählen** (10 Tage)
4. **Klick auf "📋 Bestellvorschlag generieren"**
5. **Modal zeigt nur Zutaten für ausgewählte Tage**
6. **CSV exportieren**

### Szenario 3: Nachbestellung einzelner Tage

1. **Bestehender Menüplan** (z.B. 14 Tage)
2. **Klick auf "❌ Alle abwählen"**
3. **Nur Dienstag und Mittwoch auswählen**
4. **Klick auf "📋 Bestellvorschlag generieren"**
5. **Modal zeigt nur Zutaten für 2 Tage**
6. **CSV exportieren** für Nachbestellung

---

## Styling

### Day-Card Visuelles Feedback

**Ausgewählt:**
```css
opacity: 1;
border: 2px solid #667eea;
```

**Nicht ausgewählt:**
```css
opacity: 0.5;
border: 2px solid #e0e0e0;
```

### Day Selection Controls

```css
display: flex;
gap: 10px;
align-items: center;
flex-wrap: wrap;
padding: 15px;
background: #f8f9fa;
border-radius: 8px;
border: 2px solid #e0e0e0;
```

### Order Suggestion Modal

**Modal Content:**
```css
max-width: 1200px;
max-height: 90vh;
overflow-y: auto;
```

**Component Header:**
```css
background: #667eea;
color: white;
padding: 12px 15px;
font-weight: 600;
font-size: 16px;
```

**Table:**
```css
width: 100%;
border-collapse: collapse;
```

**Table Rows (alternating):**
```css
background: white;  /* even rows */
background: #f8f9fa;  /* odd rows */
```

---

## Testing-Checkliste

### Funktionale Tests

- [ ] Tages-Checkbox funktioniert (An-/Abwählen)
- [ ] "Alle auswählen" wählt alle Tage aus
- [ ] "Alle abwählen" wählt alle Tage ab
- [ ] Visuelles Feedback bei Auswahl/Abwahl
- [ ] Bestellvorschlag-Button ist nur aktiv wenn Plan existiert
- [ ] Bestellvorschlag generiert korrekte Aggregation
- [ ] Komponenten sind alphabetisch sortiert
- [ ] Zutaten sind alphabetisch sortiert
- [ ] Mengen werden korrekt berechnet (Zutat × Portionen)
- [ ] CSV-Export funktioniert
- [ ] CSV enthält korrekte Daten
- [ ] Modal kann geschlossen werden

### Edge Cases

- [ ] Kein Plan vorhanden → Fehlermeldung
- [ ] Keine Tage ausgewählt → Fehlermeldung
- [ ] Rezept ohne Zutaten → Wird übersprungen
- [ ] Zutat ohne Komponente → Wird als "Sonstiges" kategorisiert
- [ ] Zutat ohne Einheit → Wird als "Stück" angezeigt
- [ ] Portionen = 0 → Wird übersprungen
- [ ] Mehrere Rezepte mit gleicher Zutat → Korrekte Aggregation

### UI/UX Tests

- [ ] Checkboxen sind gut sichtbar (20x20px)
- [ ] Label ist klickbar
- [ ] Visuelles Feedback ist deutlich
- [ ] Modal ist scrollbar bei viel Inhalt
- [ ] Tabellen sind übersichtlich
- [ ] Export-Buttons sind gut erreichbar
- [ ] Responsive Darstellung auf verschiedenen Bildschirmgrößen

---

## Zukünftige Erweiterungen

### 1. PDF-Export

**Implementierung:**
- Backend-Endpoint für PDF-Generierung
- Verwendung von ReportLab oder WeasyPrint
- Formatierung ähnlich wie CSV, aber mit Tabellen-Layout
- Logo und Header mit Firmenname

### 2. Erweiterte Filterung

**Features:**
- Filter nach Komponenten (z.B. nur Gemüse anzeigen)
- Filter nach Menge (z.B. nur Zutaten > 1kg)
- Suche nach Zutatennamen

### 3. Lieferanten-Zuordnung

**Features:**
- Zuordnung von Komponenten zu Lieferanten
- Separate Bestellvorschläge pro Lieferant
- Lieferanten-spezifische Export-Formate

### 4. Preisberechnung

**Features:**
- Hinterlegung von Einkaufspreisen pro Zutat
- Berechnung der Gesamtkosten pro Komponente
- Vergleich mit Budget

### 5. Bestellhistorie

**Features:**
- Speicherung vergangener Bestellvorschläge
- Vergleich mit früheren Bestellungen
- Trend-Analyse (z.B. Verbrauch pro Monat)

---

## Bekannte Einschränkungen

1. **PDF-Export nicht implementiert:**
   - Nur CSV-Export verfügbar
   - Backend-Endpoint erforderlich

2. **Keine Persistenz:**
   - Tagesauswahl wird nicht gespeichert
   - Bestellvorschlag muss neu generiert werden

3. **Keine Einheiten-Konvertierung:**
   - Zutaten mit verschiedenen Einheiten werden nicht konvertiert
   - z.B. 500g + 1kg = 500g + 1kg (nicht 1.5kg)

4. **Keine Rundung:**
   - Mengen werden auf 2 Dezimalstellen angezeigt
   - Keine automatische Rundung auf handelsübliche Mengen

---

## Changelog

### Version 1.0 - 22. Oktober 2025

**Hinzugefügt:**
- Tages-Checkboxen in Day-Cards
- Tagesauswahl-Steuerung (Alle auswählen/abwählen)
- Bestellvorschlag-Generierung
- Aggregation nach Komponenten
- Modal für Bestellvorschlag-Anzeige
- CSV-Export-Funktion
- Visuelles Feedback für ausgewählte/nicht ausgewählte Tage

**Variablen:**
- `selectedDays` (Array<number>)
- `orderSuggestionData` (ComponentMap)

**Funktionen:**
- `toggleDaySelection(dayIdx, isChecked)`
- `selectAllDays()`
- `deselectAllDays()`
- `generateOrderSuggestion()`
- `displayOrderSuggestion(componentMap)`
- `closeOrderSuggestionModal()`
- `exportOrderSuggestionCSV()`
- `exportOrderSuggestionPDF()` (Placeholder)

---

**Autor:** Manus AI Agent  
**Datum:** 22. Oktober 2025  
**Version:** 1.0

