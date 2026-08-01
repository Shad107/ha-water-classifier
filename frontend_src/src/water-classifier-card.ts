import { LitElement, html, css, type PropertyValues, type TemplateResult } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

interface HomeAssistant {
  states: Record<string, HassEntity>;
  callService: (domain: string, service: string, data?: object) => Promise<void>;
}

interface HassEntity {
  state: string;
  attributes: Record<string, unknown>;
}

interface CardConfig {
  type: string;
  entity_type: string;
  entity_volume?: string;
  entity_duration?: string;
  entity_flow?: string;
  title?: string;
  counter_prefix?: string;
  show_timeline?: boolean;
}

const TYPE_META: Record<string, { color: string; icon: string; label: string }> = {
  'WC':               { color: '#4A90E2', icon: '🚽', label: 'WC' },
  'Douche':           { color: '#50C878', icon: '🚿', label: 'Douche' },
  'Bain':             { color: '#00CED1', icon: '🛁', label: 'Bain' },
  'Machine à laver':  { color: '#FF8C00', icon: '🌀', label: 'Machine' },
  'Lave-vaisselle':   { color: '#FFB6C1', icon: '🍽', label: 'Lave-V.' },
  'Robinet/Lavabo':   { color: '#9370DB', icon: '💧', label: 'Robinet' },
  'Arrosage':         { color: '#8B4513', icon: '🌱', label: 'Arrosage' },
  'Autre':            { color: '#808080', icon: '❓', label: 'Autre' },
  'Inconnu':          { color: '#D3D3D3', icon: '⏸', label: 'Inconnu' }
};

const COUNTER_KEYS = ['wc', 'douche', 'bain', 'machine', 'lave_vaisselle', 'robinet', 'arrosage', 'autre'];
const COUNTER_TO_TYPE: Record<string, string> = {
  wc: 'WC',
  douche: 'Douche',
  bain: 'Bain',
  machine: 'Machine à laver',
  lave_vaisselle: 'Lave-vaisselle',
  robinet: 'Robinet/Lavabo',
  arrosage: 'Arrosage',
  autre: 'Autre'
};

@customElement('water-classifier-card')
export class WaterClassifierCard extends LitElement {
  @property({ attribute: false }) hass?: HomeAssistant;
  @state() private _config?: CardConfig;

  static styles = css`
    :host {
      display: block;
    }
    ha-card {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .header {
      font-weight: 500;
      font-size: 1.1em;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .last-session {
      padding: 12px;
      border-radius: 8px;
      color: white;
      display: flex;
      flex-direction: column;
      gap: 4px;
      transition: background-color 300ms ease;
    }
    .type-badge {
      font-size: 1.4em;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .metrics {
      display: flex;
      gap: 16px;
      opacity: 0.95;
      font-size: 0.9em;
    }
    .metrics div {
      display: flex;
      flex-direction: column;
    }
    .metrics span {
      font-size: 0.75em;
      opacity: 0.85;
    }
    .metrics strong {
      font-size: 1em;
    }
    .section-label {
      font-size: 0.85em;
      opacity: 0.7;
      margin-top: 4px;
    }
    .counters {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }
    .counter {
      background: var(--card-background-color, #fff);
      border: 1px solid var(--divider-color, #e0e0e0);
      border-radius: 6px;
      padding: 8px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: transform 150ms ease, box-shadow 150ms ease;
    }
    .counter.top {
      transform: scale(1.05);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    .counter .icon {
      font-size: 1.4em;
    }
    .counter .count {
      font-weight: 600;
      font-size: 1.1em;
    }
    .counter .name {
      font-size: 0.7em;
      opacity: 0.7;
    }
    @media (max-width: 480px) {
      .counters {
        grid-template-columns: repeat(2, 1fr);
      }
      .metrics {
        flex-wrap: wrap;
      }
    }
  `;

  setConfig(config: CardConfig): void {
    if (!config?.entity_type) {
      throw new Error('entity_type is required');
    }
    this._config = { show_timeline: true, counter_prefix: 'counter.water_count_', ...config };
  }

  getCardSize(): number {
    return 4;
  }

