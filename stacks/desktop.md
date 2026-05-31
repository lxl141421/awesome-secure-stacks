# Desktop Application Stacks — Security Guide

> Last updated: 2026-05-31 | Stability-first: LTS and battle-tested releases only

---

## 1. Electron 31.x + React 18 + TypeScript 5.6

**Security Score: B+**
**Stability: ★★★★★**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Electron       | 31.7.x    | 2025-10   | Chromium 126, Node 20 LTS      |
| React          | 18.3.x    | Active    | Stable concurrent features     |
| TypeScript     | 5.6.x     | Active    | Strict null checks default     |
| Node.js (bundled) | 20.x LTS | 2026-04 | Electron-internal runtime      |

### Security Checklist

- [ ] **Enable `contextIsolation: true`** (default since Electron 12 — verify never overridden)
- [ ] **Disable `nodeIntegration`** in all BrowserWindows
- [ ] Use `contextBridge.exposeInMainWorld()` for IPC — never expose raw `ipcRenderer`
- [ ] Set `sandbox: true` on all renderer processes
- [ ] Implement strict CSP in `<meta>` tags AND `session.defaultSession.webRequest`
- [ ] Validate and sanitize all IPC message payloads in main process
- [ ] Use `protocol.handle()` instead of deprecated `protocol.registerHttpProtocol`
- [ ] Strip `X-Powered-By` and other fingerprinting headers
- [ ] Pin auto-update server certificate (see below)

### CSP Configuration

```javascript
// main.ts — Electron main process
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; " +
        "img-src 'self' data: https:; connect-src 'self' https://api.yourapp.com; " +
        "font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
      ]
    }
  });
});
```

### IPC Security Pattern

```typescript
// preload.ts — contextBridge (secure)
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  getData: (id: string) => {
    if (typeof id !== 'string' || id.length > 64) throw new Error('Invalid input');
    return ipcRenderer.invoke('get-data', id);
  }
});

// main.ts — handler with validation
ipcMain.handle('get-data', async (_event, id: unknown) => {
  if (typeof id !== 'string' || !/^[a-zA-Z0-9_-]{1,64}$/.test(id)) {
    throw new Error('Invalid data ID');
  }
  return await safeDataFetch(id);
});
```

### Auto-Update Security

```typescript
import { autoUpdater } from 'electron-updater';

autoUpdater.setFeedURL({
  provider: 'generic',
  url: 'https://releases.yourapp.com/update/',
  // Certificate pinning via custom request headers or mutual TLS
});

// Verify signatures — electron-updater checks by default with code signing
autoUpdater.on('update-available', (info) => {
  // Log version, but don't allow downgrade attacks
  if (semver.lt(info.version, app.getVersion())) {
    console.error('Downgrade rejected');
    return;
  }
});
```

### Attack Surface Concerns

**Electron's larger attack surface** vs native or Tauri apps:
- Bundles full Chromium + Node.js runtime (~150–200 MB)
- Every Chromium CVE is your CVE — rapid update cadence required
- Node.js APIs available to main process increase privilege escalation risk
- Native modules (N-API) can introduce memory corruption vulnerabilities
- Recommendation: Only use Electron when cross-platform web-UI consistency is critical

### Native Module Risks

- Audit all `.node` binary modules with `npm audit` and Snyk
- Prefer N-API over NAN for ABI stability and reduced recompilation issues
- Use `electron-rebuild` to ensure native modules match Electron's Node version
- Scan with `govulncheck` equivalent for Node: `npm audit --audit-level=high`

---

## 2. Tauri 2.x + React 18 + TypeScript 5.6

**Security Score: A**
**Stability: ★★★★☆**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Tauri          | 2.4.x     | Active    | Rust backend, system WebView   |
| React          | 18.3.x    | Active    | Same frontend as Electron      |
| TypeScript     | 5.6.x     | Active    |                                |
| Rust           | 1.78+     | Required  | Minimum for Tauri 2.x          |

### Security Checklist

