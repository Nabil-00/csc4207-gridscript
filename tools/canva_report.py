#!/usr/bin/env python3
"""Push the CSC4207 group report into a Canva Doc via the Canva MCP server."""
import json
import sys
import urllib.request

MCP_URL = 'https://mcp.canva.com/v1/mcp'
AUTH_FILE = '/home/op7/.local/share/opencode/mcp-auth.json'
REPORT = sys.argv[1] if len(sys.argv) > 1 else 'report/Group1_Report.md'


def token():
    return json.load(open(AUTH_FILE))['canva']['tokens']['accessToken']


class MCP:
    def __init__(self):
        self.tok = token()
        self.sid = None
        self.mid = 0
        r = self._raw({'jsonrpc': '2.0', 'id': 0, 'method': 'initialize', 'params': {
            'protocolVersion': '2025-06-18', 'capabilities': {},
            'clientInfo': {'name': 'opencode', 'version': '1.0'}}})
        self.sid = r.headers.get('Mcp-Session-Id') or r.headers.get('mcp-session-id')
        self._raw({'jsonrpc': '2.0', 'method': 'notifications/initialized'})

    def _raw(self, payload):
        req = urllib.request.Request(MCP_URL, data=json.dumps(payload).encode(),
                                     headers={'Content-Type': 'application/json',
                                              'Accept': 'application/json, text/event-stream',
                                              'Authorization': f'Bearer {self.tok}',
                                              **({'Mcp-Session-Id': self.sid} if self.sid else {})})
        return urllib.request.urlopen(req, timeout=120)

    def call(self, method, params=None, notify=False):
        body = {'jsonrpc': '2.0', 'method': method}
        if not notify:
            self.mid += 1
            body['id'] = self.mid
        if params:
            body['params'] = params
        resp = self._raw(body)
        text = resp.read().decode()
        if notify:
            return None
        for line in text.splitlines():
            if line.startswith('data:'):
                return json.loads(line[5:])
        return json.loads(text) if text.strip() else None

    def tool(self, name, args):
        out = self.call('tools/call', {'name': name, 'arguments': args})
        if out and 'error' in out:
            raise RuntimeError(json.dumps(out['error'])[:500])
        result = out['result']
        if result.get('isError'):
            raise RuntimeError(json.dumps(result.get('content', []))[:800])
        return result


if __name__ == '__main__':
    query = open(REPORT).read()
    mcp = MCP()
    res = mcp.tool('generate-design', {
        'query': query,
        'design_type': 'doc',
        'verbatim': True,
        'user_intent': 'Create the group CSC4207 interpreter project report as a Canva Doc',
    })
    print(json.dumps(res, indent=1)[:4000])