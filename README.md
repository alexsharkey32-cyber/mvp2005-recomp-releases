# MVP Baseball 2005 Recomp

A native PC, Mac and Linux version of **MVP Baseball 2005** (PlayStation 2). This isn't an emulator: the game's
own code was translated ("statically recompiled") from the PS2 program into C++ and runs directly on your
computer, with modern graphics on top: up to 6x resolution, widescreen and ultrawide, high frame rates and an HD
texture pack.

**You need your own copy of the game.** Only the USA disc works (NTSC-U, **SLUS-21135**), as a 1:1 `.iso`. No
game code or data from EA is in the downloads below; the game reads everything from your disc.

## Download and play

1. Get the latest release from the [Releases page](../../releases/latest):
   | Your computer | File | Needs |
   |---|---|---|
   | Mac (Apple Silicon) | `MVPBaseball2005-…-mac.zip` | macOS 11 or later |
   | Windows (beta) | `MVPBaseball2005-…-windows.zip` | Windows 10 (1803) or later, 64-bit |
   | Linux (beta) | `MVPBaseball2005-…-linux-x64.tar.gz` | 64-bit, a 2022 or newer distribution |
2. Unzip it and start **MVP Baseball 2005**.
   - Mac: the first time, right-click the app and choose **Open** (it isn't signed by Apple).
   - Windows: unzip somewhere you can write to (not Program Files). If SmartScreen warns, choose **More info > Run anyway**.
3. **Setup** opens on the first start:
   - **Your disc:** choose your `.iso` or drag it onto the window. The game checks it is the USA version and tells
     you exactly what's wrong if it isn't. `.chd` and `.cso` images must be turned back into `.iso` first.
   - **Features:** tick what you want. Setup shows each one's size, the free space on your drive and a preview,
     then downloads, checks and installs them. You can add or remove features later from *Disc & Features*.
4. Press **Play Ball**.

## Features

**The game**
- Runs natively at full speed: no emulator, short loading, saves on disk
- Up to 6x internal resolution (3072 x 2688), FXAA, sharpening, 16x anisotropic filtering
- Widescreen through EA's hidden 16:9 mode, plus 16:10, 21:9, 32:9 and "match my display", with an optional
  16:9-shaped HUD on ultrawide screens
- Frame rates from 30 to 360 fps (or match your monitor) with real-time game speed, so 120 fps is smoother, not faster
- Graphics presets from Original (as on PS2) to Remastered; Metal, Vulkan or OpenGL
- Borderless or exclusive fullscreen, monitor choice, VSync, FPS counter
- A launcher with your home team's ballpark, leagues and eras, and every setting with a live preview
- Your own music in the menus (MP3, M4A, FLAC, WAV)
- Keyboard, mouse and any gamepad

**Optional downloads** (installed from Setup)
| Feature | Size | What it is |
|---|---|---|
| Today's rosters (2026) | 160 MB | every club's current players, ratings from real stats, managers and schedule; commentators say 850 new names |
| Player portraits | 660 MB | a rendered portrait for every current player |
| Today's uniforms | 11 MB | each club's closest match to what it wears today |
| Today's ballparks | 11 MB | current park names and fence distances |
| 2026 rules for CPU play | 3 MB | no shifts, pitch clock pace, more steals, universal DH |
| Varied head shapes | 1 MB | generic players stop looking alike |
| Seasons from history | 0.3-0.7 GB each | 13 eras from 1910 to 2019, each with its own league |
| HD texture pack, 4x | 44 GB | every texture on the disc redrawn at 4x |
| HD texture pack, 2x | 11 GB | the same at 2x, for less disk space |

## Build it yourself

You need the source code ([mvp-2005-recomp-source](https://github.com/alexsharkey32-cyber/mvp-2005-recomp-source)) and your own disc. The recompiled C++ is made on your machine from the game program on
your disc, so nothing from the game has to be downloaded.

### 1. Tools

| | Install |
|---|---|
| Mac | `xcode-select --install`, then with [Homebrew](https://brew.sh): `brew install sdl2 cmake ninja python molten-vk vulkan-headers` |
| Linux (Debian/Ubuntu) | `sudo apt install build-essential cmake ninja-build python3 libsdl2-dev libvulkan-dev` |
| Windows | Install [MSYS2](https://www.msys2.org), open **MSYS2 UCRT64**, then `pacman -S mingw-w64-ucrt-x86_64-{gcc,cmake,ninja,SDL2,vulkan-headers,python}` |

### 2. Source and your game program

```sh
git clone https://github.com/alexsharkey32-cyber/mvp-2005-recomp-source.git
cd mvp-2005-recomp-source
python3 tools/extract_iso.py "/path/to/MVP Baseball 2005 (USA).iso"   # copies SLUS_211.35 into game/
python3 tools/recomp/ee_recomp.py                                     # writes the C++ into generated/ (a minute)
```

### 3. Build

```sh
cmake -S . -B out -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build out
```

The first build compiles about 30,000 recompiled functions and takes 5-20 minutes. The program is `out/mvp2005`
(`out/mvp2005.exe` on Windows). On a Mac or Linux, `make -j8` does the same in one step.

### 4. Run

```sh
./out/mvp2005
```

It opens the Setup like the downloads do. Useful options: `--play` skips the launcher, `--iso <file>` picks a
disc image, `--features` lists the optional downloads and `--features install <id>` installs one from the command line.

### Packaging (optional)

`tools/release/package_mac.sh`, `package_windows.sh` and `package_linux.sh` turn a build into the same zip files
as the Releases page. `.github/workflows/build.yml` builds all three on GitHub.

## Questions

- **Does my European or Japanese disc work?** No. The game's code was recompiled from the USA disc only.
- **The game doesn't find Vulkan.** It falls back to OpenGL by itself. Vulkan needs a driver that supports it.
- **Where are my saves and settings?** Next to the program on Windows and Linux; on a Mac in
  `~/Library/Application Support/MVP Baseball 2005 Recomp`.

MVP Baseball 2005 is a trademark of Electronic Arts. This is a fan project, not made or endorsed by EA or MLB.
