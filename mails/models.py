from django.db import models

# Create your models here.

class Mails(models.Model):
    mail_head = models.CharField(max_length=200, db_index=True, verbose_name='Тема')
    mail_text = models.CharField(max_length=200, db_index=True, verbose_name='Текст')
    list_of_clients = ['e.g.hutter@gmail.com','zonaegora@gmail.com']
    from_who = 'e.g.hutter@gmail.com'
    class Meta:
            ordering = ['mail_head']
            verbose_name = 'Письма'
            verbose_name_plural = 'Письма'

    def __str__(self):
        return 'Номер: {}'.format(self.id)
"""

    def send_mails():

    message_head = "Hello"
    message_text = "text" 
    from_who = 'e.g.hutter@gmail.com'
    list_of_clients = ['e.g.hutter@gmail.com',"zonaegora@gmail.com", "zonaegora@mail.ru"]

   
    datatuple = (
        (message_head, message_text, from_who, list_of_clients),
    )

    send_mass_mail(datatuple,fail_silently=False)

            	pass        
"""