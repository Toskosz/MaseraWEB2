# Generated by Django 3.0.7 on 2020-08-03 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacao', '0006_transacao_transacao_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transacao',
            name='validadeCartao',
        ),
        migrations.AddField(
            model_name='transacao',
            name='anoValidadeCartao',
            field=models.CharField(choices=[('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39')], default=0, max_length=5),
        ),
        migrations.AddField(
            model_name='transacao',
            name='mesValidadeCartao',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')], default=0, max_length=5),
        ),
    ]
