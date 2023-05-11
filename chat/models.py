from django.db import models


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'user_auth.CustomUser', related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.email


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.email


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)


