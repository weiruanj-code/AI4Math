"""Independent certificate: direct forward Dexter graph, integer Bareiss determinant.
No imports from the existing project's mathematical implementations.
"""
import json
from pathlib import Path


def dyck(n, prefix='', up=0, down=0):
    if down == n:
        yield prefix
    else:
        if up < n:
            yield from dyck(n, prefix+'1', up+1, down)
        if down < up:
            yield from dyck(n, prefix+'0', up, down+1)


def successors(w):
    # Match parentheses by a stack; each matched pair is a primitive subpath.
    stack=[]
    for j,c in enumerate(w):
        if c=='1':
            stack.append(j)
        else:
            i=stack.pop()
            if i==0 or w[i-1]!='0' or (j+1<len(w) and w[j+1]!='1'):
                continue
            cut=i-1
            while cut>=0 and w[cut]=='0':
                yield w[:cut]+w[i:j+1]+w[cut:i]+w[j+1:]
                cut-=1


def graph(n):
    incoming={w:[] for w in dyck(n)}
    for w in incoming:
        for v in successors(w):
            incoming[v].append(w)
    return incoming


def interval(top, incoming):
    selected={top}
    queue=[top]
    while queue:
        for v in incoming[queue.pop()]:
            if v not in selected:
                selected.add(v)
                queue.append(v)
    # All upward moves increase the binary word numerically.
    vertices=sorted(selected)
    idx={v:i for i,v in enumerate(vertices)}
    reachable=[1<<i for i in range(len(vertices))]
    edges=[]
    for v in reversed(vertices):
        i=idx[v]
        for u in incoming[v]:
            j=idx[u]
            assert j<i
            reachable[j] |= reachable[i]
            edges.append([u,v])
    C=[[int(bool(reachable[i] & (1<<j))) for j in range(len(vertices))] for i in range(len(vertices))]
    return vertices,sorted(edges),C


def bareiss(a):
    a=[r[:] for r in a]
    n=len(a)
    previous=1
    sign=1
    for k in range(n-1):
        if a[k][k]==0:
            r=next((r for r in range(k+1,n) if a[r][k]),None)
            if r is None:
                return 0
            a[k],a[r]=a[r],a[k]
            sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            entry=a[i][k]
            for j in range(k+1,n):
                numerator=pivot*a[i][j]-entry*a[k][j]
                value,remainder=divmod(numerator,previous)
                assert remainder==0
                a[i][j]=value
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]


def value(C,t):
    return bareiss([[t*C[j][i]-C[i][j] for j in range(len(C))] for i in range(len(C))])


def main():
    output={'method':'Full forward Dexter graph; stack matching; lexicographic reachability; exact integer Bareiss elimination','controls':[],'candidate':[]}
    # Published control: Phi2 Phi4 Phi18 Phi54 is the Coxeter polynomial.
    # Serre polynomial at 2 equals (-1)^27 times Coxeter polynomial at -2.
    for w in ['11011000','11101000']:
        top='1'+w+'100'
        verts,edges,C=interval(top,graph(len(top)//2))
        expected=-((-2+1)*((-2)**2+1)*((-2)**6-(-2)**3+1)*((-2)**18-(-2)**9+1))
        det=value(C,2)
        assert len(verts)==27 and det==expected,(w,len(verts),det,expected)
        output['controls'].append({'w':w,'size':len(verts),'det_2CT_minus_C':str(det),'published_polynomial_matches':True})
        print('control',w,len(verts),det,flush=True)
    incoming=graph(11)
    print('full graph vertices',len(incoming),flush=True)
    assert len(incoming)==58786
    for w in ['110100110110001100','110110001101001100']:
        verts,edges,C=interval('1'+w+'100',incoming)
        det=value(C,2)
        record={'w':w,'top':'1'+w+'100','size':len(verts),'cover_count':len(edges),'det_2CT_minus_C':str(det),'residue_1009':det%1009,'vertices':verts,'covers':edges}
        output['candidate'].append(record)
        print('candidate',w,len(verts),len(edges),det,det%1009,flush=True)
    path=Path(__file__).with_name('independent_counterexample_certificate.json')
    path.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('saved',path,flush=True)

if __name__=='__main__':
    main()
