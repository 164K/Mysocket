import tkinter as tk 

root = tk.Tk()

#创建主框架frame
frame = tk.Frame(root, height=300, width=300, bg='blue', relief='raised',bd=3)
frame.pack(padx=10, pady=10)
 
#创建第二层框架frame_l和frame_r，分别左右放置在主框架frame上
frame_t = tk.Frame(frame, height=100, width=50, bg='red')
frame_b = tk.Frame(frame, height=100, width=50, bg='yellow')
frame_t.pack(side='top',padx=20, pady=20)
frame_b.pack(side='bottom',padx=20, pady=20)
 
# #创建多个标签，分别放置在第二层的frame_l、frame_r上
tk.Label(frame_t, text='左上', bg='white').pack(padx=10, pady=10)
tk.Label(frame_t, text='左下', bg='green').pack(padx=10, pady=10)
tk.Label(frame_b, text='右上', bg='purple').pack(padx=10, pady=10)
tk.Label(frame_b, text='右下', bg='pink').pack(padx=10, pady=10)
 
root.mainloop()