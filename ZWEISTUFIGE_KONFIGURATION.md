# Zweistufige Konfiguration - Implementierungsdokumentation

## Datum: 22. Oktober 2025

## Übersicht

Die zweistufige Konfiguration ermöglicht eine flexible Verwaltung von Menüplan-Einstellungen:

**Stufe 1: Globale Einstellungen (⚙️ Einstellungen)**
- Definiert den Pool aller verfügbaren Optionen
- Wird einmalig konfiguriert und gespeichert
- Gilt als Grundlage für alle Menüpläne

**Stufe 2: Menüplan-spezifische Einstellungen (Hauptformular)**
- Selektion aus dem verfügbaren Pool für den aktuellen Menüplan
- Aufklappbarer Bereich "🔧 Erweiterte Einstellungen"
- Ermöglicht individuelle Anpassung pro Menüplan

---

## Implementierte Features

### 1. Globale Einstellungen (Stufe 1)

#### Neue Konfigurationskategorie: Abneigungen

**Tab:** 🚫 Abneigungen

**Verfügbare Optionen:**
- Schweinefleisch
- Rindfleisch
- Geflügel
- Fisch
- Meeresfrüchte

**Funktion:** Ausgewählte Abneigungen werden global ausgeschlossen. Rezepte mit diesen Zutaten werden NICHT in Menüpläne aufgenommen.

**Code-Variablen:**
```javascript
const availableAversions = ['Schweinefleisch', 'Rindfleisch', 'Geflügel', 'Fisch', 'Meeresfrüchte'];
let selectedAversions = [];  // Global ausgewählte Abneigungen
```

#### Bestehende Konfigurationskategorien (aktualisiert)

1. **🍽️ Mahlzeiten**
   - Frühstück, Mittagessen, Abendessen, Zwischenmahlzeit

2. **📅 Laufzeiten**
   - Wochenstart, Standardjahr, Standardwoche, Standarddauer

3. **🚫 Allergene (Ausschluss)**
   - Gluten, Milch, Eier, Fisch, Soja, Nüsse, Schalenfrüchte, Sesam, Reis

4. **🥗 Ernährungsformen**
   - Vollkost, Vegetarisch, Vegan

5. **📋 Rezeptgruppen**
   - 16 Gruppen (Basisrezeptur, Frühstück, Kalte Küche, etc.)

6. **🍴 Menülinien**
   - 12 Linien (Mittag_Dessert, Abendessen, Spätmahlzeit, etc.)

7. **👨‍🍳 Garmethoden**
   - 10 Methoden (Sautieren, Grillieren, Braten, etc.)

8. **🚫 Abneigungen** *(NEU)*
   - 5 Kategorien (Schweinefleisch, Rindfleisch, etc.)

9. **⚙️ Standardwerte**
   - Standard-Portionen, Rezepte pro Mahlzeit

---

### 2. Menüplan-spezifische Einstellungen (Stufe 2)

#### Aufklappbarer Bereich: 🔧 Erweiterte Einstellungen

**Position:** Im Hauptformular (linke Seite), nach "Ausgeschlossene Allergene"

**Funktionalität:**
- Klick auf "🔧 Erweiterte Einstellungen" öffnet/schließt den Bereich
- Icon ändert sich: ▶ (geschlossen) ↔ ▼ (geöffnet)
- Checkboxen werden dynamisch aus den globalen Einstellungen generiert

#### Enthaltene Selektionen:

1. **📋 Rezeptgruppen**
   - Zeigt nur die in den globalen Einstellungen ausgewählten Gruppen
   - Ermöglicht Selektion für den aktuellen Menüplan
   - Scrollbarer Container (max-height: 150px)

2. **🍴 Menülinien**
   - Zeigt nur die in den globalen Einstellungen ausgewählten Linien
   - Ermöglicht Selektion für den aktuellen Menüplan
   - Scrollbarer Container (max-height: 150px)

3. **👨‍🍳 Garmethoden**
   - Zeigt nur die in den globalen Einstellungen ausgewählten Methoden
   - Ermöglicht Selektion für den aktuellen Menüplan
   - Scrollbarer Container (max-height: 150px)

