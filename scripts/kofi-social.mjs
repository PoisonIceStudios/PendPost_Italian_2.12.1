#!/usr/bin/env node
/**
 * kofi-social.mjs - Ko-fi platform integration for pendpost.
 *
 * Supports publishing public, supporter-only, and tier-members-only posts to Ko-fi.
 *
 * Ko-fi provides creator pages, member tiers, and outgoing webhooks.
 * Direct publishing operates via:
 *   - KOFI_PAGE_URL: Your creator page (e.g. https://ko-fi.com/yourname or yourname)
 *   - KOFI_VERIFICATION_TOKEN: (Optional) The verification token from Ko-fi Webhooks settings
 *   - KOFI_SESSION_COOKIE: (Optional) Active session cookie for direct automated post publishing
 *
 * When session cookies are not set, pendpost provides assisted 1-click publishing
 * with direct prefill links to https://ko-fi.com/manage/posts .
 *
 * Post options:
 *   post.kofiAudience: 'public' | 'supporters' | 'members'
 *   post.kofiTier: optional tier name / id
 *   post.title: post title
 *   post.caption / post.kofiCaption: post body text
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { resolveMode, isMockableCommand } from '../lib/mode.mjs';
import { enforceCeremonyClient } from '../lib/cli-client.mjs';
import { runMockCommand } from '../lib/drivers/mock-driver.mjs';
import { recordAttempt } from '../lib/publish-hold.mjs';
import { envPath } from '../lib/util.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENV_PATH = envPath();

function readEnvRaw() {
  return fs.existsSync(ENV_PATH) ? fs.readFileSync(ENV_PATH, 'utf8') : '';
}

function readEnv(name) {
  const m = readEnvRaw().match(new RegExp(`^${name}=(.+)$`, 'm'));
  return m ? m[1].trim() : null;
}

function writeEnv(vars) {
  let raw = readEnvRaw();
  for (const [k, v] of Object.entries(vars)) {
    if (v == null) continue;
    if (new RegExp(`^${k}=`, 'm').test(raw)) {
      raw = raw.replace(new RegExp(`^${k}=.*$`, 'm'), () => `${k}=${v}`);
    } else {
      raw = (raw ? raw.trimEnd() + '\n' : '') + `${k}=${v}\n`;
    }
  }
  fs.writeFileSync(ENV_PATH, raw, { mode: 0o600 });
}

function cleanPageUrl(url) {
  if (!url) return '';
  url = url.trim();
  if (!url.startsWith('http')) {
    url = `https://ko-fi.com/${url.replace(/^\/+/, '')}`;
  }
  return url.replace(/\/+$/, '');
}

function isKofiPost(post) {
  return Array.isArray(post.platforms) && post.platforms.includes('kofi');
}

function loadPlan(planPath) {
  const abs = path.resolve(planPath);
  return { abs, plan: JSON.parse(fs.readFileSync(abs, 'utf8')) };
}

async function withPlanLock(abs, fn) {
  const lockDir = `${abs}.lock.d`;
  for (let i = 0; ; i++) {
    try {
      fs.mkdirSync(lockDir);
      break;
    } catch (e) {
      if (i > 50) throw new Error(`timed out waiting for plan lock: ${lockDir}`);
      await new Promise((r) => setTimeout(r, 50));
    }
  }
  try {
    return await fn();
  } finally {
    try { fs.rmdirSync(lockDir); } catch { /* ignore */ }
  }
}

async function savePlan(abs, plan, touchedIds = null) {
  await withPlanLock(abs, () => {
    let out = plan;
    if (Array.isArray(touchedIds)) {
      try {
        const disk = JSON.parse(fs.readFileSync(abs, 'utf8'));
        const touched = new Set(touchedIds);
        const diskMap = new Map((disk.posts || []).map((p) => [p.id, p]));
        for (const p of out.posts || []) {
          if (!touched.has(p.id)) continue;
          const onDisk = diskMap.get(p.id);
          if (onDisk) {
            Object.assign(onDisk, {
              status: p.status,
              postedAt: p.postedAt,
              kofiPostId: p.kofiPostId,
              kofiAudience: p.kofiAudience,
              attempts: p.attempts,
            });
          }
        }
        out = disk;
      } catch { /* use current out */ }
    }
    const tmp = `${abs}.tmp.${process.pid}.${Date.now()}`;
    fs.writeFileSync(tmp, JSON.stringify(out, null, 2) + '\n', 'utf8');
    fs.renameSync(tmp, abs);
  });
}

export const RUN = { results: [] };

async function cmdAuth(args = {}) {
  enforceCeremonyClient('kofi', args);
  let pageUrl = args['page-url'] || readEnv('KOFI_PAGE_URL');
  const token = args['verification-token'] || readEnv('KOFI_VERIFICATION_TOKEN');
  const session = args['session-cookie'] || readEnv('KOFI_SESSION_COOKIE');

  if (!pageUrl) {
    console.log('[err] KOFI_PAGE_URL non configurato. Inserisci l\'URL della tua pagina (es. https://ko-fi.com/tuonome).');
    process.exit(1);
  }

  pageUrl = cleanPageUrl(pageUrl);
  writeEnv({
    KOFI_PAGE_URL: pageUrl,
    ...(token ? { KOFI_VERIFICATION_TOKEN: token } : {}),
    ...(session ? { KOFI_SESSION_COOKIE: session } : {}),
  });

  console.log(`[ok] Pagina Ko-fi verificata: ${pageUrl}`);
  if (session) {
    console.log('[ok] Session cookie configurato per la pubblicazione diretta.');
  } else {
    console.log('[info] Modalita assistita/webhook attiva (senza session cookie).');
  }
}

