from labkit import run
async def exercise(p):
    status,health=await p.request('GET','/system/healthz')
    p.check(status==200 and health['ok'],'the running application responds')
    status,schema=await p.request('GET','/openapi.json')
    p.check('/task' in schema['paths'],'the Task collection is documented')
if __name__=='__main__':run(1,exercise)
