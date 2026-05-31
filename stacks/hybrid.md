# Hybrid & WebView Stacks — Security Guide

> Last updated: 2026-05-31 | Stability-first: LTS and battle-tested releases only

---

## 1. Capacitor 5.x + Ionic 8 + Framework

**Security Score: B+**
**Stability: ★★★★★**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Capacitor      | 5.7.x     | 2025-03   | Native bridge layer            |
| Ionic          | 8.x       | Active    | UI component library           |
| Angular        | 18.x LTS  | 2025-11   | Enterprise default             |
| Vue            | 3.4.x     | Active    | Alternative framework          |
| React           | 18.3.x    | Active    | Alternative framework          |

### Security Checklist

- [ ] Enable **WebView CSP** on both Android and iOS
- [ ] Use `capacitor.config.ts` to restrict allowed origins
- [ ] Disable `allowFileAccess` and `allowUniversalAccessFromFileURLs` (Android)
- [ ] Implement **certificate pinning** via `@aspect-build/capacitor-ssl-pinning`
- [ ] Validate all JavaScript bridge calls server-side — bridge is trust boundary
- [ ] Use `CapacitorHttp` (native HTTP) for API calls — avoids WebView fetch limitations
- [ ] Strip `console.log` in production builds (info leakage)
- [ ] Enable **App Transport Security** (iOS) with no exceptions
- [ ] Set `WKWebView` process pool limits on iOS
- [ ] Audit all Capacitor plugins for native code injection vectors

### Capacitor Config Security

```typescript
// capacitor.config.ts
const config: CapacitorConfig = {
  appId: 'com.example.app',
  appName: 'MyApp',
  webDir: 'dist',
  server: {
    // CRITICAL: In production, never use live reload or cleartext
    androidScheme: 'https',
    cleartext: false,
    // Restrict allowed navigation origins
    allowNavigation: ['api.example.com'],
  },
  android: {
    // Security: disable file access in WebView
    webContentsDebuggingEnabled: false,
  },
  ios: {
    // Limits WebView process sharing
    contentInset: 'automatic',
  },
};

export default config;
```

---

## 2. WebView Security Hardening

### Android WebView Hardening

```kotlin
// MainActivity.kt
class MainActivity : BridgeActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Get the WebView from Capacitor bridge
        val webView = bridge?.webView ?: return

        webView.settings.apply {
            // Disable dangerous features
            allowFileAccess = false
            allowFileAccessFromFileURLs = false
            allowUniversalAccessFromFileURLs = false
            allowContentAccess = false

            // Enable safe browsing
            safeBrowsingEnabled = true

            // Disable JavaScript interfaces that expose native objects
            // Only use Capacitor's bridge — never add raw @JavascriptInterface

            // Force HTTPS mixed content blocking
            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
        }

        // Prevent WebView from loading arbitrary URLs
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView?, request: WebResourceRequest?
            ): Boolean {
                val url = request?.url?.toString() ?: return true
                return if (isAllowedOrigin(url)) false else true
            }
        }
    }

    private fun isAllowedOrigin(url: String): Boolean {
        val allowed = listOf("https://app.example.com", "capacitor://localhost")
        return allowed.any { url.startsWith(it) }
    }
}
```

### iOS WKWebView Hardening

```swift
// AppDelegate.swift or SceneDelegate
import WebKit

func configureWebView(_ webView: WKWebView) {
    // Restrict JavaScript navigation
    let contentController = webView.configuration.userContentController

    // Remove any non-Capacitor message handlers
    // Only Capacitor's bridge should register handlers

    // CSP via response headers (requires custom URL scheme or local server)
    // See server configuration below
}

// WKNavigationDelegate
extension ViewController: WKNavigationDelegate {
    func webView(
        _ webView: WKWebView,
        decidePolicyFor navigationAction: WKNavigationAction,
        decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
    ) {
        guard let url = navigationAction.request.url else {
            decisionHandler(.cancel)
            return
        }

        let allowed = ["capacitor://localhost", "https://app.example.com"]
        if allowed.contains(where: { url.absoluteString.hasPrefix($0) }) {
            decisionHandler(.allow)
        } else {
            decisionHandler(.cancel)
        }
    }
}
```

### WebView CSP Enforcement

```html
<!-- index.html — Meta CSP (first thing in <head>) -->
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self' capacitor://localhost;
           script-src 'self' 'unsafe-inline';
           style-src 'self' 'unsafe-inline';
           img-src 'self' data: https:;
           connect-src 'self' https://api.example.com;
           font-src 'self';
           object-src 'none';
           base-uri 'self';
           frame-ancestors 'none';
           form-action 'self' https://api.example.com;">
```

---

## 3. JavaScript Bridge Security Patterns

### The Problem

Capacitor/Cordova bridges expose native functionality to JavaScript. A compromised web page can call native APIs.

### Secure Bridge Pattern

```typescript
// Custom plugin with validation
import { registerPlugin } from '@capacitor/core';

interface SecureFilePlugin {
  readFile(options: { path: string }): Promise<{ content: string }>;
}

const SecureFile = registerPlugin<SecureFilePlugin>('SecureFile', {
  web: () => import('./web').then(m => new m.SecureFileWeb()),
});

// Native side (Android) — validate everything
@CapacitorPlugin(name = 'SecureFile')
public class SecureFilePlugin extends Plugin {
    @PluginMethod
    public void readFile(PluginCall call) {
        String path = call.getString("path");

        // Validate: path must be within app sandbox
        if (path == null || path.contains("..") || path.startsWith("/")) {
            call.reject("Invalid path", "INVALID_PATH");
            return;
        }

        // Whitelist check
        if (!path.startsWith("documents/") && !path.startsWith("cache/")) {
            call.reject("Access denied", "FORBIDDEN_PATH");
            return;
        }

        // Safe to read
        File file = new File(getContext().getFilesDir(), path);
        // ... read and return
    }
}
```

