from django.shortcuts import render, HttpResponse

from django.views.generic import View
from .models import CourseOrg, CityDict
from courses.models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm
import json


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by('click_nums')[:3]
        all_city = CityDict.objects.all()
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', '')
        if category:
            all_org = all_org.filter(category=category)
        if city_id:
            all_org = all_org.filter(city_id=city_id)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'student':
                all_org = all_org.order_by('student')
            elif sort == 'course':
                all_org = all_org.order_by('course_num')

        org_num = all_org.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        objects = all_org
        p = Paginator(objects, 2, request=request)
        page_org = p.page(page)
        return render(request, 'org-list.html',
                      {'all_org': page_org,
                       'all_city': all_city,
                       'org_num': org_num,
                       'city_id': city_id,
                       'category': category,
                       'hot_org': hot_org,
                       'sort': sort,
                       })


class AddUserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            print('保存了')
            return HttpResponse(json.dumps({'status': 'success'}))
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加出错'}))


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'org': course_org,
            'current_page': current_page
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_ort = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_ort.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'org': course_ort,
            'current_page': current_page
        })


class OrgDescView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_ort = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'org': course_ort,
            'current_page': current_page
        })


class OrgTeacherView(View):
    """
    机构教师页
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_ort = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_ort.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'org': course_ort,
            'current_page': current_page
        })
