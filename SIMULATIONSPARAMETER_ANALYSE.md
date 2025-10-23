# Simulationsparameter - Analyse und Implementierungsplan

## Datum: 22. Oktober 2025

## Quelle

Basierend auf dem Dokument "Alternative Parameter für Menüplansimulation" wurden folgende Parameterkategorien identifiziert, die für Krankenhäuser, Reha-Einrichtungen, Pflegebetriebe, Kantinen und Kindergärten relevant sind.

---

## Parameterkategorien

### 1. Ernährungs- und Nährwertparameter

#### 1.1 Kalorien- und Nährstoffbedarfe

**Beschreibung:** Menüs müssen den Energie- und Nährstoffbedarf decken (Eiweiß, Kohlenhydrate, Ballaststoffe, Vitamine, Mineralstoffe).

**Parameter:**
- **Mindest-Kalorien pro Tag** (kcal)
  - Standard: 2000 kcal
  - Bereich: 1200-3500 kcal
  - Anwendung: Krankenhäuser, Reha, Senioren

- **Maximal-Kalorien pro Tag** (kcal)
  - Standard: 2500 kcal
  - Bereich: 1500-4000 kcal
  - Anwendung: Gewichtsmanagement

- **Protein-Mindestanteil** (%)
  - Standard: 15%
  - Bereich: 10-30%
  - Anwendung: Protein-/energiereiche Ernährung

- **Kohlenhydrat-Anteil** (%)
  - Standard: 50%
  - Bereich: 30-65%
  - Anwendung: Diabeteskost

- **Fett-Anteil** (%)
  - Standard: 30%
  - Bereich: 20-40%
  - Anwendung: Fettkontrolle

**Referenz:** [918295637007799†L233-L239]

#### 1.2 Spezial-/therapeutische Diäten

**Beschreibung:** Viele Gäste benötigen spezielle Diäten wie diabetesgerechte Kost, protein-/energiereiche Ernährung, natriumarme oder glutenfreie Speisen.

**Parameter:**
- **Diabetesgerechte Kost aktivieren** (Ja/Nein)
  - Berücksichtigt niedrigen glykämischen Index
  - Begrenzt schnelle Kohlenhydrate

- **Protein-/energiereiche Kost aktivieren** (Ja/Nein)
  - Erhöht Protein- und Kaloriengehalt
  - Für Mangelernährung

- **Natriumarme Kost aktivieren** (Ja/Nein)
  - Begrenzt Salz auf max. 2g/Tag
  - Für Herz-Kreislauf-Erkrankungen

- **Glutenfreie Kost aktivieren** (Ja/Nein)
  - Schließt glutenhaltige Zutaten aus
  - Für Zöliakie

**Textmodifikationen:**
- **Weiche Kost** (Ja/Nein)
- **Fein gehackte Kost** (Ja/Nein)
- **Pürierte Kost** (Ja/Nein)

**Referenz:** [918295637007799†L206-L216]

#### 1.3 Portionsgrößen und Flüssigkeitsmengen

**Beschreibung:** Standards für Portionen und Trinkmengen (z.B. 1,5 Liter/6 Becher pro Tag bei Senioren) erleichtern Einkauf und Nährstoffkontrolle.

**Parameter:**
- **Standard-Portionsgröße** (g)
  - Standard: 400g
  - Bereich: 200-800g
  - Anwendung: Hauptmahlzeiten

- **Flüssigkeitsmenge pro Tag** (ml)
  - Standard: 1500 ml
  - Bereich: 1000-2500 ml
  - Anwendung: Senioren, Kranke

- **Anzahl Becher pro Tag**
  - Standard: 6
  - Bereich: 4-10
  - Anwendung: Trinkplan

**Referenz:** [30312339795099†L98-L123]

---

### 2. Vielfalt und Menüzyklen

#### 2.1 Menüzykluslänge

**Beschreibung:** Krankenhäuser nutzen oft 5- bis 7-Tage-Zyklen, während Kantinen/Schulen und Kindergärten längere Zyklen (4-6 Wochen) verwenden.

**Parameter:**
- **Zykluslänge** (Tage)
  - Krankenhaus: 5-7 Tage
  - Kantine/Schule: 20-30 Tage (4-6 Wochen)
  - Kindergarten: 20-30 Tage
  - Standard: 14 Tage

