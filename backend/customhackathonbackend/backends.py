from django.contrib.auth.models import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apps.backwork.models import GlobalUsers

class HackathonBackend:
    """ When try to authenticating the student should pass contest id too """
    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        try:
            # Try to find a user matching your username
            print 'inside authenticate'
            user = GlobalUsers.objects.get(gus_username=username)
            print username
            print user.gus_username
            #  Check the password is the reverse of the username
            if check_password(password, user.gus_password):
            #     # Yes? return the Django user object
                return user
            else:
            #     # No? return None - triggers default login
                print 'userid/password does not match'
                raise GlobalUsers.DoesNotExist
                # return None
        except GlobalUsers.DoesNotExist:
            # No user was found, return None - triggers default login failed
            # try:
            #     print 'Looking for user in guest'
            #     guest = TravellerDetails.objects.filter(tvl_emailid=username, tvl_isused=0)[0]
            #     if check_password(password, guest.tvl_password):
            #     #     # Yes? return the Django user object
            #         return guest
            #     else:
            #     #     # No? return None - triggers default login
            #         print 'guest userid/password does not match'

            # except Exception, e:

            #     print 'User not found in guest', e
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return GlobalUsers.objects.get(customer_id=user_id)
        except GlobalUsers.DoesNotExist:
            return None