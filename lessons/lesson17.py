import json,asyncio,websockets
from labkit import run
async def exercise(p):
    async with websockets.connect('ws://127.0.0.1:8782/ws/lessons',subprotocols=['jsonrpc']) as ws:
        frame={'jsonrpc':'2.0','method':'SocketTask.summary','params':{'title':'Ship a lesson'},'id':42}
        await ws.send(json.dumps(frame));result=json.loads(await asyncio.wait_for(ws.recv(),5))
        p.show('Actual WS request',frame,'websocket');p.show('Actual WS response',result,'websocket')
        p.check(ws.subprotocol=='jsonrpc','WebSocket negotiated jsonrpc')
        p.check(result['id']==42 and result['result']['words']==3,'custom operation preserves correlation and result')
if __name__=='__main__':run(17,exercise)
