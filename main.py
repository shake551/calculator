from tkinter import *
from tkinter import ttk
import numpy as np
import decimal

#ボタン配置を二次元配列で管理
LAYOUT = [["AC", "C", "", ""],
           ["(", ")", "^", "%"],
           ["sin", "cos", "tan", "÷"],
           ["7", "8", "9", "×"],
           ["4", "5", "6", "-"],
           ["1", "2", "3", "+"],
           ["0", ".", "π", "="]]

#演算子を定数で管理
OPERATOR = ("+", "-", "*", "**", "/", "//", "%", "^", ".", "÷", "×")
#三角関数を定数で管理
TRIGONO = ("sin", "cos", "tan", "π")


#演算子を変換する関数
def change_operator(self):
        if self == "×":
            return "*"
        elif self == "÷":
            return "/"
        elif self == "^":
            return "**"
        else:
            return self

class CalcApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.count_list = ["0"]   #計算用
        self.display_list = ["0"] #表示用
        self.create_style()
        self.create_widgets()
    
    def create_style(self):
        '''ボタン、ラベルのスタイル変更'''
        style = ttk.Style()

        #ラベルのスタイルを上書き
        style.configure('TLabel', font=('Helvetica', 20),
        highlightbackground='gray', foreground='black')

        #ボタンのスタイルを上書き
        style.configure('TButton', font=('Helvetica', 20))

    def create_widgets(self):
        '''ウィジェットの作成'''
        #計算結果表示ラベル
        self.display_var = StringVar()
        self.display_var.set('0')  #初期値を0に設定

        display_label = ttk.Label(self, textvariable=self.display_var)
        display_label.grid(column=0, row=0, columnspan=4, sticky=(N, S, E, W))
    

        #レイアウトの作成
        for y, row in enumerate(LAYOUT, 1):
            for x, char in enumerate(row):
                button = ttk.Button(self, text=char)
                button.grid(column=x, row=y, sticky=(N, S, E, W))
                button.bind('<Button-1>', self.calc)
        self.grid(column=0, row=0, sticky=(N, S, E, W))

        #横の引き伸ばし
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        #縦の引き伸ばし
        #0番目の結果表示欄は元の大きさ
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        #ウィンドウの引き伸ばし設定
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def calc(self, event):
        #押されたボタンのテキストを取得
        char = event.widget["text"]

        #最後に押したボタンの内容
        last = self.count_list[-1]
        
        if char == "=":
            #一個前が演算子ならそれを消す
            if last in OPERATOR:
                self.count_list.pop()
            #listを結合しeval関数で計算
            count = eval(''.join(self.count_list))
            self.count_list = [str(count)]
            self.display_list = [str(count)]
        
        elif char == "AC":
            #list内を0で初期化
            self.count_list = ["0"]
            self.display_list = ["0"]

        elif char == "C":
            if last in OPERATOR:
                #listの要素が3以上の時2つ消す
                if len(self.count_list) > 2:
                    self.count_list.pop()
                    self.count_list.pop()
                    self.display_list.pop()
                    self.display_list.pop()
                #それ以外は0で初期化
                else:
                    self.count_list = ["0"]
                    self.display_list = ["0"]
            else:
                #最後が数字
                #listの要素数が2以上の時1つ消す
                if len(self.count_list) > 1:
                    self.count_list.pop()
                    self.display_list.pop()
                #それ以外は0で初期化
                else:
                    self.count_list = ["0"]
                    self.display_list = ["0"]

        elif char in OPERATOR:
            #最後の入力が演算子で、今の入力も演算子の時
            if last in OPERATOR:
                #演算子を上書き
                self.count_list[-1] = change_operator(char)
                self.display_list[-1] = char
            else:
                #最後の入力が数値
                self.count_list.append(change_operator(char))
                self.display_list.append(char)

        elif char in TRIGONO:
            if last in OPERATOR:
                if char == "sin": 
                    self.count_list.append("np.sin")
                    self.display_list.append("sin")
                elif char == "cos":
                    self.count_list.append("np.cos")
                    self.display_list.append("cos")
                elif char == "tan":
                    self.count_list.append("np.tan")
                    self.display_list.append("tan")
            else:
                if char == "sin":
                    if last == "0":
                        self.count_list.pop(-1)
                        self.display_list.pop(-1)
                    if len(self.count_list) != 0: 
                        self.count_list.append("*")
                    self.count_list.append("np.sin")
                    self.display_list.append("sin")
                elif char == "cos":
                    if last == "0":
                        self.count_list.pop(-1)
                        self.display_list.pop(-1)
                    if len(self.count_list) != 0:
                        self.count_list.append("*")
                    self.count_list.append("np.cos")
                    self.display_list.append("cos")
                elif char == "tan":
                    if last == "0":
                        self.count_list.pop(-1)
                        self.display_list.pop(-1)
                    if len(self.count_list) != 0:
                        self.count_list.append("*")
                    self.count_list.append("np.tan")
                    self.display_list.append("tan")
                elif char == "π":
                    if last == "0":
                        self.count_list.pop(-1)
                        self.display_list.pop(-1)
                    elif last == OPERATOR:
                        a = 1
                    elif last == TRIGONO:
                        a = 1
                    elif last == "(":
                        a = 1
                    else:
                        self.count_list.append("*")
                    self.count_list.append("np.pi")
                    self.display_list.append("π")
        
        elif char == "(":
            if last == "0":
                self.count_list.pop(-1)
                self.display_list.pop(-1)
            elif last in OPERATOR:
                a = 1
            elif last in TRIGONO:
                if last == "π":
                    self.count_list.append("*")
            else:
                self.count_list.append("*")
            self.count_list.append(char)
            self.display_list.append(char)

        #今の入力が数値
        else:
            #最後の入力が演算子
            if last in OPERATOR:
                #リストの末尾に入力された数値を追加
                self.count_list.append(char)
                self.display_list.append(char)
            #最後の入力が数値で、0じゃない
            elif last != "0":
                #1の位に ex)1->15
                self.count_list[-1] += char
                self.display_list[-1] += char
            #最後の入力が0
            elif last == "0":
                #上書き
                self.count_list[-1] = char
                self.display_list[-1] = char
        
        #リストに格納している式を文字列にし、画面に反映
        self.display_var.set(' '.join(self.display_list))
        print(self.count_list)

def main():
    root = Tk()
    root.title("電卓")
    CalcApp(root)
    root.mainloop()
        
if __name__ == "__main__":
    main()