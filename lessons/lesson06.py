from labkit import run
from task_app import Task
from tigrbl.schema import _build_schema
async def exercise(p):
    task=await p.create()
    for verb in ('create','read','list'):
        schema=_build_schema(Task,verb=verb).model_json_schema()
        p.show(f'{verb} schema',schema)
    _,read=await p.request('GET',f"/task/{task['id']}")
    p.check(read['title']==task['title'],'the selected title value is returned on read')
    p.check('read' in Task.__tigrbl_cols__['title'].io.out_verbs,'read is an explicit output verb')
if __name__=='__main__':run(6,exercise)
