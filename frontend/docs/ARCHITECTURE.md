# PolyGen Frontend Architecture & Rendering Pipeline
*Author: Kailash-18 (Frontend Lead)*

## Tech Stack
- **Framework**: React 19 + TypeScript + Vite 8
- **3D Canvas**: `@react-three/fiber` (Three.js WebGL binding)
- **Viewport Helpers**: `@react-three/drei` (OrbitControls, Grid, Center, Html)
- **State Management**: React Context (`AuthContext`, `ThemeContext`)
- **Styling**: Modern CSS3 Tokens with responsive dark and light mode themes

## Architecture Diagram
```
+--------------------------------------------------------+
|                     PolyGen App                        |
|  +--------------------------------------------------+  |
|  |             Theme & Auth Providers               |  |
|  +--------------------------------------------------+  |
|                           |                            |
|       +-------------------+-------------------+        |
|       |                                       |        |
|  [Unauthenticated]                      [Authenticated]|
|  LoginDashboard                        AuthenticatedStudio
|                                               |
|                    +--------------------------+----+
|                    |               |               |
|                Navbar           Scene3D       StatsCard
|                                (WebGL R3F)    (Telemetry)
|                                    |
|                       +------------+------------+
|                       |                         |
|                 LoadedModel              CameraRig
|              (PBR / Clay / Wire)      (CAD Presets & Easing)
+--------------------------------------------------------+
```

## Security & Access Control
- Full-page authentication barrier blocks unauthenticated canvas rendering.
- Session persistence via `localStorage` with token validation.
