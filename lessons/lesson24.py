import asyncio,json,websockets
from labkit import run
async def exercise(p):
    task=await p.create('capstone')
    _,read=await p.request('GET',f"/task/{task['id']}")
    _,rest=await p.request('POST','/task/summary',{'title':read['title']})
    _,rpc=await p.rpc('Task.summary',{'title':read['title']})
    async with websockets.connect('ws://127.0.0.1:8782/ws/lessons',subprotocols=['jsonrpc']) as ws:
        sent={'jsonrpc':'2.0','method':'SocketTask.summary','params':{'title':read['title']},'id':24}
        await ws.send(json.dumps(sent));frame=json.loads(await asyncio.wait_for(ws.recv(),5))
    p.show('Actual WebSocket capstone result',frame,'websocket')
    p.check(rest==rpc['result']==frame['result'],'three configured surfaces produce equivalent modeled summary results')
    status,_=await p.request('POST','/task',{'id':task['id']+'-bad','title':'Rejected','status':'unknown'})
    p.check(status>=400,'the capstone also demonstrates a rejected operation')
if __name__=='__main__':run(24,exercise)
