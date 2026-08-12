import { spawn } from 'child_process';
import path from 'path';

jest.setTimeout(30000);

const waitForServer = (url: string, timeout = 15000) =>
  new Promise<void>((resolve, reject) => {
    const start = Date.now();
    const poll = async () => {
      try {
        const res = await fetch(url);
        if (res.ok) {
          resolve();
          return;
        }
      } catch {}
      if (Date.now() - start > timeout) {
        reject(new Error('Server did not start in time'));
        return;
      }
      setTimeout(poll, 200);
    };
    poll();
  });

describe('Ascension AI API integration', () => {
  let server: any;
  const port = 3010;

  beforeAll(async () => {
    server = spawn('node', [path.join(__dirname, '../dist/index.js')], {
      env: {
        ...process.env,
        PORT: String(port),
        DEV_AUTH_BYPASS: 'true',
        ASCENSION_NATIVE_ENABLED: 'true',
        ASCENSION_NATIVE_URL: 'http://localhost:19999/chat',
        PATH: process.env.PATH
      },
      stdio: 'pipe'
    });
    await waitForServer(`http://localhost:${port}/health`);
  }, 20000);

  afterAll(() => {
    if (server) {
      server.kill();
    }
  });

  test('health endpoint returns ok', async () => {
    const res = await fetch(`http://localhost:${port}/health`);
    const data = await res.json();
    expect(data.status).toBe('ok');
  });

  test('chat endpoint with native enabled returns ascension-native response', async () => {
    const res = await fetch(`http://localhost:${port}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'dev-key'
      },
      body: JSON.stringify({ message: 'hello' })
    });
    const data = await res.json();
    expect(res.status).toBe(200);
    expect(data.provider).toBe('ascension-native');
    expect(data.capabilityId).toBe('ascension_chat');
    expect(data.content).toContain('Ascension native response');
  });

  test('chat endpoint with explicit native capability returns native response', async () => {
    const res = await fetch(`http://localhost:${port}/api/v1/chat/capability`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'dev-key'
      },
      body: JSON.stringify({
        capabilityId: 'ascension_home',
        message: 'assign chores',
        permissions: {
          'calendar.read': { granted: true },
          'home.control': { granted: true }
        }
      })
    });
    const data = await res.json();
    expect(res.status).toBe(200);
    expect(data.provider).toBe('ascension-native');
    expect(data.capabilityId).toBe('ascension_home');
  });
});
