from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from matchspecit.core.celery import shared_task
from matchspecit.match.models import Match
from matchspecit.project.models import Project
from matchspecit.user.models import Role

User = get_user_model()


@shared_task
def match_user_with_project():
    users = User.objects.filter(is_active=True, role=Role.SPECIALIST)
    projects = Project.objects.all()

    for user in users:
        for project in projects:
            user_technologies = user.technologies.count()
            project_technologies = project.technologies.count()

            match_percent = round(Decimal(user_technologies) / Decimal(project_technologies), 2)

            if match_percent >= settings.MATCH_PERCENT:
                Match.objects.create(user=user, project=project, match_percent=match_percent)
    return None
