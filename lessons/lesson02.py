from labkit import run
async def exercise(p):
    task=await p.create()
    _,rows=await p.request('GET','/task')
    _,read=await p.request('GET',f"/task/{task['id']}")
    p.check(any(r['id']==task['id'] for r in rows),'created task appears in collection')
    p.check(read['id']==task['id'],'member read returns the created ID')
if __name__=='__main__':run(2,exercise)
