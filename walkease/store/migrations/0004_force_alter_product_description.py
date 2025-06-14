# walkease/store/migrations/0003_force_alter_product_description.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_category'),  # Ensure this is the correct dependency based on your migration history
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
    ]
