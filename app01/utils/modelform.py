from django import forms


class BootStrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段,给每个字段的插件设置
        for _, field in self.fields.items():
            # 字段中有属性,保留原来的属性,没有属性,才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = "请输入%s" % field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": "请输入%s" % field.label,

                }


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段,给每个字段的插件设置
        for _, field in self.fields.items():
            # 字段中有属性,保留原来的属性,没有属性,才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = "请输入%s" % field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": "请输入%s" % field.label,

                }
