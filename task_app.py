"""The Task application used by the developer lessons.

Run: uv run tigrcorn task_app:app --host 127.0.0.1 --port 8781
"""
from __future__ import annotations
from typing import Any
from tigrbl import TigrblApp, TableBase, op_ctx, hook_ctx
from tigrbl.factories.column import acol, vcol
from tigrbl.factories.engine import mem
from tigrbl._spec import S, F, IO
from sqlalchemy import String
from tigrbl_core._spec import WsBindingSpec, JsonRpcFramingSpec
from tigrbl.runtime.status import HTTPException

TRACE: list[dict[str, Any]] = []

def display_title(obj,ctx):
    """Pure producer shared by the declaration and explicit projection op."""
    return str(obj.title).upper()

class Task(TableBase):
    __tablename__ = 'lesson_tasks'
    resource_name = 'task'
    __allow_unmapped__ = True
    id = acol(storage=S(type_=String(80), primary_key=True), field=F(py_type=str),
              io=IO(in_verbs=('create',), out_verbs=('create','read','list','update')))
    title = acol(storage=S(type_=String(80), nullable=False),
                 field=F(py_type=str, constraints={'min_length':1,'max_length':80},required_in=('create',)),
                 io=IO(in_verbs=('create','update'),out_verbs=('create','read','list','update')))
    status = acol(storage=S(type_=String(20),nullable=False),field=F(py_type=str,required_in=('create',)),
                  io=IO(in_verbs=('create','update'),out_verbs=('create','read','list','update')))
    display = vcol(field=F(py_type=str),io=IO(out_verbs=('read','list')),
                   read_producer=display_title)

    @hook_ctx(ops=('create','update'), phase='PRE_HANDLER')
    def check_status(cls, ctx):
        payload=ctx.get('payload') or {}
        TRACE.append({'op':str(ctx.get('op')),'phase':'PRE_HANDLER','hook':'check_status','status':payload.get('status')})
        if payload.get('status','open') not in ('open','done'):
            raise HTTPException(status_code=422,detail='status must be open or done')

    @op_ctx(alias='summary',target='custom',arity='collection',persist='skip')
    def summary(cls, ctx):
        payload=ctx.get('payload') or {}
        title=str(payload.get('title',''))
        TRACE.append({'op':'summary','phase':'HANDLER','handler':'Task.summary','title':title})
        return {'title':title,'words':len(title.split())}

    @op_ctx(alias='preview',target='custom',arity='member',persist='skip')
    def preview(cls, ctx):
        payload=ctx.get('payload') or {}
        params=ctx.get('path_params') or {}
        TRACE.append({'op':'preview','phase':'HANDLER','handler':'Task.preview'})
        return {'id':params.get('item_id') or payload.get('id'),'preview':True}

    @op_ctx(alias='project',target='custom',arity='collection',persist='skip')
    def project(cls,ctx):
        from types import SimpleNamespace
        obj=SimpleNamespace(title=str((ctx.get('payload') or {}).get('title','')))
        return {'display':display_title(obj,ctx)}

    @hook_ctx(ops='summary',phase='PRE_HANDLER')
    def check_summary(cls,ctx):
        TRACE.append({'op':'summary','phase':'PRE_HANDLER','hook':'check_summary'})
        if not str((ctx.get('payload') or {}).get('title','')).strip():
            raise ValueError('title must contain visible text')

app=TigrblApp(engine=mem(async_=False))
app.include_table(Task)
app.initialize()
app.mount_jsonrpc(prefix='/rpc')

class SocketTask(TableBase):
    __tablename__='lesson_socket_tasks'
    __allow_unmapped__=True
    id=acol(storage=S(type_=String(80),primary_key=True),field=F(py_type=str))

    @op_ctx(alias='summary',target='custom',arity='collection',persist='skip',
            bindings=(WsBindingSpec(proto='ws',path='/ws/lessons',framing=JsonRpcFramingSpec()),))
    def summary(cls,ctx):
        title=str((ctx.get('payload') or {}).get('title',''))
        TRACE.append({'op':'SocketTask.summary','phase':'HANDLER','title':title})
        return {'title':title,'words':len(title.split())}

from dataclasses import replace
from tigrbl_core._spec import AppSpec,RouterSpec,PathSpec,TableSpec

socket_table=replace(TableSpec.collect(SocketTask),model=None,name='SocketTask',
                    model_ref='task_app:SocketTask',ops=tuple(SocketTask.__tigrbl_ops__))
socket_app=TigrblApp.from_spec(AppSpec(title='Task WebSocket lessons',version='1',
    routers=(RouterSpec(name='socket',paths=(PathSpec(path='/ws/lessons',kind='ws-jsonrpc',tables=(socket_table,)),)),)))
