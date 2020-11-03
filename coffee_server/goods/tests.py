from django.test import TestCase

# Create your tests here.



# 商品列表格式
"""
<div class="andro_product andro_product-list">
            <div class="andro_product-thumb">
              <a href="product-single.html"><img src="/static/img/products/2.png" alt="product"></a>
            </div>
            <div class="andro_product-body">
              <div class="andro_rating-wrapper">
                <div class="andro_rating">
                  <i class="fa fa-star active"></i>
                  <i class="fa fa-star active"></i>
                  <i class="fa fa-star active"></i>
                  <i class="fa fa-star active"></i>
                  <i class="fa fa-star"></i>
                </div>
                <span>4 星</span>
              </div>
              <h5 class="andro_product-title"> <a href="product-single.html"> 草莓摩卡 </a> </h5>
              <p>草莓摩卡咖啡，是世界著名咖啡之一。将一半的草莓果粒果酱和一半的冰牛奶放入到钢杯中。
                再加入草莓浓缩汁，用咖啡机蒸汽管加热至约65℃。
                再将另一半的冰牛奶和糖浆倒入钢杯，用咖啡机蒸汽管加热至约65℃。
                在温好杯的玻璃杯中，放入剩余一半的草莓果粒果酱。
                把之前打发好的草莓牛奶倒入杯中，动作要慢。
                再用勺子挡着，慢慢地注入奶泡的部分。
                用同样的方式缓缓地倒入浓缩咖啡。
                在表面挖上奶泡即可。</p>
              <div class="andro_product-footer">
                <div class="andro_product-price">
                  <span>￥19</span>
                  <span>￥29</span>
                </div>
                <div class="btn-group">
                  <a href="product-single.html" class="andro_btn-custom btn-sm">现在购买</a>
                  <button type="button" class="andro_btn-custom dropdown-toggle dropdown-toggle-split btn-sm" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span class="sr-only">Toggle Dropdown</span>
                  </button>
                  <div class="dropdown-menu">
                    <a class="dropdown-item" href="#" data-toggle="modal" data-target="#quickViewModal"> <i class="fa fa-eye"></i> 快速浏览</a>
                    <a class="dropdown-item" href="#"> <i class="fa fa-sync"></i> 对比</a>
                    <a class="dropdown-item" href="#"> <i class="fa fa-heart"></i> 添加到愿望清单</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          """
# print(bool("0"))
# import html
#
# print(html.escape("</div>")) # &lt;/div&gt;
import time

# print(time.ctime())

print(time.localtime(time.time()))