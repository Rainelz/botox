# Botox

Simple tray app to manage credentials injection

## Prerequisites

- tcl-tk `brew install tcl-tk`

## Installation

1. Move Botox.app -> Applications
2. Launch Botox
3. Customize your touchbar to display Apple Quick Actions :

   `Preferences->Keyboard->Customise Control Strip `-> Drag quick actions to your touchbar
4. Left click on 💉 in your status bar and click `Start`
5. You will be prompted for `username` and `password`
6. Open quick actions from touchbar and select `P`
7. Enable Botox to use your keyboard from `Preferences->Privacy->Accessibility->Botox`
8. You are set up

## Info

Botox stores your encrypted credentials on the filesystem by
using [Fernet symmetric encryption](https://github.com/fernet/spec/blob/master/Spec.md)
and uses your hashed password + a salt as key. your username and your password are not kept in RAM.

### Building
- Install dev dependencies `pipenv sync --dev`
- `pipenv run python setup.py py2app --resources resources`
