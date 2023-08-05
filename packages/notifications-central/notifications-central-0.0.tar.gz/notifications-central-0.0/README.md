# Notification central


This module manages the users email notifications and aims to reduce the amount of emails sent.
Users can now group their notifications on a single email that can be send daily, weekly or monthly. 

##Install and configure

1. Clone the repository and install the app using pip.

    ```shell
    > pip install notifications-central
    ```

2. Add the module to the installed apps in django settings, and execute the migration command.

    ```python
    INSTALLED_APPS = [
        'notifications',
        ...
    ]
    ```

3. Call Django migrations

    ```shell
    > python manage.py migrate
    ```
    
4. Configure Crontab to schedule the send of emails for each period.

    ```shell
        00 8 * * * python manage.py send_notifications D
        00 8 * * MON python manage.py send_notifications W
        00 8 1 * * python manage.py send_notifications M
    ```

##How it works

### In the code

Use the next code to notify the user about something. 
Then depending on how the notification is configured the user will receive the message immediately by email,
or later in grouped with other messages.

```python
from notifications.tools import notify

...

notify('NOTIFICATION UNIQUE CODE', msg_subject, msg_text, user=user_to_send)

```


###On the Web App

####Superuser view

Menu seen by the superuser:

![Superuser menu](docs/images/superuser-menu.png)

The superuser can configure the next options for the notifications:

- Set the default time when each notification type should be send.
- Activate or deactivate the notifications. In case a notification type is disabled, the messages are not going to be registered.
- Set the notifications unique code.
- Set the notifications label (Label shown to the user).
- Set a flag that avoid the user to be notified multiple times with the same message.

![Configure notifications](docs/images/superuser-notificationstypes.png)

Access all the users notifications:

![All users notifications](docs/images/superuser-allnotifications.png)



#### Users

Ordinary users, will see a icon with the unread notifications on the top menu.

![Configure notifications](docs/images/notifications-icon.png)


To view the notifications users can click in the notifications icon, and select the notifications in the list.

![Configure notifications](docs/images/notifications-app.png)


Users configuring the notifications grouping by clicking in the cog, and selecting the period when they would like to receive each type of notification.

![Configure notifications](docs/images/notifications-config.png)

