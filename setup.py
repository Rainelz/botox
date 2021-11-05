from setuptools import setup
import py2app.recipes

APP = ['src/botox.py']
APPNAME = 'Botox'
VERSION = "1.0.0"
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icon.icns',
    'plist':{
            'LSUIElement': True,
            'CFBundleIconFile':'resources/icon.icns',
            'CFBundleIdentifier':'com.Rainelz.Botox',
            'CFBundleGetInfoString': APPNAME,
            'CFBundleVersion' : VERSION,
            'CFBundleShortVersionString' : VERSION
            },
    'packages': ['rumps', 'PySimpleGUI', 'cryptography', 'cffi'],
}


class Script_recipe:
    def check(self, cmd, mf):
        return {"prescripts": ["resources/prescript.py"]}


py2app.recipes.PREScripts = Script_recipe()

setup(
    app=APP,
    name=APPNAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)
