import datetime
import uuid

from reducer.models import Users


def user_uuid_handler(request):

    """ Get exist user ID """
    user_id = request.COOKIES.get("dp_test_user_id", None)
    print(user_id)

    """ Check user in DB - exists or not """
    try:
        user = Users.objects.get(user_uuid=user_id)
    except Users.DoesNotExist:
        user = None

    if user_id and user:
        user = Users.objects.get(user_uuid=user_id)
        user.last_visited = datetime.datetime.now()
        user.save()

    else:
        new_id = uuid.uuid4()
        user = Users(user_uuid=new_id, is_banned=False)
        user.save()

    return user
