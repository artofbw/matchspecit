from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from celery import shared_task
from psycopg2 import IntegrityError

from matchspecit.match.models import Match
from matchspecit.project.models import Project

User = get_user_model()


@shared_task
def match_user_with_project():
    users = User.objects.filter(is_active=True, is_matchable=True)
    projects = Project.objects.filter(is_matchable=True, is_finish=False, is_successful=False, is_deleted=False)

    for user in users:
        for project in projects:
            if user.id != project.owner_id:
                user_technologies = user.technologies.count()
                project_technologies = project.technologies.count()

                match_percent = round(Decimal(user_technologies) / Decimal(project_technologies), 2)

                if match_percent >= settings.MATCH_PERCENT:
                    try:
                        Match.objects.create(user=user, project=project, match_percent=match_percent)
                        return {"status": "matched"}
                    except IntegrityError:
                        pass
    return None