4. **🚫 Abneigungen**
   - Zeigt nur die in den globalen Einstellungen ausgewählten Abneigungen
   - Ermöglicht Selektion für den aktuellen Menüplan
   - Scrollbarer Container (max-height: 150px)

**Code-Variablen:**
```javascript
// Menüplan-spezifische Selektionen (Stufe 2)
let planRecipeGroups = [];      // Selektion für aktuellen Plan
let planMenuLines = [];         // Selektion für aktuellen Plan
let planCookingMethods = [];    // Selektion für aktuellen Plan
let planAversions = [];         // Selektion für aktuellen Plan
```

---

## Technische Implementierung

### Neue Funktionen

#### 1. Toggle-Funktion für Erweiterte Einstellungen
```javascript
function toggleAdvancedSettings()
```
- Öffnet/schließt den erweiterten Einstellungsbereich
- Ändert das Icon (▶/▼)
- Rendert Checkboxen beim ersten Öffnen

#### 2. Render-Funktionen für Plan-spezifische Checkboxen
```javascript
function renderPlanCheckboxes()
function renderPlanRecipeGroupsCheckboxes()
function renderPlanMenuLinesCheckboxes()
function renderPlanCookingMethodsCheckboxes()
function renderPlanAversionsCheckboxes()
```
- Generieren Checkboxen dynamisch aus globalen Einstellungen
- Zeigen nur die in Stufe 1 ausgewählten Optionen
- Markieren die für den aktuellen Plan ausgewählten Optionen

#### 3. Toggle-Funktionen für Plan-spezifische Selektionen
```javascript
function togglePlanRecipeGroup(group, isChecked)
function togglePlanMenuLine(line, isChecked)
function togglePlanCookingMethod(method, isChecked)
function togglePlanAversion(aversion, isChecked)
```
- Verwalten die Selektion für den aktuellen Menüplan
- Aktualisieren die entsprechenden Arrays

#### 4. Abneigungen-Funktionen (Stufe 1)
```javascript
function toggleAversion(aversion, isChecked)
function renderAversionsCheckboxes()
```
- Verwalten globale Abneigungen-Einstellungen
- Rendern Checkboxen im Settings-Modal

---

## HTML-Struktur

### Erweiterte Einstellungen im Hauptformular

```html
<div class="config-section">
    <h3 onclick="toggleAdvancedSettings()">
        <span id="advancedSettingsIcon">▶</span> 🔧 Erweiterte Einstellungen
    </h3>
    <div id="advancedSettingsContent" style="display: none;">
        
        <!-- Rezeptgruppen -->
        <div>
            <h4>📋 Rezeptgruppen</h4>
            <div id="planRecipeGroupsCheckboxes"></div>
        </div>
        
        <!-- Menülinien -->
        <div>
            <h4>🍴 Menülinien</h4>
            <div id="planMenuLinesCheckboxes"></div>
        </div>
        
        <!-- Garmethoden -->
        <div>
            <h4>👨‍🍳 Garmethoden</h4>
            <div id="planCookingMethodsCheckboxes"></div>
        </div>
        
        <!-- Abneigungen -->
        <div>
            <h4>🚫 Abneigungen</h4>
            <div id="planAversionsCheckboxes"></div>
        </div>
        
    </div>
</div>
```

### Abneigungen-Tab in Settings

```html
<button class="settings-tab" onclick="switchSettingsTab('aversions')">
    🚫 Abneigungen
</button>

<div id="tabContentAversions" class="tab-content" style="display: none;">
    <h3>🚫 Abneigungen</h3>
    <p><strong>Wichtig:</strong> Ausgewählte Abneigungen werden ausgeschlossen.</p>
    <div id="aversionsCheckboxes"></div>
</div>
```

---

## Datenfluss

### Stufe 1 → Stufe 2

