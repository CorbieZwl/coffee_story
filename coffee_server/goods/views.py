from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from coffee_server import settings
from goods.models import GoodsInfo
from random import randint
from message.models import Messages
import html
from urllib import parse

# 数据插入
temperature_list = ["cold", "hot"]


# 问题  1.跨域资源共享 分而治之 函数合理分工   判断页面是否已到尽头
class GoodsView(View):

    # 根据参数返回商品列表
    def make_goods_list(self, st, num):
        # 当st为0时 以第一条数据为起始点  "0"的布尔值为True 分情况讨论
        if st == "0":
            try:
                coffees = GoodsInfo.objects.filter(num__gt=0).order_by('id')[:int(num)]
            except Exception as e:
                print(e)
                result = {"code": "10001", "error": f"error is {e}"}
                return result
        else:
            try:
                coffees = GoodsInfo.objects.filter(id__gt=int(st),num__gt=0)[:int(num)]
            except Exception as e:
                print(e)
                result = {"code": "10002", "error": f"error"}
                return result
        # 若无异常抛出 则返回num条咖啡数据 初始化数据列表
        coffees_list = []
        edl = []
        for i in coffees:
            # 图片路径
            a = i.imgurl
            imgurl=a.replace('127.0.0.1',settings.IP_str)
            # 评分
            score = i.score
            # 咖啡名
            name = i.name
            # 备注
            remark = i.remark
            # 价格
            price = i.price
            # 唯一编号
            id = i.id
            edl.append(i.id)
            coffees_list.append(
                {"imgurl": imgurl, "id": id, "score": score, "name": name, "remark": remark, "price": price})
        result = {"code": "200", "data": {"end": max(edl), "coffees": coffees_list}}
        return result

    # 获取单条商品信息
    def make_goods_info(self, goods_id):
        try:
            goods = GoodsInfo.objects.get(id=goods_id)
        except Exception as e:
            print(e)
            result = {"code": "10003", "error": f"error is {e}"}
        else:
            # 大于good_id的第一个 和小于good_id的第一个 默认升序
            # 下一个
            next_gs = GoodsInfo.objects.filter(id__gt=goods_id).first()
            # 上一个
            last_gs = GoodsInfo.objects.filter(id__lt=goods_id).last()
            id = goods.id
            a = goods.imgurl
            imgurl = a.replace('127.0.0.1', settings.IP_str)
            score = goods.score
            name = goods.name
            price = goods.price
            remark = goods.remark
            # 根据商品对象取出所有评论
            # 初始化评论列表
            messages = []
            # 获取所有评论
            all_message = Messages.objects.filter(goods_info=goods)
            print(all_message)
            # 添加到评论数据列表
            for i in all_message:
                content = html.escape(i.content)
                messages.append({"user": i.user_info.nickname, "time": i.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 "content": content})
            if next_gs:
                next_gs_id = next_gs.id
                next_gs_name = next_gs.name
                a =next_gs.imgurl
                imgurl = a.replace('127.0.0.1', settings.IP_str)
                next_gs_img = imgurl
            else:
                next_gs_id = None
                next_gs_name = None
                next_gs_img = None
            if last_gs:
                last_gs_id = last_gs.id
                last_gs_name = last_gs.name
                a = last_gs.imgurl
                imgurl = a.replace('127.0.0.1', settings.IP_str)
                last_gs_img = imgurl
            else:
                last_gs_id = None
                last_gs_name = None
                last_gs_img = None
            result = {"code": "200",
                      "data": {'id':id,"imgurl": imgurl, "score": score, "name": name, "price": price, "remark": remark,
                               "next_gs_id": next_gs_id, "next_gs_name": next_gs_name, "next_gs_img": next_gs_img,
                               "last_gs_id": last_gs_id, "last_gs_name": last_gs_name, "last_gs_img": last_gs_img,
                               "messages": messages}}
            return result

            # 获取商品 ？st=0&num=6

    # good_id 不确定是否传参时 给定缺省值
    def get(self, request, goods_id=None):
        # print("----------------------------------")
        # 获取多条数据  获取商品的查询字符串有两种 一种是等差获取  一种是关键字获取 查询字符串分别为st&num 或 word
        if not goods_id:

            st = request.GET.get("st")
            num = request.GET.get("num")
            word = request.GET.get('word')
            # 当word存在时 说明是通过搜索栏获取商品
            if word is not None:
                # 先对编码后对关键字解码
                word = parse.unquote(word)
                print(word,'-------')
                result = self.get_word_select_dara(word)
                return JsonResponse(result)

            # 当word不存在且st和num都存在时 返回以大于st的第一条数据开头的num条数据
            elif st and num:
                # 调用函数生成数据
                result = self.make_goods_list(st, num)
                return JsonResponse(result)
            else:
                result = {"code": "10004", "error": "st or num is None"}
                return JsonResponse(result)
        # 获取单条数据
        else:
            result = self.make_goods_info(goods_id)
            # print(result)
            return JsonResponse(result)

    def post(self, request):
        pass

    def get_word_select_dara(self, word):
        """用于返回关键在搜索请求的数据"""
        # 当关键字为空或关键字为咖啡时
        if not word or word == '咖啡':
            result = {"code": 200, "data": []}
            return result
        print(word, '-------')
        # orm模糊查询
        try:
            # 等价于 like "%data%"
            info = GoodsInfo.objects.filter(name__contains=word)
        except Exception as e:
            print(e)
            result = {"code": 200, "data": []}
            return result

        # 结果为空时
        if not info:
            result = {"code": 200, "data": []}
            return result

        # 结果不为空 组织响应数据
        goods_info_list = []
        for one_info in info:
            item = {}
            # 图片路径
            a = one_info.imgurl
            imgurl = a.replace('127.0.0.1', settings.IP_str)
            item['imgurl'] =imgurl
            # 评分
            item['score'] = one_info.score
            # 咖啡名
            item['name'] = one_info.name
            # 备注
            item['remark'] = one_info.remark
            # 价格
            item['price'] = one_info.price
            # 唯一编号
            item['id'] = one_info.id
            goods_info_list.append(item)
        result = {"code": 200, "data": goods_info_list}
        return result


