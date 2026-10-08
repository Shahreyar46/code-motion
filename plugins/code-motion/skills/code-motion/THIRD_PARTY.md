# Third-party assets

- Fonts in `engine/fonts/` are licensed under the SIL Open Font License 1.1 (licence texts alongside):
  Geist and Geist Mono (Vercel), Anton (Vernon Adams), Caveat (Impallari Type), Instrument Serif (Instrument).
- Icon paths in `engine/motion.js` (`M.IC`) follow Lucide (ISC licence, https://lucide.dev).
- Runtime dependencies installed by `scripts/setup.sh` into the user's work folder, not bundled: Playwright (Apache-2.0), Three.js (MIT), numpy (BSD), edge-tts (LGPL-3.0).
- No API keys, voices or audio samples are bundled. Premium TTS (Gemini, ElevenLabs) uses the user's own key from their environment; all sound effects are synthesised in code.
