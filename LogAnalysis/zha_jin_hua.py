import random
import string

# 1:单张,2:对子,3:顺子,4:金子,5:豹子


# 比较两个数字的大小
def compare_num(card1, card2):
    if card1 > card2:
        return 1
    elif card1 < card2:
        return 2
    else:
        return 0


# 牌面值转数字
def str_to_num(str_num):
    if str_num.isdigit():
        return int(str_num)
    elif str_num == 'J':
        return 11
    elif str_num == 'Q':
        return 12
    elif str_num == 'K':
        return 13
    else:  # 代表'A'
        return 14


# 判断是不是豹子
def is_leopard(card):
    if card[0][2:] == card[1][2:] and card[0][2] == card[2][2:]:
        print('有豹子出现!!')
        return 5
    return 0


# 判断是不是同色
def is_gold(card):
    if card[0][:2] == card[1][:2] and card[0][:2] == card[2][:2]:
        print('有金子出现!!')
        return 4
    return 0


# 判断是不是顺子
def is_order(card):
    num1 = str_to_num(card[0][2:])
    num2 = str_to_num(card[1][2:])
    num3 = str_to_num(card[2][2:])
    num_arr = [num1, num2, num3]
    num_arr.sort()
    if num_arr[0]+1 == num_arr[1] and num_arr[1]+1 == num_arr[2]:
        print('有顺子出现!!')
        return 3
    if num_arr[0] == 2 and num_arr[1] == 3 and num_arr[2] == 14:
        print('有顺子出现!!')
        return 3
    return 0


# 判断是不是对子或单张
def is_double(card):
    num1 = str_to_num(card[0][2:])
    num2 = str_to_num(card[1][2:])
    num3 = str_to_num(card[2][2:])
    num_arr = [num1, num2, num3]
    num_set = set(num_arr)
    if len(num_set) == 2:
        print('有对子出现!!')
        return 2
    else:
        print('是单张!!')
        return 1


# 比较单张
def compare_single(card1, card2):
    num_arr1 = [str_to_num(card1[0][2:]), str_to_num(card1[1][2:]), str_to_num(card1[2][2:])]
    num_arr2 = [str_to_num(card2[0][2:]), str_to_num(card2[1][2:]), str_to_num(card2[2][2:])]
    num_max1 = max(num_arr1)
    num_max2 = max(num_arr2)
    res1 = compare_num(num_max1, num_max2)
    if res1 == 0:
        num_arr1.remove(num_max1)
        num_arr2.remove(num_max2)
        num_max12 = max(num_arr1)
        num_max22 = max(num_arr2)
        res2 = compare_num(num_max12, num_max22)
        if res2 == 0:
            num_arr1.remove(num_max12)
            num_arr2.remove(num_max22)
            num_max13 = num_arr1[0]
            num_max23 = num_arr2[0]
            res3 = compare_num(num_max13, num_max23)
            if res3 == 0:
                print('三张单牌大小一样...')
                return 0
            elif res3 == 2:
                return 2
            else:
                return 0
        elif res2 == 2:
            return 2
        else:
            return 0
    elif res1 == 2:
        return 2
    else:
        return 0


# 比较顺子的大小
def compare_order_num(card1, card2):
    num_arr1 = [str_to_num(card1[0][2:]), str_to_num(card1[1][2:]), str_to_num(card1[2][2:])]
    num_arr2 = [str_to_num(card2[0][2:]), str_to_num(card2[1][2:]), str_to_num(card2[2][2:])]
    num_sum1 = num_arr1[0]+num_arr1[1]+num_arr1[2]
    num_sum2 = num_arr2[0]+num_arr2[1]+num_arr2[2]
    return compare_num(num_sum1, num_sum2)


# 比较对子的大小
def compare_double_num(card1, card2):
    num_arr1 = [str_to_num(card1[0][2:]), str_to_num(card1[1][2:]), str_to_num(card1[2][2:])]
    num_arr2 = [str_to_num(card2[0][2:]), str_to_num(card2[1][2:]), str_to_num(card2[2][2:])]
    num_arr1.sort()
    num_arr2.sort()
    num_double1 = 0
    num_double2 = 0
    for i in num_arr1:
        if num_arr1.count(i) == 2:
            num_double1 = i
            break
    for i in num_arr2:
        if num_arr2.count(i) == 2:
            num_double2 = i
            break
    if num_double1 < 1 or num_double2 < 1:
        print('比较对子错误!!')
        return 0

    res = compare_num(num_double1, num_double2)
    if res == 0:
        num_arr1.remove(num_double1)
        num_arr1.remove(num_double1)
        num_arr2.remove(num_double2)
        num_arr2.remove(num_double2)
        return compare_num(num_double1, num_double2)
    elif res == 1:  # card1 > card2
        return 0
    else:  # card2 > card1
        return 2


