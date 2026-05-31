# Game Development Stacks — Security Guide

> Last updated: 2026-05-31 | Stability-first: LTS and battle-tested releases only

---

## 1. Unity 2022 LTS + C# (.NET Standard 2.1)

**Security Score: B+**
**Stability: ★★★★★**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Unity          | 2022.3 LTS| 2025-12   | Long-term support branch       |
| C# / .NET      | .NET Standard 2.1 | — | Limited API surface in IL2CPP |
| IL2CPP         | Current   | Tied      | AOT compilation, prevents JIT |
| Netcode for GO | 1.8.x     | Tied      | Official multiplayer framework |

### Security Checklist

- [ ] Use **IL2CPP** scripting backend (not Mono) — prevents runtime IL manipulation
- [ ] Enable **Managed Stripping Level: High** — removes unused code
- [ ] Obfuscate critical assemblies with `Beebyte.Obfuscator` or equivalent
- [ ] Validate all server inputs — never trust the game client
- [ ] Use **Relay + Lobby** services for multiplayer (no direct IP exposure)
- [ ] Encrypt asset bundles with AES-256 — prevent asset ripping
- [ ] Implement **code integrity checks** (detect modified assemblies)
- [ ] Use Unity's **Anti-Cheat Toolkit** (UACT) or equivalent
- [ ] Sign asset bundles to prevent tampering
- [ ] Never store secrets in `Resources/` or `StreamingAssets/` — they're plaintext in builds

### Asset Pipeline Security

```csharp
// Encrypt asset bundles at build time
public class AssetBundleEncryptor : AssetPostprocessor
{
    private static readonly byte[] EncryptionKey = LoadKeyFromSecureConfig();

    static void OnPostprocessAllAssets(
        string[] imported, string[] deleted,
        string[] moved, string[] movedFrom)
    {
        foreach (string assetPath in imported)
        {
            if (assetPath.EndsWith(".bundle"))
            {
                byte[] data = File.ReadAllBytes(assetPath);
                byte[] encrypted = AesEncrypt(data, EncryptionKey);
                File.WriteAllBytes(assetPath + ".enc", encrypted);
            }
        }
    }

    private static byte[] AesEncrypt(byte[] data, byte[] key)
    {
        using var aes = Aes.Create();
        aes.Key = key;
        aes.GenerateIV();
        using var encryptor = aes.CreateEncryptor();
        byte[] encrypted = encryptor.TransformFinalBlock(data, 0, data.Length);
        // Prepend IV
        byte[] result = new byte[aes.IV.Length + encrypted.Length];
        Buffer.BlockCopy(aes.IV, 0, result, 0, aes.IV.Length);
        Buffer.BlockCopy(encrypted, 0, result, aes.IV.Length, encrypted.Length);
        return result;
    }
}
```

### Multiplayer Security — Server Authority

```csharp
// NEVER trust client state — server validates everything
[ServerRpc(RequireOwnership = false)]
public void MovePlayerServerRpc(Vector3 position, ServerRpcParams rpcParams = default)
{
    ulong clientId = rpcParams.Receive.SenderClientId;

    // Validate: position must be within allowed radius
    Vector3 currentPos = GetPlayerPosition(clientId);
    float maxSpeed = GetPlayerMaxSpeed(clientId);
    float maxDelta = maxSpeed * Time.fixedDeltaTime * 1.1f; // 10% tolerance

    if (Vector3.Distance(position, currentPos) > maxDelta)
    {
        // Cheat detected: teleport or rubber-band
        SetPlayerPosition(currentId, currentPos);
        LogCheatAttempt(clientId, "speed_hack");
        return;
    }

    // Valid move
    ApplyMovement(clientId, position);
}
```

### Build Reproducibility

```bash
# Unity build via CLI for reproducible builds
Unity -batchmode -nographics -projectPath . \
  -buildTarget StandaloneLinux64 \
  -executeMethod BuildScript.Build \
  -logFile build.log \
  -quit

# Store build hash
sha256sum Build/game.x86_64 > Build/game.x86_64.sha256
```

---

## 2. Godot 4.2 + GDScript/C#

