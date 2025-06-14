# walkease/store/migrations/0003_force_add_slug_to_category.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, unique=True, default=''),
            preserve_default=False,
        ),
    ]