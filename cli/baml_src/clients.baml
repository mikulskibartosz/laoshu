client<llm> Model {
  provider openai
  retry_policy Exponential
  options {
    model "gpt-4o"
    api_key env.OPENAI_API_KEY
  }
}

retry_policy Exponential {
  max_retries 2
  strategy {
    type exponential_backoff
    delay_ms 300
    multiplier 1.5
    max_delay_ms 10000
  }
}