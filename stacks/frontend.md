# Web Frontend Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. React Stack ⭐ Primary Recommendation

**Security Grade: A**

| Component | Pinned Version | License | CVEs (2024-2026) |
|-----------|---------------|---------|-------------------|
| React | 19.1.0 | MIT | 0 critical |
| Next.js | 15.3.2 | MIT | 0 critical |
| TypeScript | 5.8.3 | Apache-2.0 | N/A (compiler) |
| Vite | 6.3.5 | MIT | 0 critical |
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
  "react": "19.1.0",
  "react-dom": "19.1.0",
  "next": "15.3.2",
  "typescript": "5.8.3",
  "vite": "6.3.5",
  "@types/react": "18.3.12",
  "eslint": "8.57.1",
  "eslint-config-next": "15.3.2"
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
| Vue | 3.5.16 | MIT | 0 |
| Nuxt | 3.16.2 | MIT | 0 |
| TypeScript | 5.8.3 | Apache-2.0 | N/A |
| Vite | 6.3.5 | MIT | 0 critical |
| Pinia | 2.2.4 | MIT | 0 |

**Known Issues:**
- Nuxt 3.x early versions had SSR hydration mismatch edge cases (resolved in 3.12+)
- Vite dev server should not be exposed publicly (use `--host 127.0.0.1`)

**Lockfile Template:**
```json
{
  "vue": "3.5.16",
  "nuxt": "3.16.2",
  "typescript": "5.8.3",
  "vite": "6.3.5",
  "@pinia/nuxt": "0.5.5",
  "pinia": "2.2.4"
}
```

**Compatibility Notes:**
- Nuxt 3.16 requires Node >= 18.0.0
- Vue 3.5 includes stable Vapor Mode — safe for production use

---

## 3. Svelte Stack

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Svelte | 5.33.1 | MIT | 0 |
| SvelteKit | 2.21.1 | MIT | 0 |
| TypeScript | 5.8.3 | Apache-2.0 | N/A |
| Vite | 6.3.5 | MIT | 0 critical |

**Known Issues:**
- Svelte 5 (runes) is now stable — recommended for production
- SvelteKit adapter-node has had minor SSR bypass reports (patched in 2.5+)

**Recommended Pins:**
```json
{
  "svelte": "5.33.1",
  "@sveltejs/kit": "2.21.1",
  "@sveltejs/adapter-node": "5.2.9",
  "vite": "6.3.5",
  "typescript": "5.8.3"
}
```

**Alternatives Considered:** Solid.js (smaller community), Astro (hybrid use case)

---

## 4. Angular Stack

**Security Grade: B+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Angular | 19.2.13 | MIT | 0 critical |
| TypeScript | 5.8.3 | Apache-2.0 | N/A |
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
  "@angular/core": "19.2.13",
  "@angular/cli": "19.2.13",
  "typescript": "5.8.3",
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
| Security Grade | A | A | A | B+ |
