from setuptools import setup
import py2app.recipes

APP = ['src/botox.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icon.icns',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'PySimpleGUI', 'cryptography', 'cffi'],
}


class Script_recipe:
    def check(self, cmd, mf):
        return {"prescripts": ["resources/prescript.py"]}


py2app.recipes.PREScripts = Script_recipe()

setup(
    app=APP,
    name='Botox',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)
