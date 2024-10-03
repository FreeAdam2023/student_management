# Create your views here.
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.db.models import Q


def student_list(request):
    query = request.GET.get('q', '')  # 获取查询参数
    print(f"query -> {query}")
    if query:
        # 根据 first_name 或 last_name 执行搜索
        students = Student.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        students = Student.objects.all()
    print(f"Queryset results: {students}")
    # 添加分页，每页显示10个学生（可以根据需要调整）
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/student_list.html', {'page_obj': page_obj, 'query': query})





def student_detail(request, pk):
    try:
        student = get_object_or_404(Student, pk=pk)
    except Http404:
        return render(request, '404.html')  # Custom 404 page or generic message
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})



@login_required
def student_edit(request, pk):
    try:
        student = get_object_or_404(Student, pk=pk)
    except Http404:
        return render(request, '404.html')  # Custom 404 page

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

