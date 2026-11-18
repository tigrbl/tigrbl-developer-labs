from labkit import run
async def exercise(p):
    _,rest=await p.request('POST','/task/summary',{'title':'Shared rule'})
    _,rpc=await p.rpc('Task.summary',{'title':'Shared rule'})
    p.check(rest==rpc['result'],'valid results are equivalent')
    status,rest_error=await p.request('POST','/task/summary',{'title':''})
    _,rpc_error=await p.rpc('Task.summary',{'title':''})
    p.check(status>=400 and 'error' in rpc_error,'both projections reject empty title')
    p.show('Envelope boundary','REST and JSON-RPC preserve different error envelopes.')
if __name__=='__main__':run(16,exercise)
