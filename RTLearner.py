import numpy as np
import pandas as pd
class RTLearner:
    def __init__(self,leaf_size,verbose =False):
        self.leaf_size = leaf_size

    def author(self):
        return 'zluo76'

    def addEvidence(self,Xtrain,Ytrain):
        self.dt = self.buildtree(Xtrain,Ytrain)
        # print self.dt

    def query(self,Xtest):
        output = Xtest.copy()
        output[output.columns.values[0] +'_holding'] = output.apply(self.singlequery,axis = 1)
        output.ix[-1,output.columns.values[0] +'_holding'] = 0

        return output[[output.columns.values[0] +'_holding']]

    def singlequery(self,sigXtest):
        i = 0
        while (True):
            if sigXtest[self.dt[i][0]] <= self.dt[i][1] :
                i += self.dt[i][2]
            else:
                i += self.dt[i][3]
            if self.dt[i][0] == 'leaf':
                return self.dt[i][1]


    def getrandomweights(self,Xtrain,Ytrain):
        cors = []
        for i in range(Xtrain.shape[1]):
            cors.append(np.random.uniform())
        return cors

    def getsplitfeature(self,Xtrain,Ytrain):
        corlist = map(abs,self.getrandomweights(Xtrain,Ytrain))
        return corlist.index(np.nanmax(corlist))

    def issameY(self,Ytrain):
        temp = Ytrain.mean()
        for i in Ytrain:
            if i != temp:
                return False
        return True

    def smallerthanmed(self,Xtrain,bestf):
        med = np.median(Xtrain.ix[:,bestf])
        for i in Xtrain.ix[:,bestf]:
            if i > med:
                return False
        return True
    def find_mode(self, Ytrain):
        count = {}
        for i in Ytrain:
            if i in count:
                count[i]+= 1
            else:
                count[i] = 1
        return max(count, key=count.get)

    def buildtree(self,Xtrain,Ytrain):
#	print (Xtrain,Ytrain)
#	print (Xtrain.shape, Ytrain.shape)
        if Xtrain.shape[0] <= self.leaf_size:
            return [['leaf',self.find_mode(Ytrain),'','']]
        if self.issameY(Ytrain):
            return [['leaf',self.find_mode(Ytrain),'','']]
        else:
            bestf = self.getsplitfeature(Xtrain,Ytrain)
            SplitVal = np.median(Xtrain.ix[:,bestf]) if (not self.smallerthanmed(Xtrain,bestf)) else np.mean(Xtrain.ix[:,bestf])
	    if (len(Xtrain) == len(Xtrain.ix[Xtrain.ix[:,bestf] <= SplitVal])|(len(Xtrain) == 0)):
		return [['leaf',self.find_mode(Ytrain),'','']]
            lefttree = self.buildtree(Xtrain.ix[Xtrain.ix[:,bestf]<=SplitVal],Ytrain[Xtrain.ix[:,bestf]<=SplitVal])
            righttree = self.buildtree(Xtrain.ix[Xtrain.ix[:,bestf]>SplitVal],Ytrain[Xtrain.ix[:,bestf]>SplitVal])
            root = [bestf,SplitVal,1,len(lefttree)+1]
#	    print ([root]+lefttree+righttree)
#	    print SplitVal
            return ([root]+lefttree+righttree)
