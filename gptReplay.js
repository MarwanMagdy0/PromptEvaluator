module.exports = class GptReplayProvider {
  constructor(options) {
    this.providerId = options.id || 'gpt-replay';
  }

  id() {
    return this.providerId;
  }

  async callApi(prompt, context) {
    return {
      output: context.vars.gpt_output || '',
    };
  }
};