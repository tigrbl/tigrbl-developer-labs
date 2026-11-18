from task_app import TRACE
from labkit import run
async def exercise(p):
    TRACE.clear();task=await p.create()
    await p.request('PATCH',f"/task/{task['id']}",{'status':'done'})
    await p.request('GET','/task')
    hits=[e for e in await p.trace() if e.get('hook')=='check_status']
    p.show('Actual rule hits',hits)
    p.check({e['op'] for e in hits}=={'create','update'},'rule binds to selected writes, not list')
if __name__=='__main__':run(13,exercise)
