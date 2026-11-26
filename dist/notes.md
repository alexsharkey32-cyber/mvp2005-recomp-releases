> **Mac comes at the beginning of next month.** The Mac package will be added at the start of December.

## Smoother play

- **No more hitches from disc reads.** When reading the disc image took a moment (a hard drive seeking or waking up, antivirus scanning the file), the whole game froze until it was done – about a third of a second, several times an inning, which showed up as drops to 40–50 fps. Disc reads now happen in the background and the game keeps running, as it did on the PS2.
- **Fewer disc seeks.** The game streams crowd noise, music and commentary in small pieces from different parts of the disc. Each piece used to be its own read (a seek on a hard drive); the game now reads ahead 256 KB at a time, and keeps era/stadium pack files open instead of reopening them for every read.
- **The log explains slow frames.** If a frame takes too long, `mvp2005.log` now says what it waited for. Handy when reporting a stutter.

## Controllers on Linux (Steam Deck, Steam Machine)

- **Every connected controller works.** Pads that appear after the game starts (Steam Input creates its virtual controller around launch) are picked up, unplugging one no longer drops the others, and unknown pads get a standard layout. Steam's raw controller devices are left to Steam, so presses aren't doubled.
- **Uses your system's SDL when it is newer.** The Linux package carries an older SDL so it runs everywhere. If your system has a newer one (SteamOS and current distributions do), the game now uses it: it knows the newest controllers and works with Steam's controller settings. The log names the SDL in use; set `MVP_BUNDLED_SDL=1` to keep the packaged one.
- **Controller input in Steam game mode** keeps working even if the window is reported as unfocused.

## Updating

- **From v1.4.2 or later:** choose **Install** in the launcher when v1.5.2 appears, then **Restart**.
- **From v1.4.1 or earlier:** download the package for your system under **Assets** and extract it.

Your disc, saves, settings and installed packs stay where they are.