- **Mindestrhythmus** (Tage)
  - Standard: 21 Tage
  - Beschreibung: Mindestabstand zwischen Wiederholungen des gleichen Rezepts
  - Anwendung: Vermeidung von Monotonie

- **Mahlzeiten pro Tag**
  - Wohnformen: 3 Hauptmahlzeiten + Snacks
  - Standard: 3
  - Bereich: 2-5

**Referenz:** 
- [144068462366983†L46-L51]
- [370859594771577†L2775-L2783]
- [30312339795099†L50-L104]

#### 2.2 Abwechslung und Angebotshäufigkeiten

**Beschreibung:** Es soll täglich Gemüse/Salat, eine Stärkekomponente, Obst und Milchprodukte geben; Fleisch, süße Hauptspeisen und frittierte Gerichte sind pro 20 Verpflegungstage begrenzt, während Vollkornprodukte häufiger eingeplant werden müssen.

**Parameter:**
- **Gemüse/Salat täglich** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Mindestens eine Gemüse- oder Salatkomponente pro Tag

- **Stärkekomponente täglich** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Kartoffeln, Reis, Nudeln, Brot

- **Obst täglich** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Frisches Obst oder Obstsalat

- **Milchprodukte täglich** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Joghurt, Quark, Käse, Milch

- **Fleisch max. pro 20 Tage**
  - Standard: 8 mal
  - Bereich: 4-12 mal
  - Beschreibung: Begrenzung von Fleischgerichten

- **Süße Hauptspeisen max. pro 20 Tage**
  - Standard: 4 mal
  - Bereich: 2-8 mal
  - Beschreibung: Pfannkuchen, süße Aufläufe, etc.

- **Frittierte Gerichte max. pro 20 Tage**
  - Standard: 4 mal
  - Bereich: 2-8 mal
  - Beschreibung: Pommes, Schnitzel, etc.

- **Vollkornprodukte min. pro 20 Tage**
  - Standard: 10 mal
  - Bereich: 5-15 mal
  - Beschreibung: Vollkornbrot, -nudeln, -reis

**Referenz:** [639601461867900†L1956-L1999]

---

### 3. Budget und Kostenkontrolle

#### 3.1 Budget pro Person

**Beschreibung:** Pflegeeinrichtungen haben oft ein bestimmtes Rohkostbudget (z.B. 9 CAD pro Bewohner/Tag in Ontario). Dieses sollte als Parameter hinterlegt werden.

**Parameter:**
- **Rohkostbudget pro Person/Tag** (€)
  - Standard: 8.00 €
  - Bereich: 5.00-15.00 €
  - Anwendung: Pflegeeinrichtungen, Kantinen

- **Budget-Toleranz** (%)
  - Standard: 15%
  - Bereich: 5-30%
  - Beschreibung: Erlaubte Abweichung vom Ziel-BKT

**Referenz:** [918295637007799†L167-L173]

#### 3.2 Zutatspezifische Kosten

**Beschreibung:** Simulationsmodelle wie "RegioBioMatch" berücksichtigen Rohwarenpreise und Verfügbarkeit, um kosteneffiziente Rezeptkombinationen auszuwählen.

**Parameter:**
- **Kostenoptimierung aktivieren** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Bevorzugt günstigere Rezepte bei gleicher Qualität

- **Preisdatenbank verwenden** (Ja/Nein)
  - Standard: Nein
  - Beschreibung: Verwendet hinterlegte Zutatpreise für Kalkulation

- **Maximale Rezeptkosten** (€)
  - Standard: 5.00 €
  - Bereich: 2.00-10.00 €
  - Beschreibung: Maximale Kosten pro Rezept

**Referenz:** [453921513786693†L764-L815]

---

### 4. Verfügbarkeit, Regionalität und Nachhaltigkeit

#### 4.1 Saisonale und regionale Verfügbarkeit

**Beschreibung:** Rezepte müssen nach saisonalen und regionalen Rohwaren sowie Bio-Zertifizierung ausgewählt werden; Matching-Algorithmen nutzen Lagerbestände, Rohwareninformationen und Hard/Soft-Constraints.