1. **Globale Einstellungen speichern:**
   ```javascript
   localStorage.setItem('selectedRecipeGroups', JSON.stringify(selectedRecipeGroups));
   localStorage.setItem('selectedMenuLines', JSON.stringify(selectedMenuLines));
   localStorage.setItem('selectedCookingMethods', JSON.stringify(selectedCookingMethods));
   localStorage.setItem('selectedAversions', JSON.stringify(selectedAversions));
   ```

2. **Globale Einstellungen laden:**
   ```javascript
   const savedRecipeGroups = localStorage.getItem('selectedRecipeGroups');
   if (savedRecipeGroups) {
       selectedRecipeGroups = JSON.parse(savedRecipeGroups);
   }
   // ... für alle Kategorien
   ```

3. **Plan-spezifische Checkboxen generieren:**
   ```javascript
   for (const group of selectedRecipeGroups) {  // Nur aus globalem Pool
       const isChecked = planRecipeGroups.includes(group);
       // ... Checkbox HTML generieren
   }
   ```

### Stufe 2 → Backend

Die plan-spezifischen Selektionen werden beim Generieren des Menüplans an das Backend übergeben:

```javascript
const config = {
    // ... andere Felder
    recipe_groups: planRecipeGroups,
    menu_lines: planMenuLines,
    cooking_methods: planCookingMethods,
    aversions: planAversions
};
```

---

## Benutzerführung

### Workflow für Benutzer

1. **Globale Einstellungen konfigurieren (einmalig):**
   - Klick auf "⚙️ Einstellungen"
   - Tabs durchgehen und verfügbare Optionen auswählen
   - Beispiel: In "📋 Rezeptgruppen" 6 von 16 Gruppen auswählen
   - "Speichern" klicken

2. **Menüplan erstellen:**
   - Zeitraum, Budget, Mahlzeiten konfigurieren
   - Klick auf "🔧 Erweiterte Einstellungen" (optional)
   - Aus den 6 verfügbaren Rezeptgruppen 3 für diesen Plan auswählen
   - "🎲 Automatisch generieren" klicken

3. **Vorteile:**
   - Schnellere Menüplan-Erstellung (weniger Optionen zur Auswahl)
   - Konsistenz durch globale Vorgaben
   - Flexibilität für spezielle Anforderungen

---

## Beispiel-Szenario

### Szenario: Seniorenheim mit verschiedenen Menüplänen

**Stufe 1: Globale Einstellungen**
```
Rezeptgruppen (ausgewählt):
- Frühstück
- Vorspeise Mittagessen
- Fleisch/Fisch/Ei
- Sättigungsbeilage
- Gemüse
- Dessert

Abneigungen (ausgewählt):
- Schweinefleisch
- Meeresfrüchte
```

**Stufe 2a: Normaler Wochenplan**
```
Erweiterte Einstellungen:
Rezeptgruppen:
  ✓ Frühstück
  ✓ Vorspeise Mittagessen
  ✓ Fleisch/Fisch/Ei
  ✓ Sättigungsbeilage
  ✓ Gemüse
  ✓ Dessert

Abneigungen:
  ✓ Schweinefleisch
  ✓ Meeresfrüchte
```

**Stufe 2b: Vegetarischer Wochenplan**
```
Erweiterte Einstellungen:
Rezeptgruppen:
  ✓ Frühstück
  ✓ Vorspeise Mittagessen
  ☐ Fleisch/Fisch/Ei  ← Nicht ausgewählt
  ✓ Sättigungsbeilage
  ✓ Gemüse
  ✓ Dessert

Abneigungen:
  ✓ Schweinefleisch
  ✓ Meeresfrüchte
```

**Stufe 2c: Festtagsmenü**
```
Erweiterte Einstellungen:
Rezeptgruppen:
  ☐ Frühstück  ← Nicht benötigt
  ✓ Vorspeise Mittagessen
  ✓ Fleisch/Fisch/Ei
  ✓ Sättigungsbeilage
  ✓ Gemüse
  ✓ Dessert

Abneigungen:
  ☐ Schweinefleisch  ← Für Festtag erlaubt
  ✓ Meeresfrüchte
```

---

## Styling

### Erweiterte Einstellungen Container

