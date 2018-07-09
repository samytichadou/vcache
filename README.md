# vcache

Doing animation on Blender, even with optimisation (simplify, anim per character/layer…), can be tedious when framerate drops down, and doing a playblast (open gl render) can sometimes be time consuming too (output settings…)

VCache is an addon for blender to quickly playblast your viewport without any configuration !

Its features :

- quick cache with selected format
- automatically play generated cache
- purge cache operators
- draft mode
- Only Render Mode
- Camera Override Mode
- Detecting and Filling missing frames in sequence (through ffmpeg)
- Ability to use external player which support image sequence (like DJView…)

The entire addon UI is a simple Pie Menu, and a few shortcuts, here they are :

- Alt + Y : Cache current viewport (and play after caching if this option is set in user prefs)
- Ctrl + Alt + Y : Pie Menu
- Ctrl + Y : Play the corresponding cache (cache are stored per project)
- Shift + Y : Call Scene Settings Menu (draft, camera, only render)


Here's a quick how to video :
https://www.youtube.com/watch?v=ul6rT6f-C1Q&feature=youtu.be
