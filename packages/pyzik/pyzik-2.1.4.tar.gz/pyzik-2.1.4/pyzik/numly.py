# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 00:12:16 2019

@author: jazzn
"""


import traceback
import pandas as pd
import numpy as np
from pyzik.pandly import scatter2D,scatter3D,draw_vectors,histogram
from prettytable import PrettyTable

class Fplot:
    __G2D = 'scatter2D'
    __G3D = 'scatter3D'
    __GV2 = 'vector2D'
    __GV3 = 'vector3D'
    __H = 'histogram'
    __expectDaxis={__G2D:list(set(dict(titre="",ortho='auto', unsur=1, style_tracer='o', 
              shape=None, quadril_x=0, quadril_y=0,subplots=False, xlabel='', ylabel='',xorder='normal'))),
            __G3D:list(set(dict(titre="un titre", unsur=1))),
            __GV2:list(set(dict(unsur=1,scalvect=1,titre="sans titre",quadril_x=0,quadril_y=0,xlabel='',ylabel=''))),
                 __GV3:list(set(dict(unsur=1,scalvect=1,titre="sans titre",quadril_x=0,quadril_y=0,quadril_z=0,
                                     xlabel='',ylabel='',zlabel=''))),
                  __H:list(set(dict(titre='pas de titre',orientation='vertical',histnorm="")))}
    __expectD={__G2D:list(set(dict(color='auto',fill=''))),
            __G3D:list(set(dict(color='auto',style_tracer='o'))),
            __GV2:[],__GV3:[],__H:[]}

    
    def __check_assert(self,typ='axis',**d):
        for kd in d:
            if typ == 'axis':
                assert kd in Fplot.__expectDaxis[self.__kind],f"bad argument {kd} ...\n use :\n{Fplot.__expectDaxis[self.__kind]}"
            else:
                assert kd in Fplot.__expectD[self.__kind],f"bad argument {kd} ...\n use :\n{Fplot.__expectD[self.__kind]}"
                
    def __init__(self,kind='scatter2D',**d):
        styps = [Fplot.__G2D,Fplot.__G3D,Fplot.__GV2,Fplot.__GV3,Fplot.__H]
        assert kind in styps,f"kind must be in {styps}"
        self.__kind = kind
        self.__check_assert(typ='axis',**d)
        self.__df=[]
        self.__d = {}
        self.__d.update(self.__clean_axis_dict(d))
        self.__init = True

    
    def __clean_axis_dict(self,d):
        return {k:v for k,v in d.items() if k in Fplot.__expectDaxis[self.__kind]}  
    
    def hist(self,*x,**d):
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__H)
        assert self.__kind == Fplot.__H,f"use hist only if u want draw histogram, change ur kind type to: {Fplot.__H}"
        self.__check_assert(typ='xyz',**d)
        try:
            (_,_,_,text)=traceback.extract_stack()[-2]
            args = text[text.index('('):].lstrip('(').rstrip(')').split(',')
        except:
            args=[f"x{i}" for i in range(len(x))]
        assert len(args) == len(set(args)),"at least 2 params are same !!!"
        datf = pd.DataFrame()
        for elx,var_name in zip(x,args):
            datf0 = pd.DataFrame({var_name:elx})
            datf = pd.concat([datf,datf0], ignore_index=True, axis=1)
        datf.columns = args
        self.__df = [datf]
        self.__d.update(self.__clean_dict(d))
            
    def draw_vector2D(self,point=tuple(),vector=tuple(),**d):
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__GV2)
        assert self.__kind == Fplot.__GV2,f"use draw_vector2D only if u want draw 2D gfx with vectors, change ur kind type to: {Fplot.__GV2}"
        assert len(point)==2,'point must have 2 coordinates'
        assert len(vector)==2,'vector must have 2 coordinates'
        #assert len(set([len(i) for i in point+vector]))==1,'arrays must have same lenght'
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':point[0],'y':point[1],'ux':vector[0],'uy':vector[1]})
        datf.info = ''
        self.__df = [datf]
        self.__d.update(self.__clean_dict(d))
    
    
    def draw_vector3D(self,point=tuple(),vector=tuple(),**d):
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__GV3)
        assert self.__kind == Fplot.__GV3,f"use draw_vector2D only if u want draw 2D gfx with vectors, change ur kind type to: {Fplot.__GV2}"
        assert len(point)==3,'point must have 2 coordinates'
        assert len(vector)==3,'vector must have 2 coordinates'
        assert len(set([len(i) for i in point+vector]))==1,'arrays must all be same length'
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':point[0],'y':point[1],'z':point[2],'ux':vector[0],'uy':vector[1],'uz':vector[2]})
        datf.info = ''
        self.__df = [datf]
        self.__d.update(self.__clean_dict(d))
        
    def plot(self,x,y,label='',**d):
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__G2D)
        assert self.__kind == 'scatter2D',f"use add_plot2D only if u want draw 2D gfx, change ur kind type to: {Fplot.__G2D}"
        assert isinstance(x,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(y,(np.ndarray,list)),"x must be numpy array or list"
        assert len(x)==len(y),"arrays must have same lenght"
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':x,'y':y})
        datf.info = label
        self.__df.append(datf)
        self.__d.update(self.__clean_dict(d))
    
    def title(self,title):
        """Ex : title('titre de mon graphique')"""
        self.__d.update({'titre':title})
        return self
    
    def xlabel(self,xlabel):
        """Ex : xlabel("nom de l'axe des x")"""
        self.__d.update(self.__clean_axis_dict({'xlabel':xlabel}))
        return self
    
    def ylabel(self,ylabel):
        """Ex : ylabel("nom de l'axe des y")"""
        self.__d.update(self.__clean_axis_dict({'ylabel':ylabel}))
        return self
    
    def zlabel(self,zlabel):
        """Ex : zlabel("nom de l'axe des z")"""
        self.__d.update(self.__clean_axis_dict({'zlabel':zlabel}))
        return self
    
    def xgrid(self,xgrid):
        """Ex: xgrid(50) for have 50 (max) line in x-axis"""
        self.__d.update(self.__clean_axis_dict({'quadril_x':xgrid}))
        return self
    
    def ygrid(self,ygrid):
        """Ex: ygrid(50) for have 50 (max) line in y-axis"""
        self.__d.update(self.__clean_axis_dict({'quadril_y':ygrid}))
        return self
    
    def zgrid(self,zgrid):
        """Ex: zgrid(50) for have 50 (max) line in z-axis
        u can use 20 or 10 or ..."""
        self.__d.update(self.__clean_axis_dict({'quadril_z':zgrid}))
        return self
    
    def marker(self,marker):
        """Ex: marker('o')cfor have only points in graph
        anothers : only marker  'o' '*' '+' 'x' '[' ']' '<' '>' '/' 
        '\' '%' or with line '-o','-*',':',';' etc
        """
        self.__d.update(self.__clean_dict({'style_tracer':marker}))
        return self
    
    def subplots(self,subplots):
        """Ex: subplots(True) for have multiple gfx"""
        self.__d.update(self.__clean_axis_dict({'subplots':subplots}))
        return self
    
    def xorder(self,xorder):
        """Ex: xorder('reversed') for reverse x-axis order
        xorder('normal') is default value"""
        self.__d.update(self.__clean_axis_dict({'xorder':xorder}))
        return self
        
    def scalvect(self,scalvect):
        """Ex: scalvect(0.5) for decrease lenght of vectors
        scalvect(1.5) for increase
        or anothers floatings values of course !!!"""
        self.__d.update(self.__clean_axis_dict({'scalvect':scalvect}))
        return self

    def unsur(self,unsur):
        """Ex: unsur(3) for plot only 1 point over 3
        reduce number of points to plot"""
        self.__d.update(self.__clean_axis_dict({'unsur':unsur}))
        return self
   
    def orientation(self,orientation):
        """Ex: orientation('vertical') or orientation('horizontal') up2u"""
        self.__d.update(self.__clean_axis_dict({'orientation':orientation}))
        return self
    
    def shape(self,shape):
        """Ex: shape() too dificult ..."""
        self.__d.update(self.__clean_axis_dict({'shape':shape}))
        return self
    
    def histnorm(self,histnorm):
        """Ex: histnorm('percent') for have percent y-axis
        histnorm('normal') for normal y-axis
        """
        self.__d.update(self.__clean_axis_dict({'histnorm':histnorm}))
        return self
    
    def ortho(self,ortho):
        """Ex: ortho('ortho') for have orthonormal axes, ideal for draw trajectory"""
        self.__d.update(self.__clean_axis_dict({'ortho':ortho}))
        return self

    
    def get_methods(self):
        __methods ={'titre':self.title,'ortho':self.ortho,'unsur':self.unsur,'shape':self.shape,
                  'quadril_x':self.xgrid,'quadril_y':self.ygrid,
           'quadril_z':self.zgrid,'subplots':self.subplots,'xlabel':self.xlabel,'ylabel':self.ylabel,
                  'zlabel':self.zlabel,
           'xorder':self.xorder,'scalvect':self.scalvect,'orientation':self.orientation,'histnorm':self.histnorm,
            'style_tracer':self.marker}
        print(f"methods availables for ur kind={self.__kind}:\n")
        t = PrettyTable()
        methods = [__methods[eld].__name__ for eld in Fplot.__expectDaxis[self.__kind]]
        desc = [__methods[eld].__doc__ for eld in Fplot.__expectDaxis[self.__kind]]
        t.add_column("Method",methods)
        t.add_column("Description",desc)
        print(t,"\n")
        t = PrettyTable()
        maxl = max(len(Fplot.__expectDaxis[self.__kind]),len(Fplot.__expectD[self.__kind]))
        laxis = Fplot.__append_nones(maxl,Fplot.__expectDaxis[self.__kind])
        ldata = Fplot.__append_nones(maxl,Fplot.__expectD[self.__kind])
        t.add_column("Argument Axis",laxis)
        t.add_column("Argument Data",ldata)
        print(t)
            
    
    def __append_nones(length, list_):
        """
        Appends Nones to list to get length of list equal to `length`.
        If list is too long raise AttributeError
        """
        if len(list_) < length:
            nones = length - len(list_)
            return list_ + [None] * nones
        elif len(list_) > length:
            raise AttributeError('Length error list is too long.')
        else:
            return list_
    
    def plot3D(self,x,y,z,label,**d):        
        try:
            g = self.__init
        except:
            self.__init__(kind=Fplot.__GV2)
        assert self.__kind == Fplot.__G3D,f"use add_plot3D only if u want draw 3D gfx, change ur kind type to: {Fplot.__G3D}"
        assert isinstance(x,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(y,(np.ndarray,list)),"x must be numpy array or list"
        assert isinstance(z,(np.ndarray,list)),"x must be numpy array or list"
        assert (len(x)==len(y)) and (len(x)==len(z)),'arrays must all be same length'
        self.__check_assert(typ='xyz',**d)
        datf = pd.DataFrame({'x':x,'y':y,'z':z})
        datf.info = label
        self.__df.append(datf)
        self.__d.update(self.__clean_dict(d))
    
    def __repr__(self):
        return ''
    
    def __clean_dict(self,d):
        return {k:v for k,v in d.items() if k in Fplot.__expectD[self.__kind]}   

    def show(self):
        dd = self.__clean_axis_dict(self.__d)
        if self.__kind == Fplot.__G2D:
            if len(self.__df)>1:
                return self.__df[0].scatter2D(x='x',y='y',other_df=self.__df[1:],**self.__d),self.__init__(kind=Fplot.__G2D,**dd)
            else:
                return self.__df[0].scatter2D(x='x',y='y',**self.__d),self.__init__(kind=Fplot.__G2D,**dd)
        elif self.__kind == Fplot.__G3D:
            if len(self.__df)>1:
                return self.__df[0].scatter3D(x='x',y='y',z='z',other_df=self.__df[1:],**self.__d),self.__init__(kind=Fplot.__G3D,**dd)
            else:
                return self.__df[0].scatter3D(x='x',y='y',z='z',**self.__d),self.__init__(kind=Fplot.__G3D,**dd)
        elif self.__kind == Fplot.__GV2:
            return self.__df[0].draw_vectors(point=('x','y'),vector=('ux','uy'),**self.__d),self.__init__(kind=Fplot.__GV2,**dd)
        elif self.__kind == Fplot.__GV3:
            return self.__df[0].draw_vectors(point=('x','y','z'),vector=('ux','uy','uz'),**self.__d),self.__init__(kind=Fplot.__GV3,**dd)
        elif self.__kind == Fplot.__H:
            return self.__df[0].histogram(x=list(self.__df[0].columns),**self.__d),self.__init__(kind=Fplot.__H,**dd)

