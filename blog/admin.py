from django.contrib import admin
from .models import Article, Category, IpAddress


#Change Admin Brand name
admin.site.site_header = 'پنل مدیریت وبلاگ جنگویی '

#set the article author to ali
def chnage_author(modeladmin, request, queryset):
    rows_updated =queryset.update(author = 1)
    if rows_updated == 1:
        message_bit = 'نویسندش تغیر کرد'
    else:
        message_bit = 'نویسندش تغیر کرد'
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')
    

chnage_author.short_description = 'تغیر نویسنده مقالات انتخاب شده به ادمین'

def make_published_last(modeladmin, request, queryset):
    queryset.update(status = 'p')

make_published_last.short_description = 'انتشار مقالات انتخاب شده'

def make_published(modeladmin, request, queryset):
    rows_updated =queryset.update(status = 'p')
    if rows_updated == 1:
        message_bit = 'منتشر شد'
    else:
        message_bit = 'منتشر شدن'
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')
    

make_published.short_description = 'انتشار مقالات انتخاب شده'

def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status = 'd')
    if rows_updated == 1:
        message_bit = 'پیش نویس شد'
    else:
        message_bit = 'پیش نویس شدن'
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')


make_draft.short_description = 'پیش نویس کردن مقاله های انتخاب شده'

def make_show_category(modeladmin, request, queryset):
    row_updated = queryset.update(status = True)
    if row_updated == 1:
        message_bit = 'فعال شد'
    else:
        message_bit = 'فعال شدن'
    modeladmin.message_user(request, f'{row_updated} دسته بندی {message_bit}')

def make_disable_category(modeladmin, request, queryset):
    row_updated = queryset.update(status = False)
    if row_updated == 1:
        message_bit = 'غیرفعال شد'
    else:
        message_bit = 'غیرفعال شدن'
    modeladmin.message_user(request, f'{row_updated} دسته بندی {message_bit}')
make_show_category.short_description = 'نمایش دسته بندی های انتخاب شده'
make_disable_category.short_description = 'غیرفعال کردن دسته بندی های انتخاب شده'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position','title','slug', 'parent','status')
    list_filter  = (['status'])
    search_fields = ('title','slug')
    prepopulated_fields = {'slug':('title',)}
    actions = [make_show_category, make_disable_category,'turn_off']

    @admin.action(description = 'غیرفعال سازی در کلاس')
    def turn_off(self, request, queryset):
        queryset.update(status = False)

    

admin.site.register(Category,CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thunbnail_tag', 'slug' , 'author', 'jpublish', 'is_special', 'status','category_to_str')
    list_filter  = ('publish','status','author')
    search_fields = ('title','description')
    prepopulated_fields = {'slug':('title',)}
    ordering = ['-status','-publish']
    actions = [make_published, make_draft, chnage_author]

    # def category_to_str(self, obj):
    #         return ','.join([category.title for category in obj.category_published()])
    def category_to_str(self, obj):
        return ','.join([category.title for category in obj.category.active()])
    category_to_str.short_description = 'دسته بندی'
admin.site.register(Article,ArticleAdmin)

class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)


admin.site.register(IpAddress, IpAddressAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title','description','status','category_to_str')
    list_filter  = (['status'])
    search_fields = ('title','description')
    
    
    def category_to_str(self, obj):
        return ','.join([category.title for category in obj.category.all()])

    category_to_str.short_description = 'دسته بندی'

#deletث action from admin panel
admin.site.disable_action('delete_selected')
