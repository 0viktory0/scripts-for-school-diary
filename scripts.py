from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson, Subject
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


COMMENDATIONS = ['Замечательно!',
                'Здорово!',
                'Очень хороший ответ!',
                'Ты на верном пути!',
                'Сказано здорово – просто и ясно!',
                'Молодец!',
                'Гораздо лучше, чем я ожидал!',
                'Потрясающе!',
                'Я вижу, как ты стараешься!',
                'Ты растешь над собой!',
                'Прекрасное начало!',
                'Ты меня очень обрадовал!',
                'С каждым разом у тебя получается всё лучше!',
                'Ты растешь над собой!',
                'Теперь у тебя точно все получится!',
                'Ты многое сделал, я это вижу!',
                'Я тобой горжусь!',
                'Ты меня приятно удивил!',
                'Хорошо!',
                'Именно этого я давно ждал от тебя!',
                'Великолепно!',
                'Ты сегодня прыгнул выше головы!'
]


def get_child_card(child_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child_name)
        return schoolkid
    except ObjectDoesNotExist:
        print(f'Ученика {child_name} нет в базе школы')
    except MultipleObjectsReturned:
        print(f'Найдено больше одного ученика с именем {child_name}')


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def delete_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def get_lesson(year_of_study, group_letter, subject):
    lesson = Lesson.objects.filter(year_of_study=year_of_study,
                                   group_letter=group_letter,
                                   subject__title=subject).order_by('?').first()
    if lesson is None:
        print(f'Урок {subject} в базе не найден')
        sys.exit()
    else:
        return lesson


def make_commendation(schoolkid, lesson):
    text = random.choice(COMMENDATIONS)
    Commendation.objects.create(text=text,
                                created=lesson.date,
                                schoolkid=schoolkid,
                                subject=lesson.subject,
                                teacher=lesson.teacher)