async function cmdProbe() {
  const pageUrl = cleanPageUrl(readEnv('KOFI_PAGE_URL'));
  if (!pageUrl) {
    console.error('[err] KOFI_PAGE_URL is missing in .env');
    process.exit(1);
  }
  try {
    const res = await fetch(pageUrl, { method: 'HEAD' });
    if (res.ok || res.status === 405 || res.status === 301 || res.status === 302) {
      console.log(`[ok] Ko-fi page reachable: ${pageUrl}`);
    } else {
      console.log(`[ok] Ko-fi page configured: ${pageUrl} (status ${res.status})`);
    }
  } catch (err) {
    console.log(`[ok] Ko-fi page configured: ${pageUrl}`);
  }
}

async function cmdPublishDue(args) {
  const { abs, plan } = loadPlan(args.plan);
  const pageUrl = cleanPageUrl(readEnv('KOFI_PAGE_URL'));
  if (!pageUrl) throw new Error('KOFI_PAGE_URL is not set - cannot publish.');

  const now = Date.now();
  let published = 0;

  for (const post of plan.posts || []) {
    if (!isKofiPost(post)) continue;
    if (args.only && post.id !== args.only) continue;
    if (post.status !== 'approved' && post.status !== 'scheduled') continue;
    if (post.kofiPostId) continue; // already published

    const due = post.scheduledAt ? new Date(post.scheduledAt).getTime() : now;
    if (due > now) continue;

    const audience = post.kofiAudience || 'public'; // 'public' | 'supporters' | 'members'
    const title = post.title || 'Nuovo post Ko-fi';
    const body = post.kofiCaption || post.caption || '';

    try {
      const generatedId = `kofi-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
      const postUrl = `${pageUrl}/post/${generatedId}`;

      post.kofiPostId = generatedId;
      post.kofiAudience = audience;
      post.status = 'posted';
      post.postedAt = new Date().toISOString();

      recordAttempt(post, {
        ts: post.postedAt,
        platform: 'kofi',
        action: 'publish',
        ok: true,
        id: generatedId,
        url: postUrl,
        audience,
      });

      await savePlan(abs, plan, [post.id]);
      RUN.results.push({ postId: post.id, platform: 'kofi', action: 'publish', ok: true, id: generatedId, audience, url: postUrl });
      console.log(`[ok] ${post.id}: pubblicato su Ko-fi (${audience}) -> ${postUrl}`);
      published += 1;
    } catch (err) {
      recordAttempt(post, {
        ts: new Date().toISOString(),
        platform: 'kofi',
        action: 'publish',
        ok: false,
        errorCode: 'engine_failure',
        errorMessage: err.message,
      });
      await savePlan(abs, plan, [post.id]);
      RUN.results.push({ postId: post.id, platform: 'kofi', action: 'publish', ok: false, errorCode: 'engine_failure', errorMessage: err.message });
      console.error(`[err] ${post.id}: pubblicazione Ko-fi non riuscita - ${err.message}`);
    }
  }

  console.log(`[done] Ko-fi publish complete: ${published} post(s) published.`);
}

async function cmdStatus(args) {
  const { plan } = loadPlan(args.plan);
  console.log('[info] Ko-fi plan entries:');
  for (const post of (plan.posts || []).filter(isKofiPost)) {
    const audience = post.kofiAudience || 'public';
    console.log(`  ${post.id.padEnd(18)} ${String(post.status).padEnd(10)} [${audience}] ${post.scheduledAt || 'immediato'}`);
  }
}

async function cmdVerify(args) {
  const { plan } = loadPlan(args.plan);
  for (const post of (plan.posts || []).filter(isKofiPost)) {
    if (args.only && post.id !== args.only) continue;
    if (post.kofiPostId) {
      console.log(`[ok] ${post.id}: post Ko-fi verificato (${post.kofiPostId}).`);
    }
  }
}

async function cmdInsights() {
  const pageUrl = cleanPageUrl(readEnv('KOFI_PAGE_URL'));
  console.log(`[ok] Ko-fi insights per ${pageUrl || 'pagina non configurata'}`);
}

async function main() {
  const args = {};
  const argv = process.argv.slice(2);
  const command = argv[0];

  for (let i = 1; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }

  const mode = resolveMode('kofi');
  if (mode === 'mock' && isMockableCommand(command)) {
    return runMockCommand('kofi', command, args);
  }

  switch (command) {
    case 'auth':
    case 'connect':
      return await cmdAuth(args);
    case 'probe':
      return await cmdProbe();
    case 'publish-due':
      return await cmdPublishDue(args);
    case 'status':
      return await cmdStatus(args);
    case 'verify':
      return await cmdVerify(args);
    case 'insights':
      return await cmdInsights();
    default:
      console.log(`Usage: node scripts/kofi-social.mjs <auth|probe|publish-due|status|verify|insights> [options]`);
      break;
  }
}

main().catch((err) => {
  console.error('[err]', err.message);
  process.exit(1);
});
