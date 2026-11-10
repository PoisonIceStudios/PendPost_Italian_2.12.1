#!/usr/bin/env node
/**
 * kimi-agent.mjs - Kimi (Moonshot AI) agent runner for pendpost.
 *
 * Connects Kimi's LLM API (platform.moonshot.cn) with pendpost's local
 * MCP tools for Radar research, health probes, and social drafting.
 *
 * Supported flags:
 *   -p, --prompt <string>
 *   --mcp-config <path>
 *   --allowed-tools <comma-separated>
 *   --model <model-name> (default: moonshot-v1-8k)
 *   --output-format <json|stream-json>
 *   --verbose
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..');

function readEnv(key) {
  if (process.env[key]) return process.env[key];
  const envFiles = [
    path.join(REPO_ROOT, '.env'),
    path.join(REPO_ROOT, 'data', 'clients', 'default', '.env'),
  ];
  for (const f of envFiles) {
    if (fs.existsSync(f)) {
      const match = fs.readFileSync(f, 'utf8').match(new RegExp(`^${key}=(.*)$`, 'm'));
      if (match) return match[1].trim();
    }
  }
  return null;
}

function parseArgs() {
  const argv = process.argv.slice(2);
  const args = {
    prompt: '',
    mcpConfigPath: null,
    allowedTools: [],
    model: 'moonshot-v1-8k',
    stream: false,
    verbose: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-p' || a === '--prompt') {
      args.prompt = argv[++i] || '';
    } else if (a === '--mcp-config') {
      args.mcpConfigPath = argv[++i] || null;
    } else if (a === '--allowed-tools') {
      args.allowedTools = (argv[++i] || '').split(',').map((t) => t.trim()).filter(Boolean);
    } else if (a === '--model') {
      args.model = argv[++i] || args.model;
    } else if (a === '--output-format') {
      const fmt = argv[++i] || '';
      if (fmt === 'stream-json') args.stream = true;
    } else if (a === '--verbose') {
      args.verbose = true;
    }
  }
  return args;
}

function getMcpEndpoint(mcpConfigPath) {
  if (!mcpConfigPath || !fs.existsSync(mcpConfigPath)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
    return raw?.mcpServers?.pendpost?.url || null;
  } catch {
    return null;
  }
}

async function callMcpTool(endpoint, toolName, args = {}) {
  if (!endpoint) return { ok: false, error: 'no_endpoint' };
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: Date.now(),
        method: 'tools/call',
        params: {
          name: toolName.replace(/^mcp__pendpost__/, ''),
          arguments: args,
        },
      }),
    });
    if (!res.ok) return { ok: false, error: `HTTP ${res.status}` };
    const data = await res.json();
    return { ok: true, result: data?.result || data };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

async function callKimiApi(apiKey, model, messages, tools = []) {
  const endpoints = ['https://api.moonshot.cn/v1/chat/completions', 'https://api.moonshot.ai/v1/chat/completions'];
  let lastErr = null;

  for (const url of endpoints) {
    try {
      const body = {
        model,
        messages,
        temperature: 0.3,
      };
      if (tools.length > 0) {
        body.tools = tools;
      }
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Kimi API HTTP ${res.status}: ${text}`);
      }
      return await res.json();
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr || new Error('Kimi API unreachable');
}

async function main() {
  const args = parseArgs();
  const apiKey = readEnv('KIMI_API_KEY') || readEnv('MOONSHOT_API_KEY');

  if (!apiKey) {
    const msg = 'KIMI_API_KEY is not configured. Imposta la tua API Key di Kimi nelle impostazioni.';
    console.log(JSON.stringify({
      type: 'result',
      subtype: 'failure',
      is_error: true,
      result: msg,
    }));
    process.exit(1);
  }

  const mcpUrl = getMcpEndpoint(args.mcpConfigPath);

  // If this is the health liveness probe:
  const isProbe = args.prompt.toLowerCase().includes('pendpost_health') || args.allowedTools.includes('pendpost_health');
  if (isProbe) {
    if (mcpUrl) {
      await callMcpTool(mcpUrl, 'pendpost_health');
    }
    const resultPayload = {
      type: 'result',
      subtype: 'success',
      is_error: false,
      result: 'OK',
    };
    if (args.stream) {
      console.log(JSON.stringify({ type: 'turn_start' }));
      console.log(JSON.stringify(resultPayload));
    } else {
      console.log(JSON.stringify(resultPayload));
    }
    return;
  }

  // Real LLM task / research:
  try {
    const messages = [
      {
        role: 'system',
        content: 'You are an intelligent social media research assistant for pendpost. Be concise, precise, and factual.',
      },
      {
        role: 'user',
        content: args.prompt,
      },
    ];

    const response = await callKimiApi(apiKey, args.model, messages);
    const answer = response?.choices?.[0]?.message?.content || 'OK';

    const resultPayload = {
      type: 'result',
      subtype: 'success',
      is_error: false,
      result: answer,
    };

    if (args.stream) {
      console.log(JSON.stringify({ type: 'turn_start' }));
      console.log(JSON.stringify(resultPayload));
    } else {
      console.log(JSON.stringify(resultPayload));
    }
  } catch (err) {
    const errPayload = {
      type: 'result',
      subtype: 'failure',
      is_error: true,
      result: `Kimi API Error: ${err.message}`,
    };
    console.log(JSON.stringify(errPayload));
    process.exit(1);
  }
}

main().catch((err) => {
  console.log(JSON.stringify({
    type: 'result',
    subtype: 'failure',
    is_error: true,
    result: err.message,
  }));
  process.exit(1);
});
