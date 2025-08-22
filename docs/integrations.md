# Integration Setup

External services such as Stripe, SendGrid and Twilio are configured via
environment variables in `.env`. The sample `makerworks/infra/.env.example`
contains placeholders for all supported providers.

For development without credentials, stub values are accepted and the
application will operate in a no-op mode.
