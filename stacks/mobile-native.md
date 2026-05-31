# Native Mobile & Cross-Platform Deep Dive

> **Philosophy**: Stability-first versions. Security is non-negotiable on mobile — devices are untrusted environments. Every stack below assumes hostile networks, rooted/jailbroken devices, and adversarial users.

---

## Table of Contents

1. [Android Native](#android-native)
2. [Android with AI](#android-with-ai)
3. [iOS Native](#ios-native)
4. [iOS with AI](#ios-with-ai)
5. [HarmonyOS](#harmonyos)
6. [uni-app (Cross-Platform)](#uni-app-cross-platform)
7. [Kotlin Multiplatform](#kotlin-multiplatform)
8. [Shared Security Patterns](#shared-security-patterns)
9. [OTA Update Security](#ota-update-security)
10. [Supply Chain Verification](#supply-chain-verification)

---

## Android Native

### Core Stack
- **Language**: Kotlin 2.0 (stable, K2 compiler)
- **Build**: Gradle 8.5 + AGP 8.2
- **UI**: Jetpack Compose (Material 3)
- **Min SDK**: 24 (Android 7.0) — covers 98%+ active devices
- **Target SDK**: 34 (Android 14)
- **Architecture**: MVVM + Hilt DI + Navigation Compose

### Dependencies (Stability-Pinned)
```kotlin
// build.gradle.kts
plugins {
    id("com.android.application") version "8.2.2"
    id("org.jetbrains.kotlin.android") version "2.0.0"
    id("com.google.devtools.ksp") version "2.0.0-1.0.21"
}

dependencies {
    // Jetpack BOM — pins all Jetpack libs to compatible versions
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")
    
    // Lifecycle + ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    
    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.7")
    
    // Networking
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-kotlinx-serialization:2.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
    
    // Image loading
    implementation("io.coil-kt:coil-compose:2.6.0")
    
    // DI
    implementation("com.google.dagger:hilt-android:2.50")
    ksp("com.google.dagger:hilt-compiler:2.50")
    
    // Database
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")
    
    // Security
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
    implementation("net.zetetic:android-database-sqlcipher:4.5.6")
}
```

### Secure Storage
```kotlin
// EncryptedSharedPreferences for tokens/secrets
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val securePrefs = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Android Keystore for cryptographic keys
val keyPairGenerator = KeyPairGenerator.getInstance(
    KeyProperties.KEY_ALGORITHM_RSA, "AndroidKeyStore"
)
keyPairGenerator.initialize(
    KeyGenParameterSpec.Builder("key_alias",
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
        .setDigests(KeyProperties.DIGEST_SHA256, KeyProperties.DIGEST_SHA512)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_RSA_OAEP)
        .setUserAuthenticationRequired(true)
        .setUserAuthenticationParameters(300, KeyProperties.AUTH_BIOMETRIC_STRONG)
        .build()
)
```

### Certificate Pinning
```kotlin
// OkHttp Certificate Pinning
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.example.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // backup pin
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

// Network Security Config (res/xml/network_security_config.xml)
// <network-security-config>
//     <domain-config>
//         <domain includeSubdomains="true">api.example.com</domain>
//         <pin-set expiration="2025-12-31">
//             <pin digest="SHA-256">AAAAAAAAAAAAAAAA...</pin>
//             <pin digest="SHA-256">BBBBBBBBBBBBBBBB...</pin>
//         </pin-set>
//     </domain-config>
//     <base-config cleartextTrafficPermitted="false" />
// </network-security-config>
```

### Code Obfuscation
```groovy
// proguard-rules.pro
-keepattributes Signature
-keepattributes *Annotation*

# Keep data classes for serialization
-keep class com.example.api.** { *; }

# Obfuscate everything else
-repackageclasses ''
-allowaccessmodification
-overloadaggressively

# R8 full mode (aggressive)
android.enableR8.fullMode=true
```

### Build Integrity
```kotlin
// Verify APK signature at runtime
fun verifyAppSignature(context: Context): Boolean {
    val packageInfo = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
        context.packageManager.getPackageInfo(
            context.packageName, PackageManager.GET_SIGNING_CERTIFICATES
        )
    } else {
        @Suppress("DEPRECATION")
        context.packageManager.getPackageInfo(
            context.packageName, PackageManager.GET_SIGNATURES
        )
    }
    
    val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
        packageInfo.signingInfo.apkContentsSigners
    } else {
        @Suppress("DEPRECATION")
        packageInfo.signatures
    }
    
    val cert = signatures[0].toByteArray()
    val md = MessageDigest.getInstance("SHA-256")
    val digest = md.digest(cert)
    val expectedHash = "YOUR_EXPECTED_HASH_HERE"
    
    return Base64.encodeToString(digest, Base64.NO_WRAP) == expectedHash
}
```

---

## Android with AI

### On-Device AI Stack
- **Gemini Nano**: On-device LLM (Android AICore, Pixel 8+ / Galaxy S24+)
- **ML Kit**: Vision, NLP, barcode scanning
- **TensorFlow Lite**: Custom models, GPU delegate
- **MediaPipe**: Real-time ML pipelines (pose, face, hand tracking)

### TFLite with Security
```kotlin
// Encrypted model loading
fun loadEncryptedModel(context: Context, modelName: String): MappedByteBuffer {
    val encryptedModel = context.assets.open("$modelName.tflite.enc")
    val key = getDecryptionKey() // from AndroidKeyStore
    
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(128, iv))
    
    val encryptedBytes = encryptedModel.readBytes()
    val decryptedBytes = cipher.doFinal(encryptedBytes)
    
    return ByteBuffer.wrap(decryptedBytes).order(ByteOrder.nativeOrder())
}

// TFLite Interpreter with GPU delegate
val options = Interpreter.Options().apply {
    addDelegate(GpuDelegate())
    setNumThreads(4)
}
val interpreter = Interpreter(loadEncryptedModel(context, "mobilenet_v3"), options)
```

### ML Kit Security
```kotlin
// On-device text recognition (no data leaves device)
val recognizer = TextRecognition.getClient(ChineseTextRecognizerOptions.Builder().build())
val image = InputImage.fromBitmap(bitmap, 0)
recognizer.process(image)
    .addOnSuccessListener { text ->
        // Process locally — never send raw images to server
        processLocally(text)
    }
```

### Gemini Nano Security
```kotlin
// Gemini Nano via Android AICore
// Ensure sensitive prompts never leave device
val generativeModel = GenerativeModel(
    modelName = "gemini-nano",
    // Runs entirely on-device via AICore
)

// NEVER log prompts containing user data
// Rate-limit inference calls to prevent abuse
// Validate all model outputs before display
```

---

## iOS Native

### Core Stack
- **Language**: Swift 5.10
- **IDE**: Xcode 15.4
- **UI**: SwiftUI + UIKit interop where needed
- **Min iOS**: 16.0 — covers 90%+ active devices
- **Architecture**: MVVM + SwiftUI + async/await

### Dependencies (SPM)
```swift
// Package.swift or Xcode SPM
dependencies: [
    .package(url: "https://github.com/Alamofire/Alamofire.git", exact: "5.9.1"),
    .package(url: "https://github.com/kean/Nuke.git", exact: "12.8.0"),
    .package(url: "https://github.com/realm/SwiftLint.git", exact: "0.54.0"),
    .package(url: "https://github.com/stephencelis/SQLite.swift.git", exact: "0.15.3"),
]
```

### Secure Storage — Keychain
```swift
import Security

class KeychainManager {
    static func save(key: String, value: String) -> Bool {
        let data = value.data(using: .utf8)!
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]
        SecItemDelete(query as CFDictionary) // Remove old value
        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }
    
    static func load(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess, let data = result as? Data else { return nil }
        return String(data: data, encoding: .utf8)
    }
}

// Keychain Access Control with biometrics
func saveWithBiometric(key: String, value: String) -> Bool {
    let access = SecAccessControlCreateWithFlags(
        nil,
        kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
        .biometryCurrentSet,
        nil
    )!
    let data = value.data(using: .utf8)!
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: key,
        kSecValueData as String: data,
        kSecAttrAccessControl as String: access
    ]
    SecItemDelete(query as CFDictionary)
    return SecItemAdd(query as CFDictionary, nil) == errSecSuccess
}
```

### Certificate Pinning
```swift
import Alamofire

// Custom server trust manager with pinning
class PinnedServerTrustManager: ServerTrustManager {
    override func serverTrust(
        forHost host: String,
        in session: URLSession
    ) -> ServerTrust? {
        guard let trust = super.serverTrust(forHost: host, in: session) else {
            return nil
        }
        return trust
    }
}

// Using URLSession with pinning
class PinningDelegate: NSObject, URLSessionDelegate {
    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        guard let serverTrust = challenge.protectionSpace.serverTrust,
              let certificate = SecTrustGetCertificateAtIndex(serverTrust, 0) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }
        
        let serverCertData = SecCertificateCopyData(certificate) as Data
        let serverCertHash = sha256(data: serverCertData)
        
        // Pin against embedded certificate hash
        let pinnedHashes = [
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
            "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
        ]
        
        if pinnedHashes.contains(serverCertHash) {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```

### App Transport Security
```xml
<!-- Info.plist -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
    <key>NSExceptionDomains</key>
    <dict>
        <key>api.example.com</key>
        <dict>
            <key>NSExceptionRequiresForwardSecrecy</key>
            <true/>
            <key>NSRequiresCertificateTransparency</key>
            <true/>
        </dict>
    </dict>
</dict>
```

---

## iOS with AI

### Core ML Stack
- **Core ML 8**: On-device inference, GPU/Neural Engine
- **Create ML**: Model training on Mac
- **Vision**: Image analysis, OCR, face detection
- **NaturalLanguage**: Text analysis, sentiment

### Secure Model Loading
```swift
import CoreML

// Encrypt model at rest, decrypt only when needed
func loadSecureModel(named name: String) throws -> MLModel {
    let modelURL = Bundle.main.url(forResource: name, withExtension: "mlmodelc")!
    
    // Verify model integrity before loading
    let modelData = try Data(contentsOf: modelURL)
    let hash = SHA256.hash(data: modelData)
    let expectedHash = "YOUR_EXPECTED_HASH"
    guard hash.map({ String(format: "%02x", $0) }).joined() == expectedHash else {
        throw SecurityError.modelIntegrityFailure
    }
    
    let config = MLModelConfiguration()
    config.computeUnits = .cpuAndNeuralEngine // Prefer Neural Engine
    return try MLModel(contentsOf: modelURL, configuration: config)
}

// Vision framework — all processing on-device
func analyzeImage(_ image: CGImage) {
    let request = VNRecognizeTextRequest { request, error in
        guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
        // Process locally — never upload images to cloud
        for observation in observations {
            let text = observation.topCandidates(1).first?.string ?? ""
            processLocally(text)
        }
    }
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    try? handler.perform([request])
}
```

---

## HarmonyOS

### Core Stack
- **Language**: ArkTS (TypeScript superset for HarmonyOS)
- **SDK**: HarmonyOS NEXT SDK (API 12+)
- **IDE**: DevEco Studio 5.0
- **UI**: ArkUI (declarative)
- **Min Target**: HarmonyOS NEXT 5.0

### ArkTS Security Patterns
```typescript
// Secure storage using HUKS (Huawei Universal Keystore Service)
import { huks } from '@ohos.security.huks';

async function generateKey(alias: string): Promise<void> {
    const properties: huks.HuksParam[] = [
        { tag: huks.HuksTag.HUKS_TAG_ALGORITHM, value: huks.HuksKeyAlg.HUKS_ALG_AES },
        { tag: huks.HuksTag.HUKS_TAG_KEY_SIZE, value: huks.HuksKeySize.HUKS_AES_KEY_SIZE_256 },
        { tag: huks.HuksTag.HUKS_TAG_PURPOSE, value: 
            huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_ENCRYPT | 
            huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_DECRYPT },
        { tag: huks.HuksTag.HUKS_TAG_BLOCK_MODE, value: huks.HuksKeyBlockMode.HUKS_MODE_GCM },
        { tag: huks.HuksTag.HUKS_TAG_PADDING, value: huks.HuksKeyPadding.HUKS_PADDING_NONE },
    ];
    
    const options: huks.HuksOptions = { properties };
    await huks.generateKeyItem(alias, options);
}

// Certificate pinning
import { security } from '@ohos.net.security';

async function secureRequest(url: string): Promise<string> {
    const sslConfig: security.SSLConfig = {
        certificates: [rawFile('certs/pinned.cer')],
    };
    // ... make request with pinned cert
}
```

### App Signature Verification
```typescript
import { bundleManager } from '@ohos.bundle.bundleManager';

async function verifyAppSignature(): Promise<boolean> {
    const bundleInfo = await bundleManager.getBundleInfo(
        'com.example.app',
        bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_SIGNATURES
    );
    const certHash = await hashSignature(bundleInfo.signatureInfo.certificate);
    return certHash === 'YOUR_EXPECTED_HASH';
}
```

---

## uni-app (Cross-Platform)

### Core Stack
- **Framework**: Vue 3 + uni-app 3.x
- **Language**: TypeScript 5.3
- **Build**: Vite 5 + uni-cli
- **Targets**: HBuilderX or CLI builds for Android, iOS, HarmonyOS, WeChat Mini Program, Alipay Mini Program, Huawei Quick App, Web

### Why uni-app
- Single codebase → all Chinese app stores (小米, 华为, OPPO, vivo, 魅族, etc.)
- Native rendering on mobile (not WebView for core components)
- Massive market reach in China ecosystem

### Security Configuration
```typescript
// uni-app secure storage wrapper
// Uses native Keychain (iOS) / Keystore (Android) behind the scenes

import { SecureStorage } from '@/utils/secure-storage';

const storage = new SecureStorage();

// Store sensitive data
await storage.set('auth_token', token);
await storage.set('refresh_token', refreshToken);

// uni.request with SSL pinning (native plugin required)
uni.request({
    url: 'https://api.example.com/data',
    method: 'GET',
    sslVerify: true,
    // Use native plugin for certificate pinning
    // dcloudio/uni-ssl-pinning
    success: (res) => { /* ... */ }
});
```

### Code Obfuscation
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import obfuscator from 'rollup-plugin-obfuscator';

export default defineConfig({
    plugins: [
        obfuscator({
            options: {
                compact: true,
                controlFlowFlattening: true,
                controlFlowFlatteningThreshold: 0.75,
                deadCodeInjection: true,
                deadCodeInjectionThreshold: 0.4,
                stringArray: true,
                stringArrayEncoding: ['base64'],
                stringArrayThreshold: 0.75,
                transformObjectKeys: true,
                unicodeEscapeSequence: false
            }
        })
    ]
});
```

### Supply Chain Security
```json
// package.json — pin exact versions, no ^ or ~
{
    "dependencies": {
        "@dcloudio/uni-app": "3.0.0-4020120250310001",
        "@dcloudio/uni-ui": "1.4.28",
        "vue": "3.4.21",
        "typescript": "5.3.3"
    },
    "overrides": {
        "semver": "7.6.0"
    }
}
```

---

## Kotlin Multiplatform

### Core Stack
- **KMP**: Kotlin 2.0 with Compose Multiplatform 1.6
- **Targets**: Android, iOS, Desktop, Web (WASM)
- **Shared**: Business logic, networking, database, models
- **Native**: Platform UI (optional: shared Compose UI)

### KMP Security — Shared Module
```kotlin
// shared/src/commonMain/kotlin/SecureStorage.kt
expect class SecureStorage() {
    suspend fun save(key: string, value: string)
    suspend fun load(key: string): String?
    suspend fun delete(key: string)
}

// shared/src/androidMain/kotlin/SecureStorage.kt
actual class SecureStorage actual constructor() {
    private val prefs = EncryptedSharedPreferences.create(/* ... */)
    actual suspend fun save(key: String, value: String) = prefs.edit().putString(key, value).apply()
    actual suspend fun load(key: String): String? = prefs.getString(key, null)
    actual suspend fun delete(key: String) = prefs.edit().remove(key).apply()
}

// shared/src/iosMain/kotlin/SecureStorage.kt
actual class SecureStorage actual constructor() {
    actual suspend fun save(key: String, value: String) {
        val query = mapOf(
            kSecClass to kSecClassGenericPassword,
            kSecAttrAccount to key,
            kSecValueData to value.encodeToByteArray().toNSData(),
            kSecAttrAccessible to kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        )
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, null)
    }
    // ... load, delete similarly
}
```

### Shared Networking with Pinning
```kotlin
// shared/src/commonMain/kotlin/NetworkModule.kt
fun createHttpClient(): HttpClient {
    return HttpClient {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true; isLenient = true })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
            connectTimeoutMillis = 10_000
        }
        // Platform-specific certificate pinning
        install(getPlatformPinningPlugin())
        
        install(Logging) {
            level = if (isDebugBuild()) LogLevel.BODY else LogLevel.NONE
            // NEVER log in production
        }
    }
}
```

---

## Shared Security Patterns

### Biometric Authentication (All Platforms)
```kotlin
// Android
val biometricPrompt = BiometricPrompt(activity, executor,
    object : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            // Access crypto object for decryption
            val cryptoObject = result.cryptoObject
        }
    })

val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Authenticate")
    .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG)
    .setNegativeButtonText("Cancel")
    .build()

biometricPrompt.authenticate(promptInfo)
```

### Root/Jailbreak Detection
```kotlin
// Android — multi-signal detection
fun isDeviceCompromised(context: Context): Boolean {
    val checks = listOf(
        checkSuBinary(),
        checkBusyBox(),
        checkSuperUserApk(),
        checkDangerousApps(context),
        checkRWPaths(),
        checkTestKeys(),
        checkMagisk()
    )
    return checks.any { it }
}
```

### Secure Logging
```kotlin
// NEVER log sensitive data in production
object SecureLog {
    private val isDebug = BuildConfig.DEBUG
    
    fun d(tag: String, message: String) {
        if (isDebug) Log.d(tag, message.sanitize())
    }
    
    private fun String.sanitize(): String {
        return this
            .replace(Regex("(token|password|secret|key)[=:]\\s*\\S+", RegexOption.IGNORE_CASE), "[REDACTED]")
            .replace(Regex("\\b\\d{16}\\b"), "[REDACTED_CARD]")
            .replace(Regex("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"), "[REDACTED_EMAIL]")
    }
}
```

---

## OTA Update Security

### Rules for All Platforms
1. **Never auto-update without user consent** (except critical security patches)
2. **Always verify signatures** on update packages before applying
3. **Use HTTPS with certificate pinning** for update checks
4. **Rollback capability** — keep previous version intact until update confirmed stable
5. **Differential updates** — minimize download size, reduce attack surface
6. **Code signing** — all update bundles must be signed by your organization's key

### Android App Bundle / Play Feature Delivery
```kotlin
// Use Play Core for secure dynamic feature delivery
val manager = SplitInstallManagerFactory.create(context)
// Updates are verified by Google Play infrastructure
```

### iOS (No OTA for native code)
- Hot code push only possible via WebView-based solutions (Capacitor, Cordova)
- Apple's TestFlight for beta distribution
- MDM for enterprise deployment
- **Never bypass App Store review** — it's your last security gate

---

## Supply Chain Verification

### All Platforms
```bash
# Verify dependency integrity
# Android — Gradle dependency verification
# gradle/verification-metadata.xml
./gradlew --write-verification-metadata sha256

# iOS — SPM checksum verification
swift package compute-checksum YourLibrary.xcframework.zip

# npm (for uni-app / web)
npm audit
npm ls --all # check for unexpected dependencies
```

### Build Reproducibility
```kotlin
// Android — enable reproducible builds
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
        }
    }
    packagingOptions {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}
```

---

## Security Audit Checklist (All Platforms)

- [ ] Certificate pinning implemented with backup pins
- [ ] All sensitive data stored in platform secure storage (Keychain/Keystore/HUKS)
- [ ] Root/jailbreak detection active
- [ ] Debugger detection in release builds
- [ ] Code obfuscation enabled (R8/ProGuard for Android, Bitcode for iOS)
- [ ] No hardcoded secrets, API keys, or tokens in source
- [ ] SSL/TLS 1.3 enforced, no cleartext traffic
- [ ] Biometric auth for sensitive operations
- [ ] Screenshot/screen recording prevention for sensitive screens
- [ ] Clipboard data auto-clear for sensitive content
- [ ] Deep link validation (no open redirect vulnerabilities)
- [ ] WebView security (no JavaScript injection, restricted URL loading)
- [ ] Intent/URL scheme validation
- [ ] Dependency audit passed (no known CVEs)
- [ ] App signature verification at runtime
- [ ] Secure logging (no PII in production logs)
- [ ] Rate limiting on API calls
- [ ] Offline data encryption (SQLCipher / encrypted Realm)
- [ ] Memory scrubbing for sensitive data after use
- [ ] Tamper detection and response

---

*Last updated: 2026-05-31*
*Principle: Devices are hostile environments. Defense in depth.*