**Parameter:**
- **Saisonale Produkte bevorzugen** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Bevorzugt Rezepte mit saisonalen Zutaten

- **Regionale Produkte bevorzugen** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Bevorzugt Rezepte mit regionalen Zutaten

- **Bio-Produkte bevorzugen** (Ja/Nein)
  - Standard: Nein
  - Beschreibung: Bevorzugt Bio-zertifizierte Zutaten

- **Regionalitäts-Radius** (km)
  - Standard: 100 km
  - Bereich: 50-500 km
  - Beschreibung: Maximale Entfernung für "regionale" Produkte

**Referenz:** [453921513786693†L764-L815]

#### 4.2 Nachhaltigkeitsquoten

**Beschreibung:** Gesundheits-Leitlinien fordern, den Anteil regionaler/bio-zertifizierter Speisen zu erhöhen und Verpackungsmüll zu reduzieren.

**Parameter:**
- **Mindestanteil Bio-Produkte** (%)
  - Standard: 20%
  - Bereich: 0-100%
  - Beschreibung: Mindestanteil bio-zertifizierter Zutaten

- **Mindestanteil regionale Produkte** (%)
  - Standard: 50%
  - Bereich: 0-100%
  - Beschreibung: Mindestanteil regionaler Zutaten

- **CO₂-Footprint max.** (kg CO₂/Tag)
  - Standard: 5.0 kg
  - Bereich: 2.0-10.0 kg
  - Beschreibung: Maximaler CO₂-Fußabdruck pro Person/Tag

- **Verpackungsmüll reduzieren** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Bevorzugt unverpackte oder minimal verpackte Produkte

**Referenz:** [956053796148753†L1932-L2064]

#### 4.3 Produktions- und Logistikkapazitäten

**Beschreibung:** Verschiedene Küchenmodelle (Cook & Serve, Cook & Chill, Cook & Freeze) haben Einfluss auf Produktionszeiten, Lagerung und Wartezeiten. Logistik-Parameter wie pünktliche Lieferung und Vermeidung von Leerfahrten sind besonders in Krankenhäusern wichtig.

**Parameter:**
- **Küchenmodell**
  - Optionen: Cook & Serve, Cook & Chill, Cook & Freeze
  - Standard: Cook & Serve
  - Beschreibung: Produktionsmodell der Küche

- **Maximale Produktionszeit pro Rezept** (Minuten)
  - Standard: 120 Minuten
  - Bereich: 30-240 Minuten
  - Beschreibung: Zeitlimit für Rezeptzubereitung

- **Lagerkapazität berücksichtigen** (Ja/Nein)
  - Standard: Nein
  - Beschreibung: Prüft verfügbare Lager- und Kühlkapazität

- **Lieferzeitfenster** (Stunden)
  - Standard: 24 Stunden
  - Bereich: 2-72 Stunden
  - Beschreibung: Zeitfenster für Zutatlieferung

**Referenz:** 
- [288359014377925†L436-L449]
- [439950951248352†L154-L171]

---

### 5. Zielgruppen-spezifische Anforderungen

#### 5.1 Personalisierte Präferenzen

**Beschreibung:** Speisen sollen Bewohner- und Patientenwünsche, kulturelle/religiöse Vorgaben und Allergien berücksichtigen. Feedback-Mechanismen wie Residentenkreise, Kinderfeedback (Smileys) oder Speisenkomitees erhöhen die Akzeptanz.

**Parameter:**
- **Bewohnerwünsche berücksichtigen** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Berücksichtigt individuelle Präferenzen

- **Kulturelle/religiöse Vorgaben** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Berücksichtigt kulturelle und religiöse Anforderungen

- **Feedback-System aktivieren** (Ja/Nein)
  - Standard: Nein
  - Beschreibung: Sammelt und berücksichtigt Bewohner-Feedback

- **Akzeptanz-Schwellwert** (%)
  - Standard: 70%
  - Bereich: 50-95%
  - Beschreibung: Mindestakzeptanz für Rezepte (basierend auf historischem Feedback)

**Referenz:** 
- [918295637007799†L179-L187]
- [370859594771577†L2848-L2857]

#### 5.2 Spezielle Menülinien

