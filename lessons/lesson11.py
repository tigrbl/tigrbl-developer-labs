from tigrbl import op_ctx
from labkit import run
async def exercise(p):
    class Owner:pass
    p.show('Before attachment',hasattr(Owner,'ping'))
    @op_ctx(alias='ping',target='custom',bind=Owner,persist='skip')
    def ping(cls,ctx):return {'owner':cls.__name__}
    spec=Owner.__tigrbl_ops__[-1]
    p.show('After attachment',{'alias':spec.alias,'owner':Owner.ping({})})
    p.check(spec.alias=='ping','bind attaches the semantic operation to an owner')
    p.show('Distinct keyword','bindings describes transport projections; bind attaches an owner.')
if __name__=='__main__':run(11,exercise)