# 比较对子
def compare_double(card1, card2):
    res1 = is_double(card1)
    res2 = is_double(card2)
    res = compare_num(res1, res2)
    if res == 0:
        if res1 == 1:  # 都不是顺子
            return compare_single(card1, card2)
        else:  # 都是对子 比谁的大
            res = compare_double_num(card1, card2)
            if res == 2:
                return 2
            else:
                return 0
    elif res == 1:  # card1 > card2
        return 0
    else:  # card2 > card1
        return 2


# 比较顺子
def compare_order(card1, card2):
    res1 = is_order(card1)
    res2 = is_order(card2)
    res = compare_num(res1, res2)
    if res == 0:
        if res1 == 0:  # 都不是顺子
            return compare_double(card1, card2)
        else:  # 都是顺子 比谁的大
            res = compare_order_num(card1, card2)
            if res == 2:
                return 2
            else:
                return 0
    elif res == 1:  # card1 > card2
        return 0
    else:  # card2 > card1
        return 2


# 比较金子中的情况
def compare_gold_order(card1, card2):
    res1 = is_order(card1)
    res2 = is_order(card2)
    res = compare_num(res1, res2)
    if res == 0:
        if res1 == 0:  # 都不是顺子
            return compare_single(card1, card2)
        else:  # 都是顺子 比谁的顺子大
            res = compare_order_num(card1, card2)
            if res == 2:
                return 2
            else:
                return 0
    elif res == 1:  # card1 > card2
        return 0
    else:  # card2 > card1
        return 2


# 比较金子
def compare_gold(card1, card2):
    res1 = is_gold(card1)
    res2 = is_gold(card2)
    res = compare_num(res1, res2)
    if res == 0:
        if res1 == 0:  # 都不是金子 继续比
            return compare_order(card1, card2)
        else:  # 都是金子 比谁的金子大
            res = compare_gold_order(card1, card2)
            if res == 2:
                return 2
            else:
                return 0
    elif res == 1:  # card1 > card2
        return 0
    else:  # card2 > card1
        return 2


# 比较豹子
def compare_leopard(card1, card2):
    res1 = is_leopard(card1)
    res2 = is_leopard(card2)
    res = compare_num(res1, res2)
    if res == 0:
        if res1 == 0:  # 都不是豹子 继续比
            return compare_gold(card1, card2)
        else:  # 都是豹子 比谁的豹子大
            res = compare_num(str_to_num(card1[0][2:]), str_to_num(card2[0][2:]))
            if res == 2:
                return 2
            else:
                return 0
    elif res == 1:  # card1 > card2
        return 0
    else:  # card2 > card1
        return 2




# 生成牌
cards = []
arr1 = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
arr2 = ['黑桃','红桃','方片','梅花']
for num in arr1:
    for color in arr2:
        cards.append(color+num)
# print(len(cards), cards)

num_card_person = 3


def game_start(personnum):
    person_info = {}
    # 生成用户信息
    start_index = 1
    while start_index <= personnum:
        name_len = random.randint(4, 8)
        name_arr = random.sample(string.ascii_lowercase, name_len)
        name_str = "".join(name_arr)
        person_info[name_str.title()] = []
        start_index += 1
    num_person = len(person_info)
    # 取牌 发牌
    select_card = random.sample(cards, num_person*num_card_person)
    card_index = 0
    for info in person_info:
        index = 0
        while index < num_card_person:
            person_info.get(info).append(select_card[card_index * num_card_person + index])
            index += 1
        card_index += 1

    for info in person_info:
        print(info, ':', person_info[info])

    # 比较每个人牌的大小
    biggest_cards = []
    for info in person_info:
        if len(biggest_cards) < 1:
            biggest_cards.append(info)
            biggest_cards.append(person_info.get(info))
            continue
        print('-' * 10)
        biggest_card_info = biggest_cards[1]
        now_card_info = person_info.get(info)
        # 比较豹子
        res1 = compare_leopard(biggest_card_info, now_card_info)
        if res1 == 1:
            print('biggest_card_info>now_card_info!!!')
        elif res1 == 2:
            biggest_cards[0] = info
            biggest_cards[1] = now_card_info
        else:
            # print('牌面相等!!!')
            continue
        print('-' * 10)
    print('Winner:', biggest_cards)


while True:
    num_person_str = input('请输入玩炸金花的人数（必须2-7）:')
    if not num_person_str.isdigit():
        print('非法输入!!')
        continue
    num_person = int(num_person_str)
    if num_person < 2 or num_person > 7:
        exit('输入人数错误,已退出!')
    game_start(num_person)


