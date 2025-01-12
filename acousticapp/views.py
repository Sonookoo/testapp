from collections import defaultdict
import itertools
import random
from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods
from acousticapp.forms import AnswerForm, CommentForm
from acousticapp.models import Answer, Comment
from django.db.models import Avg, Count
from testapp.models import Acoustic, MosTest
import numpy as np 
from scipy import stats
from scipy.stats import wilcoxon, shapiro, friedmanchisquare

# Create your views here.
@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def answer_new(request, test_id):
    # フォームセットを作成する
    random.seed(test_id) 
    test_acoustics = Acoustic.objects.filter(mos_test_id=test_id).order_by('?')
    test_count = test_acoustics.count()
    test = get_object_or_404(MosTest, pk=test_id)
    AnswerFormSet = forms.formset_factory(AnswerForm, extra=test_count)
    answer_formset = AnswerFormSet()
    comment_form = CommentForm()
    
    context = {
        'test_acoustics': test_acoustics, 
        'answer_form_set': answer_formset,
        'test': test,
        'comment_form': comment_form,
        'error': False,
    }

    if request.method == 'POST':
        answer_formset = AnswerFormSet(request.POST)
        comment_form = CommentForm(request.POST)

        if not answer_formset.is_valid():
            context['error'] = True
            return render(request, 'answer/answer_new.html', context)
            
        for form, audio in zip(answer_formset, test_acoustics):
            if not form.is_valid():
                context['error'] = True
                return render(request, 'answer/answer_new.html', context)
            
            answer = form.save(commit=False)

            if not answer.mos:
                context['error'] = True
                context['answer_form_set'] = answer_formset
                return render(request, 'answer/answer_new.html', context)
        
            result = Answer.objects.filter(created_by=request.user, target_audio_id=audio)
            if result.exists():
                old_answer = Answer.objects.get(pk=result[0].id)
                old_answer.mos = answer.mos
                old_answer.save()
            else:
                answer.target_audio = audio
                answer.created_by = request.user
                answer.save()

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.created_by = request.user
            comment.test = test
            comment.save()
                
        return redirect("top")
    else:
        return render(request, 'answer/answer_new.html', context)
    


@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def result(request, test_id):
    """テストの回答を集計して結果を表示する"""

    def get_stats(scores):
        """統計量を計算するサブ関数"""
        #1. データの分散、平均など必要なデータを求める
        n = len(scores)
        if n <= 1:
            return

        mean_score = np.mean(scores)
        std_dev = np.std(scores, ddof=1)
        sem = std_dev / np.sqrt(n)

        #2. t分布を用いてデータの信頼区間を求める
        # データの平均からの誤差を算出し、信頼区間の上限値、下限値を求める
        # 信頼区間の計算
        confidence = 0.95
        df = n - 1
        t_value = stats.t.ppf((1 + confidence) / 2, df)
        margin_of_error = t_value * sem

        #3. データの正規性を検定する
        stat, p_value = shapiro(scores)
        is_norm = "true"
        if p_value < 0.05:
            is_norm = "false"  

        rtn_dict = {
            "count": n, 
            "average": mean_score,  
            "error": margin_of_error,
            "string": f"{mean_score:.2f} ± {margin_of_errpr:.2f}",
            "is_norm": is_norm,
        }

        return rtn_dict

    test = get_object_or_404(MosTest, pk=test_id)
    if test.created_by_id != request.user.id:
        return HttpResponseForbidden("このテストの結果閲覧は許可されておりません。")
    
    test_audios = Acoustic.objects.filter(mos_test_id=test_id)
    comments = Comment.objects.filter(test=test)
    num_of_audios = len(test_audios)
    
    if not test_audios:
        return HttpResponseForbidden("このテストにはまだ回答がされておりません。")
    
    acoustic_models = test_audios.values_list('acoustic_model_name', flat=True).distinct()
    num_of_models = len(acoustic_models)

    result_dict = dict()
    mos_list = [[] for _ in range(num_of_models)]

    for i, model in enumerate(acoustic_models, 0):
        model_audios = test_audios.filter(acoustic_model_name=model)

        for audio in model_audios:
            answers = Answer.objects.filter(target_audio_id=audio)
            num_of_subjects = len(answers)
            mos_list[i] += answers.values_list('mos', flat=True)

        result_dict[f"{i}_{model}"] = get_stats(mos_list[i])

    context = {
        "test": test,
        "num_of_subjects": num_of_subjects,
        "num_of_answers": num_of_subjects*num_of_audios,
        "result_dict": result_dict,
        "p_value": None,
        "comments": comments,
        "friedmanchisquare": None
    }

    p_value_dict = dict()
    for m1, m2 in itertools.combinations(range(len(mos_list)), 2):

        # ウィルコクソンの符号順位検定
        statistic, p_value = wilcoxon(mos_list[m1], mos_list[m2])

        # 結果の出力
        print("統計量:", statistic)
        print("p値:", p_value)

        p_value_dict[f"model_({m1}, {m2})"] = f"{p_value:.3f}"
    context["p_value"] = p_value_dict

    if num_of_models >= 3:
        statistic, p_value = friedmanchisquare(*mos_list)
        context["friedmanchisquare"] = p_value

    return render(request, 'answer/result.html', context=context)
