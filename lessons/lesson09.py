from labkit import run
async def exercise(p):
    _,rest=await p.request('POST','/task/summary',{'title':'Ship a lesson'})
    _,rpc=await p.rpc('Task.summary',{'title':'Ship a lesson'})
    p.check(rest==rpc['result']=={'title':'Ship a lesson','words':3},'modeled results match across REST and RPC')
    p.check(rpc['id']==42,'RPC preserves request correlation')
if __name__=='__main__':run(9,exercise)
