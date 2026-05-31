# Web Frontend Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. React Stack ⭐ Primary Recommendation

**Security Grade: A**

| Component | Pinned Version | License | CVEs (2024-2026) |
|-----------|---------------|---------|-------------------|
| React | 18.3.1 | MIT | 0 critical |
| Next.js | 14.2.15 | MIT | 2 moderate (patched) |
| TypeScript | 5.4.5 | Apache-2.0 | N/A (compiler) |
| Vite | 5.4.11 | MIT | 1 low |
| Node.js runtime | 20.18.0 | MIT | See backend.md |

**Known Vulnerabilities (patched):**
- Next.js CVE-2024-34350: HTTP response header injection (fixed in 14.1.1)
- Next.js CVE-2024-46982: Cache poisoning (fixed in 14.2.10)

**Recommended Lockfile Hash:**
```bash
# package-lock.json integrity
npm ci --ignore-scripts
sha256sum package-lock.json
```

**Key Dependencies (pinned):**
```json
{
  "react": "18.3.1",
  "react-dom": "18.3.1",
  "next": "14.2.15",
  "typescript": "5.4.5",
  "vite": "5.4.11",
  "@types/react": "18.3.12",
  "eslint": "8.57.1",
  "eslint-config-next": "14.2.15"
}
```

**Security Best Practices:**
- Enable `reactStrictMode: true` in next.config.js
- Use `Content-Security-Policy` headers via Next.js middleware
- Pin all dependencies; run `npm audit` in CI
- Use `--ignore-scripts` during install to prevent supply chain attacks

**Alternatives Considered:** Remix (deferred — smaller ecosystem), Astro (static-only use case)

---

## 2. Vue Stack

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Vue | 3.4.38 | MIT | 0 |
| Nuxt | 3.13.2 | MIT | 1 low |
| TypeScript | 5.4.5 | Apache-2.0 | N/A |
| Vite | 5.4.11 | MIT | 1 low |
| Pinia | 2.2.4 | MIT | 0 |

**Known Issues:**
- Nuxt 3.x early versions had SSR hydration mismatch edge cases (resolved in 3.12+)
- Vite dev server should not be exposed publicly (use `--host 127.0.0.1`)

**Lockfile Template:**
```json
{
  "vue": "3.4.38",
  "nuxt": "3.13.2",
  "typescript": "5.4.5",
  "vite": "5.4.11",
  "@pinia/nuxt": "0.5.5",
  "pinia": "2.2.4"
}
```

**Compatibility Notes:**
- Nuxt 3.13 requires Node >= 18.0.0
- Vue 3.4 uses Vapor Mode preview — avoid in production until 3.5 stable

---

## 3. Svelte Stack

**Security Grade: A-**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Svelte | 4.2.19 | MIT | 0 |
| SvelteKit | 2.7.3 | MIT | 0 |
| TypeScript | 5.4.5 | Apache-2.0 | N/A |
| Vite | 5.4.11 | MIT | 1 low |

**Known Issues:**
- Svelte 5 (runes) released but still stabilizing — stay on 4.x for production
- SvelteKit adapter-node has had minor SSR bypass reports (patched in 2.5+)

**Recommended Pins:**
```json
{
  "svelte": "4.2.19",
  "@sveltejs/kit": "2.7.3",
  "@sveltejs/adapter-node": "5.2.9",
  "vite": "5.4.11",
  "typescript": "5.4.5"
}
```

**Alternatives Considered:** Solid.js (smaller community), Astro (hybrid use case)

---

## 4. Angular Stack

**Security Grade: B+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Angular | 17.3.12 | MIT | 1 moderate (patched) |
| TypeScript | 5.4.5 | Apache-2.0 | N/A |
| RxJS | 7.8.1 | Apache-2.0 | 0 |
| Angular CLI | 17.3.11 | MIT | 0 |

**Known Vulnerabilities:**
- Angular 17.0.x had a DOM clobbering issue (CVE-2024-21511, patched in 17.1.0)

**Compatibility Notes:**
- Angular 17 introduces standalone components by default
- Requires Node >= 18.13.0
- Larger bundle size vs React/Vue/Svelte alternatives

**Recommended Pins:**
```json
{
  "@angular/core": "17.3.12",
  "@angular/cli": "17.3.11",
  "typescript": "5.4.5",
  "rxjs": "7.8.1",
  "zone.js": "0.14.10"
}
```

**Alternatives Considered:** Angular 18 (deferred — too new), React (ecosystem preference)

---

## Cross-Cutting Security Checklist (All Frontend Stacks)

- [ ] Enable CSP headers (script-src, style-src, connect-src)
- [ ] Sanitize all user inputs (DOMPurify for HTML, parameterize queries)
- [ ] Use `HttpOnly` + `Secure` + `SameSite=Strict` cookies
- [ ] Run `npm audit` / `pnpm audit` in CI pipeline
- [ ] Pin lockfile with `npm ci` (never `npm install` in CI)
- [ ] Enable Dependabot or Renovate with auto-merge for patch updates
- [ ] Use Subresource Integrity (SRI) for CDN-loaded assets
- [ ] Enable HSTS with min 1-year max-age + includeSubDomains

## Toolchain Comparison

| Feature | React/Next | Vue/Nuxt | Svelte/Kit | Angular |
|---------|-----------|----------|------------|---------|
| Bundle Size | ~45KB | ~33KB | ~2KB | ~65KB |
| Hydration | Partial | Partial | Partial | Full |
| SSG Support | ✅ | ✅ | ✅ | Limited |
| SSR | ✅ | ✅ | ✅ | ✅ |
| Ecosystem | Largest | Large | Growing | Large |
| Security Grade | A | A | A- | B+ |
