from rest_framework import serializers

from chat.models import Chat, Contact, Message
from chat.views import get_user_contact


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'contact', 'content', 'timestamp')
        read_only_fields = ('id', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        read_only = ('id')

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for id in participants:
            contact = get_user_contact(id)
            chat.participants.add(contact)
        chat.save()
        return chat