```css
.config-section h3 {
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 8px;
}

#advancedSettingsContent {
    margin-top: 15px;
}

#advancedSettingsContent h4 {
    font-size: 14px;
    margin-bottom: 8px;
    color: #667eea;
}

#advancedSettingsContent .checkbox-group {
    max-height: 150px;
    overflow-y: auto;
    border: 1px solid #e0e0e0;
    padding: 8px;
    border-radius: 4px;
}
```

---

## Zukünftige Erweiterungen

### Geplante Features

1. **Weitere Konfigurationskategorien:**
   - Kostformen (erweitert)
   - Unterkostformen
   - Unverträglichkeiten (zusätzlich zu Allergenen)
   - Zusatzinfo (Bio, Regional, etc.)

2. **Vorlagen-System:**
   - Speichern von häufig verwendeten Stufe-2-Konfigurationen
   - Schnelles Laden von Vorlagen (z.B. "Vegetarisch", "Festtag", "Schonkost")

3. **Backend-Integration:**
   - Filterung der Rezepte basierend auf plan-spezifischen Selektionen
   - Berücksichtigung von Abneigungen im Algorithmus

4. **Validierung:**
   - Warnung, wenn keine Optionen in Stufe 2 ausgewählt sind
   - Hinweis, wenn Stufe-1-Pool leer ist

---

## Testing-Checkliste

### Funktionale Tests

- [ ] Globale Einstellungen speichern und laden
- [ ] Abneigungen-Tab anzeigen und bedienen
- [ ] Erweiterte Einstellungen aufklappen/zuklappen
- [ ] Plan-spezifische Checkboxen werden korrekt generiert
- [ ] Nur global ausgewählte Optionen erscheinen in Stufe 2
- [ ] Selektion in Stufe 2 funktioniert unabhängig
- [ ] LocalStorage-Persistenz für alle neuen Variablen

### UI/UX Tests

- [ ] Icon-Wechsel beim Aufklappen (▶ ↔ ▼)
- [ ] Scrollbare Container bei vielen Optionen
- [ ] Responsive Darstellung auf verschiedenen Bildschirmgrößen
- [ ] Tooltips und Beschreibungen sind verständlich
- [ ] Keine Optionen werden angezeigt, wenn Pool leer ist

### Integration Tests

- [ ] Konfiguration wird korrekt an Backend übergeben
- [ ] Menüplan-Generierung berücksichtigt Stufe-2-Selektionen
- [ ] Keine Konflikte mit bestehenden Features

---

## Bekannte Einschränkungen

1. **Backend-Integration ausstehend:**
   - Plan-spezifische Selektionen werden noch nicht im Backend verarbeitet
   - Rezept-Filterung basiert noch auf globalen Einstellungen

2. **Keine Vorlagen:**
   - Stufe-2-Konfigurationen müssen für jeden Plan neu erstellt werden
   - Keine Speicherung häufig verwendeter Kombinationen

3. **Keine Validierung:**
   - Keine Warnung bei leeren Selektionen
   - Keine Prüfung auf sinnvolle Kombinationen

---

## Changelog

### Version 1.0 - 22. Oktober 2025

**Hinzugefügt:**
- Zweistufige Konfigurationsarchitektur
- Abneigungen-Tab in globalen Einstellungen
- Erweiterte Einstellungen im Hauptformular
- 4 plan-spezifische Selektionsbereiche
- 9 neue JavaScript-Funktionen
- LocalStorage-Persistenz für alle neuen Variablen

**Geändert:**
- Settings-Modal um Abneigungen-Tab erweitert
- Hauptformular um erweiterte Einstellungen ergänzt
- `showSettings()` um `renderAversionsCheckboxes()` erweitert
- `saveAllSettings()` um Abneigungen-Speicherung erweitert
- `loadAllSettings()` um Abneigungen-Laden erweitert

**Dokumentiert:**
- Vollständige Implementierungsdokumentation
- Benutzerführung und Workflow
- Beispiel-Szenarien
- Testing-Checkliste

---

**Autor:** Manus AI Agent  
**Datum:** 22. Oktober 2025  
**Version:** 1.0

