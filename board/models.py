from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """
    A writing project, done by an user.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return f"Project <{self.name}>"


class Advancement(models.Model):
    """
    A single modification of the number of words in a project.
    """
    project = models.ForeignKey(Project,
                                related_name='advancements',
                                on_delete=models.CASCADE,
                                null=False)
    delta = models.IntegerField()
    start = models.DateTimeField(auto_now_add=True, null=False)
    end = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"Advancement<{self.project.name} {self.delta:+}"