def asdas(request):
    # 插入数据函数
    # ["id","name","price","temperature","brand","indent_num","inventory","score","pnumber","remark"]
    l = [{"name": "草莓摩卡", "remark": """草莓摩卡咖啡，是世界著名咖啡之一。将一半的草莓果粒果酱和一半的冰牛奶放入到钢杯中。
                    再加入草莓浓缩汁，用咖啡机蒸汽管加热至约65℃。
                    再将另一半的冰牛奶和糖浆倒入钢杯，用咖啡机蒸汽管加热至约65℃。
                    在温好杯的玻璃杯中，放入剩余一半的草莓果粒果酱。
                    把之前打发好的草莓牛奶倒入杯中，动作要慢。
                    再用勺子挡着，慢慢地注入奶泡的部分。
                    用同样的方式缓缓地倒入浓缩咖啡。
                    在表面挖上奶泡即可。"""},
         {"name": "阿拉比卡绿", "remark": """阿拉比卡咖啡豆是Arabica植物的浆果种子，并且是两种用于生产咖啡的咖啡豆之一，另一种是Robusta。阿拉比卡咖啡豆的咖啡因含量少，酸度低，口味更芳香，因此被许多咖啡爱好者视为上等咖啡豆。一些咖啡混合了Arabica和Robusta两种咖啡豆，这样能在降低成本的情况下改善口味，但标准最高的咖啡大多数是用100%的纯阿拉比卡咖啡豆生产。

                Arabica咖啡树土生土长在西南阿拉伯半岛，已经有数千年的生长历史。然而，还可以在拉丁美洲和亚洲，以及非洲等亚热带和赤道地区发现这种咖啡豆的许多变种。全球大约有80%的咖啡产品都是用阿拉比卡咖啡豆生产的，剩下的不到20%是Robusta咖啡豆的市场。"""},
         {"name": "卡布奇诺", "remark": """卡布奇诺最大的特点是加入了大量的奶沫，这使它具有了强烈的口感，
          有些人喝它就是为了品味其奶沫的口感，享受奶沫的密度与紧实的感觉。这种奶沫的做法，
          是通过搅拌的方式，搅拌时的力度不同，时间不一，最终的奶沫也状态不一。奶沫打好之后，
          要浇到咖啡与奶的混合液体上，碰到一个热爱生活懂得美的咖啡店员，他会把奶沫浇出花样，
          不幸碰到平板的家伙，就只是咖啡加奶加奶沫了。所以，卡布奇诺有点像《阿甘正传》
          里阿甘妈常说的巧克力———你不知道下一杯会碰到什么样的卡布奇诺。"""},
         {"name": "阿拉比卡", "remark": """单就成分来看，阿拉比卡咖啡的咖啡因含量较低，比例约在0.9%到1.2%之间，脂肪和糖的含量相当丰富，因此气味柔和、不刺激，口感清新微甜，有时会带一些清爽怡人的酸味，受到绝大多数咖啡爱好者的喜爱。阿拉比卡咖啡抗虫能力弱，种植海拔高，结果实慢，因此，阿拉比卡多用于新鲜的咖啡制作。
                单从价格来看，阿拉比卡咖啡确实更加昂贵，其平均价格会比罗布斯塔咖啡高1.5到2倍。但凡事没有绝对，品质上等的罗布斯塔咖啡绝对优于平庸的阿拉比卡咖啡。近年来，在越南等地，咖啡农们尝试着提高罗布斯塔咖啡的种植高度，去除果中的杂味，培育了高品质的中果咖啡。"""},
         {"name": "罗布斯塔烘焙",
          "remark": "味，取而代之的是更厚、更沉稳的口感，以及仿佛吃到花生酱、榛果酱般强烈核桃、花生、榛果、小麦风味。罗布斯塔豆拥有许多阿拉比卡豆所没有的特质，只要熟悉并且充分掌握这些特质，一位优秀的咖啡烘焙师就能端出具有慑人魔力的菜肴（意式咖啡豆）。相较于阿拉比卡豆有44对染色体，罗布卡斯塔豆的染色体只有22对，咖啡因含量分别是1.5%以及2.8%，两者是完全不同的品种，不能混合配种，也说明了为何两者有许多完全相异之处。"},
         {"name": "意大利咖啡", "remark": """意大利咖啡Espresso是意式咖啡的精髓，他的做法起源于意大利，在意大利文中是“特别快”的意思，其特征乃是利用蒸汽压力，瞬间将咖啡液抽出。所有的牛奶咖啡或花式咖啡都是以Espresso为基础制作出来的。所以Espresso是检验一杯咖啡品质好坏的关键。
                种类有卡布奇诺咖啡、泡沫意大利咖啡(Macchiato) 、奶特/拿铁咖啡(Latte) 、克烈特和力士烈特(Ristretto)双倍浓度的意大利咖啡。"""}]
    for i in range(60):
        d = l[randint(0, 5)]
        GoodsInfo.objects.create(name=d["name"] + str(i),
                                 price=19,
                                 temperature=temperature_list[randint(0, 1)],
                                 brand="b01",
                                 indent_num=randint(30, 50),
                                 inventory=randint(100, 150),
                                 score=randint(1, 5),
                                 pnumber=randint(10, 20),
                                 remark=d["remark"],
                                 imgurl =f"http://127.0.0.1:8000/static/{randint(1,15)}.png")
    return HttpResponse("60条数据插入成功")
