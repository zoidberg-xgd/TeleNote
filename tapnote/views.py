import markdown
import json
import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Note, Comment, LikeRecord
import re

MAX_CONTENT_LENGTH = 200000

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def api_comments(request):
    if request.method == 'GET':
        site_id = request.GET.get('siteId')
        work_id = request.GET.get('workId')
        chapter_id = request.GET.get('chapterId')
        
        if not all([site_id, work_id, chapter_id]):
            return JsonResponse({'error': 'missing params'}, status=400)
            
        comments = Comment.objects.filter(site_id=site_id, work_id=work_id, chapter_id=chapter_id).order_by('created_at')
        
        # Determine current user identity for "liked" status
        current_user_id = None
        ip = get_client_ip(request)
        if ip:
             # Same logic as creation
             ip_hash = hashlib.md5((ip + site_id).encode()).hexdigest()
             current_user_id = f"ip_{ip_hash}"

        # Get set of comment IDs liked by this user
        liked_comment_ids = set()
        if current_user_id:
            liked_comment_ids = set(
                LikeRecord.objects.filter(user_id=current_user_id, comment__in=comments)
                .values_list('comment_id', flat=True)
            )
        
        # Group by para_index
        comments_by_para = {}
        for c in comments:
            idx = str(c.para_index)
            if idx not in comments_by_para:
                comments_by_para[idx] = []
            
            comments_by_para[idx].append({
                'id': c.id,
                'paraIndex': c.para_index,
                'content': c.content,
                'userName': c.user_name,
                'userId': c.user_id,
                'userAvatar': c.user_avatar,
                'createdAt': c.created_at.isoformat(),
                'likes': c.likes,
                'contextText': c.context_text,
                'isLiked': c.id in liked_comment_ids
            })
            
        return JsonResponse({'commentsByPara': comments_by_para})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            site_id = data.get('siteId')
            work_id = data.get('workId')
            chapter_id = data.get('chapterId')
            para_index = data.get('paraIndex')
            content = data.get('content')
            context_text = data.get('contextText')
            
            if not all([site_id, work_id, chapter_id]) or para_index is None or not content:
                return JsonResponse({'error': 'missing fields'}, status=400)
                
            # Identity logic
            user_name = "匿名"
            user_id = None
            ip = get_client_ip(request)
            
            if ip:
                ip_hash = hashlib.md5((ip + site_id).encode()).hexdigest()
                user_id = f"ip_{ip_hash}"
                user_name = f"访客-{ip_hash[:6]}"
            
            comment = Comment.objects.create(
                site_id=site_id,
                work_id=work_id,
                chapter_id=chapter_id,
                para_index=para_index,
                content=content,
                user_name=user_name,
                user_id=user_id,
                context_text=context_text,
                ip=ip
            )
            
            return JsonResponse({
                'id': comment.id,
                'paraIndex': comment.para_index,
                'content': comment.content,
                'userName': comment.user_name,
                'userId': comment.user_id,
                'createdAt': comment.created_at.isoformat(),
                'likes': comment.likes
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
             return JsonResponse({'error': 'permission denied'}, status=403)
             
        try:
            data = json.loads(request.body)
            comment_id = data.get('commentId')
            Comment.objects.filter(id=comment_id).delete()
            return JsonResponse({'success': True})
        except Exception as e:
             return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'method not allowed'}, status=405)

@csrf_exempt
def api_like_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_id = data.get('commentId')
            site_id = data.get('siteId')
            
            if not comment_id or not site_id:
                 return JsonResponse({'error': 'missing commentId or siteId'}, status=400)

            comment = get_object_or_404(Comment, id=comment_id)
            
            # Identity logic
            ip = get_client_ip(request)
            user_id = None
            
            if ip:
                ip_hash = hashlib.md5((ip + site_id).encode()).hexdigest()
                user_id = f"ip_{ip_hash}"
            
            if not user_id:
                 return JsonResponse({'error': 'cannot identify user'}, status=400)

            # Check if already liked
            if LikeRecord.objects.filter(comment=comment, user_id=user_id).exists():
                return JsonResponse({'error': 'already liked', 'likes': comment.likes}, status=400)
            
            # Create record and increment
            try:
                LikeRecord.objects.create(comment=comment, user_id=user_id, ip=ip)
                comment.likes += 1
                comment.save()
            except Exception as e:
                # Handle race condition or unique constraint violation
                return JsonResponse({'error': 'already liked', 'likes': comment.likes}, status=400)
            
            return JsonResponse({'likes': comment.likes})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'method not allowed'}, status=405)

def apply_strikethrough(md_text):
    # Replace ~~something~~ with <del>something</del>
    pattern = re.compile(r'~~(.*?)~~', re.DOTALL)
    return pattern.sub(r'<del>\1</del>', md_text)

