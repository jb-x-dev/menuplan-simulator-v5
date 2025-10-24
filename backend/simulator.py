"""
Menüplansimulator - Kern-Algorithmus
"""
import json
import math
import random
from datetime import date, timedelta
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict


@dataclass
class Recipe:
    id: int
    name: str
    cost: float
    allergens: List[str]
    dietary_forms: List[str]
    category: str
    group: str
    menu_component: str
    seasonality: List[int]
    popularity: int
    nutritional_values: Dict[str, float]
    is_enabled: bool
    status: str
    calculation_basis: int
    processing_time: float
    ingredients: List[Dict]
    # Optionale neue Felder
    additives: List[str] = None
    aversions: List[str] = None
    description: str = ""
    portion_size: str = "1 Portion"
    
    # NEU: Kategorien für Häufigkeitsbeschränkungen
    contains_meat: bool = False
    is_sweet: bool = False
    is_fried: bool = False
    is_whole_grain: bool = False
    
    # NEU: Qualitätsmerkmale
    contains_raw_milk: bool = False
    contains_raw_eggs: bool = False
    contains_raw_sausage: bool = False
    contains_raw_meat: bool = False
    
    def __post_init__(self):
        # Setze Defaults für optionale Felder
        if self.additives is None:
            self.additives = []
        if self.aversions is None:
            self.aversions = []


@dataclass
class MealSlot:
    """Repräsentiert eine Mahlzeit mit mehreren Rezeptoptionen.
    
    Der Benutzer kann zwischen den Optionen wählen.
    """
    options: List['Recipe']
    selected_index: int = 0
    
    @property
    def selected(self) -> 'Recipe':
        """Gibt das aktuell ausgewählte Rezept zurück."""
        if not self.options or self.selected_index >= len(self.options):
            return None
        return self.options[self.selected_index]
    
    @property
    def cost(self) -> float:
        """Gibt die Kosten des ausgewählten Rezepts zurück."""
        return self.selected.cost if self.selected else 0.0
    
    @property
    def id(self) -> int:
        """Gibt die ID des ausgewählten Rezepts zurück."""
        return self.selected.id if self.selected else 0
    
    @property
    def allergens(self) -> List[str]:
        """Gibt die Allergene des ausgewählten Rezepts zurück."""
        return self.selected.allergens if self.selected else []
    
    def to_dict(self):
        """Konvertiert MealSlot zu Dictionary für JSON-Serialisierung."""
        return {
            'options': [asdict(r) for r in self.options],
            'selected_index': self.selected_index,
            'selected': asdict(self.selected) if self.selected else None
        }


@dataclass
class SimulatorConfig:
    start_date: str
    end_date: str
    menu_lines: List[Dict]
    bkt_target: float
    bkt_tolerance: float
    dietary_forms: List[str]
    excluded_allergens: List[str]
    repetition_interval: int = 7
    consider_seasonality: bool = True
    kitchen_id: int = 1
    excluded_aversions: List[str] = None
    recipe_options_count: int = 2  # Anzahl der Rezeptoptionen pro Mahlzeit
    
    # NEU: Simulationsparameter
    simulation_params: Dict = None
    
    # NEU: Erweiterte Einstellungen
    selected_recipe_groups: List[str] = None
    selected_aversions: List[str] = None
    
    def __post_init__(self):
        if self.excluded_aversions is None:
            self.excluded_aversions = []
        if self.simulation_params is None:
            self.simulation_params = {}
        if self.selected_recipe_groups is None:
            self.selected_recipe_groups = []
        if self.selected_aversions is None:
            self.selected_aversions = []
    
    @property
    def bkt_min(self):
        return self.bkt_target * (1 - self.bkt_tolerance)
    
    @property
    def bkt_max(self):
        return self.bkt_target * (1 + self.bkt_tolerance)
    
    @property
    def start_date_obj(self):
        return date.fromisoformat(self.start_date)
    
    @property
    def end_date_obj(self):
        return date.fromisoformat(self.end_date)


