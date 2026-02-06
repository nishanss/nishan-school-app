from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from academics.models import Grade
from .models import Exam, Mark
from students.models import Student

def enter_marks(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    students = Student.objects.filter(section=exam.section, is_active=True)
    
    if request.method == 'POST':
        for student in students:
            score = request.POST.get(f'marks_{student.id}')
            if score:
                Mark.objects.update_or_create(
                    exam=exam,
                    student=student,
                    defaults={'marks_obtained': score}
                )
        messages.success(request, f"Marks for {exam.subject.name} saved!")
        return redirect('exam_list')

    return render(request, 'exams/enter_marks.html', {
        'exam': exam,
        'students': students
    })

def exam_list(request):
    # exams = Exam.objects.all().select_related('subject', 'section').order_by('-date')
    # return render(request, 'exams/exam_list.html', {'exams': exams})
    
    exams = Exam.objects.all().select_related('subject', 'section__grade')
    
    grade_id = request.GET.get('grade')
    exam_type = request.GET.get('type')

    if grade_id:
        exams = exams.filter(section__grade_id=grade_id)
    if exam_type:
        exams = exams.filter(exam_type=exam_type)

    grades = Grade.objects.all()
    return render(request, 'exams/exam_list.html', {
        'exams': exams,
        'grades': grades,
        'exam_types': Exam.EXAM_TYPES 
    })