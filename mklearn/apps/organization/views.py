from django.shortcuts import render, HttpResponse

from django.views.generic import View
from .models import CourseOrg, CityDict

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