- [ ] **Use allowlist-based permissions** — deny all by default in `tauri.conf.json`
- [ ] Enable `security.csp` in Tauri config
- [ ] Use `tauri::command` with typed parameters (compile-time safety)
- [ ] Audit all plugins — each Tauri plugin expands attack surface
- [ ] Enable code signing for all platforms (macOS notarization, Windows Authenticode)
- [ ] Use system WebView (no bundled engine) — reduces patching burden
- [ ] Validate all IPC commands in Rust (type checking + bounds checking)

### Tauri Permission Model (v2)

```json
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:allow-open",
    "fs:allow-read",
    "fs:allow-exists",
    {
      "identifier": "fs:scope",
      "allow": [{ "path": "$APPDATA/**" }]
    },
    "shell:allow-open"
  ]
}
```

### CSP Configuration

```json
// tauri.conf.json
{
  "security": {
    "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://api.yourapp.com; img-src 'self' data: https:; font-src 'self'; object-src 'none'; base-uri 'self'",
    "freezePrototype": false
  }
}
```

### Rust Command Security

```rust
use tauri::command;
use serde::Deserialize;

#[derive(Deserialize)]
struct FileRequest {
    path: String,
}

#[command]
fn read_file(request: FileRequest) -> Result<String, String> {
    // Validate path is within allowed directory
    let base = dirs::data_dir().ok_or("No data dir")?;
    let full_path = base.join(&request.path);
    let canonical = full_path.canonicalize()
        .map_err(|_| "Invalid path")?;

    if !canonical.starts_with(&base) {
        return Err("Path traversal detected".into());
    }

    std::fs::read_to_string(&canonical)
        .map_err(|e| format!("Read error: {}", e))
}
```

### Auto-Update Security

```rust
// Tauri updater with signature verification
tauri::Builder::default()
    .plugin(tauri_plugin_updater::Builder::new().build())
    .setup(|app| {
        let handle = app.handle().clone();
        tauri::async_runtime::spawn(async move {
            let updater = handle.plugin::<tauri_plugin_updater::Updater>()
                .unwrap();
            if let Ok(update) = updater.check().await {
                // Signature verification is built-in with Tauri's updater
                update.download_and_install(|_, _| {}, || {}).await.ok();
            }
        });
        Ok(())
    })
```

### Attack Surface Comparison: Electron vs Tauri

| Aspect              | Electron           | Tauri              |
|---------------------|--------------------|--------------------|
| Bundle size         | ~150 MB            | ~3–10 MB           |
| Runtime             | Chromium + Node    | System WebView + Rust |
| Memory safety       | C++ (Chromium), JS | Rust (memory-safe) |
| Node.js exposure    | Full (main process)| None               |
| IPC model           | JSON messages      | Typed Rust commands |
| Web engine updates  | Bundled (manual)   | OS-provided (auto) |

**Verdict**: Tauri significantly reduces attack surface. Prefer Tauri for new desktop projects unless Electron-specific APIs are required.

---

## 3. Qt 6.6 + C++17

**Security Score: A**
**Stability: ★★★★★**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Qt             | 6.6.3     | 2025-09   | LTS-adjacent, widely deployed  |
| C++            | C++17     | Compiler  | Mature, well-understood        |
| CMake          | 3.22+     | Build     | Required for Qt 6              |

### Security Checklist

- [ ] Use `QNetworkAccessManager` with TLS 1.2+ enforcement
- [ ] Enable `/GS` (MSVC) or `-fstack-protector-strong` (GCC/Clang)
- [ ] Compile with `-D_FORTIFY_SOURCE=2` and `-fPIE -pie`
- [ ] Use `QString` over raw `char*` — prevents buffer overflows
- [ ] Validate all `QUrl` inputs before `QDesktopServices::openUrl()`
- [ ] Use `QProcess` carefully — sanitize all arguments, never use `shell=True` equivalent
- [ ] Enable Qt's built-in address space layout randomization
- [ ] Use `QCryptographicHash` for hashing (not custom implementations)
- [ ] Audit QML for JavaScript injection in dynamic `Qt.createQmlObject()` calls