**Beschreibung:** Leitlinien für Kindergärten ermöglichen eine ovo-lacto-vegetarische Menülinie und fordern, die kritischen Nährstoffe (Protein, Omega-3, Jod, Eisen) zu berücksichtigen.

**Parameter:**
- **Ovo-lacto-vegetarische Linie aktivieren** (Ja/Nein)
  - Standard: Nein
  - Anwendung: Kindergärten, Schulen

- **Kritische Nährstoffe überwachen**
  - Protein (Ja/Nein)
  - Omega-3 (Ja/Nein)
  - Jod (Ja/Nein)
  - Eisen (Ja/Nein)
  - Standard: Alle Ja
  - Beschreibung: Stellt sicher, dass kritische Nährstoffe ausreichend vorhanden sind

- **Kinderfreundliche Rezepte bevorzugen** (Ja/Nein)
  - Standard: Nein
  - Anwendung: Kindergärten, Schulen
  - Beschreibung: Bevorzugt bekannte und beliebte Gerichte

**Referenz:** [639601461867900†L1909-L1921]

---

### 6. Qualitäts- und Hygienestandards

#### 6.1 Salz-, Zucker- und Fettbegrenzung

**Beschreibung:** Speisen sollten wenig Salz, Zucker und gesättigte Fette enthalten; Convenience-Produkte sind beschränkt und müssen palmölfrei oder aus nachhaltigem Palmöl sein.

**Parameter:**
- **Maximale Salzmenge pro Tag** (g)
  - Standard: 6.0 g
  - Bereich: 3.0-10.0 g
  - Beschreibung: WHO-Empfehlung: max. 5g/Tag

- **Maximale Zuckermenge pro Tag** (g)
  - Standard: 50.0 g
  - Bereich: 25.0-100.0 g
  - Beschreibung: WHO-Empfehlung: max. 50g/Tag

- **Maximale gesättigte Fette** (% der Gesamtkalorien)
  - Standard: 10%
  - Bereich: 5-15%
  - Beschreibung: Begrenzung gesättigter Fettsäuren

- **Convenience-Produkte begrenzen** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Reduziert Fertigprodukte

- **Palmölfrei oder nachhaltig** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Schließt nicht-nachhaltiges Palmöl aus

**Referenz:** 
- [639601461867900†L1937-L1947]
- [370859594771577†L2813-L2890]

#### 6.2 Lebensmittelsicherheit

**Beschreibung:** Für empfindliche Gruppen werden bestimmte Lebensmittel (Rohmilchprodukte, rohe Eier, Rohwurst, ungekochtes Mett) ausgeschlossen.

**Parameter:**
- **Rohmilchprodukte ausschließen** (Ja/Nein)
  - Standard: Ja
  - Anwendung: Senioren, Kranke, Kinder

- **Rohe Eier ausschließen** (Ja/Nein)
  - Standard: Ja
  - Anwendung: Senioren, Kranke, Kinder

- **Rohwurst ausschließen** (Ja/Nein)
  - Standard: Ja
  - Anwendung: Senioren, Kranke, Kinder

- **Ungekochtes Mett ausschließen** (Ja/Nein)
  - Standard: Ja
  - Anwendung: Senioren, Kranke, Kinder

- **Maximale Warmhaltezeit** (Stunden)
  - Standard: 3 Stunden
  - Bereich: 1-6 Stunden
  - Beschreibung: HACCP-Richtlinie

- **Minimale Kühlzeit** (Stunden)
  - Standard: 2 Stunden
  - Bereich: 1-4 Stunden
  - Beschreibung: Schnelle Abkühlung nach Produktion

**Referenz:** [370859594771577†L2799-L2807]

---

### 7. Betriebsorganisation und Feedback

#### 7.1 Prognose- und Bestellparameter

**Beschreibung:** Daten wie erwartete Essenteilnehmer pro Tag, Öffnungstage und saisonale Schwankungen helfen, Produktionsmengen und Abfall zu planen.

**Parameter:**
- **Erwartete Essenteilnehmer pro Tag**
  - Standard: 50
  - Bereich: 10-1000
  - Beschreibung: Durchschnittliche Anzahl Gäste

- **Öffnungstage pro Woche**
  - Standard: 7
  - Bereich: 5-7
  - Beschreibung: Anzahl Betriebstage

