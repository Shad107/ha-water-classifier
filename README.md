# 💧 Water Pattern Classifier

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![hass](https://img.shields.io/badge/HA-2024.1+-blue.svg)](https://www.home-assistant.io)

**Home Assistant integration to automatically classify each water usage session into type of appliance** (=WC, shower, bath, washing machine, dishwasher, faucet, garden watering, other).

Complementary to [markaggar/Water-Monitor](https://github.com/markaggar/Water-Monitor) which detects sessions but does not classify them.

## 🎯 Features

- ✅ **Rule-based cascade classifier** based on WEUSEDTO / REUWS / AutoFlow signatures
- ✅ **Live classification** of every water session (=via Water-Monitor sensors)
- ✅ **8 tunable thresholds** — adjust from HA UI to fit your household
- ✅ **Per-type counters** — number of WC flushes, showers, etc. per day
- ✅ **Time-of-day awareness** — differentiates shower from morning/evening garden watering
- ✅ **No cloud, no ML training needed** — pure Python, runs on your HA instance
- 🔜 **Optional ML upgrade** (=roadmap v0.2)

## 📊 Classification cascade

The classifier applies rules in this order (=most specific first) :

| Order | Type | Conditions |
|---|---|---|
| 1 | **Machine à laver** | duration > 30 min AND volume > 30 L |
| 2 | **Lave-vaisselle** | duration > 30 min AND volume < 30 L |
| 3 | **Bain** | volume > 100 L AND duration > 3 min |
| 4 | **Arrosage** | volume > 50 L AND avg_flow > 8 L/min AND hour ∈ [18-8] |
| 5 | **Douche** | duration > 3 min AND volume > 25 L AND avg_flow > 4 L/min |
| 6 | **WC** | 4 ≤ volume ≤ 9 L AND duration < 2 min AND peak > 4 L/min |
| 7 | **Robinet/Lavabo** | volume < 3 L AND duration < 60 s |
| 8 | **Autre** | fallback |

## 🚀 Installation

### Via HACS (recommended, once accepted in default repo)

1. HACS → Integrations → Custom repositories
2. Add `https://github.com/Shad107/ha-water-classifier` as Integration
3. Install "Water Pattern Classifier"
4. Restart Home Assistant

### Manual

Copy `custom_components/water_classifier/` to your HA `/config/custom_components/` and restart.

## ⚙️ Configuration

1. **Settings → Devices & Services → + Add Integration → Water Pattern Classifier**
2. Select :
   - `flow_sensor` : your L/min flow rate sensor (=e.g. `sensor.debitmetre_eau_debit_eau`)
   - `session_volume_sensor` : Water-Monitor last session volume (=e.g. `sensor.eau_maison_last_session_volume`)
   - `session_duration_sensor` : Water-Monitor last session duration
   - `session_flow_sensor` : Water-Monitor last session average flow

## 📖 Data sources

Thresholds are derived from :

- **WEUSEDTO** (=Water End USE Dataset and TOols) — https://github.com/Water-End-Use-Dataset-Tools/WEUSEDTO
- **REUWS** (=Residential End Uses of Water Study, DeOreo 2016)
- **AutoFlow v3.1** (=Nguyen 2015, F1 86-96%)
- French Geberit / plumbing specs

## 🗺️ Roadmap

- v0.1 — Rule-based cascade classifier ← **current**
- v0.2 — Feedback loop : manual label correction via HA `input_select`
- v0.3 — ML upgrade : Random Forest trained on collected labels (=uses [scikit-learn](https://scikit-learn.org))
- v0.4 — Dockerized companion service for advanced ML (=optional LXC deployment)

## 🤝 Contributing

PRs welcome ! See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT — see [LICENSE](LICENSE).