class MenuPlanSimulator:
    def __init__(self, config: SimulatorConfig, recipes: List[Recipe]):
        self.config = config
        self.all_recipes = recipes
        self.eligible_recipes = None
        self.current_plan = None
        self.progress = 0
        
    def generate_plan(self) -> Dict:
        """Hauptmethode zur Generierung eines Menüplans"""
        print("🔍 Phase 1: Filtering recipes...")
        self.progress = 10
        self.eligible_recipes = self._filter_recipes()
        
        print("✅ Phase 2: Checking BKT feasibility...")
        self.progress = 20
        is_feasible, min_bkt, max_bkt = self._check_bkt_feasibility()
        if not is_feasible:
            raise ValueError(
                f"BKT target {self.config.bkt_target:.2f}€ not achievable. "
                f"Range: [{min_bkt:.2f}€, {max_bkt:.2f}€]"
            )
        
        print("🏗️  Phase 3: Constructing initial plan (Greedy)...")
        self.progress = 40
        self.current_plan = self._greedy_construct_plan()
        
        print("🎯 Phase 4: Optimizing plan (Local Search)...")
        self.progress = 70
        
        # NEU: Deaktiviere Local Search wenn Häufigkeitsbeschränkungen oder
        # Wiederholungsabstand aktiv sind (Local Search berücksichtigt diese nicht)
        variety_params = self.config.simulation_params.get('variety', {})
        has_frequency_constraints = (
            variety_params.get('maxMeat', 999) < 999 or
            variety_params.get('maxSweet', 999) < 999 or
            variety_params.get('maxFried', 999) < 999
        )
        has_repetition_constraint = variety_params.get('minRepetition', 21) < 21
        
        if has_frequency_constraints or has_repetition_constraint:
            if has_frequency_constraints:
                print("  ⚠️  Local Search disabled (frequency constraints active)")
            if has_repetition_constraint:
                print("  ⚠️  Local Search disabled (repetition distance active)")
        else:
            self.current_plan = self._local_search_optimize(max_iterations=500)
        
        print("🔍 Phase 5: Validating plan...")
        self.progress = 90
        is_valid, repaired_plan, violations = self._validate_and_repair()
        
        if not is_valid:
            print(f"⚠️  Warning: {len(violations)} constraint violations found")
            for v in violations[:3]:  # Zeige nur erste 3
                print(f"  - {v}")
        
        self.current_plan = repaired_plan
        self.progress = 100
        
        print("✅ Plan generation completed!")
        return self._format_output()
    
    def _filter_recipes(self) -> Dict:
        """Filtert Rezepte basierend auf Hard Constraints"""
        eligible = defaultdict(list)
        
        # NEU: Qualitäts-Parameter holen
        quality_params = self.config.simulation_params.get('quality', {})
        exclude_raw_milk = quality_params.get('excludeRawMilk', True)
        exclude_raw_eggs = quality_params.get('excludeRawEggs', True)
        exclude_raw_sausage = quality_params.get('excludeRawSausage', True)
        exclude_raw_meat = quality_params.get('excludeRawMeat', True)
        
        for recipe in self.all_recipes:
            # Status-Check
            if recipe.status != "Freigegeben" or not recipe.is_enabled:
                continue
            
            # Allergen-Check
            if set(recipe.allergens) & set(self.config.excluded_allergens):
                continue
            
            # Abneigungen-Check
            if set(recipe.aversions) & set(self.config.excluded_aversions):
                continue
            
            # Ernährungsformen-Check
            if not (set(recipe.dietary_forms) & set(self.config.dietary_forms)):
                continue
            
            # NEU: Qualitäts-Checks
            if exclude_raw_milk and recipe.contains_raw_milk:
                continue
            if exclude_raw_eggs and recipe.contains_raw_eggs:
                continue
            if exclude_raw_sausage and recipe.contains_raw_sausage:
                continue
            if exclude_raw_meat and recipe.contains_raw_meat:
                continue
            
            # NEU: Rezeptgruppen-Filter
            if self.config.selected_recipe_groups and recipe.group not in self.config.selected_recipe_groups:
                continue
            
            # NEU: Abneigungen-Filter (zusätzlich zu excluded_aversions)
            if self.config.selected_aversions:
                # Prüfe ob Rezept eine der ausgewählten Abneigungen enthält
                # Abneigungen sind z.B. "Schweinefleisch", "Rindfleisch", etc.
                # Diese müssen mit recipe.aversions abgeglichen werden
                if set(recipe.aversions) & set(self.config.selected_aversions):
                    continue
            
            # Zuordnung zu Menülinien
            for menu_line in self.config.menu_lines:
                for cost_form in menu_line['cost_forms']:
                    if recipe.menu_component == cost_form['component']:
                        key = (menu_line['id'], cost_form['id'])
                        eligible[key].append(recipe)
        
        return eligible
    
    def _check_bkt_feasibility(self) -> Tuple[bool, float, float]:
        """Prüft, ob BKT-Budget erreichbar ist
        
        BKT = Maximale Kosten PRO TAG
        - Einzelne Tage können höher/niedriger sein
        - Durchschnitt über alle Tage muss BKT einhalten (mit Toleranz)
        """
        min_daily = 0.0
        max_daily = 0.0
        
        for menu_line in self.config.menu_lines:
            for cost_form in menu_line['cost_forms']:
                key = (menu_line['id'], cost_form['id'])
                recipes = self.eligible_recipes.get(key, [])
                
                if not recipes:
                    raise ValueError(
                        f"No recipes for {menu_line['name']}/{cost_form['name']}"
                    )
                
                min_daily += min(r.cost for r in recipes)
                max_daily += max(r.cost for r in recipes)
        
        # BKT ist MAXIMUM PRO TAG
        # Wir prüfen ob es möglich ist, unter dem BKT zu bleiben
        # Einzelne Tage können abweichen, Durchschnitt muss unter BKT liegen
        is_feasible = (min_daily <= self.config.bkt_max)
        
        return is_feasible, min_daily, max_daily
    
    def _greedy_construct_plan(self) -> Dict:
        """Konstruiert initialen Plan mit Greedy-Heuristik"""
        plan = {}
        used_recipes = defaultdict(list)
        
        # NEU: Häufigkeits-Zähler für Kategorien
        category_counts = {
            'meat': 0,
            'sweet': 0,
            'fried': 0
        }
        
        # NEU: Limits aus Parametern holen
        variety_params = self.config.simulation_params.get('variety', {})
        max_meat = variety_params.get('maxMeat', 999)
        max_sweet = variety_params.get('maxSweet', 999)
        max_fried = variety_params.get('maxFried', 999)
        min_repetition = variety_params.get('minRepetition', 7)
        
        current_date = self.config.start_date_obj
        total_days = (self.config.end_date_obj - current_date).days + 1
        day_count = 0
        
        while current_date <= self.config.end_date_obj:
            daily_cost = 0.0
            
            for menu_line in self.config.menu_lines:
                for cost_form in menu_line['cost_forms']:
                    key = (menu_line['id'], cost_form['id'])
                    candidates = self.eligible_recipes[key]
                    
                    # NEU: Filtere Rezepte die Häufigkeitslimits überschreiten würden
                    available_candidates = []
                    soft_constraint_candidates = []  # Kandidaten mit kleiner Überschreitung
                    
                    for recipe in candidates:
                        # Prüfe Häufigkeitslimits (Hard Constraints)
                        violates_hard = False
                        violates_soft = False
                        
                        # Erlaubt eine kleine Überschreitung (+2) als Soft Constraint
                        if recipe.contains_meat:
                            if category_counts['meat'] >= max_meat + 2:
                                violates_hard = True
                            elif category_counts['meat'] >= max_meat:
                                violates_soft = True
                        
                        if recipe.is_sweet:
                            if category_counts['sweet'] >= max_sweet + 2:
                                violates_hard = True
                            elif category_counts['sweet'] >= max_sweet:
                                violates_soft = True
                        
                        if recipe.is_fried:
                            if category_counts['fried'] >= max_fried + 2:
                                violates_hard = True
                            elif category_counts['fried'] >= max_fried:
                                violates_soft = True
                        
                        if violates_hard:
                            continue
                        
                        # Prüfe Wiederholungsabstand
                        if recipe.id in used_recipes:
                            last_used_dates = used_recipes[recipe.id]
                            if last_used_dates:
                                days_since_last_use = (current_date - max(last_used_dates)).days
                                if days_since_last_use < min_repetition:
                                    continue
                        
                        if violates_soft:
                            soft_constraint_candidates.append(recipe)
                        else:
                            available_candidates.append(recipe)
                    
                    # Fallback-Strategie:
                    # 1. Bevorzuge Kandidaten ohne Constraint-Verletzung
                    # 2. Falls keine: Verwende Kandidaten mit Soft-Constraint-Verletzung
                    # 3. Falls keine: Verwende alle Kandidaten (letzter Ausweg)
                    if not available_candidates:
                        if soft_constraint_candidates:
                            available_candidates = soft_constraint_candidates
                        else:
                            available_candidates = candidates
                    
                    # Score berechnen
                    scored = [
                        (self._calculate_score(r, current_date, plan, 
                                              used_recipes, daily_cost), r)
                        for r in available_candidates
                    ]
                    scored.sort(reverse=True, key=lambda x: x[0])
                    
                    # Die besten N verfügbaren Rezepte wählen (N = recipe_options_count)
                    options = []
                    for score, recipe in scored:
                        if len(options) < self.config.recipe_options_count:
                            if self._is_repetition_allowed(recipe, current_date, 
                                                           used_recipes):
                                options.append(recipe)
                    
                    # Fallback: Wenn weniger als N gefunden, fülle mit den besten auf
                    if len(options) < self.config.recipe_options_count and len(scored) > 0:
                        for score, recipe in scored:
                            if recipe not in options and len(options) < self.config.recipe_options_count:
                                options.append(recipe)
                    
                    # Mindestens 1 Rezept muss vorhanden sein
                    if not options:
                        options = [scored[0][1]]  # Absoluter Fallback
                    
                    # Wähle das günstigste Rezept als Standard aus
                    cheaper_index = 0
                    min_cost = options[0].cost
                    for i, opt in enumerate(options):
                        if opt.cost < min_cost:
                            min_cost = opt.cost
                            cheaper_index = i
                    
                    # MealSlot erstellen (standardmäßig ist das günstigere Rezept ausgewählt)
                    meal_slot = MealSlot(options=options, selected_index=cheaper_index)
                    
                    # Speichern
                    plan_key = (current_date, menu_line['id'], cost_form['id'])
                    plan[plan_key] = meal_slot
                    used_recipes[meal_slot.selected.id].append(current_date)
                    daily_cost += meal_slot.cost
                    
                    # NEU: Aktualisiere Häufigkeits-Zähler
                    selected_recipe = meal_slot.selected
                    if selected_recipe.contains_meat:
                        category_counts['meat'] += 1
                    if selected_recipe.is_sweet:
                        category_counts['sweet'] += 1
                    if selected_recipe.is_fried:
                        category_counts['fried'] += 1
            
            current_date += timedelta(days=1)
            day_count += 1
            
            # Progress Update
            self.progress = 40 + int((day_count / total_days) * 30)
        
        return plan
    
    def _calculate_score(self, recipe, date, plan, used_recipes, 
                        current_daily_cost) -> float:
        """Berechnet Score für ein Rezept"""
        score = 0.0
        
        # BKT-Konformität (35%)
        # BKT = MAXIMUM PRO TAG (nicht Ziel)
        # Bevorzuge günstigere Rezepte, aber vermeide Überschreitung
        projected_cost = current_daily_cost + recipe.cost
        
        # Prüfe ob wir das Maximum überschreiten
        if projected_cost > self.config.bkt_max:
            bkt_score = 0.0  # Überschreitet Maximum
        else:
            # Je günstiger, desto besser (aber nicht zu billig)
            # Optimal ist 70-90% des BKT-Targets
            cost_ratio = projected_cost / self.config.bkt_target
            if cost_ratio < 0.5:
                bkt_score = 0.7  # Zu billig
            elif cost_ratio <= 0.9:
                bkt_score = 1.0  # Optimal
            else:
                bkt_score = 1.0 - (cost_ratio - 0.9) / 0.2  # Akzeptabel bis Maximum
        score += 0.35 * max(0, bkt_score)
        
        # Vielfalt (25%)
        usage_count = len(used_recipes.get(recipe.id, []))
        variety_score = 1.0 / (1.0 + usage_count)
        
        # Ähnlichkeit zu kürzlich verwendeten Rezepten
        recent_similarity = 0.0
        lookback_days = min(7, len([d for d in plan.keys() if d[0] < date]))
        if lookback_days > 0:
            recent_dates = [date - timedelta(days=i) for i in range(1, lookback_days + 1)]
            similarity_count = 0
            for recent_date in recent_dates:
                for key, meal_slot in plan.items():
                    if key[0] == recent_date:
                        # Verwende das ausgewählte Rezept aus dem MealSlot
                        used_recipe = meal_slot.selected if hasattr(meal_slot, 'selected') else meal_slot
                        similarity = self._calculate_similarity(recipe, used_recipe)
                        recent_similarity += similarity
                        similarity_count += 1
            if similarity_count > 0:
                recent_similarity /= similarity_count
        
        variety_score *= (1.0 - recent_similarity)
        score += 0.25 * variety_score
        
        # Beliebtheit (15%)
        popularity_score = recipe.popularity / 10.0
        score += 0.15 * popularity_score
        
        # Saisonalität (15%)
        if self.config.consider_seasonality:
            seasonality_score = 1.0 if date.month in recipe.seasonality else 0.0
            score += 0.15 * seasonality_score
        else:
            score += 0.15 * 0.5  # Neutral
        
        # Nährwerte (10%) - vereinfacht
        target_calories = 600
        calorie_deviation = abs(recipe.nutritional_values.get('calories', 600) - target_calories)
        nutrition_score = 1.0 - min(1.0, calorie_deviation / target_calories)
        score += 0.10 * nutrition_score
        
        return score
    
    def _calculate_similarity(self, recipe1, recipe2) -> float:
        """Berechnet Ähnlichkeit zwischen zwei Rezepten"""
        if recipe1.id == recipe2.id:
            return 1.0
        
        similarity = 0.0
        
        # Gleiche Gruppe?
        if recipe1.group == recipe2.group:
            similarity += 0.5
        
        # Gleiche Kategorie?
        if recipe1.category == recipe2.category:
            similarity += 0.3
        
        # Ähnliche Allergene?
        allergens1 = set(recipe1.allergens)
        allergens2 = set(recipe2.allergens)
        if allergens1 or allergens2:
            jaccard = len(allergens1 & allergens2) / len(allergens1 | allergens2) if (allergens1 | allergens2) else 0
            similarity += 0.2 * jaccard
        
        return min(1.0, similarity)
    
    def _is_repetition_allowed(self, recipe, date, used_recipes) -> bool:
        """Prüft Wiederholungsintervall"""
        if recipe.id not in used_recipes:
            return True
        
        for last_date in used_recipes[recipe.id]:
            days_since = (date - last_date).days
            if days_since < self.config.repetition_interval:
                return False
        
        return True
    
    def _local_search_optimize(self, max_iterations=500) -> Dict:
        """Optimiert Plan durch Local Search"""
        current_plan = self.current_plan.copy()
        current_cost = self._evaluate_plan(current_plan)
        
        best_plan = current_plan.copy()
        best_cost = current_cost
        
        improvements = 0
        
        for iteration in range(max_iterations):
            # Erzeuge Nachbarn
            neighbor = self._generate_neighbor(current_plan)
            neighbor_cost = self._evaluate_plan(neighbor)
            
            # Akzeptiere Verbesserungen
            if neighbor_cost < current_cost:
                current_plan = neighbor
                current_cost = neighbor_cost
                improvements += 1
                
                if current_cost < best_cost:
                    best_plan = current_plan.copy()
                    best_cost = current_cost
            
            # Progress Update
            if iteration % 50 == 0:
                self.progress = 70 + int((iteration / max_iterations) * 20)
        
        print(f"  ✓ Found {improvements} improvements")
        return best_plan
    
    def _evaluate_plan(self, plan) -> float:
        """Bewertet Plan (niedriger = besser)"""
        dates = set(key[0] for key in plan.keys())
        total_bkt_dev = 0.0
        
        for d in dates:
            daily_cost = sum(
                meal_slot.cost for (date, ml, cf), meal_slot in plan.items() 
                if date == d
            )
            # Penalisiere Überschreitung des Maximums stärker
            if daily_cost > self.config.bkt_max:
                total_bkt_dev += (daily_cost - self.config.bkt_max) * 3.0  # 3x Penalty
            else:
                # Bevorzuge Kosten nahe am Ziel (aber unter Maximum)
                total_bkt_dev += abs(daily_cost - self.config.bkt_target * 0.8)
        
        avg_bkt_dev = total_bkt_dev / len(dates) if dates else 0
        
        # Vielfalt-Penalty
        recipe_counts = defaultdict(int)
        for meal_slot in plan.values():
            recipe_counts[meal_slot.id] += 1
        
        variety_penalty = sum(count ** 2 for count in recipe_counts.values()) / len(plan)
        
        return avg_bkt_dev + 0.1 * variety_penalty
    
    def _generate_neighbor(self, plan) -> Dict:
        """Erzeugt Nachbarplan durch zufällige Änderung"""
        neighbor = plan.copy()
        
        # Zufällige Position wählen
        keys = list(plan.keys())
        random_key = random.choice(keys)
        
        # Alternatives Rezept wählen
        date, ml, cf = random_key
        candidates = self.eligible_recipes[(ml, cf)]
        
        current_slot = plan[random_key]
        
        # Strategie 1 (50%): Wechsle selected_index innerhalb der vorhandenen Optionen
        if len(current_slot.options) > 1 and random.random() < 0.5:
            new_index = 1 - current_slot.selected_index  # Toggle zwischen 0 und 1
            new_slot = MealSlot(
                options=current_slot.options,
                selected_index=new_index
            )
            neighbor[random_key] = new_slot
        else:
            # Strategie 2 (50%): Ersetze die gesamte MealSlot mit neuen Optionen
            alternatives = [r for r in candidates if r.id != current_slot.id]
            
            if alternatives:
                # Wähle 2 neue Rezepte
                new_options = random.sample(alternatives, min(2, len(alternatives)))
                new_slot = MealSlot(options=new_options, selected_index=0)
                neighbor[random_key] = new_slot
        
        return neighbor
    
    def _validate_and_repair(self) -> Tuple[bool, Dict, List[str]]:
        """Validiert Plan"""
        violations = []
        
        # Vollständigkeitsprüfung
        expected_entries = (
            (self.config.end_date_obj - self.config.start_date_obj).days + 1
        ) * sum(
            len(ml['cost_forms']) for ml in self.config.menu_lines
        )
        
        if len(self.current_plan) != expected_entries:
            violations.append(f"Incomplete plan: {len(self.current_plan)}/{expected_entries}")
        
        # BKT-Prüfung
        dates = set(key[0] for key in self.current_plan.keys())
        total_bkt = sum(
            sum(recipe.cost for (d, ml, cf), recipe in self.current_plan.items() if d == date)
            for date in dates
        )
        avg_bkt = total_bkt / len(dates) if dates else 0
        
        if avg_bkt < self.config.bkt_min or avg_bkt > self.config.bkt_max:
            violations.append(
                f"BKT {avg_bkt:.2f}€ outside [{self.config.bkt_min:.2f}€, {self.config.bkt_max:.2f}€]"
            )
        
        is_valid = len(violations) == 0
        
        return is_valid, self.current_plan, violations
    
    def _format_output(self) -> Dict:
        """Formatiert Plan für Ausgabe"""
        days = []
        
        current_date = self.config.start_date_obj
        while current_date <= self.config.end_date_obj:
            day_data = {
                'date': current_date.isoformat(),
                'day_of_week': current_date.strftime('%A'),
                'total_cost': 0.0,  # Gesamtkosten pro Tag
                'menu_lines': []
            }
            
            for menu_line in self.config.menu_lines:
                ml_data = {
                    'name': menu_line['name'],
                    'recipes': []
                }
                
                for cost_form in menu_line['cost_forms']:
                    key = (current_date, menu_line['id'], cost_form['id'])
                    meal_slot = self.current_plan.get(key)
                    
                    if meal_slot:
                        # Konvertiere MealSlot zu Dictionary mit allen Optionen
                        meal_data = {
                            'options': [
                                {
                                    'recipe_id': opt.id,
                                    'recipe_name': opt.name,
                                    'cost_per_serving': opt.cost,
                                    'allergens': opt.allergens,
                                    'dietary_forms': opt.dietary_forms,
                                    'popularity': opt.popularity,
                                    'additives': opt.additives,
                                    'ingredients': opt.ingredients,
                                    'description': opt.description,
                                    'group': opt.group,
                                    'category': opt.category
                                }
                                for opt in meal_slot.options
                            ],
                            'selected_index': meal_slot.selected_index,
                            'is_user_modified': False
                        }
                        
                        ml_data['recipes'].append(meal_data)
                        day_data['total_cost'] += meal_slot.cost
                
                day_data['menu_lines'].append(ml_data)
            
            days.append(day_data)
            current_date += timedelta(days=1)
        
        # Statistiken
        # BKT = Maximale Kosten PRO TAG
        # Durchschnitt muss im Toleranzbereich liegen
        total_cost = sum(day['total_cost'] for day in days)
        avg_daily_cost = total_cost / len(days) if days else 0
        
        return {
            'days': days,
            'statistics': {
                'total_days': len(days),
                'average_bkt': round(avg_daily_cost, 2),  # Durchschnitt pro Tag
                'total_cost': round(total_cost, 2),  # Gesamtkosten über alle Tage
                'bkt_target': self.config.bkt_target,  # Maximum pro Tag
                'bkt_min': round(self.config.bkt_min, 2),
                'bkt_max': round(self.config.bkt_max, 2),
                'within_budget': avg_daily_cost <= self.config.bkt_max  # Durchschnitt unter Maximum
            }
        }


def load_recipes_from_file(filepath: str) -> List[Recipe]:
    """Lädt Rezepte aus JSON-Datei"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return [Recipe(**recipe) for recipe in data]


def run_simulation(config_dict: Dict, recipes: List[Recipe]) -> Dict:
    """Führt Simulation aus"""
    config = SimulatorConfig(**config_dict)
    simulator = MenuPlanSimulator(config, recipes)
    return simulator.generate_plan()

