
movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
        ["Grail Chapman",
         ["Michael Palin","Jone Cleese","Terry Gilliam","Eric Idel","Terry Jones"]]]

""" 定义函数print_lol  """
def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end=" ")
                
            print(each_item)
""" 定义函数结束      """
print_lol(movies,1)   #调用函数
print("\n")
