def _setMatrix(mat,d,r,lis,fill,cmat,fmat,uniform,seed,null):
    # =============================================================================
    #Handle arguments

    if isinstance(d,int):
        mat._setDim(d)

    #Empty list given
    if len(lis)==0:
        if fill == None:
            fill = null if mat._dfMat else uniform 
        elif isinstance(fill,str):
            if mat.dtype.__name__ != "dataframe":
                raise TypeError("Can't fill matrix with strings if dtype isn't set to dataframe")

    isMethod = bool(type(fill).__name__ in ["method","function","builtin_function_or_method","null"])

    if lis in [None,"",{}]:
        lis = []
    if not isinstance(lis,(list,str,dict)):
        raise TypeError("'data' parameter only accepts lists,strings and dictionaries")
    
    #Dictionary given
    if isinstance(lis,dict):
        from MatricesM.C_funcs.linalg import Ctranspose

        names,values = list(lis.keys()),list(lis.values())
        if len(values) == 0:
            raise ValueError("No data found")
        
        if not all([1 if isinstance(val,list) else 0 for val in values]):
            raise IndexError("Dictionary's values should be lists")

        col_length = len(values[0])
        if col_length == 0:
            raise IndexError("Can't use empty lists as columns")
        if not all([1 if len(val)==col_length else 0 for val in values[1:]]):
            raise IndexError("Dictionary's values should be same length lists")
            
        transposed = Ctranspose(len(names),col_length,values)

        mat._matrix = transposed
        mat._Matrix__dim=mat._declareDim()
        mat.features = names
        return None
    
    #Set new range    
    if r==None:
        r=mat.initRange
    else:
        mat._Matrix_initRange=r
        
    # =============================================================================
    #Save the seed for reproduction
    if mat.seed==None and len(lis)==0 and isMethod:
        randseed = int(uniform(-2**24,2**24))
        mat._Matrix__seed = randseed
    
    elif isMethod and len(lis)==0:
        seed(mat.seed)
    else:
        mat._Matrix__seed=None
        
    # =============================================================================
    #Set the new matrix
    #Matrix from given string
    if isinstance(lis,str):
        mat._matrix=mat._listify(lis)
        if mat.dim == [0,0]:
            mat._Matrix__dim=mat._declareDim()       
    #Matrix from a list or other filling methods
    else:
        if len(lis)>0:
            if isinstance(lis[0],list):                        
                mat._matrix = [a[:] for a in lis[:]]
                if mat.dim == [0,0]:
                    mat._Matrix__dim=mat._declareDim()
            else:
                try:
                    if mat.dim != [0,0]:
                        assert mat.dim[0]*mat.dim[1] == len(lis)
                        mat._matrix=[]
                        for j in range(0,len(lis),mat.dim[1]):
                            mat._matrix.append(lis[j:j+mat.dim[1]]) 
                    else:
                        mat._matrix = [lis]

                except Exception as err:
                    print(err)
                else:
                    mat._Matrix__dim=mat._declareDim()
        # =============================================================================
        #Same range for all columns
        elif len(lis)==0 and (isinstance(r,list) or isinstance(r,tuple)):

            if isinstance(fill,(str,int,float,complex)):
                from MatricesM.C_funcs.randgen import getfill
                mat._matrix=getfill(d[0],d[1],fill)
                return None
            
            elif isMethod:
                if fill.__name__=="uniform":
                    m,n=max(r),min(r)
                    if cmat:
                        mat._matrix=[[complex(uniform(n,m),uniform(n,m)) for a in range(d[1])] for b in range(d[0])]
                    
                    elif fmat:
                        if r==[0,1]:
                            from MatricesM.C_funcs.zerone import pyfill
                            mat._matrix=pyfill(d[0],d[1],mat.seed)
                        else:
                            from MatricesM.C_funcs.randgen import getuni
                            mat._matrix=getuni(d[0],d[1],n,m,mat.seed)
                    
                    else:
                        if r==[0,1]:
                            from MatricesM.C_funcs.randgen import igetrand
                            mat._matrix=igetrand(d[0],d[1],mat.seed)
                        else:
                            from MatricesM.C_funcs.randgen import igetuni
                            mat._matrix=igetuni(d[0],d[1],n-1,m+1,mat.seed)
                            
                elif fill.__name__ in ["gauss","betavariate","gammavariate","lognormvariate"]:
                    m,s=r[0],r[1]
                    if cmat:
                        mat._matrix=[[complex(fill(m,s),fill(m,s)) for a in range(d[1])] for b in range(d[0])]
                    
                    elif fmat:
                        mat._matrix=[[fill(m,s) for a in range(d[1])] for b in range(d[0])]
                    
                    else:
                        mat._matrix=[[round(fill(m,s)) for a in range(d[1])] for b in range(d[0])]
                        
                elif fill.__name__=="triangular":
                    n,m,o = r[0],r[1],r[2]
                    if cmat:
                        mat._matrix=[[complex(fill(n,m,o),fill(n,m,o)) for a in range(d[1])] for b in range(d[0])]
                    
                    elif fmat:
                        mat._matrix=[[fill(n,m,o) for a in range(d[1])] for b in range(d[0])]
                    else:
                        mat._matrix=[[round(fill(n,m,o)) for a in range(d[1])] for b in range(d[0])]

                elif fill.__name__=="expovariate":
                    lmb = r[0]
                    if cmat:
                        mat._matrix=[[complex(fill(lmb),fill(lmb)) for a in range(d[1])] for b in range(d[0])]
                    
                    elif fmat:
                        mat._matrix=[[fill(lmb) for a in range(d[1])] for b in range(d[0])]
                    
                    else:
                        mat._matrix=[[round(fill(lmb)) for a in range(d[1])] for b in range(d[0])]  
                else:
                    from MatricesM.C_funcs.randgen import getfill
                    mat._matrix=getfill(d[0],d[1],fill)
                    return None
                
            #Ranged has no affect after this point
            elif type(fill) == list:
                if len(fill)!=d[1]:
                    raise ValueError(f"Given list {fill} should have {d[1]} values")
                else:
                    mat._matrix = [fill for _ in range(d[0])]

            elif type(fill) == range:
                l = list(fill)
                if len(l)!=d[1]:
                    raise ValueError(f"Given range {fill} should have {d[1]} values")
                else:
                    mat._matrix = [fill for _ in range(d[0])]
            
            else:
                raise TypeError(f"Couldn't fill the matrix with fill value:{fill}")

        # =============================================================================               
        #Different ranges over individual columns
        elif len(lis)==0 and isinstance(r,dict):
            try:
                assert len([i for i in r.keys()])==mat.dim[1]
                vs=[len(i) for i in r.values()]
                assert vs.count(vs[0])==len(vs)
                feats=[i for i in r.keys()]
                mat.features=feats

            except Exception as err:
                print(err)
            else:
                lis=list(r.values())

                if isinstance(fill,(str,int,float,complex)):
                    from MatricesM.C_funcs.randgen import getfill
                    mat._matrix=getfill(d[0],d[1],fill)
                    return None

                elif isMethod:
                    if fill.__name__=="uniform":                    
                        if cmat:
                            temp=[[complex(uniform(min(lis[i]),max(lis[i])),uniform(min(lis[i]),max(lis[i]))) for _ in range(d[0])] for i in range(d[1])]
                        
                        elif fmat:
                            temp=[[uniform(min(lis[i]),max(lis[i])) for _ in range(d[0])] for i in range(d[1])]                        
                        
                        else:
                            temp=[[round(uniform(min(lis[i]),max(lis[i])+1))//1 for _ in range(d[0])] for i in range(d[1])]
                    
                    elif fill.__name__ in ["gauss","betavariate","gammavariate","lognormvariate"]:                    
                        if cmat:
                            temp=[[complex(fill(lis[i][0],lis[i][1]),fill(lis[i][0],lis[i][1])) for _ in range(d[0])] for i in range(d[1])]
                        
                        elif fmat:
                            temp=[[fill(lis[i][0],lis[i][1]) for _ in range(d[0])] for i in range(d[1])]                        
                        
                        else:
                            temp=[[round(fill(lis[i][0],lis[i][1]+1))//1 for _ in range(d[0])] for i in range(d[1])]
                            
                    elif fill.__name__=="triangular":                    
                        if cmat:
                            temp=[[complex(fill(lis[i][0],lis[i][1],lis[i][2]),fill(lis[i][0],lis[i][1],lis[i][2])) for _ in range(d[0])] for i in range(d[1])]
                            
                        elif fmat:
                            
                            temp=[[fill(lis[i][0],lis[i][1],lis[i][2]) for _ in range(d[0])] for i in range(d[1])]                                                
                        else:
                            temp=[[round(fill(lis[i][0],lis[i][1]+1,lis[i][2]))//1 for _ in range(d[0])] for i in range(d[1])]

                    elif fill.__name__=="expovariate":                    
                        if cmat:
                            temp=[[complex(fill(lis[i][0]),fill(lis[i][0])) for _ in range(d[0])] for i in range(d[1])]
                        
                        elif fmat:
                            temp=[[fill(lis[i][0]) for _ in range(d[0])] for i in range(d[1])]                        
                        
                        else:
                            temp=[[round(fill(lis[i][0]))//1 for _ in range(d[0])] for i in range(d[1])]
                    else:
                        from MatricesM.C_funcs.randgen import getfill
                        mat._matrix=getfill(d[0],d[1],fill)
                        return None
                #Ranged has no affect after this point
                elif type(fill) == list:
                    if len(fill)!=d[1]:
                        raise ValueError(f"Given list {fill} should have {d[1]} values")
                    else:
                        mat._matrix = [fill for _ in range(d[0])]
                        return None

                elif type(fill) == range:
                    l = list(fill)
                    if len(l)!=d[1]:
                        raise ValueError(f"Given range {fill} should have {d[1]} values")
                    else:
                        mat._matrix = [fill for _ in range(d[1])]
                        return None
                else:
                    raise TypeError(f"Couldn't fill the matrix with fill value:{fill}")
                
                from MatricesM.C_funcs.linalg import Ctranspose #Change the process so this won't be necessary
                mat._matrix=Ctranspose(d[1],d[0],temp)
        else:
            return None