- **Saisonale Schwankungen berücksichtigen** (Ja/Nein)
  - Standard: Ja
  - Beschreibung: Passt Produktionsmengen an Saison an

- **Abfall-Zielwert** (%)
  - Standard: 10%
  - Bereich: 5-20%
  - Beschreibung: Maximaler akzeptabler Lebensmittelabfall

**Referenz:** [415549036610966†L2680-L2724]

#### 7.2 "Immer-auf-der-Karte"-Gerichte

**Beschreibung:** Langzeitpflege-Einrichtungen empfehlen eine ständig verfügbare Basisauswahl (Suppen, belegte Brote, Obst), die qualitativ und quantitativ definiert ist.

**Parameter:**
- **Basis-Menü aktivieren** (Ja/Nein)
  - Standard: Ja
  - Anwendung: Pflegeeinrichtungen

- **Basis-Menü Optionen** (Mehrfachauswahl)
  - Suppen
  - Belegte Brote
  - Obst
  - Salate
  - Joghurt/Quark
  - Standard: Alle ausgewählt

- **Mindestanzahl Basis-Optionen**
  - Standard: 3
  - Bereich: 2-6
  - Beschreibung: Immer verfügbare Alternativen

**Referenz:** [792220669722781†L114-L130]

#### 7.3 Feedback und Überarbeitung

**Beschreibung:** Menüs sollten regelmäßig (mindestens einmal jährlich) überprüft werden; Befragungen und Tellerreste-Analysen helfen, das Angebot zu verbessern.

**Parameter:**
- **Feedback-Intervall** (Monate)
  - Standard: 12 Monate
  - Bereich: 3-24 Monate
  - Beschreibung: Häufigkeit der Menü-Überprüfung

- **Tellerreste-Analyse aktivieren** (Ja/Nein)
  - Standard: Nein
  - Beschreibung: Erfasst und analysiert Lebensmittelabfall

- **Befragungen durchführen** (Ja/Nein)
  - Standard: Nein
  - Beschreibung: Sammelt Gäste-Feedback systematisch

- **Mindest-Bewertung für Rezepte** (1-5 Sterne)
  - Standard: 3.0
  - Bereich: 2.0-5.0
  - Beschreibung: Minimale Bewertung für Rezeptaufnahme

**Referenz:** 
- [3482118150481†L325-L414]
- [918295637007799†L179-L187]

---

## Implementierungsvorschlag

### UI-Struktur

**Button:** ⚙️ Simulationsparameter

**Modal-Struktur:**
```
📊 Simulationsparameter
├── 🍎 Ernährung & Nährwerte
│   ├── Kalorien & Makronährstoffe
│   ├── Spezialdiäten
│   └── Portionsgrößen
├── 🔄 Vielfalt & Zyklen
│   ├── Menüzykluslänge
│   └── Abwechslungsregeln
├── 💰 Budget & Kosten
│   ├── Rohkostbudget
│   └── Kostenoptimierung
├── 🌱 Nachhaltigkeit
│   ├── Regionalität & Saisonalität
│   ├── Bio-Anteil
│   └── CO₂-Footprint
├── 👥 Zielgruppen
│   ├── Personalisierung
│   └── Spezielle Menülinien
├── ✅ Qualität & Hygiene
│   ├── Nährstoffbegrenzungen
│   └── Lebensmittelsicherheit
└── 📋 Organisation
    ├── Prognose & Planung
    ├── Basis-Menü
    └── Feedback-System
```

### Priorisierung für MVP

**Phase 1 (Sofort):**
1. Ernährung & Nährwerte - Kalorien & Makronährstoffe
2. Vielfalt & Zyklen - Menüzykluslänge
3. Budget & Kosten - Rohkostbudget
4. Qualität & Hygiene - Nährstoffbegrenzungen

**Phase 2 (Kurzfristig):**
5. Nachhaltigkeit - Regionalität & Saisonalität
6. Zielgruppen - Spezielle Menülinien
7. Organisation - Prognose & Planung

**Phase 3 (Mittelfristig):**
8. Ernährung & Nährwerte - Spezialdiäten
9. Qualität & Hygiene - Lebensmittelsicherheit
10. Organisation - Feedback-System

---