def process_markdown_links(html_content):
    # Keep existing link processing
    pattern = r'<a(.*?)href="(.*?)"(.*?)>'
    replacement = r'<a\1href="\2"\3 target="_blank" rel="noopener noreferrer">'
    html_content = re.sub(pattern, replacement, html_content)

    # Existing anchor-based YouTube embed:
    anchor_yt_pattern = r'<p><a href="https?://(?:www\.)?youtu\.be/([^"]+)".*?>.*?</a></p>'
    anchor_yt_replacement = (
        r'<iframe width="560" height="315" '
        r'src="https://www.youtube.com/embed/\1" '
        r'frameborder="0" allowfullscreen></iframe>'
    )
    html_content = re.sub(anchor_yt_pattern, anchor_yt_replacement, html_content)

    # **Added** plain-text YouTube embed (no anchor tag):
    plain_yt_pattern = r'<p>https?://(?:www\.)?youtu\.be/([^<]+)</p>'
    plain_yt_replacement = (
        r'<iframe width="560" height="315" '
        r'src="https://www.youtube.com/embed/\1" '
        r'frameborder="0" allowfullscreen></iframe>'
    )
    html_content = re.sub(plain_yt_pattern, plain_yt_replacement, html_content)

    return html_content

def home(request):
    # If no users exist, redirect to setup page
    if not User.objects.exists():
        return redirect('setup_admin')
    return render(request, 'tapnote/editor.html')

@csrf_exempt
def setup_admin(request):
    # Security check: only allow if no users exist
    if User.objects.exists():
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        
        if username and password:
            user = User.objects.create_superuser(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
            
    return render(request, 'tapnote/setup.html')

@csrf_exempt
def publish(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if len(content) > MAX_CONTENT_LENGTH:
            return render(request, 'tapnote/editor.html', {
                'error': f'Content exceeds the limit of {MAX_CONTENT_LENGTH} characters.',
                'note': {'content': content}
            })
        if content:
            note = Note.objects.create(content=content)
            response = redirect('view_note', hashcode=note.hashcode)
            response.set_cookie(f'edit_token_{note.hashcode}', note.edit_token, max_age=31536000)
            return response
    return redirect('home')

def view_note(request, hashcode):
    note = get_object_or_404(Note, hashcode=hashcode)
    
    # FIRST apply strikethrough by regex
    raw_with_del = apply_strikethrough(note.content)

    # THEN convert with standard Markdown (no strikethrough extension)
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'footnotes'])
    html_content = md.convert(raw_with_del)
    html_content = process_markdown_links(html_content)
    
    can_edit = (
        request.COOKIES.get(f'edit_token_{note.hashcode}') == note.edit_token or
        request.GET.get('token') == note.edit_token
    )
    
    return render(request, 'tapnote/view_note.html', {
        'note': note,
        'content': html_content,
        'can_edit': can_edit,
    })

@csrf_exempt
def edit_note(request, hashcode):
    note = get_object_or_404(Note, hashcode=hashcode)
    edit_token = request.COOKIES.get(f'edit_token_{note.hashcode}')
    url_token = request.GET.get('token')
    
    if edit_token != note.edit_token and url_token != note.edit_token:
        raise Http404()
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if len(content) > MAX_CONTENT_LENGTH:
            return render(request, 'tapnote/editor.html', {
                'note': note,
                'error': f'Content exceeds the limit of {MAX_CONTENT_LENGTH} characters.'
            })
            
        if content:
            note.content = content
            note.save()
            return redirect('view_note', hashcode=note.hashcode)
    
    return render(request, 'tapnote/editor.html', {'note': note})

def handler404(request, exception):
    return render(request, 'tapnote/404.html', status=404)

@staff_member_required
def migration(request):
    return render(request, 'tapnote/migration.html')

@staff_member_required
def export_data(request):
    notes = Note.objects.all()
    data = []
    for note in notes:
        data.append({
            'hashcode': note.hashcode,
            'content': note.content,
            'edit_token': note.edit_token,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat(),
        })
    
    response = HttpResponse(
        json.dumps(data, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="tapnote_backup.json"'
    return response

@csrf_exempt
@staff_member_required
def import_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            json_file = request.FILES['file']
            data = json.load(json_file)
            
            count = 0
            for item in data:
                defaults = {
                    'content': item['content'],
                    'edit_token': item['edit_token'],
                }
                if 'created_at' in item:
                    defaults['created_at'] = parse_datetime(item['created_at'])
                
                note, created = Note.objects.update_or_create(
                    hashcode=item['hashcode'],
                    defaults=defaults
                )
                
                # Force update updated_at if present
                if 'updated_at' in item:
                    updated_at = parse_datetime(item['updated_at'])
                    Note.objects.filter(pk=note.pk).update(updated_at=updated_at)
                
                count += 1
                
            return render(request, 'tapnote/migration.html', {'success': f'Successfully imported {count} notes.'})
        except Exception as e:
            return render(request, 'tapnote/migration.html', {'error': f'Error importing file: {str(e)}'})
            
    return redirect('migration')
