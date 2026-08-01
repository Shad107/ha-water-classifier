# Changelog

## [0.2.0] - 2026-08-01

### Added
- **Custom Lovelace card** `water-classifier-card` built in TypeScript + lit-element
  - Displays last session type with colored badge (=color palette per appliance)
  - Live metrics: volume, duration, avg flow
  - Grid of daily counters (=WC, Douche, Bain, Machine, Lave-vaisselle, Robinet, Arrosage, Autre)
  - Top counter highlighted with matching color
  - Responsive layout (=mobile-first)
- `frontend_setup.py` — registers card as Lovelace resource in storage mode dashboards
- `frontend/water-classifier-card.js` — pre-built minified bundle (=~23KB) shipped in the repo
- `frontend_src/` — TypeScript sources + rollup config for building

### Changed
- `__init__.py` — invokes `JSModuleRegistration.async_register` on first entry setup

## [0.1.1] - 2026-08-01

### Added
- Initial release with rule-based cascade classifier
- 8 supported session types
- Feature-based thresholds from WEUSEDTO / REUWS / AutoFlow
- Time-of-day awareness for garden watering detection
- HACS-compatible
- Test suite covering 13 canonical signatures
