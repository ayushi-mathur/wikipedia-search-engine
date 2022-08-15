class abc:
    val = 0
    
    def fun(self):
        abc.val+=1

obj = abc()
print(abc.val)
obj.fun()
print(abc.val)