## Datenmodell

### Simulation Configuration Object

```javascript
const simulationConfig = {
    // Ernährung & Nährwerte
    nutrition: {
        minCaloriesPerDay: 2000,
        maxCaloriesPerDay: 2500,
        proteinPercentage: 15,
        carbsPercentage: 50,
        fatPercentage: 30,
        portionSize: 400,
        fluidIntakePerDay: 1500
    },
    
    // Spezialdiäten
    specialDiets: {
        diabetic: false,
        highProtein: false,
        lowSodium: false,
        glutenFree: false,
        textureModified: {
            soft: false,
            minced: false,
            pureed: false
        }
    },
    
    // Vielfalt & Zyklen
    variety: {
        cycleLength: 14,
        minRepetitionInterval: 21,
        mealsPerDay: 3,
        dailyRequirements: {
            vegetables: true,
            starch: true,
            fruit: true,
            dairy: true
        },
        maxPer20Days: {
            meat: 8,
            sweetMains: 4,
            fried: 4
        },
        minPer20Days: {
            wholeGrain: 10
        }
    },
    
    // Budget & Kosten
    budget: {
        costPerPersonDay: 8.00,
        tolerance: 15,
        costOptimization: true,
        maxRecipeCost: 5.00
    },
    
    // Nachhaltigkeit
    sustainability: {
        preferSeasonal: true,
        preferRegional: true,
        preferBio: false,
        regionalRadius: 100,
        minBioPercentage: 20,
        minRegionalPercentage: 50,
        maxCO2Footprint: 5.0,
        reducePackaging: true
    },
    
    // Produktions- und Logistik
    production: {
        kitchenModel: 'cook_and_serve',
        maxProductionTime: 120,
        considerStorage: false,
        deliveryWindow: 24
    },
    
    // Zielgruppen
    targetGroups: {
        considerPreferences: true,
        culturalReligious: true,
        feedbackSystem: false,
        minAcceptance: 70,
        childFriendly: false,
        ovoLactoVegetarian: false,
        monitorCriticalNutrients: {
            protein: true,
            omega3: true,
            iodine: true,
            iron: true
        }
    },
    
    // Qualität & Hygiene
    quality: {
        maxSaltPerDay: 6.0,
        maxSugarPerDay: 50.0,
        maxSaturatedFat: 10,
        limitConvenience: true,
        sustainablePalmOil: true,
        excludeRawMilk: true,
        excludeRawEggs: true,
        excludeRawSausage: true,
        excludeRawMeat: true,
        maxWarmHoldingTime: 3,
        minCoolingTime: 2
    },
    
    // Organisation
    organization: {
        expectedGuestsPerDay: 50,
        openDaysPerWeek: 7,
        considerSeasonalFluctuation: true,
        maxWastePercentage: 10,
        baseMenuActive: true,
        baseMenuOptions: ['soup', 'sandwich', 'fruit', 'salad', 'yogurt'],
        minBaseOptions: 3,
        feedbackInterval: 12,
        plateWasteAnalysis: false,
        surveys: false,
        minRecipeRating: 3.0
    }
};
```

---

## Zusammenfassung

Das Dokument identifiziert **7 Hauptkategorien** mit insgesamt **über 60 einzelnen Parametern**, die für eine realistische Menüplansimulation in verschiedenen Einrichtungstypen (Krankenhäuser, Reha, Pflege, Kantinen, Kindergärten) relevant sind.

Die Parameter decken ab:
- ✅ Ernährungsphysiologische Anforderungen
- ✅ Wirtschaftliche Aspekte (Budget, Kosten)
- ✅ Nachhaltigkeit und Regionalität
- ✅ Zielgruppen-spezifische Bedürfnisse
- ✅ Qualitäts- und Hygienestandards
- ✅ Betriebsorganisation und Feedback

Die Integration dieser Parameter ermöglicht die Erstellung von ausgewogenen, nachhaltigen und kostenbewussten Menüplänen, die sowohl ernährungsphysiologische als auch wirtschaftliche und organisatorische Aspekte berücksichtigen.

---

**Autor:** Manus AI Agent  
**Datum:** 22. Oktober 2025  
**Quelle:** Alternative Parameter für Menüplansimulation (PDF)

