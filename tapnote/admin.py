from django.contrib import admin
from .models import Note, Comment

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('hashcode', 'short_content', 'created_at', 'updated_at')
    search_fields = ('content', 'hashcode')
    readonly_fields = ('hashcode', 'edit_token', 'created_at', 'updated_at')

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'short_content', 'site_id', 'work_id', 'para_index', 'likes', 'created_at')
    list_filter = ('site_id', 'created_at')
    search_fields = ('content', 'user_name', 'work_id')
    readonly_fields = ('created_at', 'ip')

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
