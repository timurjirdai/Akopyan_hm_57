from datetime import timedelta
from django.utils import timezone
from tracker.models import Issue
from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from tracker.models import Type

month_ago = timezone.now() - timedelta(days=30)

query_1 = Issue.objects.filter(
    status__name = 'Done',
    updated_at__gte = month_ago
)

query_2 = Issue.objects.filter(
    status__name__in = ['new', 'Done'],
    types__name__in = ['Bug', 'Task']
).distinct()

query_3 = Issue.objects.exclude(
    status__name = 'Done'
).filter(
    Q(summary__icontains='bug') |
    Q(types__name='Bug')
).distinct()

query_bonus_1 = Issue.objects.values(
    'id',
    'summary',
    'status__name',
    'types__name'
)

query_bonus_2 = Issue.objects.filter(
    summary=F('description')
)

query_bonus_3 = Type.objects.annotate(
    issues_count=Count('issue')
)