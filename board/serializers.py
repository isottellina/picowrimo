from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Project, Advancement

class UserSerializer(serializers.ModelSerializer):
    projects = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Project.objects,
        view_name='project-detail'
    )

    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = User
        fields = ('url', User.USERNAME_FIELD, 'is_active',
                  'projects',
                  )

    def get_url(self, obj):
        request = self.context['request']
        return reverse('user-detail', kwargs={
                User.USERNAME_FIELD: getattr(obj, User.USERNAME_FIELD)
            },
            request=request
        )


class ProjectSerializer(serializers.ModelSerializer):
    advancements = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Advancement.objects,
        view_name='advancement-detail',
    )

    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects,
        view_name='user-detail',
        lookup_field=User.USERNAME_FIELD
    )

    wordcount = serializers.SerializerMethodField('get_wordcount')

    def get_wordcount(self, obj):
        return sum(adv.delta for adv in obj.advancements.all())

    class Meta:
        model = Project
        fields = ('url',
                  'name',
                  'description',
                  'user',
                  'wordcount',
                  'advancements')


class AdvancementSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        queryset=Project.objects,
        view_name='project-detail'
    )

    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        if start > end:
            raise serializers.ValidationError("Start date cannot be greater than end date")
        if start > datetime.now():
            raise serializers.ValidationError("Start date cannot be greater than current date")
        if end > datetime.now():
            raise serializers.ValidationError("End date cannot be greater than current date")

    class Meta:
        model = Advancement
        fields = ('url',
                  'project',
                  'delta',
                  'start',
                  'end')