**Security Score: B**
**Stability: ★★★★☆**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Godot          | 4.2.2     | Active    | Stable 4.x branch              |
| GDScript       | 2.0       | Tied      | Python-like, interpreted       |
| C# (.NET)      | .NET 6+   | Tied      | Mono runtime in export         |
| GDExtension    | Current   | Tied      | C/C++ native extensions        |

### Security Checklist

- [ ] **GDScript is interpreted** — source is easily extractable from PCK files
- [ ] Encrypt PCK exports with AES-256 (built-in Godot option)
- [ ] Use C# for sensitive logic (compiled IL is harder to reverse than GDScript)
- [ ] Validate all multiplayer RPCs server-side
- [ ] Use **ENet** or **WebSocket** with TLS for networking
- [ ] Never store credentials in project settings — use environment variables
- [ ] Audit GDExtension plugins — native code has full memory access
- [ ] Sign exported executables

### PCK Encryption

```ini
# export_presets.cfg
[preset.0]
name="Linux"
encryption_include_filters="*.gd,*.tscn,*.tres"
encryption_exclude_filters=""
encryption_key="your-64-char-hex-key-here"
encrypt_pck=true
encrypt_directory=true
```

### GDScript Source Protection

```gdscript
# Problem: GDScript is trivially extractable
# Solution: Move sensitive logic to GDExtension (C++)

# gdextension/security_module.gdextension
[entry]
linux.debug = "res://bin/libsecurity.linux.debug.so"
linux.release = "res://bin/libsecurity.linux.release.so"
windows.release = "res://bin/security.windows.release.dll"
```

### Multiplayer RPC Validation

```gdscript
# Server-authoritative movement validation
@rpc("any_peer", "reliable")
func request_move(target_pos: Vector3) -> void:
    if not is_multiplayer_authority():
        return

    var sender_id = multiplayer.get_remote_sender_id()
    var player = get_player(sender_id)

    # Validate movement
    var distance = player.position.distance_to(target_pos)
    var max_move = player.speed * get_physics_process_delta_time() * 1.2

    if distance > max_move:
        # Reject — possible speed hack
        rpc_id(sender_id, "correct_position", player.position)
        return

    player.position = target_pos
```

---

## 3. Unreal Engine 5.4 + C++20

**Security Score: A-**
**Stability: ★★★★★**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Unreal Engine  | 5.4.x     | Active    | Latest stable, proven in AAA   |
| C++            | C++20     | Compiler  | MSVC 14.38+, Clang 15+        |
| UE Networking  | Current   | Tied      | Built-in replication system    |
| EOS            | Current   | Tied      | Epic Online Services           |

### Security Checklist

- [ ] Enable **pak file encryption** (AES-256) in Project Settings
- [ ] Use **shipping build** configuration — strips debug symbols and console
- [ ] Validate all RPC inputs in `UFUNCTION(Server)` handlers
- [ ] Implement **EasyAntiCheat** or **BattlEye** for competitive games
- [ ] Use **SSL certificate pinning** for all HTTP requests
- [ ] Enable `/GS` buffer security checks (default in shipping builds)
- [ ] Use `FMemory::Memcpy` with size validation (no raw `memcpy`)
- [ ] Audit Blueprint exposure — Blueprint-accessible functions expand attack surface
- [ ] Use encrypted pak files + signing to prevent asset extraction

### Server-Authoritative Networking

```cpp
// MyGameCharacter.cpp
void AMyGameCharacter::ServerMove_Implementation(FVector_NetQuantize NewLocation)
{
    // Server validation
    float DeltaTime = GetWorld()->GetDeltaSeconds();
    float MaxDistance = GetCharacterMovement()->MaxWalkSpeed * DeltaTime * 1.15f;

    float ActualDistance = FVector::Dist(GetActorLocation(), NewLocation);
    if (ActualDistance > MaxDistance)
    {
        // Reject and correct
        ClientCorrectPosition(GetActorLocation());
        UE_LOG(LogNet, Warning, TEXT("Speed hack detected: %s"), *GetName());
        return;
    }

    SetActorLocation(NewLocation);
}
```

### Build Security Configuration

```ini
# DefaultEngine.ini — Shipping build hardening
[/Script/UnrealEd.ProjectPackagingSettings]
BuildConfiguration=PPBC_Shipping
bUsePakFile=true
bUseIoStore=true
bEncryptPakFiles=true
PakEncryptionKey=<your-key>
bSignPakFiles=true
```

