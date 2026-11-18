"""Shared instrumentation for real Tigrbl lesson runs, not framework middleware."""
from __future__ import annotations
import asyncio, json, sys, time
from pathlib import Path
from typing import Any
import httpx
from task_app import app, Task, TRACE

ROOT=Path(__file__).parent
BASE='http://127.0.0.1:8782'

class Probe:
    def __init__(self,number):
        self.number=number;self.records=[];self.checks=[];self.client=None
    def show(self,label,value,kind='inspection'):
        self.records.append({'label':label,'kind':kind,'value':value});return value
    def check(self,condition,message):
        self.checks.append({'passed':bool(condition),'assertion':message})
        assert condition,message
    async def request(self,method,path,body=None):
        response=await self.client.request(method,path,json=body)
        try:result=response.json()
        except Exception:result=response.text
        self.show(f'{method} {path}',{'request':body,'status':response.status_code,'response':result},'http')
        return response.status_code,result
    async def rpc(self,alias,params,request_id=42):
        return await self.request('POST','/rpc',{'jsonrpc':'2.0','method':alias,'params':params,'id':request_id})
    async def create(self,suffix='a',**changes):
        key=f'lab-{self.number}-{time.time_ns()}-{suffix}'
        payload={'id':key,'title':'Ship a lesson','status':'open',**changes}
        status,row=await self.request('POST','/task',payload)
        self.check(status==201,'create returns HTTP 201')
        return row
    async def trace(self):
        response=await self.client.get('/lab/trace');return response.json()

async def execute(number,exercise):
    TRACE.clear();p=Probe(number);started=time.time()
    async with httpx.AsyncClient(base_url=BASE,timeout=12) as client:
        p.client=client
        await client.post('/lab/reset-trace')
        await exercise(p)
    result={'lesson':number,'passed':all(x['passed'] for x in p.checks),'checks':p.checks,
            'records':p.records,'trace':list(TRACE),'runtime':'Tigrbl 0.4.5 / Tigrcorn 0.3.18',
            'recorded_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'elapsed_seconds':round(time.time()-started,3)}
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence'/f'{number:02d}.json').write_text(json.dumps(result,indent=2,default=str),'utf-8')
    return result

def run(number,exercise):
    result=asyncio.run(execute(number,exercise))
    print(json.dumps(result,indent=2,default=str))