  private _renderLastSession(): TemplateResult {
    if (!this.hass || !this._config) return html``;
    const typeState = this.hass.states[this._config.entity_type];
    const type = typeState?.state || 'Inconnu';
    const meta = TYPE_META[type] ?? TYPE_META.Inconnu;

    const volumeS = this._config.entity_volume ? this.hass.states[this._config.entity_volume] : undefined;
    const durationS = this._config.entity_duration ? this.hass.states[this._config.entity_duration] : undefined;
    const flowS = this._config.entity_flow ? this.hass.states[this._config.entity_flow] : undefined;

    const volume = volumeS ? parseFloat(volumeS.state) : NaN;
    const duration = durationS ? parseFloat(durationS.state) : NaN;
    const flow = flowS ? parseFloat(flowS.state) : NaN;

    return html`
      <div class="last-session" style="background-color: ${meta.color}">
        <div class="type-badge">
          <span>${meta.icon}</span>
          <span>${meta.label}</span>
        </div>
        <div class="metrics">
          <div>
            <span>Volume</span>
            <strong>${isNaN(volume) ? '—' : volume.toFixed(1) + ' L'}</strong>
          </div>
          <div>
            <span>Durée</span>
            <strong>${isNaN(duration) ? '—' : this._formatDuration(duration)}</strong>
          </div>
          <div>
            <span>Débit</span>
            <strong>${isNaN(flow) ? '—' : flow.toFixed(1) + ' L/min'}</strong>
          </div>
        </div>
      </div>
    `;
  }

  private _formatDuration(seconds: number): string {
    if (seconds < 60) return `${Math.round(seconds)} s`;
    const m = Math.floor(seconds / 60);
    const s = Math.round(seconds % 60);
    if (m < 60) return `${m} min ${s.toString().padStart(2, '0')} s`;
    const h = Math.floor(m / 60);
    return `${h}h ${(m % 60).toString().padStart(2, '0')} min`;
  }

  private _renderCounters(): TemplateResult {
    if (!this.hass || !this._config) return html``;
    const prefix = this._config.counter_prefix || 'counter.water_count_';
    const values: { key: string; count: number }[] = COUNTER_KEYS.map((k) => {
      const eid = `${prefix}${k}_today`;
      const s = this.hass!.states[eid];
      return { key: k, count: s ? parseInt(s.state, 10) : 0 };
    });
    const maxCount = Math.max(...values.map((v) => v.count));
    return html`
      <div class="section-label">Aujourd'hui</div>
      <div class="counters">
        ${values.map((v) => {
          const type = COUNTER_TO_TYPE[v.key];
          const meta = TYPE_META[type];
          const isTop = maxCount > 0 && v.count === maxCount;
          return html`
            <div
              class="counter ${isTop ? 'top' : ''}"
              style="${isTop ? `background-color: ${meta.color}22; border-color: ${meta.color}` : ''}"
              title="${meta.label}"
            >
              <span class="icon">${meta.icon}</span>
              <span class="count" style="color: ${isTop ? meta.color : ''}">${v.count}</span>
              <span class="name">${meta.label}</span>
            </div>
          `;
        })}
      </div>
    `;
  }

  render(): TemplateResult {
    if (!this._config || !this.hass) {
      return html`<ha-card><div>Config missing</div></ha-card>`;
    }
    const title = this._config.title || '💧 Water Classifier';
    return html`
      <ha-card>
        <div class="header">${title}</div>
        ${this._renderLastSession()}
        ${this._renderCounters()}
      </ha-card>
    `;
  }

  static getStubConfig(): CardConfig {
    return {
      type: 'custom:water-classifier-card',
      entity_type: 'sensor.last_session_type',
      entity_volume: 'sensor.eau_maison_last_session_volume',
      entity_duration: 'sensor.eau_maison_last_session_duration',
      entity_flow: 'sensor.eau_maison_last_session_average_flow'
    };
  }
}

declare global {
  interface Window {
    customCards?: Array<{
      type: string;
      name: string;
      description: string;
      preview?: boolean;
    }>;
  }
  interface HTMLElementTagNameMap {
    'water-classifier-card': WaterClassifierCard;
  }
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'water-classifier-card',
  name: 'Water Classifier Card',
  description: 'Displays live water session classification and daily counters.',
  preview: false
});

console.info(
  '%c WATER-CLASSIFIER-CARD %c v0.2.0 ',
  'color: white; background: #50C878; font-weight: 700;',
  'color: #50C878; background: transparent; font-weight: 700;'
);
