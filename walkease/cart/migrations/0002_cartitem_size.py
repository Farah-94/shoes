from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='size',  # or 'shoe_size' if you renamed it
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
    ]