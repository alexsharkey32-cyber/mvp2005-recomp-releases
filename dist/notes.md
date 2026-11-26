> **Mac comes at the beginning of next month.** The Mac package, with the Mac speed fixes below, will be added at the start of December.

## Speed

- **OpenGL shows every frame (Linux especially).** With OpenGL (Linux's default renderer, or chosen in Settings), the screen only got about 15 new pictures a second while the game ran at 60. The finished frame is now kept for the window: 55–60 pictures a second.
- **Mac (in the December Mac build).** The game's threads now ask macOS for the fast cores. On Apple Silicon they could run on the slower efficiency cores, and drawing work was split across all cores, so the slow ones held every frame back.
- **Linux on hybrid CPUs.** Drawing work is split over the fast cores only.

## Fixes

- **No more freezes after clicking back into the window.** "Pause in the background" could miss your return and leave the game frozen. Now any key, click or controller button resumes it too.
- **Fast forward toggle.** Shift+Tab keeps fast forward on until you press Tab again. Holding Tab still works as before.

## Updating

- **From v1.4.2 or later:** choose **Install** in the launcher when v1.5.1 appears, then **Restart**.
- **From v1.4.1 or earlier:** download the package for your system under **Assets** and extract it.

Your disc, saves, settings and installed packs stay where they are.
