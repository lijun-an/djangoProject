from django.utils.safestring import mark_safe
import copy
import math


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", page_show=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据(根据此数据进行分页处理)
        :param page_size: 每页显示多少条数据
        :param page_param: 获取在URL中传递的分页参数, 例如: /pretty/list/?page=21
        :param page_show: 页码显示前几页后几页
        """
        # 防止搜索出结果进行翻页时,URL参数没有了搜索参数
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        # 当前页面数.如果不是整数
        self.page = int(query_dict.get(page_param, 1))
        # 如果不是整数
        if type(self.page) != int:
            # 强制让页码为1
            self.page = 1
        # 数据总数
        self.data_count = queryset.count()
        # 页面数
        self.total_page = math.ceil(self.data_count / page_size)
        self.start_page = self.page - page_show
        self.end_page = self.page + page_show
        self.page_param = page_param
        self.page_show = page_show
        self.page_size = page_size
        self.page_data = queryset[page_size * (self.page - 1):page_size * self.page]

    def html(self):
        page_string_list = []
        # 跳到首页
        head_page = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'.format(
            self.get_param_url(1))
        page_string_list.append(head_page)
        # 跳到上10页
        # 如果当前页面小于 11, 防止超过最小页数
        if self.page < self.page_show * 2 + 1:
            prev = '<li><a href="?{}">{}</a></li>'.format(self.get_param_url(1), "<<")
            page_string_list.append(prev)
        else:
            prev = '<li><a href="?{}">{}</a></li>'.format(self.get_param_url(self.page - 10), "<<")
            page_string_list.append(prev)
        # 处理特殊情况
        if self.page <= self.page_show:
            self.start_page = 1
        if self.page >= self.total_page - self.page_show:
            self.end_page = self.total_page
        for p in range(self.start_page, self.end_page + 1):
            if p == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.get_param_url(p), p)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.get_param_url(p), p)
            page_string_list.append(ele)
        # 跳到下10页
        # 如果当前页面页数 大于 最大页面数量减去(page_show*2+1),则直接跳到最后一页,防止超过最大页数
        if self.page >= self.total_page - self.page_show * 2 + 1:
            next = '<li><a href="?{}">{}</a></li>'.format(self.get_param_url(self.total_page), ">>")
            page_string_list.append(next)
        else:
            next = '<li><a href="?{}">{}</a></li>'.format(self.get_param_url(self.page + 10), ">>")
            page_string_list.append(next)
        # 跳到尾页
        end_page = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">尾页</span></a></li>'.format(
            self.get_param_url(self.total_page))
        page_string_list.append(end_page)
        page_string = mark_safe(''.join(page_string_list))
        return page_string

    def get_param_url(self, p):
        self.query_dict.setlist(self.page_param, [p])
        return self.query_dict.urlencode()
