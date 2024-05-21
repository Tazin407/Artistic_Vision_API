from django.db import models
from artist.models import Artist

# Create your models here.
class Art(models.Model):
    artist= models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='art')
    title= models.CharField(max_length=30)
    image= models.ImageField(upload_to='art/media')
    desciption= models.TextField()
    creation_date= models.DateField(auto_now_add=True)
    likes= models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.title} by {self.artist.username}"

class Like(models.Model):
    art = models.ForeignKey(Art, on_delete=models.CASCADE )
    artist= models.ForeignKey(Artist, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.artist.username} liked {self.art.title}"