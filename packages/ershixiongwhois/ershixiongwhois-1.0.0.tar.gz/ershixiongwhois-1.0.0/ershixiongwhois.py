
movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
        ["Grail Chapman",
         ["Michael Palin","Jone Cleese","Terry Gilliam","Eric Idel","Terry Jones"]]]

""" 定义函数print_lol  """
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
""" 定义函数结束      """
print_lol(movies)   #调用函数
print("\n")
