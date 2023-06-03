# df_player_mini_micropython
simple example to play .mp3 continuously on df player and pi pico.

df player mini requrements:
1. files should be named 001.mp3, 002.mp3 etc.
2. sd card limit is 32 Gb

You can create multiple folder and name them 01, 02 etc.
In this case you need to modify next_track() functions.
In this example next_track() is only working in "root" folder - #1.

Features/fixes currently in progress:
  1. issue with not playing after reaching last song in folder
  2. add folders support
