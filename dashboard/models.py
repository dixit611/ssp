from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description=models.TextField()


  def __str__(self):
    return self.title

  class Meta:
    verbose_name = "Notes"
    verbose_name_plural = "Notes"

  
class Homework(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  subject =models.CharField(max_length=50)
  title = models.CharField(max_length=200)
  description=models.TextField()
  due = models.DateTimeField()
  is_finished=models.BooleanField(default=False)


  def __str__(self):
    return self.title
  
class Todo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  is_finished=models.BooleanField(default=False)

  def __str__(self):
    return self.title


class ChessMove(models.Model):
    start_x = models.PositiveSmallIntegerField()
    start_y = models.PositiveSmallIntegerField()
    end_x = models.PositiveSmallIntegerField()
    end_y = models.PositiveSmallIntegerField()
    piece = models.CharField(max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.piece} from ({self.start_x}, {self.start_y}) to ({self.end_x}, {self.end_y})"
    

from django.db import models

class CodeSnippet(models.Model):
    email = models.EmailField()
    code = models.TextField()
    language = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.language}"


from django.db import models

class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period = models.IntegerField()
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.day} - Period {self.period}: {self.subject}'


from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    time = models.CharField(max_length=100)
    day = models.CharField(max_length=50)


