from labkit import run
from task_app import Task
from tigrbl.schema import _build_schema
async def exercise(p):
    spec=Task.__tigrbl_cols__['title']
    schema=_build_schema(Task,verb='create').model_json_schema()
    p.show('Storage',str(spec.storage))
    p.show('Field',str(spec.field))
    p.show('Operation IO',str(spec.io))
    p.show('Create JSON Schema',schema)
    p.check(schema['properties']['title']['maxLength']==80,'field max length projects into JSON Schema')
if __name__=='__main__':run(5,exercise)
