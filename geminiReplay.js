module.exports = class GeminiReplayProvider {
  constructor(options) {
    this.providerId = options.id || 'gemini-replay';
  }

  id() {
    return this.providerId;
  }

  async callApi(prompt, context) {
    return {
      output: context.vars.gemini_output || '',
    };
  }
};