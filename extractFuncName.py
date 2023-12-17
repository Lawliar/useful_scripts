from subprocess import check_output,DEVNULL,CalledProcessError
import json
from IPython import embed

def funcNameExtract(file):
    try:
        output = check_output(["clang","-Xclang","-ast-dump=json",file],stderr=DEVNULL)
    except CalledProcessError as e:
        output = e.output
    output = output.decode('utf-8')
    output = json.loads(output)
    assert(output['kind'] == 'TranslationUnitDecl')
    ret = []
    for eachEntry in output['inner']:
        ## only look at top-level object

        ## filter non function
        if eachEntry['kind'] != 'FunctionDecl':
            continue
        ## filter extern
        if('storageClass' in eachEntry):
            assert(eachEntry['storageClass'] == 'extern')
            continue
        ## filter function decl without function definition
        if('inner' not in eachEntry):
            continue
        ret.append(eachEntry['name'])
    return ret
if __name__ == '__main__':
    import sys
    ret = funcNameExtract(sys.argv[1])
    print(ret)
