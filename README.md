# NoCap
A parametric circular MX keycap optimised for FDM 3D printing. Based on [Fake1](https://www.thingiverse.com/thing:4917086) keycaps.

This keycap uses a rectangular stem shaft which is much easier to print on FDM printers even with a 0.4mm nozzle. It is parametric so you may adjust the tolerances for your own specific printer, or adjust the size, top edge fillet, etc.

<img src="https://user-images.githubusercontent.com/1266473/230948285-6babcf5c-bc04-4d4a-8a9e-c2aa203232a2.png" width="400" />

This model was designed using [build123d](https://github.com/gumyr/build123d). To tweak the parameters of this model, you should install either [OCP CAD Viewer for VS Code](https://github.com/bernhard-42/vscode-ocp-cad-viewer), or a development build of [this fork of CQ-Editor](https://github.com/jdegenstein/jmwright-CQ-Editor#development-packages). You can then open the `NoCap.py` file in VS Code or CQ-Editor, modify the parameters at the top of the file as needed, run the script, and the updated model will be outputted to `NoCap.step` and `NoCap.stl`.

A STEP file is also included in this repository for those who would prefer to
edit the model using their CAD package of choice.
