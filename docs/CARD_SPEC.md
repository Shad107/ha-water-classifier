# Water Classifier Card — Cahier des charges v0.2

## Objectif

Custom lit-element Lovelace card pour visualiser en un coup d'œil la classification des sessions d'eau, avec compteurs journaliers colorés par type, dernière session en highlight, et micro-timeline.

## Positionnement

- **Format** : card unique (=~4 unités de hauteur, largeur pleine colonne)
- **Emplacement** : à insérer dans l'onglet Eau après la section "Détection de sessions"
- **Style** : cohérent avec Material Design HA (=variables CSS `--primary-color`, `--card-background-color`, etc.)

## Layout visuel

```
┌─────────────────────────────────────────────────┐
│ 💧 Water Classifier                             │
├─────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────┐   │
│  │ 🚿 DOUCHE                                │   │
│  │ 58.3 L · 7 min 45 s · 7.5 L/min          │   │
│  │ ●●●●●●○○○ (=confidence badge)             │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  Aujourd'hui                                    │
│  🚽 3   🚿 2   🛁 0   🌀 1   🍽 0             │
│  💧 5   🌱 0   ❓ 1                            │
│                                                 │
│  Micro-timeline 24h (=bar par session colorée)  │
│  ▂▂▁ ▁▂ █▂ ▂▁ ▁ ▂ ▁ ▂                        │
└─────────────────────────────────────────────────┘
```

## Composants UI

### 1. Header
- Icône 💧 + titre "Water Classifier" (=configurable via `title:`)

### 2. Bloc "Dernière session"
- Type courant en badge coloré (=chaque type sa couleur, cf. palette ci-dessous)
- 3 métriques : volume L, durée mm:ss, débit moyen L/min
- Bar horizontale des dernières valeurs vs typical range (=optionnel v0.3)

### 3. Grille compteurs journaliers
- 8 tuiles : WC, Douche, Bain, Machine, Lave-vaisselle, Robinet, Arrosage, Autre
- Chaque tuile : icône + nombre du jour
- Tuile ayant le plus haut count : mise en avant (=fond coloré)

### 4. Micro-timeline
- Barres verticales dernières 24h, hauteur = volume, couleur = type
- Cliquable → highlight card avec détails de la session
- Utilise historique des sessions Water-Monitor

## Palette couleurs par type

| Type | Couleur | Icône |
|---|---|---|
| WC | `#4A90E2` (=bleu ciel) | mdi:toilet |
| Douche | `#50C878` (=vert émeraude) | mdi:shower |
| Bain | `#00CED1` (=turquoise) | mdi:bathtub |
| Machine à laver | `#FF8C00` (=orange) | mdi:washing-machine |
| Lave-vaisselle | `#FFB6C1` (=rose) | mdi:dishwasher |
| Robinet/Lavabo | `#9370DB` (=violet) | mdi:faucet |
| Arrosage | `#8B4513` (=marron) | mdi:sprinkler |
| Autre | `#808080` (=gris) | mdi:water-alert |
| Inconnu | `#D3D3D3` (=gris clair) | mdi:help-circle |

## Configuration YAML

```yaml
type: custom:water-classifier-card
entity_type: sensor.last_session_type
entity_volume: sensor.eau_maison_last_session_volume
entity_duration: sensor.eau_maison_last_session_duration
entity_flow: sensor.eau_maison_last_session_average_flow
title: "💧 Water Classifier"           # optional
show_timeline: true                    # optional, default true
counter_prefix: counter.water_count_   # optional, prefix pour les 8 compteurs
```

## Architecture technique

### Stack
- **Langage** : TypeScript
- **Framework** : lit-element 3.x (=standard HA cards)
- **Build** : rollup avec plugins TS + terser
- **Output** : `dist/water-classifier-card.js` (=IIFE minified, ~15-25KB gzipped)
- **Tests** : @open-wc/testing pour unit tests

### Intégration HA Python
- `frontend/water-classifier-card.js` (=fichier compilé livré)
- `frontend_setup.py` : enregistrement de la card comme `/water_classifier/water-classifier-card.js` via HA URL
- `__init__.py` : appel `async_register_static_paths` + `async_add_extra_js_url`

### Files structure

```
custom_components/water_classifier/
├── frontend/
│   └── water-classifier-card.js    ← compilé, versionné dans le repo
├── frontend_setup.py                ← enregistrement HA
├── __init__.py                      ← import frontend_setup + call
└── (autres fichiers existants...)

frontend_src/
├── package.json
├── tsconfig.json
├── rollup.config.js
└── src/
    └── water-classifier-card.ts     ← code source card
```

## Roadmap

- **v0.2.0** ← cette itération : layout de base fonctionnel (=header + last session + counters + palette couleurs)
- v0.2.1 : micro-timeline 24h + click session
- v0.2.2 : édition inline seuils via card editor
- v0.3.0 : intégration ML self-learning basé feedback utilisateur

## Non-goals (=hors périmètre v0.2)

- Édition inline des seuils (=v0.2.2)
- Graph historique long terme (=utiliser statistics-graph existant)
- Configuration flow via card_editor (=YAML only pour v0.2.0)
- Feedback correction manuel (=v0.3)
