from django.db import models


company = (('avangard', 'avangard'),)


class Article(models.Model):
	company_name = models.CharField(max_length=350, choices=company,db_index=True, blank = True)
	file_obj = models.FileField(upload_to='docs/')
