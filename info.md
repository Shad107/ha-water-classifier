# Water Pattern Classifier

Home Assistant integration to automatically classify each water usage session into type of appliance (=WC, shower, bath, washing machine, dishwasher, faucet, garden watering, other).

Complementary to [markaggar/Water-Monitor](https://github.com/markaggar/Water-Monitor) which detects sessions but does not classify them.

## Features

- Rule-based cascade classifier based on WEUSEDTO / REUWS / AutoFlow signatures
- Live classification of every water session
- 8 tunable thresholds — adjust from HA UI
- Per-type counters — number of WC flushes, showers, etc. per day
- Time-of-day awareness — differentiates shower from garden watering
- No cloud, no ML training needed

## Configuration

After install, add via **Settings → Devices & Services → + Add Integration → Water Pattern Classifier**.

Several meters? Add the integration once per meter (e.g. city water, well water) and give each its own title: each one becomes a separate device with its own sensors.

## Documentation

See [README](https://github.com/Shad107/ha-water-classifier).
