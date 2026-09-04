#!/usr/bin/env python3
"""
Drives VS Code (via Chrome DevTools Protocol) to capture real screenshots
of the GridScript project: editor + integrated terminal running tests.

Prereq: VS Code launched with --remote-debugging-port=9222
Run:    python3 vs_code_shots.py
Out:    report/vscode_shots/*.png
"""
import base64
import json
import time
import urllib.request

from websocket import create_connection

OUT_DIR = 'report/vscode_shots'
DEBUG_HOST = 'http://127.0.0.1:9222'


def get_ws_url():
    with urllib.request.urlopen(f'{DEBUG_HOST}/json/list', timeout=5) as r:
        targets = json.load(r)
    for t in targets:
        if t['type'] == 'page' and 'vscode' in t.get('url', ''):
            return t['webSocketDebuggerUrl']
    raise SystemExit('no vscode page target found')


class CDP:
    def __init__(self, url):
        self.ws = create_connection(url, timeout=30, suppress_origin=True)
        self.msg_id = 0

    def call(self, method, **params):
        self.msg_id += 1
        mid = self.msg_id
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params}))
        deadline = time.time() + 60
        while time.time() < deadline:
            data = json.loads(self.ws.recv())
            if data.get('id') == mid:
                if 'error' in data:
                    raise RuntimeError(f"{method}: {data['error']}")
                return data.get('result', {})
        raise TimeoutError(method)

    def shot(self, path):
        data = self.call('Page.captureScreenshot', format='png')
        with open(path, 'wb') as f:
            f.write(base64.b64decode(data['data']))
        print(f"  saved {path}")

    def keys(self, text):
        self.call('Input.dispatchKeyEvent', type='keyDown', text=text,
                  unmodifiedText=text, windowsVirtualKeyCode=0)
        self.call('Input.dispatchKeyEvent', type='keyUp', text=text,
                  unmodifiedText=text, windowsVirtualKeyCode=0)

    def type_text(self, text):
        for ch in text:
            self.keys(ch)

    def press(self, key, code, vk, mods=None):
        base = {'key': key, 'code': code, 'windowsVirtualKeyCode': vk}
        if mods:
            base['modifiers'] = mods
        self.call('Input.dispatchKeyEvent', type='rawKeyDown', **base)
        self.call('Input.dispatchKeyEvent', type='keyUp', **base)

    def enter(self):
        self.press('Enter', 'Enter', 13)

    def ctrl_s(self):
        self.press('s', 'KeyS', 83, mods=2)

    def close_terminal(self):
        self.call('Input.dispatchKeyEvent', type='rawKeyDown',
                  key='d', code='KeyD', windowsVirtualKeyCode=68, modifiers=2)
        self.call('Input.dispatchKeyEvent', type='keyUp',
                  key='d', code='KeyD', windowsVirtualKeyCode=68, modifiers=2)


def open_terminal(cdp):
    cdp.call('Input.dispatchKeyEvent', type='rawKeyDown',
             key='`', code='Backquote', windowsVirtualKeyCode=192, modifiers=2)
    cdp.call('Input.dispatchKeyEvent', type='keyUp',
             key='`', code='Backquote', windowsVirtualKeyCode=192, modifiers=2)
    time.sleep(2.5)


def run_in_terminal(cdp, cmd, settle=3.5):
    cdp.type_text(cmd + '\n')
    time.sleep(settle)


SHOTS = [
    ('01_full_test_suite', 'python3 run_tests.py'),
    ('02_unit_tests', 'python3 test_interpreter.py'),
    ('03_patrol_demo', 'python3 gridscript.py tests/valid/patrol.gsc'),
    ('04_shadowing_demo', 'python3 gridscript.py tests/valid/shadowing.gsc'),
    ('05_recursion_demo', 'python3 gridscript.py tests/valid/recursion.gsc'),
    ('06_tokens_demo', 'python3 gridscript.py --tokens tests/valid/patrol.gsc'),
    ('07_ast_demo', 'python3 gridscript.py --ast tests/valid/scale.gsc'),
    ('08_lexer_error', 'python3 gridscript.py tests/invalid/bad_char.gsc'),
    ('09_parse_error', 'python3 gridscript.py tests/invalid/missing_then.gsc'),
    ('10_runtime_error', 'python3 gridscript.py tests/invalid/type_error_add.gsc'),
]


def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    url = get_ws_url()
    cdp = CDP(url)

    cdp.call('Page.enable')
    cdp.call('Runtime.enable')
    time.sleep(1)

    # focus editor pane
    cdp.call('Input.dispatchKeyEvent', type='rawKeyDown',
             key='Escape', code='Escape', windowsVirtualKeyCode=27)
    cdp.call('Input.dispatchKeyEvent', type='keyUp',
             key='Escape', code='Escape', windowsVirtualKeyCode=27)
    time.sleep(1)

    open_terminal(cdp)

    for name, cmd in SHOTS:
        print(f"shot: {name}  ({cmd})")
        run_in_terminal(cdp, cmd)
        time.sleep(1)
        cdp.shot(f"{OUT_DIR}/{name}.png")

    print("\nAll VS Code screenshots in report/vscode_shots/")


if __name__ == '__main__':
    main()