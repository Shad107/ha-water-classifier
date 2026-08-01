import resolve from '@rollup/plugin-node-resolve';
import typescript from '@rollup/plugin-typescript';
import terser from '@rollup/plugin-terser';

export default {
  input: 'src/water-classifier-card.ts',
  output: {
    file: '../custom_components/water_classifier/frontend/water-classifier-card.js',
    format: 'iife',
    name: 'WaterClassifierCard',
    sourcemap: false
  },
  plugins: [
    resolve(),
    typescript({ tsconfig: './tsconfig.json' }),
    terser()
  ]
};
