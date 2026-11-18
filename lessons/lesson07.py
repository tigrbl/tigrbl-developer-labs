from task_app import Task
from labkit import run
async def exercise(p):
    status,values=await p.request('POST','/task/project',{'title':'Ship a lesson'})
    p.show('Declared virtual producer',Task.__tigrbl_cols__['display'].read_producer.__name__)
    p.show('Persisted columns',list(Task.__table__.columns.keys()))
    p.check(status==200 and values['display']=='SHIP A LESSON','explicit projection operation returns computed output')
    p.check('display' not in Task.__table__.columns,'computed field is not a stored column')
    p.show('Scope','This release uses an explicit custom projection handler reusing the pure producer. The vcol declaration is inspected separately; automatic CRUD virtual-field output is not claimed.')
if __name__=='__main__':run(7,exercise)
