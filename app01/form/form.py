import random
import re
from app01.models import User, Pretty, Admin, Order
from django import forms
from django.core.exceptions import ValidationError
from app01.utils.modelform import BootStrapModelForm, BootStrapForm
from app01.utils.sms import send_sms
from django.core.validators import RegexValidator
from app01.utils.encrypt import md5
from django_redis import get_redis_connection


# 使用ModelForm进行验证
class UserModelForm(BootStrapModelForm):
    # 自定义数据校验
    # 例如: 用户名最小三个字符
    name = forms.CharField(min_length=2, max_length=20,
                           label="用户名")
    password = forms.CharField(min_length=6, max_length=18,
                               label="密码")

    class Meta:
        model = User
        fields = ["name", "password", "age", "account_balance", "create_time", "gender", "depart"]
        # 逐一控制标签的样式
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

        # 这里让日期可以手动点击鼠标选择,所以单独拎出来,加上日期插件
        widgets = {
            "create_time": forms.DateInput(attrs={'class': 'form-control', 'id': 'myDate'}),
        }


# 使用ModelForm进行验证
class PrettyModelForm(BootStrapModelForm):
    # 电话号码格式校验
    # 方法一 正则表达式
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    # )

    # 方法二 hook函数
    def clean_mobile(self):
        mobile_txt = self.cleaned_data.get('mobile')
        # 验证手机号码格式
        pattern = r'^1[3-9]\d{9}$'
        if not re.match(pattern, mobile_txt):
            raise ValidationError('手机号格式错误')
        # 验证手机号是否已存在
        exists_data = Pretty.objects.filter(mobile=mobile_txt).exists()
        if exists_data:
            raise ValidationError('手机号码已存在')
        return mobile_txt

    class Meta:
        model = Pretty
        # fields = "__all__"    表示取表中所有的字段
        fields = ['mobile', 'price', 'level', 'status']
        # exclude = ['level']   表示取除了表中的某个字段的所有字段


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号",
    #                          validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ], )

    def clean_mobile(self):
        mobile_txt = self.cleaned_data.get('mobile')
        # 验证手机号码格式
        pattern = r'^1[3-9]\d{9}$'
        if not re.match(pattern, mobile_txt):
            raise ValidationError('手机号格式错误')
        # 验证手机号是否已存在
        # self.instance.pk 表示当前表单所关联的模型实例的主键值（Primary Key，通常是数据库中每个记录的唯一标识符）
        exists_data = Pretty.objects.exclude(id=self.instance.pk).filter(mobile=mobile_txt).exists()
        if exists_data:
            raise ValidationError('手机号码已存在')
        return mobile_txt

    class Meta:
        model = Pretty
        fields = ['mobile', 'price', 'level', 'status']


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Admin
        fields = ["name", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exists_data = Admin.objects.exclude(id=self.instance.pk).filter(name=name).exists()
        if exists_data:
            raise ValidationError('改用户名已被使用！')
        return name

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    #     确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if confirm_pwd != pwd:
            raise ValidationError('密码不一致！')
        return confirm_pwd


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exists_data = Admin.objects.exclude(id=self.instance.pk).filter(name=name).exists()
        if exists_data:
            raise ValidationError('改用户名已被使用！')
        return name


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # clean_字段名
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 校验当前数据库中的密码与用户输入的新密码是否一致
        exists = Admin.objects.filter(id=self.instance.pk, password=md5(pwd))
        if exists:
            raise ValidationError("密码不能与当前密码一致!")
        # return什么.password字段保存什么
        return md5(pwd)

    # 钩子函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(confirm) != pwd:
            raise ValidationError("密码不一致!")
        # return返回什么,字段 confirm_password 保存至数据库的值就是什么
        return md5(confirm)


class LoginForm(forms.Form):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class RegisterForm(BootStrapForm):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput(),
        required=True,
    )
    email = forms.CharField(
        label="邮箱",
        widget=forms.TextInput(),
        required=True,
        validators=[RegexValidator(
            r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(com|cn|net)$',
            '邮箱格式错误'), ],
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(),
        required=True,
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(),
        required=True,
    )
    phone = forms.CharField(
        label="手机号",
        widget=forms.TextInput(),
        required=True,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
        required=True,
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exists = Admin.objects.filter(name=name).exists()
        if exists:
            raise ValidationError('改用户名已被注册使用')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = Admin.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('改邮箱已被注册使用')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        exists = Admin.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError('改电话已被注册使用')
        return phone

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
        # 钩子函数

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(confirm) != pwd:
            raise ValidationError("密码不一致")
        # return返回什么,字段 confirm_password 保存至数据库的值就是什么
        return md5(confirm)

    def clean_code(self):
        input_code = self.cleaned_data.get("code")
        mobile_phone = self.cleaned_data.get('phone')
        # 从redis中获取改手机号对应的验证码
        if not mobile_phone:
            return input_code
        conn = get_redis_connection('default')  # default是连接池的名称
        code = conn.get(mobile_phone)
        code_text = code.decode('utf-8') if code else ''
        print(code_text, input_code)
        if code_text != input_code:
            raise ValidationError('验证码错误')


class SendSmsForm(forms.Form):
    phone = forms.CharField(
        label="手机号",
        widget=forms.TextInput(),
        required=True,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )
    tpl = forms.CharField(
        label="短信业务类型",
        widget=forms.TextInput(),
        required=True,
    )

    def clean_phone(self):
        # 判断业务是登录还是注册
        tpl = self.request.GET.get('tpl')
        mobile_phone = self.cleaned_data.get("phone")
        exists = Admin.objects.filter(phone=mobile_phone).exists()
        if tpl == 'login':
            # 检查手机号是否注册过
            if not exists:
                raise ValidationError('改手机号未被注册')
        else:
            if exists:
                raise ValidationError('改手机号已被注册')
        # 发送短信
        code = random.randrange(1000, 9999)
        # 阿里云发送短信代码
        send_res = send_sms(mobile_phone, code)
        print(send_res)
        if send_res['Message'] != 'OK':
            self.errors.add_error("code", send_res['Message'])
        print('手机号为: ', mobile_phone, '验证码为: ', code)
        # 存入redis
        conn = get_redis_connection('default')  # default是连接池的名称
        conn.set(mobile_phone, code, 60)
        return mobile_phone

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class SmsLoginForm(BootStrapForm):
    phone = forms.CharField(
        label="手机号",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )

    def clean_phone(self):
        mobile_phone = self.cleaned_data.get('phone')
        exists = Admin.objects.filter(phone=mobile_phone).exists()
        if not exists:
            raise ValidationError('手机号不存在')
        return mobile_phone

    def clean_code(self):
        mobile_phone = self.cleaned_data.get('phone')
        input_code = self.cleaned_data.get('code')
        if not mobile_phone:
            return input_code
        conn = get_redis_connection('default')  # default是连接池的名称
        code = conn.get(mobile_phone)
        code_text = code.decode('utf-8') if code else ''
        print(code_text, input_code)
        if code_text != input_code:
            raise ValidationError('验证码错误')
        return input_code


class OrderModelForm(BootStrapModelForm):
    price = forms.IntegerField(
        min_value=0,
        label="价格",
    )

    class Meta:
        model = Order
        fields = ["title", "price", "status"]
        # exclude = ["oid", "admin"]


class ExcelForm(forms.Form):
    pass
