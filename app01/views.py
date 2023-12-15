from django.shortcuts import render, HttpResponse, redirect
from app01.models import User, Department, Pretty, Admin
from app01.utils.pagiation import Pagination
from app01.form.form import PrettyModelForm, PrettyEditModelForm, UserModelForm, AdminModelForm, AdminEditModelForm, \
    AdminResetModelForm, LoginForm
from app01.utils.code import check_code
from django.shortcuts import HttpResponse
from io import BytesIO


# Create your views here.
def index(request):
    return redirect('/department/list')


# #################################   部门管理  # #################################
def department_list(request):
    """部门列表"""
    department_objs = Department.objects.all()
    return render(request, 'department_list.html', {'department_info': department_objs})


def department_add(request):
    """部门添加"""
    if request.method == "GET":
        return render(request, 'department_add.html')
    depart_name = request.POST.get('depart_name')
    # 保存到数据库
    Department.objects.create(name=depart_name)
    return redirect("/department/list/")


def department_delete(request):
    """部门删除"""

    nid = request.GET.get('nid')
    Department.objects.filter(id=nid).delete()
    # 重定向回部门列表
    return redirect("/department/list/")


def department_edit(request, nid):
    """部门编辑"""
    if request.method == "POST":
        # post请求将修改数据提交到数据库
        # 如果是POST请求,保存修改
        depart_name = request.POST.get('depart_name')
        Department.objects.filter(id=nid).update(name=depart_name)
        return redirect("/department/list/")
    # get请求，返回编辑页面
    department_obj = Department.objects.filter(id=nid).get()
    return render(request, 'department_edit.html', {'department_obj': department_obj})


# #################################   用户管理  # #################################
def user_list(request):
    # 获取所有用户列表
    user_data = User.objects.all()
    for user in user_data:
        print(user.get_gender_display())
    return render(request, "user_list.html", {"user_data": user_data})


def user_add(request):
    """用户添加"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})
        # 使用ModelForm进行验证POST请求提交数据
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 直接保存至数据库
        form.save()
        return redirect("/user/list/")
    # 校验失败(在页面上显示错误信息)
    return render(request, "user_add.html", {"form": form})


def user_delete(request):
    """用户删除"""
    nid = request.POST.get('nid')
    User.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_edit(request, nid):
    """编辑用户"""
    row_obj = User.objects.filter(id=nid).first()
    # GET请求
    if request.method == "GET":
        form = UserModelForm(instance=row_obj)
        return render(request, "user_edit.html", {"form": form})
    # POST请求
    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


# #################################   靓号管理  # #################################
def pretty_list(request):
    """
    靓号列表
    :param request:
    :return:
    """

    # 获取所有用户列表
    data_dic = {}
    query = request.GET.get('query', "")
    if query:
        data_dic['mobile__contains'] = query
    queryset = Pretty.objects.filter(**data_dic).order_by("-level")
    # 分页操作
    page_obj = Pagination(request, queryset, 2)
    # 分页后的数据
    page_pretty_data = page_obj.page_data
    # 分页html页面
    page_html = page_obj.html()
    return render(request, "pretty_list.html",
                  {"pretty_data": page_pretty_data, 'query': query, "page_string": page_html})


def pretty_add(request):
    """
    靓号添加
    :param request:
    :return:
    """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
        # 使用ModelForm进行验证POST请求提交数据
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 直接保存至数据库
        form.save()
        return redirect("/pretty/list/")
    # 校验失败(在页面上显示错误信息)
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """
   靓号编辑
   :param request:
   :return:
   """
    """编辑用户"""
    row_obj = Pretty.objects.filter(id=nid).first()
    # GET请求
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, "pretty_edit.html", {"form": form})
    # POST请求
    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    """
   靓号删除
   :param request:
   :return:
   """
    Pretty.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")


def admin_list(request):
    """
    管理员列表
    :param request:
    :return:
    """
    # 获取所有管理员列表
    data_dic = {}
    query = request.GET.get('query', "")
    if query:
        # 筛选出包含
        data_dic['name__contains'] = query
    queryset = Admin.objects.filter(**data_dic)
    # 分页操作
    page_obj = Pagination(request, queryset, 2)
    # 分页后的数据
    page_data = page_obj.page_data
    # 分页html页面
    page_html = page_obj.html()
    return render(request, "admin_list.html",
                  {"page_data": page_data, 'query': query, "page_string": page_html})


def admin_edit(request, nid):
    """
    管理员编辑页面
    :param request:
    :return:
    """
    # 判断 nid 是否存在
    row_object = Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "admin_edit.html", {"form": form})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, "admin_edit.html", {"form": form})


def admin_add(request):
    """
    管理员添加页面
    :param request:
    :return:
    """
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "admin_add.html", {"form": form})
        # 使用ModelForm进行验证POST请求提交数据
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 直接保存至数据库
        form.save()
        return redirect("/admin/list/")
    # 校验失败(在页面上显示错误信息)
    return render(request, "admin_add.html", {"form": form})


def admin_delete(request, nid):
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    row_object = Admin.objects.filter(id=nid).first()
    title = "重置密码 - {}".format(row_object.name)
    if request.method == "GET":
        form = AdminResetModelForm(instance=row_object)
        return render(request, "admin_reset.html", {'form': form})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "admin_reset.html", {'form': form, 'title': title})


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        input_code = form.cleaned_data.pop("code")
        img_code = request.session.get("image_code", "")
        print("user_input_code={}, image_code={}".format(input_code, img_code))
        # 用户名和密码校验
        admin_object = Admin.objects.filter(**form.cleaned_data).first()
        if img_code.upper() != input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})
        # 不存在
        if not admin_object:
            form.add_error("password", "用户密码错误")
            return render(request, 'login.html', {"form": form})
        # 存在则登录成功，网站生成随机字符串，写到用户浏览器的cookie中，与服务器中的session进行校验
        request.session['info'] = {"id": admin_object.pk, "name": admin_object.name}
        return redirect("/admin/list")
    return render(request, 'login.html', {"form": form})


def logout(request):
    """ 注销 """
    # 清楚当前session
    request.session.clear()
    return redirect("/login/")


def image_code(request):
    """ 生成图片验证码 """
    # 调用pillow函数,生成图片
    img, code_string = check_code()
    print('生成验证码:', code_string)
    # 写入到自己的session中,以便于后续获取验证码再进行校验
    request.session['image_code'] = code_string
    # 给session设置 60s 超时
    request.session.set_expiry(60 * 60 * 24)
    # 将图片保存到内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
