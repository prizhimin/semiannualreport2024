from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .forms import ReportForm
from .models import Report, CreatorsSummaryReport, UserCompany
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user  # Установите поле user
            report.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'sixmonths2024/report_form.html', {'form': form})


@login_required
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')  # Замените 'report_list' на имя вашего URL-шаблона
    else:
        form = ReportForm(instance=report)
    return render(request, 'sixmonths2024/report_form.html', {'form': form})


@login_required
def report_list(request):
    user = request.user

    creators_summary_report = CreatorsSummaryReport.objects.first()
    if creators_summary_report and user in creators_summary_report.creators.all():
        reports = Report.objects.all()
        return render(request, 'sixmonths2024/report_list.html', {'reports': reports})
    else:
        user_company = UserCompany.objects.get(user=user)
        company = user_company.companies.first()

        # Если для этой компании уже есть отчет, получаем его
        report = Report.objects.filter(company=company).first()

        if request.method == 'POST':
            form = ReportForm(request.POST, instance=report)
            if form.is_valid():
                report = form.save(commit=False)
                report.user = request.user  # Устанавливаем текущего пользователя
                report.save()
                return redirect('report_list')
        else:
            form = ReportForm(instance=report, initial={'company': company})
            user_company = UserCompany.objects.filter(user=user).first()
            available_companies = user_company.companies.all()  # Компании, доступные пользователю
            form.fields['company'].queryset = available_companies  # Ограничиваем доступные компании
        return render(request, 'sixmonths2024/report_form.html', {'form': form})

# @login_required
# def report_list(request):
#     user = request.user  # Получаем текущего пользователя
#
#     # Получаем единственный объект CreatorsSummaryReport
#     creators_summary_report = CreatorsSummaryReport.objects.first()
#
#     # Проверяем, является ли пользователь создателем сводного отчета
#     if creators_summary_report and user in creators_summary_report.creators.all():
#         # Пользователь имеет право создавать сводные отчеты
#         reports = Report.objects.all()
#         return render(request, 'sixmonths2024/report_list.html', {'reports': reports})
#     else:
#         # Пользователь не имеет права создавать сводные отчеты
#         user_company = UserCompany.objects.filter(user=user).first()
#         available_companies = user_company.companies.all()  # Компании, доступные пользователю
#
#         if request.method == 'POST':
#             # Если запрос POST, создаем форму с данными из запроса
#             form = ReportForm(request.POST)
#             form.fields['company'].queryset = available_companies  # Ограничиваем доступные компании
#             if form.is_valid():
#                 print(1)
#                 # Если форма валидна, сохраняем отчет
#                 report = form.save(commit=False)
#                 report.user = user  # Устанавливаем пользователя
#                 report.save()
#                 return redirect('report_list')  # Перенаправляем на список отчетов
#         else:
#             # Если запрос GET, создаем форму с начальными данными
#             form = ReportForm(initial={'company': user_company, 'user': request.user})
#             form.fields['company'].queryset = available_companies  # Ограничиваем доступные компании
#
#         return render(request, 'sixmonths2024/report_form.html', {
#             'form': form,  # Передаем форму в шаблон
#         })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Вы вошли как {username}.')
                return redirect('report_list')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'sixmonths2024/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('report_list')
