# Mobile Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. React Native + Expo ⭐ Cross-Platform Recommendation

**Security Grade: A-**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| React Native | 0.73.11 | MIT | 0 |
| Expo SDK | 50.0.19 | MIT | 0 |
| TypeScript | 5.4.5 | Apache-2.0 | N/A |
| Hermes Engine | 0.73.x | MIT | 0 |
| Metro Bundler | 0.80.12 | MIT | 0 |

**Dependency Lockfile:**
```json
{
  "react-native": "0.73.11",
  "expo": "~50.0.19",
  "expo-secure-store": "~13.0.2",
  "expo-local-authentication": "~14.0.1",
  "expo-crypto": "~13.0.2",
  "typescript": "5.4.5"
}
```

**Security Best Practices:**
- Use `expo-secure-store` for sensitive data (not AsyncStorage)
- Enable Hermes for production (faster, smaller, more secure)
- Certificate pinning via `react-native-ssl-pinning` or custom native module
- Use `expo-updates` with code signing enabled
- Jailbreak/root detection via `react-native-jailbreak-detector`

**Known Issues:**
- Expo Go (dev client) should never be used in production
- Third-party native modules may introduce vulnerabilities — audit carefully

**Build Reproducibility:**
```bash
eas build --platform ios --profile production --local
# Use EAS Build with locked versions for reproducible builds
```

---

## 2. Flutter

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Flutter | 3.19.6 | BSD-3 | 0 |
| Dart | 3.3.4 | BSD-3 | 0 |
| Riverpod | 2.5.1 | MIT | 0 |
| Dio | 5.5.0 | MIT | 0 |

**Dependency Lockfile:**
```yaml
# pubspec.yaml
environment:
  sdk: ">=3.3.4 <4.0.0"
  flutter: ">=3.19.6 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  dio: 5.5.0
  flutter_secure_storage: 9.2.2
  local_auth: 2.2.0
  pointycastle: 3.9.1
```

```bash
# pubspec.lock verification
dart pub deps --json | jq '.packages[] | {name, version}'
```

**Security Best Practices:**
- Use `flutter_secure_storage` (Keychain/KeyStore backed)
- Enable `obfuscation` in release builds: `flutter build apk --obfuscate`
- Certificate pinning via `dio` + custom `HttpClient`
- Use `dart run build_runner build` for generated code verification
- Split debug info: `--split-debug-info=build/debug-info`

**Known Issues:**
- Dart AOT compilation doesn't guarantee code obfuscation (use `--obfuscate`)
- Platform views on iOS may have security edge cases

---

## 3. Kotlin Multiplatform (KMP)

**Security Grade: A-**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Kotlin | 2.0.21 | Apache-2.0 | 0 |
| KMP Plugin | 2.0.21 | Apache-2.0 | 0 |
| Ktor | 2.3.12 | Apache-2.0 | 0 |
| SQLDelight | 2.0.2 | Apache-2.0 | 0 |
| Compose Multiplatform | 1.6.11 | Apache-2.0 | 0 |

**Build Configuration:**
```kotlin
// build.gradle.kts
kotlin {
    jvmToolchain(21)
    sourceSets {
        commonMain.dependencies {
            implementation("io.ktor:ktor-client-core:2.3.12")
            implementation("app.cash.sqldelight:runtime:2.0.2")
        }
    }
}
```

**Security Best Practices:**
- Use Ktor's HttpClient with TLS configuration
- SQLDelight for type-safe, injection-proof database access
- Enable R8/ProGuard for Android obfuscation
- Use Security framework for iOS keychain access

---

## 4. Native iOS (Swift)

**Security Grade: A+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Swift | 5.10 | Apache-2.0 | 0 |
| Xcode | 15.4 | Apple SLA | N/A |
| iOS Deployment Target | 16.0+ | N/A | N/A |
| Swift Package Manager | 5.10 | Apache-2.0 | 0 |

**Security Features:**
- App Transport Security (ATS) enforced by default
- Keychain Services for sensitive data
- CryptoKit for cryptographic operations
- Face ID / Touch ID via LocalAuthentication
- App Sandbox (mandatory on iOS)
- Data Protection API (file-level encryption)

**Security Checklist:**
- [ ] Enable ATS (no arbitrary loads)
- [ ] Use Keychain for tokens/credentials
- [ ] Certificate pinning via `URLSessionDelegate`
- [ ] Enable `ENABLE_HARDENED_RUNTIME = YES`
- [ ] Disable `UIFileSharingEnabled` unless needed
- [ ] Use CryptoKit for hashing/encryption
- [ ] Enable App Transport Security exceptions logging

**Dependency Management:**
```swift
// Package.swift — pin versions
dependencies: [
    .package(url: "https://github.com/Alamofire/Alamofire.git", exact: "5.9.1"),
    .package(url: "https://github.com/onevcat/Kingfisher.git", exact: "7.12.0"),
]
```

---

## 5. Native Android (Kotlin)

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Kotlin | 1.9.25 | Apache-2.0 | 0 |
| AGP (Android Gradle Plugin) | 8.2.2 | Apache-2.0 | 0 |
| Target SDK | 34 | Apache-2.0 | N/A |
| Min SDK | 24 | N/A | N/A |
| Compose BOM | 2024.02.00 | Apache-2.0 | 0 |

**Build Configuration:**
```kotlin
// build.gradle.kts
android {
    compileSdk = 34
    defaultConfig {
        minSdk = 24
        targetSdk = 34
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
        }
    }
}
```

**Security Best Practices:**
- Use EncryptedSharedPreferences (Jetpack Security)
- Enable R8/ProGuard for obfuscation
- Network Security Config (certificate pinning)
- BiometricPrompt for authentication
- Play Integrity API for device attestation

```xml
<!-- res/xml/network_security_config.xml -->
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set expiration="2026-12-31">
            <pin digest="SHA-256">base64hash=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

---

## Cross-Cutting Mobile Security Checklist

- [ ] Certificate pinning on all API endpoints
- [ ] Secure storage for tokens/keys (Keychain/KeyStore)
- [ ] Jailbreak/root detection with response strategy
- [ ] Code obfuscation enabled in release builds
- [ ] No sensitive data in logs (debug or production)
- [ ] Proguard/R8 rules reviewed for leaks
- [ ] App binary signing with secure key management
- [ ] Dependency scanning in CI (OWASP Dependency-Check)
- [ ] SAST scanning (Semgrep, MobSF)
- [ ] Binary analysis post-build (MobSF, Ghidra review)

## Comparison Matrix

| Feature | React Native | Flutter | KMP | iOS Native | Android Native |
|---------|-------------|---------|-----|------------|----------------|
| Platform | Cross | Cross | Cross | iOS only | Android only |
| Language | TypeScript | Dart | Kotlin | Swift | Kotlin |
| Bundle Size | ~7MB | ~5MB | ~3MB | ~2MB | ~3MB |
| Secure Storage | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| Obfuscation | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| Code Signing | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Grade** | **A-** | **A** | **A-** | **A+** | **A** |
