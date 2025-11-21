# anarchkey-client (Node)

Port of the original Python `AnarchKeyClient` to Node.js — includes both a programmatic client and a CLI.

## Install

```bash
npm install anarchkey-client -g
```

## CLI

Initialize the local token (writes `~/.anarchkey` with 0o600 permissions):

```bash
anarchkey init --username YourName --password YourPassword
```

Options:
- `--base-url` Base URL of the service (default: `https://anarchkey.pythonanywhere.com/`)
- `--out-file` Path to write the init token (default: `~/.anarchkey`)

## Programmatic usage

```js
const AnarchKeyClient = require('anarchkey-client'); // when installed from npm
// OR local: const AnarchKeyClient = require('./lib/AnarchKeyClient');

(async () => {
  // initialize (optional) - equivalent to `anarchkey init`
  try {
    const token = await AnarchKeyClient.doInit({ username: 'me', password: 'secret' });
    console.log('init token:', token);
  } catch (e) {
    console.error('init failed:', e);
  }

  // use client
  const c = new AnarchKeyClient({ apiKey: 'myapikey', username: 'me' });
  const result = await c.getApiKey('myproject');
  if (result instanceof Error) {
    console.error(result.message);
  } else {
    console.log('result:', result);
  }
})();
```

## Notes

- The package writes `~/.anarchkey` with user-only permissions where possible.
- Behavior is intentionally close to the original Python client (including concatenating `apiKey + token` in the payload to `/get_api_key`).