### Bridge Injection Risk Matrix

| Risk                      | Impact | Mitigation                          |
|---------------------------|--------|-------------------------------------|
| XSS → native API call    | High   | CSP + bridge input validation       |
| Deep link abuse           | High   | Validate all deep link parameters   |
| Plugin supply chain       | High   | Audit all Capacitor plugins         |
| WebView JS injection      | Medium | No `evaluateJavascript` from native |
| Clipboard access          | Medium | Disable clipboard plugin in prod    |
| Geolocation leak          | Medium | Runtime permission prompts only     |

---

## 4. Cordova (Legacy) — Security Warnings

**Security Score: C**
**Stability: ★★★☆☆ (maintenance mode)**

### ⚠️ Security Warnings

- **Cordova is in maintenance mode** — prefer Capacitor for new projects
- Plugin ecosystem is aging with unpatched vulnerabilities
- `config.xml` `<access>` and `<allow-navigation>` are easy to misconfigure
- Cordova-Android uses older WebView APIs with known issues

### If You Must Use Cordova

```xml
<!-- config.xml — Restrictive configuration -->
<access origin="https://api.example.com" />
<allow-navigation href="https://api.example.com/*" />
<!-- Remove ALL wildcard access -->
<!-- <access origin="*" /> ← NEVER DO THIS -->

<platform name="android">
    <preference name="AndroidXEnabled" value="true" />
    <preference name="GradlePluginGoogleServicesEnabled" value="true" />
</platform>

<platform name="ios">
    <preference name="WKWebViewOnly" value="true" />
    <!-- Force modern WebView -->
</platform>
```

---

## 5. PWA as Secure Alternative

**Security Score: A-**
**Stability: ★★★★★**

PWAs avoid native bridge risks entirely by running in the browser's security sandbox.

### PWA Security Advantages

- No native bridge to exploit — browser sandbox enforces permissions
- HTTPS mandatory (enforced by service worker registration)
- Origin-based security model (CORS, CSP)
- No app store supply chain risks
- Automatic browser security updates

### PWA Security Checklist

- [ ] Enforce HTTPS everywhere — no mixed content
- [ ] Implement strict CSP (no `unsafe-eval`)
- [ ] Use `Sec-Fetch-*` headers to validate request origin
- [ ] Pin service worker scope — prevent scope hijacking
- [ ] Cache sensitive responses with `Cache-Control: no-store`
- [ ] Implement `Permissions-Policy` header to restrict APIs
- [ ] Use Web Crypto API for client-side crypto (not JS libraries)

### Service Worker Security

```javascript
// sw.js — Service Worker with secure caching
const CACHE_NAME = 'v1.2.3';
const ALLOWED_ORIGINS = ['https://api.example.com'];

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Only cache same-origin GET requests
  if (event.request.method !== 'GET') return;
  if (!ALLOWED_ORIGINS.includes(url.origin) && url.origin !== self.location.origin) {
    return; // Don't cache cross-origin requests by default
  }

  // Never cache authenticated responses
  if (event.request.headers.get('Authorization')) {
    event.respondWith(fetch(event.request));
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request).then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        return response;
      });
    })
  );
});
```

---

## 6. Certificate Pinning Comparison

| Platform       | Method                                    | Capacitor Plugin           |
|----------------|-------------------------------------------|---------------------------|
| Android        | Network Security Config XML               | Built-in since API 24     |
| Android        | OkHttp CertificatePinner                  | `@aspect-build/ssl-pin`   |
| iOS            | NSURLSessionDelegate / TrustKit           | `@aspect-build/ssl-pin`   |
| PWA            | Not possible (browser manages TLS)        | N/A                       |
| Electron       | `ses.setCertificateVerifyProc()`          | Native                    |

### Android Network Security Config

```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set expiration="2027-01-01">
            <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
            <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
            <!-- Include backup pin for rotation -->
        </pin-set>
    </domain-config>
</network-security-config>
```

---

## Cross-Stack Security Comparison

| Stack                    | Score | Attack Surface | Native Access | Maintenance |
|--------------------------|-------|---------------|---------------|-------------|
| Capacitor + Ionic + Angular | B+  | Medium        | Full (bridge) | Active      |
| Cordova (legacy)         | C     | High          | Full (bridge) | Minimal     |
| PWA (no native)          | A-    | Low           | None          | Browser     |
| Capacitor + Ionic + React | B+  | Medium        | Full (bridge) | Active      |
| Capacitor + Ionic + Vue  | B+   | Medium        | Full (bridge) | Active      |

## Recommendations

1. **New hybrid projects**: Capacitor 5.x + Ionic 8 + your preferred framework
2. **Existing Cordova**: Migrate to Capacitor incrementally
3. **No native APIs needed**: Use PWA — eliminates bridge attack surface entirely
4. **Sensitive apps (banking)**: Native (Swift/Kotlin) with no WebView layer