### Secure QNetworkAccessManager

```cpp
QNetworkAccessManager *manager = new QNetworkAccessManager(this);

// Enforce TLS
QSslConfiguration sslConfig = QSslConfiguration::defaultConfiguration();
sslConfig.setProtocol(QSsl::TlsV1_2OrLater);
sslConfig.setPeerVerifyMode(QSslSocket::VerifyPeer);

// Certificate pinning
QList<QSslCertificate> pinned = QSslCertificate::fromPath(":/certs/api.pem");
sslConfig.setCaCertificates(pinned);

QNetworkRequest request(QUrl("https://api.example.com/data"));
request.setSslConfiguration(sslConfig);
manager->get(request);
```

### Secure QProcess Usage

```cpp
void launchTool(const QString &userInput) {
    // NEVER: process->start("tool " + userInput);  // command injection
    // SAFE:
    QStringList args;
    args << "--safe-flag" << sanitize(userInput);
    QProcess::startDetached("/usr/bin/tool", args);
}
```

---

## 4. .NET MAUI 8 (LTS)

**Security Score: A-**
**Stability: ★★★★★**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| .NET           | 8.0.x LTS| 2026-11   | Long-term support              |
| MAUI           | 8.0.x     | Tied to .NET 8 | Cross-platform native   |
| C#             | 12        | Tied to .NET 8 | Nullable refs, source gen |

### Security Checklist

- [ ] Enable **nullable reference types** project-wide
- [ ] Use `HttpClient` with certificate pinning via `ServerCertificateCustomValidationCallback`
- [ ] Enable **Platform Linker** to strip unused code (reduces attack surface)
- [ ] Use **Secure Storage** (`SecureStorage.Default`) for tokens/secrets
- [ ] Implement **App Transport Security** (iOS) / **Network Security Config** (Android)
- [ ] Enable **code signing** for all target platforms
- [ ] Use `Microsoft.AspNetCore.Components.WebView.Maui` with CSP for Blazor views
- [ ] Audit all NuGet packages — MAUI ecosystem has less vetting than mature .NET

### Certificate Pinning

```csharp
var handler = new HttpClientHandler
{
    ServerCertificateCustomValidationCallback = (message, cert, chain, errors) =>
    {
        if (cert == null) return false;
        // Pin to specific certificate thumbprint
        string expectedThumbprint = "A1B2C3D4E5F6...";
        return cert.GetCertHashString() == expectedThumbprint;
    }
};
var client = new HttpClient(handler);
```

### Secure Storage

```csharp
// Platform-encrypted storage (Keychain on iOS, EncryptedSharedPreferences on Android)
await SecureStorage.Default.SetAsync("auth_token", token);
string? token = await SecureStorage.Default.GetAsync("auth_token");
```

---

## Cross-Stack Security Comparison

| Stack           | Score | Bundle Size | Memory Safety | Patch Burden | Best For              |
|-----------------|-------|-------------|---------------|--------------|-----------------------|
| Electron + React| B+    | ~150 MB     | Medium        | High         | Web-UI consistency    |
| Tauri + React   | A     | ~5 MB       | High (Rust)   | Low          | New desktop projects  |
| Qt 6.6 + C++17  | A     | ~20 MB      | Medium (C++)  | Medium       | Native performance    |
| .NET MAUI 8     | A-    | ~30 MB      | Managed       | Medium       | .NET ecosystem teams  |

## Recommendations

1. **New projects**: Prefer **Tauri 2.x** — smallest attack surface, memory-safe backend
2. **Enterprise/.NET shops**: .NET MAUI 8 LTS is solid with proper hardening
3. **Existing Electron apps**: Migrate to Tauri incrementally, or harden with aggressive CSP + sandboxing
4. **Performance-critical**: Qt 6.6 with C++17 security hardening flags