---

## 4. Bevy 0.13 (Rust ECS)

**Security Score: A**
**Stability: ★★★☆☆**

### Version Matrix

| Component      | Version   | EOL       | Notes                          |
|----------------|-----------|-----------|--------------------------------|
| Bevy           | 0.13.x    | Active    | Rapid iteration, API instability|
| Rust           | 1.76+     | Required  | Memory-safe by default         |
| bevy_replicon  | 0.24      | Community | Popular multiplayer plugin     |

### Security Checklist

- [ ] Rust's ownership model prevents memory corruption by default
- [ ] Use `#[deny(unsafe_code)]` — avoid `unsafe` blocks unless audited
- [ ] Validate all network inputs with `serde` + custom validators
- [ ] Use `tokio` with rate limiting for multiplayer servers
- [ ] Compile with `--release` and `lto = true` for production
- [ ] Audit third-party Bevy plugins — ecosystem is young
- [ ] Use `cargo-audit` and `cargo-deny` in CI for dependency vulnerabilities

### Secure ECS Networking

```rust
use bevy::prelude::*;
use bevy_replicon::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Component, Serialize, Deserialize)]
struct PlayerPosition {
    x: f32,
    y: f32,
    z: f32,
}

// Server-side validation system
fn validate_movement(
    mut commands: Commands,
    players: Query<(Entity, &PlayerPosition, &NetworkOwner)>,
    time: Res<Time>,
) {
    for (entity, pos, owner) in &players {
        // Validate position bounds
        if pos.x.abs() > 10000.0 || pos.y.abs() > 10000.0 || pos.z.abs() > 10000.0 {
            warn!("Invalid position from client {:?}", owner.id);
            commands.entity(entity).insert(Despawn); // Kick
        }
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(ReplicationPlugins)
        .add_systems(Update, validate_movement.run_if(has_authority))
        .run();
}
```

### Anti-Cheat Considerations by Engine

| Engine    | Built-in       | Third-party         | Effectiveness |
|-----------|---------------|---------------------|---------------|
| Unity     | None          | UACT, EAC, BattlEye | Good          |
| Godot     | None          | Manual              | Limited       |
| Unreal    | EOS + EAC     | BattlEye            | Excellent     |
| Bevy      | None          | Manual (Rust safety)| DIY           |

### Mod Security

```csharp
// Unity: Sandboxed mod loading with restricted permissions
public class ModLoader
{
    // Whitelist of allowed API calls for mods
    private static readonly HashSet<string> AllowedTypes = new()
    {
        "UnityEngine.GameObject",
        "UnityEngine.Transform",
        "UnityEngine.MeshRenderer",
        // No: System.IO, System.Net, System.Reflection
    };

    public static Assembly LoadModSafely(byte[] modAssembly)
    {
        // Verify signature
        if (!VerifyModSignature(modAssembly))
            throw new SecurityException("Invalid mod signature");

        // Load in restricted AppDomain / AssemblyLoadContext
        var context = new AssemblyLoadContext("ModContext", isCollectible: true);
        using var stream = new MemoryStream(modAssembly);
        return context.LoadFromStream(stream);
    }
}
```

---

## Cross-Stack Security Comparison

| Stack               | Score | Memory Safety | Anti-Cheat    | Mod Safety | Maturity |
|---------------------|-------|---------------|---------------|------------|----------|
| Unity 2022 LTS      | B+    | Managed (.NET)| Good (plugins)| Moderate   | AAA      |
| Godot 4.2           | B     | GDScript/C#   | Limited       | Weak       | Indie    |
| Unreal Engine 5.4   | A-    | C++ (manual)  | Excellent     | Good       | AAA      |
| Bevy 0.13           | A     | Rust (safe)   | DIY           | Strong     | Hobby    |

## Recommendations

1. **Competitive multiplayer**: Unreal 5.4 with EAC/BattlEye — best built-in anti-cheat
2. **Indie/single-player**: Unity 2022 LTS — largest ecosystem, proven stability
3. **Open-source priority**: Godot 4.2 — MIT licensed, growing community
4. **Maximum safety**: Bevy (Rust) — memory-safe by design, but immature ecosystem
5. **Server-authoritative architecture**: Mandatory for ALL multiplayer games regardless of engine
