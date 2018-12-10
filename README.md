# ParticlePy

## Project structure

There are two folders: `detector` is for code related to using the Raspberry Pi to detect muons, and `analysis` is for code related to analysing the data from muon detectors in the lab. Each folder uses a `data` subfolder to store data separately from the code. The data in `analysis/data` is tracked by Git.

Some code in the `detector` folder will not run unless your device is a Raspberry Pi with PiCamera.

## Windows and Linux

Most instructions are for Windows - on Linux you will need to replace `python` and `pip` with `python3` and `pip3` but the general setup process should be simpler.

## Preparing your system

You must install Python 3.5 or higher. Verify that `python` and `pip` are in the path by opening a terminal (on Windows, press Win+X followed by I where Win is the Windows key) and running `python --version` and `pip freeze`. If either command causes an error, add the Python installation folder and its `Scripts` subdirectory to the path and open a new terminal.

You will also need to install the required dependencies, by opening an administrator terminal (on Windows, press Win+X followed by A), and running the command `pip install numpy scipy matplotlib imageio`. 

You are recommended to [install VS Code](https://code.visualstudio.com/Download) as an editor, and you can then use the suggested Python extension in VS Code.

## Downloading the code

The best way is to use Git, if you may wish to make changes to the code. You can [download Git here](https://git-scm.com/download/win) for Windows. 

After installing Git, open a new terminal in a desired folder (on Windows, hold shift while right-clicking when viewing the folder, then click "open Powershell window here") and run `git clone https://github.com/TheGreatCabbage/ParticlePy.git`. 

Git will create a folder and download the code into it. You can then open VS Code in the folder by running `code ParticlePy` if the folder is named `ParticlePy`.

## Running the code

To run some code, open a terminal in the same folder as the file. In VS Code, just click *Terminal->New Terminal* and then `cd` into the correct subdirectory - e.g. `cd analysis`. On Windows, you could also hold shift while right-clicking when viewing the folder, then click "open Powershell window here".)

Then you can run `python file.py` where `file.py` is the code you wish to execute. You could instead use the *Code runner* extension in VS Code while the correct file is opened.

If this causes an error, you may be in the wrong directory (in this case, use `cd` to change directories - e.g `cd analysis` to change from `ParticlePy` to `ParticlePy/analysis`).