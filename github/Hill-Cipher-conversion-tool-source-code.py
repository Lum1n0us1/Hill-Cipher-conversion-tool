import numpy as np
import sys
from tkinter import *


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("Hill密码转换工具")  # 窗口名
        self.init_window_name.geometry('700x500+300+120')
        self.init_window_name["bg"] = "Lavender"

        # 标签
        self.crypto_string_label = Label(self.init_window_name, text="加/解密字符串", font=13)
        self.crypto_string_label.place(x=80, y=60)

        self.row_num_label = Label(self.init_window_name, text="矩阵行数", font=13)
        self.row_num_label.place(x=120, y=120)

        self.encrypt_matrix_label = Label(self.init_window_name, text="加密矩阵", font=13)
        self.encrypt_matrix_label.place(x=120, y=220)

        self.encrypt_matrix_label = Label(self.init_window_name, text="(空格分隔)", font=13)
        self.encrypt_matrix_label.place(x=110, y=240)

        self.crypto_result_label = Label(self.init_window_name, text="加/解密结果", font=13)
        self.crypto_result_label.place(x=100, y=330)

        self.supple_string_label = Label(self.init_window_name, text="字符增补记录", font=13)
        self.supple_string_label.place(x=90, y=400)

        # 文本框
        self.crypto_string_Text = Text(self.init_window_name, width=40, height=2)  # 加/解密字符串
        self.crypto_string_Text.place(x=220, y=60)

        self.row_num_Text = Text(self.init_window_name, width=40, height=2)  # 矩阵行数
        self.row_num_Text.place(x=220, y=120)

        self.encrypt_matrix_Text = Text(self.init_window_name, width=40, height=9)  # 加密矩阵
        self.encrypt_matrix_Text.place(x=220, y=180)

        self.crypto_result_Text = Text(self.init_window_name, width=40, height=2)  # 加/解密结果
        self.crypto_result_Text.place(x=220, y=330)

        self.supple_string_Text = Text(self.init_window_name, width=40, height=2)
        self.supple_string_Text.place(x=220, y=400)

        # 按钮
        self.encrypt_button = Button(self.init_window_name, text="加密", bg="LavenderBlush", width=10,
                                     command=self.encrypt)
        self.encrypt_button.place(x=580, y=150)

        self.decrypt_button = Button(self.init_window_name, text="解密", bg="LavenderBlush", width=10,
                                     command=self.decrypt)
        self.decrypt_button.place(x=580, y=300)

    # 判断矩阵是否存在逆矩阵
    def judge_inverse_matrix(self, matrix):
        try:
            np.linalg.inv(matrix)
        except:
            return False
        return True

    # 输入列表并转换为矩阵
    def inputmatrix(self):
        row_num = int(self.row_num_Text.get("1.0", "end"))
        all_list = []
        num_list2 = []
        num_list = self.encrypt_matrix_Text.get("1.0", "end").split(' ')
        for a in num_list:
            # 文本框输入的最后一位有换行符，需要去掉
            num_list2.append(int(a.strip('\n')))

        # 生成矩阵
        for num in num_list2:
            num_list2[num_list2.index(num)] = int(num_list2[num_list2.index(num)])
        for i in range(0, len(num_list2), row_num):
            all_list.append(num_list2[i: i + row_num])
        encrypt_matrix = np.array(all_list)
        if not self.judge_inverse_matrix(encrypt_matrix):
            # print("该矩阵不存在逆矩阵，请重修输入")
            self.crypto_result_Text.delete("1.0", "end")
            self.crypto_result_Text.insert("1.0", "该矩阵不存在逆矩阵，请重修输入")
        return encrypt_matrix

    # 生成矩阵的逆矩阵。如果逆矩阵含有小数，就四舍五入
    def generate_inverse_matrix(self, matrix):
        inverse_matrix = np.linalg.inv(matrix)
        print("加密矩阵的逆矩阵为：")
        for array in inverse_matrix:
            print(array)
        return inverse_matrix

    # 生成字母-数字对应的字典
    def alphabet_number(self):
        alphabet_number_dict = {}
        for i in range(97, 123):
            alphabet_number_dict[chr(i)] = i % 97
        return alphabet_number_dict

    def encrypt(self):
        # 按下加密按钮后获取文本框内明文
        input_plaintext = self.crypto_string_Text.get("1.0", "end").strip('\n')

        # 明文字母转换成对应数字
        num_list = []
        dic = self.alphabet_number()
        for i in input_plaintext:
            num_list.append(dic[i])

        # 如果矩阵行数不能整除明文，则用'z'的数字25补全
        matrix = self.inputmatrix()
        row_num = len(matrix)
        supple_num = row_num - (len(num_list) % row_num)
        if len(num_list) % row_num != 0:
            for n in range(1, supple_num + 1):
                num_list.append(25)
        output = f"添加了{supple_num}个z补全明文"
        self.supple_string_Text.delete("1.0", "end")
        self.supple_string_Text.insert("1.0", output)

        # 分组加密
        group_num = int(len(num_list) / row_num)
        whole_encrypt_num_list = []
        for g in range(0, group_num):
            plaintext_matrix = np.array(num_list[0 + g * row_num: (g + 1) * row_num])
            encrypt_num_list = np.matmul(plaintext_matrix, matrix)
            for num in encrypt_num_list:
                whole_encrypt_num_list.append(num)

        # 将加密后的数字转换为字母
        ciphertext = ""
        for ennum in whole_encrypt_num_list:
            # 对超出范围的数字取模
            if ennum > 25:
                ennum = ennum % 26
            for k in dic:
                if dic[k] == ennum:
                    ciphertext = ciphertext + k
        self.crypto_result_Text.delete("1.0", "end")
        self.crypto_result_Text.insert("1.0", ciphertext)
        # print("加密后密文为：", ciphertext, '\n')

    def decrypt(self):
        # 输入密文并转换为对应数字
        input_ciphertext = self.crypto_string_Text.get("1.0", "end").strip('\n')
        num_list2 = []

        dic2 = self.alphabet_number()
        for i in input_ciphertext:
            num_list2.append(dic2[i])

        # 解密就不添加'z'来补全密文了
        matrix = self.inputmatrix()
        row_num2 = len(matrix)
        supple_num2 = row_num2 - (len(num_list2) % row_num2)

        # 用逆矩阵分组解密
        inserve_matrix = self.generate_inverse_matrix(matrix)
        group_num2 = int(len(num_list2) / row_num2)
        whole_decrypt_num_list = []
        for g in range(0, group_num2):
            plaintext_matrix = np.array(num_list2[0 + g * row_num2: (g + 1) * row_num2])
            decrypt_num_list = np.matmul(plaintext_matrix, inserve_matrix)
            for num in decrypt_num_list:
                whole_decrypt_num_list.append(num)

        # 将矩阵中的数字四舍五入
        for j in range(len(whole_decrypt_num_list)):
            whole_decrypt_num_list[j] = round(whole_decrypt_num_list[j])

        # 将解密后的数字转换为对应字母
        plaintext = ""
        for denum in whole_decrypt_num_list:
            if denum > 25 or denum < -26:
                denum = denum % 26

            # 防止取模后是负数，字典中找不到对应的字母
            if denum < 0:
                denum = denum + 26

            # 字典中寻找与数字对应的字母
            for k in dic2:
                if dic2[k] == denum:
                    plaintext = plaintext + k
        self.crypto_result_Text.delete("1.0", "end")
        self.crypto_result_Text.insert("1.0", plaintext)
        # print("解密后明文为：", plaintext, '\n')
        self.supple_string_Text.delete("1.0", "end")


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()
