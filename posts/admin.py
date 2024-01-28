from django.contrib import admin

from posts.models import Post, Report


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'updated_at')
    display = ('user', 'caption', 'files', 'created_at', 'updated_at')
    readonly_fields = ('user', 'caption', 'files', 'created_at',
                       'updated_at', 'likes', 'retweets', 'saves', 'mentions', 'hashtags', 'post', 'reply_to')

    def files(self, obj):
        ' '.join([str(i.file) for i in obj.files.all()])


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = ('id',)
    search_fields = ('post__caption', 'user__username', 'description')
