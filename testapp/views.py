from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from testapp.models import Acoustic, MosTest
from testapp.forms import MosTestForm

# Create your views here.

@require_safe
def top(request):
    tests = MosTest.objects.all()
    context = {"tests": tests}
    return render(request, "test/top.html", context)


def test_detail(request, test_id):
    test = get_object_or_404(MosTest, pk=test_id)
    context = {'test': test}
    return render(request, 'test/test_detail.html', context)


@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def test_edit(request, test_id):
    test = get_object_or_404(MosTest, pk=test_id)
    if test.created_by_id != request.user.id:
        return HttpResponseForbidden("このテストの編集は許可されておりません。")
    
    if request.method == 'POST':
        form = MosTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('test_detail', test_id=test_id)
    else:
        form = MosTestForm(instance=test)
    context = {'form': form}
    return render(request, 'test/test_edit.html', context)


@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def test_delete(request, test_id):
    test = get_object_or_404(MosTest, pk=test_id)
    if test.created_by_id != request.user.id:
        return HttpResponseForbidden("このテストの削除は許可されておりません。")
    
    if request.method == 'POST':
        test.delete()
        return redirect('top')

    context = {'test': test}
    return render(request, 'test/test_delete.html', context)


@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def test_new(request):
    if request.method == 'POST':
        # MosTest モデルのデータを受け取る
        mos_test_form = MosTestForm(request.POST)
        if mos_test_form.is_valid():
            mos_test = mos_test_form.save(commit=False)
            mos_test.created_by = request.user
            mos_test.save()

        # Acostic モデルのデータを受け取る
        form_length = int(request.POST.get('js-value_formcount'))
        for prefix in range(form_length):
            model_name = request.POST.get(f"form-{prefix}_model_name")
            text = request.POST.get(f"form-{prefix}_text")
            for audio in request.FILES.getlist(f"form-{prefix}_audios"):
                Acoustic.objects.create(
                    mos_test=mos_test,
                    acoustic_model_name=model_name,
                    audio=audio,
                    text=text)
        return redirect('top')
    else:
        mos_form = MosTestForm()
    
    return render(request, 'test/test_new.html', {'mos_form': mos_form})


@login_required
@require_http_methods(["GET"])
def get_new_form(request):
    prefix = request.GET.get('prefix')  # JavaScriptから渡されたprefixを取得
    rendered_form = render_to_string('test/add_forms.html', {'prefix': prefix})
    return HttpResponse(rendered_form)
